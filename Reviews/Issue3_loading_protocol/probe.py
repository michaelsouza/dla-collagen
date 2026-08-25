"""R2-1 evidence: instrument the canonical loading protocol.

For every force step F we record
  sweeps      : number of probabilistic assessment sweeps performed at F
  n_prob      : molecules removed by the stochastic rule at F
  n_struct    : molecules removed for losing the load path at F
  sum_p       : sum_i P_R,i  in the STOPPING configuration
                = expected removals if one further sweep were performed
  q_quiet     : prod_i (1 - P_R,i) in the STOPPING configuration
                = probability that one further sweep also removes nothing
  n_rods      : rods still in the backbone
"""
import sys, os, json, math, time, argparse
sys.path.insert(0, os.path.join(os.getcwd(), 'Code', 'Fracture_fibril'))
import numpy as np
import stress_strain_ava as S


def probe_run(ssd, dF=0.5, k_quiet=1):
    ssd.filter_rids(reverse=False)
    ssd.filter_rids(reverse=True)

    F = dF
    rows = []
    sweeps = n_prob = n_struct = 0
    quiet_streak = 0

    while True:
        prob_deleted = S.random_deleted_rids(ssd, F)
        sweeps += 1

        if not prob_deleted:
            # every rod's .p is current: it was just evaluated in this sweep
            ps = np.array([r.p for r in ssd.rods.values()], dtype=float)
            ps = np.clip(ps, 0.0, 1.0)
            sum_p = float(ps.sum())
            with np.errstate(divide='ignore'):
                q_quiet = float(np.exp(np.log1p(-ps).sum())) if (ps < 1).all() else 0.0
            quiet_streak += 1
            if quiet_streak < k_quiet:
                continue
            rows.append(dict(F=F, sweeps=sweeps, n_prob=n_prob, n_struct=n_struct,
                             n_total=n_prob + n_struct, sum_p=sum_p, q_quiet=q_quiet,
                             n_rods=len(ssd.rods), ruptured=0))
            F += dF
            sweeps = n_prob = n_struct = 0
            quiet_streak = 0
            continue

        quiet_streak = 0
        ssd.drop_rids(set(prob_deleted))
        n_prob += len(prob_deleted)
        act1, s1 = ssd.filter_rids(reverse=False)
        n_struct += len(s1)
        if not act1:
            rows.append(dict(F=F, sweeps=sweeps, n_prob=n_prob, n_struct=n_struct,
                             n_total=n_prob + n_struct, sum_p=float('nan'),
                             q_quiet=float('nan'), n_rods=0, ruptured=1))
            break
        act2, s2 = ssd.filter_rids(reverse=True)
        n_struct += len(s2)
        if not act2:
            rows.append(dict(F=F, sweeps=sweeps, n_prob=n_prob, n_struct=n_struct,
                             n_total=n_prob + n_struct, sum_p=float('nan'),
                             q_quiet=float('nan'), n_rods=0, ruptured=1))
            break
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-file', required=True)
    ap.add_argument('-n', type=int, default=5)
    ap.add_argument('-m', type=int, default=2)
    ap.add_argument('-dF', type=float, default=0.5)
    ap.add_argument('-kquiet', type=int, default=1)
    ap.add_argument('-seed', type=int, default=12345)
    ap.add_argument('-out', required=True)
    a = ap.parse_args()

    np.random.seed(a.seed)
    ssd = S.read_or_create_ssd(a.file)
    ssd.set_rods_exponent(a.m)

    out = []
    for k in range(a.n):
        c = ssd.copy()
        t0 = time.time()
        rows = probe_run(c, dF=a.dF, k_quiet=a.kquiet)
        for r in rows:
            r['run'] = k
        out.extend(rows)
        print(f'  run {k+1}/{a.n}: {len(rows)} force steps, '
              f'F_rupture={rows[-1]["F"]:.1f}, {time.time()-t0:.1f}s', flush=True)

    with open(a.out, 'w') as fh:
        json.dump(dict(file=a.file, dF=a.dF, kquiet=a.kquiet, m=a.m,
                       seed=a.seed, rows=out), fh)
    print('wrote', a.out)


if __name__ == '__main__':
    main()
