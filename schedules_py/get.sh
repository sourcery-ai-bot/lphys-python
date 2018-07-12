#!/usr/bin/env zsh

for i in {1..9}; do wget -qO- --no-check-certificate https://www.lasphys.com/workshops/lasphys18/program-seminar-$i | pandoc -f html -t markdown --wrap=none | sed -e 1,/Schedule/d -e /^$/d > p_sem_$i.md ; done
