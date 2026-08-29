# Consolidação da DAG

**Data:** 2026-08-25  
**Origem:** §13 de `DAG_dependencias_revisao.md`, dividida em 2026-08-29.

> Entrada de registro. **Append-only** — não editar. Se um fato aqui deixar de
> valer, escreva uma entrada nova com a correção e cite esta.

As §9–§12 vinham sendo acrescentadas sem atualizar o cabeçalho, e o documento
passou a se contradizer: a §2 dava N5 como "decisão de escopo tomada" enquanto
a §11 pedia sua reabertura, e descrevia N2 pelo protocolo de varredura com
$\Delta F=0{,}5$ que a §12 havia substituído. Um documento de dependências que
contradiz os próprios apêndices é pior que nenhum.

Reescritos: §2 (tabela de nós), §3 (grafo), §4 (arestas), §5 (ordem
topológica) e §7 (inconsistências). As §9–§12 ficam como registro datado das
decisões e não foram alteradas, exceto pela correção de uma linha da §12 que
dava uma verificação como pendente depois de ela ter concluído.

#### Mudanças de estado

| Nó | Antes | Agora | Motivo |
|:--|:--|:--|:--|
| N2 | fechado | **reaberto** | protocolo substituído; falta o texto |
| N5 | escopo decidido | **reaberto** | Parkinson1997 varre $m$ (§11) |
| N8 | divergente/bloqueante | **dissolvido** | cascata determinística é a avalanche |
| N9 | fechado | **reaberto** | $\varphi(F)$ muda de escala com o protocolo |
| N15, N16 | — | **novos** | validação do gerador e campanha viraram portões reais |

#### O que a consolidação revelou

Dois achados que só aparecem ao reconciliar cabeçalho e apêndices:

1. **N9 estava fechado indevidamente.** Ninguém havia notado que a troca de
   protocolo invalida $\alpha$ e $\beta$. O piloto mostra $F_{rup}$ uma ordem
   de grandeza maior, então o eixo de força da Fig. 8 muda inteiramente.
2. **N5 precisa ser decidido antes da campanha, não depois.** Se a varredura em
   $m$ for aceita, $m$ vira eixo de produção e multiplica o custo da campanha.
   Decidir depois obriga a re-rodar tudo. Por isso N5 → N16 é aresta, e por
   isso N5 aparece na onda 2 da §5, e não mais adiante.
