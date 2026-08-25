#!/usr/bin/env bash
# Submit a campaign stage repeatedly until every manifest item is done.
#
#     CAMPAIGN_KIND=fracture run_until_complete.sh [MAX_ROUNDS]
#
# Why this exists: on this cluster roughly a third of array task launches fail
# with "launch failed requeued held" -- measured at 3 of 8 in a controlled test
# and 5 of 16 across earlier submissions.  The failures are random: they do not
# depend on the array index, the array size, or the node, and the partition had
# idle cores throughout.  scontrol release often does not stick either.
#
# The cause is unknown and is probably not ours to fix.  What is ours is to
# stop treating it as an incident.  Because both workers are idempotent, a
# resubmission does only the missing work, so the reliable procedure is simply
# to repeat until the completeness check passes.  With a one-third failure rate
# the fraction still missing after n rounds is about (1/3)^n: 67% done after
# one round, 89% after two, 96% after three.
set -euo pipefail

max_rounds="${1:-6}"
here="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
repo="${DLA_REPO:-$(cd -- "$here/../../.." && pwd)}"
if [[ -z "${DLA_PROJECT:-}" ]]; then
    # shellcheck source=../../cluster/sdumont2nd/env.sh
    source "$repo/Code/cluster/sdumont2nd/env.sh"
fi
# shellcheck source=campaign_common.sh
source "$here/campaign_common.sh"

kind="${CAMPAIGN_KIND:?set CAMPAIGN_KIND=generate|fracture}"

for ((round = 1; round <= max_rounds; round++)); do
    echo "=============== round $round/$max_rounds ($kind) ==============="

    if "$here/check_campaign.sh" "$kind" > /tmp/dla-check-$$.log 2>&1; then
        tail -5 /tmp/dla-check-$$.log
        rm -f /tmp/dla-check-$$.log
        echo "stage complete after $((round - 1)) round(s)"
        exit 0
    fi
    grep -E "^(complete|missing|short)" /tmp/dla-check-$$.log || true
    rm -f /tmp/dla-check-$$.log

    # A held task from the previous round occupies a submit slot and will never
    # run; clear it before asking for more.
    #
    # Scoped to THIS driver's previous job on purpose.  Filtering by user would
    # also match held tasks from the same person's other projects on this
    # cluster, and cancelling someone's unrelated work because it happens to
    # share an account is not ours to do.
    if [[ -n "${prev_job:-}" ]]; then
        held="$(squeue -h -j "$prev_job" -r -t PENDING -o "%i %r" 2>/dev/null \
                | awk '/launch failed/ {print $1}' | tr '\n' ' ')"
        if [[ -n "$held" ]]; then
            echo "cancelling held tasks of $prev_job: $held"
            # shellcheck disable=SC2086
            scancel $held 2>/dev/null || true
            sleep 5
        fi
    fi

    job="$("$here/submit_campaign.sh" 2>&1 | tee /dev/stderr \
           | awk '/Submitted batch job/ {print $NF}')"
    if [[ -z "$job" ]]; then
        echo "submission failed; stopping" >&2
        exit 1
    fi

    prev_job="$job"
    echo "waiting on job $job ..."
    while squeue -h -j "$job" -r -t PENDING,RUNNING,CONFIGURING 2>/dev/null \
          | grep -qv "launch failed"; do
        sleep 30
    done
    # Anything still queued at this point is held and will not progress.
    sleep 10
done

echo "still incomplete after $max_rounds rounds" >&2
"$here/check_campaign.sh" "$kind" || true
exit 1
