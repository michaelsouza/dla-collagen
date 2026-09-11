"""Testes do caminho de carga em arrays (load_path_arrays.py).

1. Fixtures pequenos com resultado conhecido, comparando o motor em arrays com
   o legado (StressStrainData.filter_rids) no mesmo objeto: conectividade
   simples, camada vazia, e o caso em que o vizinho Y e ativado acima da
   ultima camada compartilhada com X (X nao pode ser ativado via Y).
2. Byte a byte contra a escada de 2026-09-02: ts_128_seed_900001, 17x17,
   semente 1, 5 realizacoes == Reviews/PhaseC_periodic_cylinder/avalanche_ladder_raw/ts128_w17.txt.
   Pulado se o tronco estendido nao estiver em $DLA_EXTENDED.

Le:      $DLA_EXTENDED/ts_128_seed_900001.dat (opcional)
         Reviews/PhaseC_periodic_cylinder/avalanche_ladder_raw/ts128_w17.txt
Escreve: nada (arquivos temporarios)
Chamado: pytest Code/Fracture_fibril/
"""
from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import stress_strain_ava as S  # noqa: E402
from fiber_bundle_ava import FibrilSystem, quasistatic_rupture, run_realizations  # noqa: E402
from load_path_arrays import LoadPathArrays, load_path_from_ssd  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]


def escreve_dat(linhas: list[tuple[int, int, int, int]]) -> str:
    """linhas = (uid, x, y, z) por particula; devolve o caminho do .dat."""
    d = tempfile.mkdtemp()
    fn = Path(d) / "dla_mode_s_ts_1_nb_1_seed_1__open.dat"
    fn.write_text("id uid x y z\n" + "".join(f"uid {u} {x} {y} {z}\n" for u, x, y, z in linhas), encoding="utf-8")
    return str(fn)


def bastao(uid, x, z, y0, y1):
    return [(uid, x, y, z) for y in range(y0, y1 + 1)]


class SweepSemanticsTest(unittest.TestCase):
    def ativos_legado(self, fn):
        ssd = S.read_or_create_ssd(fn, half_width=50, half_length=50)
        ssd.filter_rids(reverse=False)
        ssd.filter_rids(reverse=True)
        return sorted(ssd.rods.keys())

    def ativos_arrays(self, fn):
        ssd = S.read_or_create_ssd(fn, half_width=50, half_length=50)
        lpa = load_path_from_ssd(ssd)
        return sorted(int(r) for r in lpa.rids)

    def test_two_rods_side_by_side_both_active(self):
        fn = escreve_dat(bastao(1, 0, 0, 0, 5) + bastao(2, 1, 0, 0, 5))
        self.assertEqual(self.ativos_legado(fn), [1, 2])
        self.assertEqual(self.ativos_arrays(fn), [1, 2])

    def test_isolated_rod_above_bottom_is_dropped(self):
        # 3 nao toca ninguem e nao esta na camada de baixo: cai nos dois motores
        fn = escreve_dat(bastao(1, 0, 0, 0, 5) + bastao(2, 1, 0, 0, 5) + bastao(3, 5, 5, 2, 5))
        self.assertEqual(self.ativos_legado(fn), [1, 2])
        self.assertEqual(self.ativos_arrays(fn), [1, 2])

    def test_neighbour_activated_above_last_shared_layer_does_not_activate(self):
        # 1 na base (0-2); Y=2 em 0-9 mas so toca 1 pela camada... nao: Y toca 1 em 0-2
        # X=3 em 3-5 toca Y em 3-5 -> ativado (Y ativo desde a camada 0)
        # Z=4 em 0-1 toca W=5 (2-9) em nenhuma camada -> W isolado da base?
        # Caso A: W=5 (camadas 2-9) toca Y=2 em 2-9 e e ativado na camada 2;
        # V=6 (camadas 0-1)... V esta na base, ativo. U=7 (camadas 1-1) toca so W:
        # W so fica ativo na camada 2 > 1 = ultima compartilhada -> U NAO ativa.
        linhas = (bastao(1, 0, 0, 0, 2) + bastao(2, 1, 0, 0, 9) + bastao(3, 2, 0, 3, 5)
                  + bastao(5, 1, 1, 2, 9) + bastao(7, 1, 2, 1, 1))
        fn = escreve_dat(linhas)
        self.assertEqual(self.ativos_legado(fn), [1, 2, 3, 5])
        self.assertEqual(self.ativos_arrays(fn), [1, 2, 3, 5])

    def test_empty_layer_kills_everything(self):
        # 3 sozinho sustenta as camadas 3-6; ao cair, a camada 3 fica vazia e tudo cai
        fn = escreve_dat(bastao(1, 0, 0, 0, 2) + bastao(2, 1, 0, 0, 2) + bastao(3, 0, 1, 2, 6))
        ssd = S.read_or_create_ssd(fn, half_width=50, half_length=50)
        leg = ssd.copy()
        leg.filter_rids(reverse=False); leg.filter_rids(reverse=True)
        self.assertEqual(sorted(leg.rods), [1, 2, 3])
        leg.drop_rids({3}); leg.filter_rids(reverse=False)
        self.assertEqual(sorted(leg.rods), [])
        lpa = load_path_from_ssd(ssd.copy())
        self.assertEqual(sorted(int(r) for r in lpa.rids), [1, 2, 3])
        lpa.drop([int(np.nonzero(lpa.rids == 3)[0][0])])
        self.assertEqual(lpa.filter(), 0)

    def test_full_rupture_matches_legacy_on_small_fixture(self):
        linhas = []
        uid = 1
        for x in range(4):
            for z in range(4):
                linhas += bastao(uid, x, z, 0, 9); uid += 1
        fn = escreve_dat(linhas)
        ssd = S.read_or_create_ssd(fn, half_width=50, half_length=50)
        leg = FibrilSystem(ssd.copy(), m=2, rng=np.random.default_rng(3))
        ev_leg, F_leg = quasistatic_rupture(leg)
        arr = FibrilSystem(m=2, rng=np.random.default_rng(3), arrays=load_path_from_ssd(ssd.copy()))
        ev_arr, F_arr = quasistatic_rupture(arr)
        self.assertEqual(ev_leg, ev_arr)
        self.assertEqual(F_leg, F_arr)
        self.assertEqual([r["clusters"] for r in leg.log], [r["clusters"] for r in arr.log])


class LadderByteIdentityTest(unittest.TestCase):
    def test_ts128_w17_seed1_five_realizations(self):
        ext = os.environ.get("DLA_EXTENDED")
        dat = Path(ext) / "ts_128_seed_900001.dat" if ext else None
        if dat is None or not dat.exists():
            self.skipTest("DLA_EXTENDED nao aponta para o tronco estendido ts_128_seed_900001.dat")
        ref = RAIZ / "Reviews" / "PhaseC_periodic_cylinder" / "avalanche_ladder_raw" / "ts128_w17.txt"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "ts_128" / "ts_128_seed_900001_m_2.txt"
            run_realizations(str(dat), 5, m=2, seed=1, legacy_path=str(out),
                             half_width=8, half_length=100, engine="arrays")
            self.assertEqual(out.read_bytes(), ref.read_bytes())


if __name__ == "__main__":
    unittest.main()
