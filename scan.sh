#!/bin/bash

dominio=$1

dig +short A $dominio > A.txt
dig +short CNAME $dominio > CNAME.txt
dig +short NS $dominio > NS.txt
dig +short MX $dominio > MX.txt

nmap -T4 -F $dominio > nmap.txt

echo "RESULTADO DE ESCANEO DE $dominio" > resultado_$dominio.txt
echo "--------" >> resultado_$dominio.txt
echo "A" >> resultado_$dominio.txt
cat A.txt >> resultado_$dominio.txt
echo "--------" >> resultado_$dominio.txt
echo "CNAME" >> resultado_$dominio.txt
cat CNAME.txt >> resultado_$dominio.txt
echo "--------" >> resultado_$dominio.txt
echo "NS" >> resultado_$dominio.txt
cat NS.txt >> resultado_$dominio.txt
echo "--------" >> resultado_$dominio.txt
echo "MX" >> resultado_$dominio.txt
cat MX.txt >> resultado_$dominio.txt
echo "--------" >> resultado_$dominio.txt
cat nmap.txt >> resultado_$dominio.txt
echo "--------" >> resultado_$dominio.txt

enscript resultado_$dominio.txt -o - | ps2pdf - resultado_$dominio.pdf

rm A.txt
rm CNAME.txt
rm NS.txt
rm MX.txt
rm nmap.txt
rm resultado_$dominio.txt
