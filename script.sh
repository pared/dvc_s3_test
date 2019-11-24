#!/bin/bash

rm -rf repo
mkdir repo

pushd repo
git init >> /dev/null && dvc init -q

mkdir data
for i in {1..1000}
do
	dd bs=1000000 count=1 status=none </dev/urandom >data/$i 
done

echo "-------------------------"
dvc add -q data
dvc remote add -d rmt s3://prd-dvc-test/cache

rm result.txt
ulimit -n 256
dvc push --jobs=128
process_id=$!

# for i in {1..1000000}
# do
# 	# clear
# 	sleep 0.0001
# 	ls -la /proc/$process_id/fd >> ../result.txt
# 	ls /proc/$process_id/fd | wc -l >> ../result.txt
# 	echo "---------------" >> ../result.txt
# done
