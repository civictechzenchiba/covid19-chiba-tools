date >> error.log
python download_pubdata.py 2>> error.log
python convert_pubdata.py 2>> error.log | jq . -M  2>> error.log 
cat error.log