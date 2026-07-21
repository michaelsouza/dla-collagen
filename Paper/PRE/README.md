# paper-bela

## Ambiente Computacional (este run)

Use estas informações para distinguir este ambiente de outros:

- Data/hora da coleta: `2026-02-24T16:10:59-03:00`
- Hostname: `penguin`
- Sistema: Debian GNU/Linux 12 (bookworm)
- Kernel: `Linux 6.6.99-09000-gd3ae1caecf39 x86_64`
- Shell: `/usr/bin/zsh`
- CPU: `Intel(R) Celeron(R) CPU N3350 @ 1.10GHz` (2 vCPUs)
- Memória: ~2.7 GiB RAM, sem swap
- Contexto prático: ambiente Linux (Crostini/KVM) com arquivos em
  `/mnt/chromeos/MyFiles/Downloads/...`

## Compilação de `paper_PRE.tex` com TinyTeX + latexmk

### Objetivo

Compilar `paper_PRE.tex` usando a instalação TeX em:

`~/gitrepos/tinytex/.TinyTeX`

### Comando base

```bash
export PATH=~/gitrepos/tinytex/.TinyTeX/bin/x86_64-linux:$PATH
latexmk -pdf -interaction=nonstopmode -file-line-error paper_PRE.tex
```

### Via Makefile

```bash
make
make check
make env
make watch
make clean
make distclean
```

Variaveis uteis (override):

- `MAIN=paper_PRE` (documento principal, sem `.tex`)
- `TINY_TEX=~/gitrepos/tinytex/.TinyTeX`
- `TEXBIN=.../bin/x86_64-linux`

### Problemas encontrados e solução aplicada

1. Erro inicial: `revtex4-2.cls not found`.
2. Tentativa com `tlmgr install revtex` travou neste ambiente (processo preso em `p9_client_rpc`).
3. Solução robusta adotada: instalar manualmente no `texmf-local` da TinyTeX
   via CTAN e atualizar a base com `mktexlsr`.

Pacotes/arquivos instalados manualmente em
`~/gitrepos/tinytex/.TinyTeX/texmf-local`:

- `revtex4-2.cls` + `apsrev4-2.bst` (de `revtex.tds.zip`)
- `textcase.sty` (gerado com `latex textcase.ins`)
- Babel inglês (`english.ldf` e variantes de `babel-contrib/english`)
- `lineno.sty` (e arquivos relacionados)

Após cada instalação:

```bash
mktexlsr ~/gitrepos/tinytex/.TinyTeX/texmf-local
```

Validações úteis:

```bash
kpsewhich revtex4-2.cls
kpsewhich apsrev4-2.bst
kpsewhich textcase.sty
kpsewhich english.ldf
kpsewhich lineno.sty
```

### Comando final que fechou a compilação

```bash
export PATH=~/gitrepos/tinytex/.TinyTeX/bin/x86_64-linux:$PATH
latexmk -g -pdf -interaction=nonstopmode -file-line-error paper_PRE.tex
```

Resultado final nesta máquina:

- `paper_PRE.pdf` gerado com sucesso
- `latexmk`: `All targets (paper_PRE.pdf) are up-to-date`

## Observações para uso futuro

- Se `tlmgr` travar novamente neste ambiente, repetir a estratégia de instalação
  manual em `texmf-local`.
- Se for usar outra máquina/ambiente, registre aqui `hostname`, `uname -a`,
  versão do sistema e caminho da instalação TeX para facilitar comparação.
