# covid19-chiba-tools

千葉県版のツール

## 使い方

```
git clone https://github.com/civictechzenchiba/covid19-chiba-tools.git
cd covid19-chiba-tools
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
python download.py
python convert.py | jq . > data.json
```

## ファイル

download.pyはdataディレクトリに[Google Drive](https://drive.google.com/drive/folders/1SxZqdYCx5vN2JUPycePzfbnW7L7VTiiS)から以下のxlsxファイルをダウンロードします。

- 検査実施サマリ.xlsx
- 検査実績（データセット）千葉県衛生研究所2019-nCoVラインリスト<日付>.xlsx
- 【<日付>】千葉県_感染者発生状況.xlsx
