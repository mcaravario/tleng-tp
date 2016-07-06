#!/bin/bash
# Uso: ./check_test.sh [archivo1.i] [archivo2.i] ...

PARSER=../src/SLSParser

count=0
passed=0

for f in $@; do
	echo "########################################################"
	echo "  Parsing $f"
	echo "########################################################"
	${PARSER} -c $f | diff -y - ${f%.i}.io
	if [ $? -eq 0 ]; then
		echo -e "[$f] : \e[32mOK\e[0m"
		passed=$(($passed + 1))
	else
		echo -e "[$f] : \e[0;49;31mFAIL\e[0m"
	fi
	count=$(($count + 1))
done
echo "Se han pasado $passed test sobre un total de $count"
