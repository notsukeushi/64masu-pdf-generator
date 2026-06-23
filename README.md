# 64ます計算 PDFジェネレーター

子供の学習用に、A4サイズで印刷できる「64ます計算」のPDFを自動生成するPythonスクリプトです。

## 特徴
- 毎回ランダムな数値で問題を生成
- 足し算、引き算、掛け算に対応
- 問題ページと解答ページ（丸付け用）をセットで出力
- 最小値・最大値を指定して難易度調整が可能

## インストール

```bash
pip install -r requirements.txt
```

## 使い方

基本の実行（2桁の足し算）:
```bash
python generate_pdf.py
```

引き算の問題を作る場合:
```bash
python generate_pdf.py -o -
```

掛け算の問題を作る場合:
```bash
python generate_pdf.py -o x
```

数字の桁数（難易度）を変える場合（例: 1桁の計算）:
```bash
python generate_pdf.py -min 1 -max 9
```
