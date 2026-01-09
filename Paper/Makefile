TARGET = paper

all: $(TARGET).pdf

$(TARGET).pdf: $(TARGET).tex references.bib Figures/figure_1.pdf Figures/figure_2.pdf Figures/figure_3.pdf Figures/figure_4.pdf Figures/figure_5.pdf Figures/figure_6.pdf Figures/figure_7.pdf Figures/figure_8.pdf Figures/figure_9.pdf biophys-new.cls
	pdflatex $(TARGET)
	bibtex $(TARGET)
	pdflatex $(TARGET)
	pdflatex $(TARGET)

clean:
	rm -f *.aux *.log *.bbl *.blg *.toc *.out *.lof *.lot $(TARGET).pdf

.PHONY: all clean