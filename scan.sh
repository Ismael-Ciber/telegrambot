#!/bin/bash

dominio=$1

dig +short A $dominio > A.txt
dig +short CNAME $dominio > CNAME.txt
dig +short NS $dominio > NS.txt
dig +short MX $dominio > MX.txt

nmap -T4 -F $dominio > nmap.txt

echo "RESULTADO DE ESCANEO DE $dominio" > resultado.txt
echo "--------" >> resultado.txt
echo "A" >> resultado.txt
cat A.txt >> resultado.txt
echo "--------" >> resultado.txt
echo "CNAME" >> resultado.txt
cat CNAME.txt >> resultado.txt
echo "--------" >> resultado.txt
echo "NS" >> resultado.txt
cat NS.txt >> resultado.txt
echo "--------" >> resultado.txt
echo "MX" >> resultado.txt
cat MX.txt >> resultado.txt
echo "--------" >> resultado.txt
cat nmap.txt >> resultado.txt
echo "--------" >> resultado.txt

enscript resultado.txt -o - | ps2pdf - resultado.pdf

rm A.txt
rm CNAME.txt
rm NS.txt
rm MX.txt
rm nmap.txt
rm resultado.txt
