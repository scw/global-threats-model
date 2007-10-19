#!/bin/bash
#
#$ -cwd
#$ -j y
#$ -S /bin/bash
#
python monte_carlo_threats.py $1 $2
