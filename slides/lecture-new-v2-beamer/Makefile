MAIN = main
ENGINE = xelatex

all: $(MAIN).pdf

$(MAIN).pdf: $(MAIN).tex preamble.tex beamertheme3b1b.sty
	latexmk -$(ENGINE) -interaction=nonstopmode -halt-on-error $(MAIN).tex

clean:
	latexmk -c

distclean:
	latexmk -C

watch:
	latexmk -$(ENGINE) -pvc $(MAIN).tex

.PHONY: all clean distclean watch
