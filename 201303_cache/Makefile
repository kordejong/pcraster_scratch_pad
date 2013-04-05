first: all
all: run

pcraster := ~/tmp/pcraster-gcc-4_x86-64-20130321

clone: clone.map

clone.map:
	PATH=${pcraster}/bin/mapattr -s -R 92 -C 149 -B clone.map

clean:
	rm -fr 1* 2* 3* 4* 5* 6* 7* 8* 9*
	rm -f clone.map

run: clean clone
	PYTHONPATH=${pcraster}/python:${PYTHONPATH} python model.py

debug: clean clone
	PYTHONPATH=${pcraster}/python:${PYTHONPATH} cgdb --args python model.py
