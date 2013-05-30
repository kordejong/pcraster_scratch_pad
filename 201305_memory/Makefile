SHELL := /bin/bash

all: run

clone: clone.map

clone.map:
	mapattr -s -R 920 -C 1490 -B clone.map

clean:
	rm -fr 1* 2* 3* 4* 5* 6* 7* 8* 9*
	rm -f clone.map memory.{col,pdf} runtime.{col,pdf}

run: clean clone
	python model.py

memory.col: model.py
	make run

memory.pdf: memory.col
	plot.py --lines memory.col --output memory.pdf

plots: memory.pdf
