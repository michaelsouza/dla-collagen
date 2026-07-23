# Makefile for building paper_PRE.tex with latexmk.
#
# Default behavior:
# - Uses TinyTeX at ~/gitrepos/tinytex/.TinyTeX if present
# - Falls back to system TeX/latexmk otherwise
#
# Usage:
#   make            # builds paper_PRE.pdf
#   make watch      # auto-rebuild on changes (latexmk -pvc)
#   make clean      # removes aux files (keeps PDF)
#   make distclean  # removes aux files + PDF
#   make check      # verifies required TeX files are found
#   make env        # prints TeX environment details

MAIN ?= paper_PRE
TEXFILE := $(MAIN).tex
PDF := $(MAIN).pdf

# TinyTeX root (override if you keep it elsewhere).
TINY_TEX ?= $(HOME)/gitrepos/tinytex/.TinyTeX

# Auto-detect TinyTeX bin dir (override via TEXBIN=... if needed).
TEXBIN ?= $(patsubst %/,%,$(firstword $(wildcard $(TINY_TEX)/bin/*/)))

ifneq ($(strip $(TEXBIN)),)
export PATH := $(TEXBIN):$(PATH)
endif

LATEXMK ?= latexmk
LATEXMKFLAGS ?= -pdf -interaction=nonstopmode -file-line-error

.PHONY: all pdf watch clean distclean check env

all: pdf

pdf: $(PDF)

$(PDF): $(TEXFILE)
	$(LATEXMK) $(LATEXMKFLAGS) $(TEXFILE)

watch:
	$(LATEXMK) -pvc $(LATEXMKFLAGS) $(TEXFILE)

clean:
	$(LATEXMK) -c $(TEXFILE)

distclean:
	$(LATEXMK) -C $(TEXFILE)

check:
	@command -v $(LATEXMK) >/dev/null || { echo "ERROR: latexmk not found in PATH"; exit 1; }
	@command -v kpsewhich >/dev/null || { echo "ERROR: kpsewhich not found in PATH"; exit 1; }
	@for f in revtex4-2.cls apsrev4-2.bst textcase.sty english.ldf lineno.sty; do \
		kpsewhich $$f >/dev/null || { echo "ERROR: missing TeX file: $$f"; exit 1; }; \
	done
	@echo "OK: TeX dependencies found."

env:
	@echo "TINY_TEX=$(TINY_TEX)"
	@echo "TEXBIN=$(TEXBIN)"
	@echo "PATH=$$PATH"
	@echo "---"
	@echo "latexmk: $$(command -v $(LATEXMK) || true)"
	@$(LATEXMK) -v 2>/dev/null | sed -n '1,2p' || true
	@echo "---"
	@echo "TEXMFHOME=$$(kpsewhich -var-value=TEXMFHOME 2>/dev/null || true)"
	@echo "TEXMFDIST=$$(kpsewhich -var-value=TEXMFDIST 2>/dev/null || true)"
