import json, glob, os, sys
import numpy as np

SP = os.path.dirname(os.path.abspath(__file__))
order = ['ts2_base','ts128_base','ts8192_base','ts128_k2','ts128_k3','ts128_k5',
         'ts128_dF025','ts128_dF10','ts2_k3','ts8192_k3']
print(f'{"label":<13}{"dF":>5}{"k":>3}{"runs":>5}{"F_rup":>9}{"sd":>7}'
      f'{"sweeps/step":>13}{"max sw":>8}{"E[extra]":>10}{"Q_quiet":>9}'
      f'{"aval_n":>8}{"aval_mn":>9}{"aval_max":>9}')
for lab in order:
    fn = os.path.join(SP, f'p_{lab}.json')
    if not os.path.exists(fn):
        continue
    d = json.load(open(fn))
    rows = d['rows']
    runs = sorted({r['run'] for r in rows})
    Frup = [max(r['F'] for r in rows if r['run'] == k) for k in runs]
    pre = [r for r in rows if not r['ruptured']]
    sw = np.array([r['sweeps'] for r in pre], float)
    sp = np.array([r['sum_p'] for r in pre], float)
    qq = np.array([r['q_quiet'] for r in pre], float)
    av = np.array([r['n_total'] for r in pre if r['n_total'] > 0], float)
    print(f'{lab:<13}{d["dF"]:>5}{d["kquiet"]:>3}{len(runs):>5}'
          f'{np.mean(Frup):>9.1f}{np.std(Frup):>7.1f}'
          f'{sw.mean():>13.2f}{int(sw.max()):>8}'
          f'{np.nanmean(sp):>10.3f}{np.nanmean(qq):>9.3f}'
          f'{len(av):>8}{av.mean():>9.2f}{int(av.max()):>9}')
