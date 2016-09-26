echo "Running ${1} with ${2} inserted as Trojan"
rm -rf results_${1}_${2}-${3}_random
mkdir -p results_${1}_${2}-${3}_random
  
  python sim.py --verbose 6 --ff -b --ckt partitioned/pyTrojan_${1}.bench-ckt.bench --bist partitioned/pyTrojan_${1}.bench_inputs.pickle ${1}_${2}-${3}/bench/pyTrojan_${1}.bench-ckt.bench 
  python sim.py --verbose 6 -b --ckt partitioned/pyTrojan_${1}.bench-ckt.bench --bist partitioned/pyTrojan_${1}.bench_inputs.pickle ${1}_${2}-${3}_random/bench/pyTrojan_${1}.bench_*-badckt.bench
