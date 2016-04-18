#!/bin/bash
while [ $# > 0 ]; do
  echo $*
  if [ $# -le 1 ]; then
    shift
    continue
  fi
  echo "Running ${1} with ${2} inserted as Trojan"
  rm -rf results_${1}_${2}_random
  mkdir -p ${1}_${2}_random/part ${1}_${2}_random/bench ${1}_${2}_random/bench results_${1}_${2}_random ${1}_${2}/random
  
  pypy sim.py --verbose 0 --ff -b --ckt ${1}_${2}_random/bench/pyTrojan_${1}.bench-ckt.bench --bist ${1}_${2}_random/input/pyTrojan_${1}.bench_inputs.pickle ${1}_${2}_random/bench/pyTrojan_${1}.bench-ckt.bench | gzip > ${1}_${2}.`hostname`.random.ff.sim.log.gz
  
  pypy sim.py --verbose 0 -b --ckt ${1}_${2}/bench/pyTrojan_${1}.bench-ckt.bench --bist ${1}_${2}/input/pyTrojan_${1}.bench_inputs.pickle ${1}_${2}_random/bench/pyTrojan_${1}.bench_*-badckt.bench | gzip > ${1}_${2}.`hostname`.random.sim.log.gz

#  for i in `seq -w 0 499`; do echo "Checking ckt $i"; pypy unpack_pickled.py ${1}_${2}/pyTrojan_${1}.bench_${i}.pickle results_${1}_${2}/pyTrojan_${1}.bench_392-badckt.bench_ff  results_${1}_${2}/pyTrojan_${1}.bench_${i}*bench ; done | tee ${1}_${2}.compare_results.log 
  shift 
  shift
done
