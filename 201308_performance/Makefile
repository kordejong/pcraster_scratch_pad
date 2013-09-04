first: all
all: run

python := LD_LIBRARY_PATH=/opt/pcraster/python-2.7.3/lib PYTHONPATH=~/Development/projects/devenv/sources /opt/pcraster/python-2.7.3/bin/python
plot.py := ~/Development/projects/PersonalFiles/Environment/Scripts/plot.py
pcraster_3 := /opt/PCRaster-3.0
pcrcalc_3 := ${pcraster_3}/bin/pcrcalc
pcraster_4 := /opt/pcraster/pcraster-dev
pcrcalc_4 := ${pcraster_4}/bin/pcrcalc


# objects := ${HOME}/Development/objects/gcc-4_x86-64/Release
# pcrcalc_dev := ${objects}/pcrtree2/bin/pcrcalc

# pcrcalc_dev := ~/tmp/pcraster-lsbcc-4_x86-64-20130801/bin/pcrcalc
pcrcalc_dev := ~/tmp/pcrtree2_Release/bin/pcrcalc
# pcrcalc_dev := /home/kor/Development/objects/lsbcc-4_x86-64/Release/pcrtree2/bin/pcrcalc
# time_format := '%U\t%S'
time_format := '%U'
time := time --format ${time_format} --append
nr_rows := 10000
nr_cols := 10000

clone.map:
	${pcraster_4}/bin/mapattr -s -R ${nr_rows} -C ${nr_cols} -B clone.map

scalar.map: clone.map
	${pcraster_4}/bin/pcrcalc "scalar.map=if(clone.map, scalar(5))"

clean:
	rm -f scalar.map clone.map
	rm -f result_3.map log_3.txt
	rm -f result_4.map log_4.txt
	rm -f result_dev.map log_dev.txt
	rm -f plot.pdf

run_3: log_3.txt
run_4: log_4.txt
run_dev: log_dev.txt

log_3.txt: scalar.map
	rm -f log_3.txt
	rm -f result_3.map
	${time} --output log_3.txt ${pcrcalc_3} "result_3.map = 5 * scalar.map"
	rm -f result_3.map
	${time} --output log_3.txt ${pcrcalc_3} "result_3.map = 5 * scalar.map"
	rm -f result_3.map
	${time} --output log_3.txt ${pcrcalc_3} "result_3.map = 5 * scalar.map"

log_4.txt: scalar.map
	rm -f log_4.txt
	rm -f result_4.map
	${time} --output log_4.txt ${pcrcalc_4} "result_4.map = 5 * scalar.map"
	rm -f result_4.map
	${time} --output log_4.txt ${pcrcalc_4} "result_4.map = 5 * scalar.map"
	rm -f result_4.map
	${time} --output log_4.txt ${pcrcalc_4} "result_4.map = 5 * scalar.map"

log_dev.txt: scalar.map
	rm -f log_dev.txt
	rm -f result_dev.map
	${time} --output log_dev.txt ${pcrcalc_dev} "result_dev.map = 5 * scalar.map"
	rm -f result_dev.map
	${time} --output log_dev.txt ${pcrcalc_dev} "result_dev.map = 5 * scalar.map"
	rm -f result_dev.map
	${time} --output log_dev.txt ${pcrcalc_dev} "result_dev.map = 5 * scalar.map"

plot: log_3.txt log_4.txt log_dev.txt
	${python} ${plot.py} --bar log_3.txt --bar log_4.txt --bar log_dev.txt plot.pdf

run: run_3 run_4 run_dev
