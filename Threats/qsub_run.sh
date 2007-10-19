#!/bin/bash

if [ -z "$1" ]
  then
  printf "Usage: $0 start..end\n"
else
  # trick from http://tardate.blogspot.com/2007/01/handling-range-parameters-in-bash.html
  v_range="$1"       # or you could have taken it as a script parameter
  v_start=${v_range%%.*} # chomp everything from the left-most matching "."
  v_end=${v_range##*.}   # chomp everything up to the right-most matching "."

  for ((a=v_start; a<= v_end; a++))
  do
    qsub monte_carlo_threats.sh ~/csv/MC$a.csv /state/partition1/grass/mc
  done
fi
