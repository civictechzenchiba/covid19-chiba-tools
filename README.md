# covid19-chiba-tools

千葉県版のツール

## 使い方

https://drive.google.com/drive/folders/1Sul3YKEwpI3MZzDW1dAnlMuO6A5S3fVR

まず、上記Google Driveからxlsxファイルをダウンロードをしておく。

```
git clone https://github.com/civictechzenchiba/covid19-chiba-tools.git
cd covid19-chiba-tools
cp ~/Downloads/covid19健康福祉部*.xlsx downloads/
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python convert.py | jq . > data.json
```
