#!/bin/bash
echo "Running ${1} with ${2} inserted as Trojan, width ${3}"
mkdir -p ${1}_${2}/input ${1}_${2}/part ${1}_${2}/bench results_${1}_${2}

python sim.py --verbose 6 --ff -b --ckt ${1}_${2}/bench/pyTrojan_${1}.bench-ckt.bench --bist ${1}_${2}/input/pyTrojan_${1}.bench_inputs.pickle ${1}_${2}/bench/pyTrojan_${1}.bench-ckt.bench

python sim.py --verbose 6 -b --ckt ${1}_${2}/bench/pyTrojan_${1}.bench-ckt.bench --bist ${1}_${2}/input/pyTrojan_${1}.bench_inputs.pickle ${1}_${2}/bench/pyTrojan_${1}.bench_*-badckt.bench

