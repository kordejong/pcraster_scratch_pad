first: all
all: run

pcraster := /opt/pcraster/pcraster-4-dev

clone: clone.map

clone.map:
	${pcraster}/bin/mapattr -s -R 92 -C 149 -B clone.map

clean:
	rm -fr 1* 2* 3* 4* 5* 6* 7* 8* 9*
	rm -f clone.map memory.{col,pdf} runtime.{col,pdf}

run: clean clone
	PYTHONPATH=${pcraster}/python:${PYTHONPATH} python model.py

memory.pdf: memory.col
	plot.py --lines memory.col --output memory.pdf

runtime.pdf: runtime.col
	plot.py --lines runtime.col --output runtime.pdf

plots: memory.pdf runtime.pdf
