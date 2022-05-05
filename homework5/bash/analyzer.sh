#!/bin/bash

echo "1. Общее количество запросов:" > bash_result.txt 
wc -l < access.log >> bash_result.txt 

echo "\n2. Общее количество запросов по типу:" >> bash_result.txt 
awk '{print $6}' access.log | cut -c 2- | sort | uniq -c | sort -rn | awk '{print $2, $1}' >> bash_result.txt \

echo "\n3. Топ 10 самых частых запросов:" >> bash_result.txt 
awk '{print $7}' access.log | sort | uniq -c | sort -nr | head -10 | awk '{print $2, $1}' >> bash_result.txt

echo "\n4. Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой" >> bash_result.txt 
awk '$9 ~ /4../' access.log | awk '{print $7, $9, $10, $1}' | sort -k3 -rn | head -5 >> bash_result.txt

echo  "\n5. Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой" >> bash_result.txt
awk '$9 ~ /5../' access.log | awk '{print $1}' | uniq -c | sort -rn | head -5  | awk '{print $2, $1}' >> bash_result.txt
