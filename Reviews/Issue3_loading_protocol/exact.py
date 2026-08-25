"""Compare the shipped sigma caching against exact per-sweep recomputation.

exact=0 : shipped behaviour (Rod.prob_break uses the cached sigma_mean unless
          the rod's own neighbourhood changed)
exact=1 : Rod.prob_break always recomputes sigma from the current layer
          occupancies, i.e. sigma(i)=F/N(i) exactly as written in Eqs. (2)-(3)
"""
import sys, os, json, argparse, time
sys.path.insert(0, os.path.join(os.getcwd(), 'Code', 'Fracture_fibril'))
import numpy as np
import stress_strain_ava as S


def signed_report(ssd, F):
    d = []
    for rod in ssd.rods.values():
        n = []
        for pid in rod.pids:
            if pid in ssd.particles:
                p = ssd.particles[pid]
                if p.lid in ssd.layers and ssd.layers[p.lid].len() > 0:
                    n.append(F / ssd.layers[p.lid].len())
        if n:
            ex = float(np.mean(n))
            if ex > 0:
                d.append((rod.sigma_mean - ex) / ex)
    return np.array(d)


def run(ssd, exact, dF=0.5):
    ssd.filter_rids(reverse=False); ssd.filter_rids(reverse=True)
    F = dF
    n0 = ssd.num_active_particles()
    steps = []
    tot = 0
    while True:
        if exact:
            for rod in ssd.rods.values():
                rod.updated = False
        dele = S.random_deleted_rids(ssd, F)
        if not dele:
            steps.append((F, tot)); tot = 0; F += dF; continue
        ssd.drop_rids(set(dele)); tot += len(dele)
        a1, s1 = ssd.filter_rids(reverse=False); tot += len(s1)
        if not a1: break
        a2, s2 = ssd.filter_rids(reverse=True); tot += len(s2)
        if not a2: break
    return F, steps, n0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-file', required=True); ap.add_argument('-n', type=int, default=20)
    ap.add_argument('-seed', type=int, default=11); ap.add_argument('-out', required=True)
    a = ap.parse_args()
    ssd0 = S.read_or_create_ssd(a.file); ssd0.set_rods_exponent(2)

    # signed drift of the cached sigma, shipped behaviour
    c = ssd0.copy(); c.filter_rids(reverse=False); c.filter_rids(reverse=True)
    F = 0.5; drift = []
    while F <= 160:
        dele = S.random_deleted_rids(c, F)
        if not dele:
            if abs(F % 20) < 1e-9:
                d = signed_report(c, F)
                drift.append(dict(F=F, mean=float(d.mean()), p05=float(np.percentile(d, 5)),
                                  frac_negative=float((d < 0).mean())))
            F += 0.5; continue
        c.drop_rids(set(dele))
        a1, _ = c.filter_rids(reverse=False)
        if not a1: break
        a2, _ = c.filter_rids(reverse=True)
        if not a2: break

    out = {'drift': drift, 'runs': {}}
    for exact in (0, 1):
        np.random.seed(a.seed)
        Fr, av = [], []
        t0 = time.time()
        for k in range(a.n):
            c = ssd0.copy()
            Frup, steps, n0 = run(c, exact)
            Fr.append(Frup)
            av.extend([s[1] for s in steps if s[1] > 0])
        out['runs'][f'exact{exact}'] = dict(
            F_rupture_mean=float(np.mean(Fr)), F_rupture_sd=float(np.std(Fr)),
            n_avalanches=len(av), av_mean=float(np.mean(av)),
            av_p50=float(np.percentile(av, 50)), av_p99=float(np.percentile(av, 99)),
            av_max=int(np.max(av)), secs=round(time.time() - t0, 1))
        print(f'exact={exact}: {out["runs"][f"exact{exact}"]}', flush=True)
    json.dump(out, open(a.out, 'w'))
    print('wrote', a.out)


if __name__ == '__main__':
    main()
