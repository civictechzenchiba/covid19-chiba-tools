from download_pubdata import download
from convert_pubdata import convert
 
def lambda_handler(event, context):
    print(event, context)
    download(False)
    convert(False)
