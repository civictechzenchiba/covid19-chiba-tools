# covid19-chiba-tools

千葉県版のツール

## 使い方

- [健康福祉部データ](https://drive.google.com/drive/folders/1Sul3YKEwpI3MZzDW1dAnlMuO6A5S3fVR)
- [検査実績データ](https://drive.google.com/file/d/1iwE3SzdG_m-cjrTfb4OQWTeMCSy8DEeG/view)

まず、上記Google Driveからxlsxファイルをダウンロードをしておく。

```
git clone https://github.com/civictechzenchiba/covid19-chiba-tools.git
cd covid19-chiba-tools
cp ~/Downloads/covid19健康福祉部*.xlsx health_and_welfare_department/
cp ~/Downloads/検査実績*.xlsx result_set/
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python convert.py | jq . > data.json
```
