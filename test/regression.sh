#!/bin/sh
set -e
out=$(../build/nanoc ./regression.nc)
echo "$out"
echo "$out" | grep -q "fwd 5" || { echo "regression failed: forward call"; exit 1; }
echo "$out" | grep -q "bare xfunc" || { echo "regression failed: bare xfunc"; exit 1; }
echo "$out" | grep -q "keep 7" || { echo "regression failed: bare xfunc in function"; exit 1; }
echo "$out" | grep -q "0 6 6 7 8 hi 0" || { echo "regression failed: for/expression"; exit 1; }
echo "$out" | grep -q "^40$" || { echo "regression failed: forward declarations"; exit 1; }
echo "regression test OK"
