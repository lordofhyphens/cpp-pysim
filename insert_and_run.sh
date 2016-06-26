#!/bin/bash
echo "Running ${1} with ${2} inserted as Trojan"
rm -rf ${1}_${2} results_${1}_${2}
mkdir -p ${1}_${2}/input ${1}_${2}/part ${1}_${2}/bench results_${1}_${2}

pypy ./test.py --outdir ${1}_${2} -tc i85/${2}.bench i85/${1}.bench > /dev/null

python sim.py --verbose 0 --ff -b --ckt ${1}_${2}/bench/pyTrojan_${1}.bench-ckt.bench --bist ${1}_${2}/input/pyTrojan_${1}.bench_inputs.pickle ${1}_${2}/bench/pyTrojan_${1}.bench_001-badckt.bench | tee ${1}_${2}.`hostname`.sim.log

python sim.py --verbose 0 -b --ckt ${1}_${2}/bench/pyTrojan_${1}.bench-ckt.bench --bist ${1}_${2}/input/pyTrojan_${1}.bench_inputs.pickle ${1}_${2}/bench/pyTrojan_${1}.bench_*-badckt.bench | tee ${1}_${2}.`hostname`.sim.log
