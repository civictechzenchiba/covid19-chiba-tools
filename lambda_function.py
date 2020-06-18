from download_pubdata import download
from convert_pubdata import convert
from uploadS3 import uploadS3
 
def lambda_handler(event, context):
    print(event, context)
    download(False)
    data = convert(False)
    uploadS3(data)
