from download_pubdata import download
from convert_pubdata import convert
from uploadS3 import uploadS3
 

def lambda_handler(event, context):
    print(event, context)
    download(False)
    data = convert(False)

    if(event['detail-type'] == 'test'):
        # 本番反映前のテスト用、AWS Web lambda Consol
        # テストイベント設定で"event-type":"test"を設定
        uploadS3(data, "DataPubTest.json")
    else:
        uploadS3(data, "DataPub.json")
