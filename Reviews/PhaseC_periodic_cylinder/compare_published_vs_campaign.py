#!/usr/bin/env python3
"""N15 pelo alvo novo: a estrutura local das fibrilas da campanha bate com a das publicadas?

Lê:      <dir>/published/*.dat  (fibrilas do artigo, do zip em Data_fibrils/)
         <dir>/campaign_style/*.dat (geradas pelo fast_dla2 atual com os flags da
         campanha: -rng fast -jumps 1 -coverstop 1, nb=30000)
Escreve: relatório em stdout
Chamado: à mão, para fechar N15 (Estado_revisao_ER12738.md)

Por que este é o teste certo: o alvo antigo de N15 era o D_f publicado, que a
Fase C e o relatório da campanha mostraram ser escolha de janela. Coordenação K
e encaixes 0D–4D são médias sobre milhares de moléculas em cada fibrila, bem
determinadas em qualquer tamanho, e não dependem de janela. Reusa o analisador
do passo 1 da Fase C (compare_local_structure.py), com a margem de borda.
"""
import glob, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compare_local_structure import analisar, carregar, resumo

def main(base):
    for ts in (2, 128, 8192):
        pub = sorted(glob.glob(f"{base}/published/dla_mode_s_ts_{ts}_nb_30000_seed_*.dat"))
        cam = sorted(glob.glob(f"{base}/campaign_style/dla_mode_s_ts_{ts}_nb_30000_seed_*.dat"))
        cam = [f for f in cam if sum(1 for _ in open(f)) >= 30001]
        print(f"\n=== Ts = {ts} ===")
        if not pub or not cam:
            print(f"  faltam arquivos (publicadas={len(pub)}, campanha={len(cam)} completas)"); continue
        rp = [analisar(carregar(f), None, 90) for f in pub]
        rc = [analisar(carregar(f), None, 90) for f in cam]
        kp, sp, stp = resumo(f"publicadas ({len(rp)})", rp)
        kc, sc, stc = resumo(f"campanha atual ({len(rc)})", rc)
        sig = math.sqrt(sp**2 + sc**2) or 1e-9
        print(f"  -> K difere {100*(kc-kp)/kp:+.1f}%  ({abs(kc-kp)/sig:.1f} desvios)")
        pior = max(range(5), key=lambda i: abs(stc[i]-stp[i]))
        print(f"  -> maior diferença de encaixe: {pior}D, {100*(stc[pior]-stp[pior]):+.1f} pontos percentuais")

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".")
