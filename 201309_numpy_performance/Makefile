first: all
all: run

python := LD_LIBRARY_PATH=/opt/pcraster/python-2.7.3/lib PYTHONPATH=~/Development/projects/devenv/sources /opt/pcraster/python-2.7.3/bin/python
plot.py := ~/Development/projects/PersonalFiles/Environment/Scripts/plot.py

pcraster_3 := /opt/PCRaster-3.0
python_3 := LD_LIBRARY_PATH=/opt/pcraster/python-2.7.3/lib PYTHONPATH=${pcraster_3}/Python /opt/pcraster/python-2.7.3/bin/python

pcraster_4 := /opt/pcraster/pcraster-dev
python_4 := LD_LIBRARY_PATH=/opt/pcraster/python-2.7.3/lib PYTHONPATH=${pcraster_4}/python /opt/pcraster/python-2.7.3/bin/python

objects := ${HOME}/Development/objects/gcc-4_x86-64/Release
pcraster_dev := ${objects}/pcrtree2
python_dev := LD_LIBRARY_PATH=/opt/pcraster/python-2.7.3/lib PYTHONPATH=${pcraster_dev}/bin /opt/pcraster/python-2.7.3/bin/python

nr_rows := 30000
nr_cols := 2000

clone.map:
	${pcraster_4}/bin/mapattr -s -R ${nr_rows} -C ${nr_cols} -B clone.map

run: run_3 run_4 run_dev

run_3: log_3.txt

log_3.txt: clone.map model.py
	${python_3} model.py > log_3.txt

run_4: log_4.txt

log_4.txt: clone.map model.py
	${python_4} model.py > log_4.txt

run_dev: log_dev.txt

log_dev.txt: clone.map model.py
	${python_dev} model.py > log_dev.txt

plot: plot.pdf

plot.pdf: log_3.txt log_4.txt log_dev.txt
	${python} ${plot.py} --bar log_3.txt --bar log_4.txt --bar log_dev.txt plot.pdf

clean:
	rm -f clone.map
	rm -f log_3.txt log_4.txt log_dev.txt
	rm -f plot.pdf
