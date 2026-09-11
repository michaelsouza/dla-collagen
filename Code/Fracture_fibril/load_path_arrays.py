"""Caminho de carga do tronco em arrays, com a semantica exata de StressStrainData.filter_rids.

O motor legado (stress_strain_ava.py) guarda particulas, bastoes e camadas como
objetos Python e, a cada passo de cascata, varre todas as particulas duas vezes
(sweep de baixo para cima e de cima para baixo) e reconstroi o dicionario de
bastoes. Isso e O(R) por passo em objetos Python, com o numero de passos
proporcional a R: 1 h 54 por realizacao na secao inteira (~58 mil bastoes).
Aqui a mesma varredura roda sobre arrays CSR em numba: dezenas de ms por passo
na secao inteira.

Semantica preservada (stress_strain_ava.py:41-68):
  * bottom-up: a camada lid_min ativa todo bastao com particula nela; em cada
    camada seguinte, o bastao de uma particula fica ativo se algum bastao
    vizinho dessa particula (mesma camada, distancia <= 1) ja esta ativo; o
    conjunto ativo so cresce ao longo do sweep. NAO e conectividade pura: um
    vizinho ativado acima da ultima camada compartilhada nao ativa o bastao.
  * camada vazia => tudo inativo (e a ruptura); lid_min/lid_max fixos.
  * top-down: o mesmo, uma vez so, sem ponto fixo.
Ordem das particulas dentro do bastao: o legado soma a_i = <1/n> iterando
`rod.pids`, um `set` copiado por realizacao (ssd0.copy()); a ordem de iteracao
desse set muda os ultimos bits da soma e, portanto, de F*. Para reproduzir o
legado byte a byte, rod_pids usa exatamente essa ordem, emulada com
`list(set(...).copy())` sobre os pids em ordem crescente (a ordem de insercao
do loader). E um detalhe de ponto flutuante, nao de fisica.
Ordem das particulas dentro da camada: o legado itera `layer.pids`, tambem um
`set` copiado por realizacao; a ordem muda o resultado no empate em que o
vizinho Y e ativado na mesma camada, depois da particula de X, essa e a ultima
camada compartilhada, e X nao tem outra rota. Com ordem de pid crescente isso
mudou o caminho de carga inicial em 38 dos 40 troncos do N18 (2% dos bastoes
em T_s = 2, 0,1% em T_s >= 32). Por isso layer_pids usa a mesma ordem emulada
do set copiado, e o resultado fica byte a byte igual ao legado
(Reviews/N19_full_section_fracture/engine_equivalence.csv). Remocoes nao
alteram a ordem relativa dos que ficam num set do CPython, entao a ordem
emulada uma vez no inicio vale para todo o carregamento.

Le:      objeto StressStrainData de stress_strain_ava.read_or_create_ssd (cache .db)
Escreve: nada
Chamado: Code/Fracture_fibril/fiber_bundle_ava.py (engine="arrays");
         Code/Fracture_fibril/test_load_path_arrays.py
"""
from __future__ import annotations

import numpy as np
from numba import njit
from scipy.sparse import coo_matrix


@njit(cache=True)
def _sweep(layer_ptr, layer_pids, part_rod, neigh_ptr, neigh_rids, rod_active, reverse):
    """Um sweep de filter_rids. Devolve o novo vetor de bastoes ativos."""
    n_layers = layer_ptr.shape[0] - 1
    R = rod_active.shape[0]
    new_active = np.zeros(R, dtype=np.bool_)
    for step in range(n_layers):
        li = n_layers - 1 - step if reverse else step
        a, b = layer_ptr[li], layer_ptr[li + 1]
        if step == 0:
            for q in range(a, b):
                r = part_rod[layer_pids[q]]
                if rod_active[r]:
                    new_active[r] = True
            continue
        any_particle = False
        for q in range(a, b):
            p = layer_pids[q]
            r = part_rod[p]
            if not rod_active[r]:
                continue
            any_particle = True
            if new_active[r]:
                continue
            for t in range(neigh_ptr[p], neigh_ptr[p + 1]):
                if new_active[neigh_rids[t]]:
                    new_active[r] = True
                    break
        if not any_particle:
            # camada vazia: filter_rids esvazia active_rids e retorna
            return np.zeros(R, dtype=np.bool_)
    return new_active


def _ordem_do_set_copiado(pids) -> list:
    """Ordem em que o legado itera um set de pids inserido em ordem crescente e copiado."""
    orig = set()
    for pid in sorted(pids):
        orig.add(pid)
    return list(orig.copy())


class LoadPathArrays:
    """Tronco em CSR: particulas (indexadas por pid), bastoes (por ordem de rid) e camadas."""

    def __init__(self, rids, part_rod, part_lid, layer_ptr, layer_pids,
                 neigh_ptr, neigh_rids, rod_ptr, rod_pids, lid_min):
        self.rids = np.asarray(rids)
        self.part_rod = part_rod
        self.part_lid = part_lid
        self.layer_ptr = layer_ptr
        self.layer_pids = layer_pids
        self.neigh_ptr = neigh_ptr
        self.neigh_rids = neigh_rids
        self.rod_ptr = rod_ptr
        self.rod_pids = rod_pids
        self.lid_min = int(lid_min)
        self.R = len(self.rids)
        self.rod_active = np.ones(self.R, dtype=np.bool_)
        self._static = None

    # ------------------------------------------------------------ construcao
    @classmethod
    def from_ssd(cls, ssd) -> "LoadPathArrays":
        """Converte o StressStrainData carregado (todos os bastoes ativos)."""
        rids = sorted(ssd.rods.keys())
        rid_index = {rid: k for k, rid in enumerate(rids)}
        n_pid = max(ssd.particles.keys()) + 1
        part_rod = np.full(n_pid, -1, dtype=np.int64)
        part_lid = np.zeros(n_pid, dtype=np.int64)
        for pid, prt in ssd.particles.items():
            k = rid_index.get(prt.rid, -1)
            part_rod[pid] = k
            part_lid[pid] = prt.lid
        # so particulas de bastoes carregados
        pids = np.nonzero(part_rod >= 0)[0]
        lid_min, lid_max = int(ssd.lid_min), int(ssd.lid_max)
        n_layers = lid_max - lid_min + 1
        # camadas: pids na ordem de iteracao do set copiado do legado (ver cabecalho)
        li = part_lid[pids] - lid_min
        counts = np.bincount(li, minlength=n_layers)
        layer_ptr = np.zeros(n_layers + 1, dtype=np.int64)
        layer_ptr[1:] = np.cumsum(counts)
        layer_pids = np.empty(len(pids), dtype=np.int64)
        for lid, layer in ssd.layers.items():
            k = lid - lid_min
            layer_pids[layer_ptr[k]:layer_ptr[k + 1]] = _ordem_do_set_copiado(layer.pids)
        # vizinhos por particula (bastoes vizinhos na mesma camada), CSR por pid
        neigh_ptr = np.zeros(n_pid + 1, dtype=np.int64)
        neigh_list = []
        for pid in range(n_pid):
            prt = ssd.particles.get(pid)
            if prt is None or part_rod[pid] < 0:
                neigh_ptr[pid + 1] = neigh_ptr[pid]
                continue
            vs = [rid_index[r] for r in prt.neigh_rids if r in rid_index]
            neigh_list.extend(vs)
            neigh_ptr[pid + 1] = neigh_ptr[pid] + len(vs)
        neigh_rids = np.asarray(neigh_list, dtype=np.int64)
        # particulas por bastao, CSR por indice de bastao
        rod_counts = np.bincount(part_rod[pids], minlength=len(rids))
        rod_ptr = np.zeros(len(rids) + 1, dtype=np.int64)
        rod_ptr[1:] = np.cumsum(rod_counts)
        # ordem das particulas de cada bastao = ordem de iteracao de rod.pids no
        # legado (set construido por insercao crescente e depois copiado)
        rod_pids = np.empty(len(pids), dtype=np.int64)
        for k, rid in enumerate(rids):
            rod_pids[rod_ptr[k]:rod_ptr[k + 1]] = _ordem_do_set_copiado(ssd.rods[rid].pids)
        return cls(rids, part_rod, part_lid, layer_ptr, layer_pids, neigh_ptr, neigh_rids,
                   rod_ptr, rod_pids, lid_min)

    def compact(self) -> "LoadPathArrays":
        """Novo objeto so com os bastoes ativos (mesma ordem de rid), todos ativos."""
        keep = np.nonzero(self.rod_active)[0]
        new_index = np.full(self.R, -1, dtype=np.int64)
        new_index[keep] = np.arange(len(keep))
        part_rod = np.where(self.part_rod >= 0, new_index[np.maximum(self.part_rod, 0)], -1)
        part_rod[self.part_rod < 0] = -1
        n_layers = self.layer_ptr.shape[0] - 1
        # subsequencia da ordem original (remocao nao reordena um set do CPython)
        layer_pids = self.layer_pids[part_rod[self.layer_pids] >= 0]
        li = self.part_lid[layer_pids] - self.lid_min
        counts = np.bincount(li, minlength=n_layers)
        layer_ptr = np.zeros(n_layers + 1, dtype=np.int64)
        layer_ptr[1:] = np.cumsum(counts)
        n_pid = len(self.part_rod)
        neigh_ptr = np.zeros(n_pid + 1, dtype=np.int64)
        chunks = []
        for pid in range(n_pid):
            if part_rod[pid] < 0:
                neigh_ptr[pid + 1] = neigh_ptr[pid]
                continue
            vs = new_index[self.neigh_rids[self.neigh_ptr[pid]:self.neigh_ptr[pid + 1]]]
            vs = vs[vs >= 0]
            chunks.append(vs)
            neigh_ptr[pid + 1] = neigh_ptr[pid] + len(vs)
        neigh_rids = np.concatenate(chunks).astype(np.int64) if chunks else np.zeros(0, np.int64)
        # mantem a ordem das particulas dentro de cada bastao (ver cabecalho)
        rod_pids = self.rod_pids[part_rod[self.rod_pids] >= 0]
        rod_counts = np.bincount(part_rod[rod_pids], minlength=len(keep))
        rod_ptr = np.zeros(len(keep) + 1, dtype=np.int64)
        rod_ptr[1:] = np.cumsum(rod_counts)
        return LoadPathArrays(self.rids[keep], part_rod, self.part_lid, layer_ptr, layer_pids,
                              neigh_ptr, neigh_rids, rod_ptr, rod_pids, self.lid_min)

    # ------------------------------------------------------------- dinamica
    def sweep(self, reverse: bool) -> int:
        self.rod_active = _sweep(self.layer_ptr, self.layer_pids, self.part_rod,
                                 self.neigh_ptr, self.neigh_rids, self.rod_active, reverse)
        return int(self.rod_active.sum())

    def filter(self) -> int:
        """drop ja feito: filter_rids(False), depois (se sobrou) filter_rids(True)."""
        if self.sweep(False):
            self.sweep(True)
        return int(self.rod_active.sum())

    def drop(self, idx) -> None:
        self.rod_active[np.asarray(idx, dtype=np.int64)] = False

    def reset(self) -> None:
        self.rod_active = np.ones(self.R, dtype=np.bool_)

    def num_active(self) -> int:
        return int(self.rod_active.sum())

    # -------------------------------------------- estruturas estaticas do FibrilSystem
    def static_structures(self) -> dict:
        """flat_lids/flat_rod/n_parts, matriz C de contatos e adjacencia, como em FibrilSystem."""
        if self._static is not None:
            return self._static
        R = self.R
        flat_rod = np.repeat(np.arange(R, dtype=np.int64), np.diff(self.rod_ptr))
        flat_lids = self.part_lid[self.rod_pids] - self.lid_min
        n_parts = np.diff(self.rod_ptr).astype(float)
        # c[j, i] = numero de particulas do bastao i adjacentes ao bastao j
        # (legado: rod j, neigh_pids -> rid da particula). Aqui: para cada
        # particula p de i, cada vizinho j de p conta (j, i) += 1.
        deg = np.diff(self.neigh_ptr)
        src_p = np.repeat(np.arange(len(deg), dtype=np.int64), deg)   # particula p
        rows = self.neigh_rids                                        # j (vizinho de p)
        cols = self.part_rod[src_p]                                   # i = bastao de p
        ok = cols >= 0
        C = coo_matrix((np.ones(ok.sum()), (rows[ok], cols[ok])), shape=(R, R)).tocsr()
        C.sum_duplicates()
        adj = [set() for _ in range(R)]
        Cc = C.tocoo()
        for j, i in zip(Cc.row.tolist(), Cc.col.tolist()):
            adj[j].add(i)
            adj[i].add(j)
        self._static = dict(flat_lids=flat_lids, flat_rod=flat_rod, n_parts=n_parts,
                            L=int(flat_lids.max()) + 1 if len(flat_lids) else 0, C=C, adj=adj)
        return self._static


def load_path_from_ssd(ssd) -> LoadPathArrays:
    """Conversao + os dois sweeps iniciais de FibrilSystem.__init__ + compactacao."""
    lpa = LoadPathArrays.from_ssd(ssd)
    lpa.sweep(False)
    lpa.sweep(True)
    return lpa.compact()
