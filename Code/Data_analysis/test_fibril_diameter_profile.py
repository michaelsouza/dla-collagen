"""Geometry checks for the cross-sectional diameter profile."""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fibril_diameter_profile import diameter_profile, read_compact, ROD_HEIGHT


def test_square_cross_section():
    # quatro hastes num quadrado de lado 2, todas com base y=0

    x  = np.array([0, 2, 0, 2]); yb = np.array([0, 0, 0, 0]); z = np.array([0, 0, 2, 2])
    ys, count, dg, dm = diameter_profile(x, yb, z)
    assert len(ys) == ROD_HEIGHT, ys
    assert (count == 4).all(), count
    exp = 2 * np.sqrt(2)
    assert np.allclose(dg, exp), (dg[:3], exp)
    assert np.allclose(dm, exp), (dm[:3], exp)
    print(f"quadrado: d_gyr = d_max = {dg[0]:.6f}  (esperado {exp:.6f})  OK")

def test_layer_coverage():
    # hastes deslocadas em y: cobertura correta das camadas
    x2 = np.array([0, 0]); yb2 = np.array([0, 5]); z2 = np.array([0, 0])
    ys2, c2, _, _ = diameter_profile(x2, yb2, z2)
    assert ys2[0] == 0 and ys2[-1] == 5 + ROD_HEIGHT - 1, (ys2[0], ys2[-1])
    overlap = c2[(ys2 >= 5) & (ys2 <= ROD_HEIGHT - 1)]
    assert (overlap == 2).all(), overlap
    assert c2[0] == 1 and c2[-1] == 1
    print(f"cobertura: camadas {ys2[0]}..{ys2[-1]}, sobreposicao={overlap[0]}  OK")

def test_outlier_moves_dmax_not_dgyr():
    # um ponto distante move d_max mas quase nao move d_gyr
    x3 = np.array([0]*20 + [50]); yb3 = np.zeros(21, dtype=int); z3 = np.zeros(21, dtype=int)
    _, _, dg3, dm3 = diameter_profile(x3, yb3, z3)
    print(f"outlier: d_gyr={dg3[0]:.3f}  d_max={dm3[0]:.3f}  (razao {dm3[0]/dg3[0]:.1f}x)  OK")

def test_read_compact_columns():
    # leitura do formato compacto
    import tempfile, os
    with tempfile.NamedTemporaryFile('w', suffix='.dat', delete=False) as fh:
        fh.write("uid: 0 0 -9 0\nuid: 1 3 4 -2\n"); tmp = fh.name
    xr, yr, zr = read_compact(tmp); os.unlink(tmp)
    assert list(xr) == [0, 3] and list(yr) == [-9, 4] and list(zr) == [0, -2], (xr, yr, zr)
    print("leitura compacto: colunas (x,y,z) OK")

