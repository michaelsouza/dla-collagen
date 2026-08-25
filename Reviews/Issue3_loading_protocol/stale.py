"""Audit: does the cached sigma_mean track the true F/N(i) after removals?

Rod.update_force() rescales a cached sigma_mean by F/F_old and only recomputes
it from the current layer occupancies when the rod's own neighbourhood changed
(Particle.innactive -> Rod.del_neigh_pid -> updated=False).  A rod that shares a
cross-section with a removed rod WITHOUT being its spatial neighbour keeps
updated=True, so its sigma_mean can lag the true value.

Here we recompute the exact sigma for every rod at the end of selected force
steps and compare with the cached value actually used by prob_break.
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.join(os.getcwd(), 'Code', 'Fracture_fibril'))
import numpy as np
import stress_strain_ava as S


def exact_sigma(ssd, rod, F):
    n = []
    for pid in rod.pids:
        if pid in ssd.particles:
            p = ssd.particles[pid]
            if p.lid in ssd.layers:
                L = ssd.layers[p.lid].len()
                if L > 0:
                    n.append(F / L)
    return float(np.mean(n)) if n else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-file', required=True)
    ap.add_argument('-m', type=int, default=2)
    ap.add_argument('-seed', type=int, default=7)
    ap.add_argument('-every', type=int, default=25, help='audit every k-th force step')
    ap.add_argument('-out', required=True)
    a = ap.parse_args()

    np.random.seed(a.seed)
    ssd = S.read_or_create_ssd(a.file)
    ssd.set_rods_exponent(a.m)
    ssd = ssd.copy()

    ssd.filter_rids(reverse=False)
    ssd.filter_rids(reverse=True)

    F = 0.5
    step = 0
    audits = []
    while True:
        prob_deleted = S.random_deleted_rids(ssd, F)
        if not prob_deleted:
            step += 1
            if step % a.every == 0:
                rel = []
                stale_flag = 0
                for rod in ssd.rods.values():
                    ex = exact_sigma(ssd, rod, F)
                    ca = rod.sigma_mean
                    if ex > 0:
                        rel.append(abs(ca - ex) / ex)
                    if rod.updated:
                        stale_flag += 1
                rel = np.array(rel)
                audits.append(dict(
                    step=step, F=F, n_rods=len(ssd.rods),
                    frac_cached=stale_flag / max(1, len(ssd.rods)),
                    rel_mean=float(rel.mean()), rel_p95=float(np.percentile(rel, 95)),
                    rel_max=float(rel.max()),
                    frac_above_1pct=float((rel > 0.01).mean()),
                    frac_above_5pct=float((rel > 0.05).mean())))
                print(f'F={F:7.1f} rods={len(ssd.rods):6d} '
                      f'rel_mean={rel.mean():.3e} p95={np.percentile(rel,95):.3e} '
                      f'max={rel.max():.3e} >1%={100*(rel>0.01).mean():.2f}%', flush=True)
            F += 0.5
            continue
        ssd.drop_rids(set(prob_deleted))
        act1, _ = ssd.filter_rids(reverse=False)
        if not act1:
            break
        act2, _ = ssd.filter_rids(reverse=True)
        if not act2:
            break

    json.dump(dict(file=a.file, audits=audits), open(a.out, 'w'))
    print('wrote', a.out)


if __name__ == '__main__':
    main()
