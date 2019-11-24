# Tello Voice Command

[Ryze Tech Tello](https://store.dji.com/jp/shop/tello-series)用の音声操作プログラムです。

## 使い方

ファイル一式をダウンロードし、ダウンロードしたファイルと同じフォルダ内から以下のコマンドを実行してください。

python3 ./tello_voice_command.py

「準備ができたら <SHIFT> キーを押してください」のメッセージが表示された後、音声コマンドをマイクに向かって発話してください。発話が認識され、操作可能なコマンドが発話されていたら、操作が実行されます。なお、現在サポートされている音声コマンドは以下の通りです。

- 飛べ
- 着陸
- 前
- 後ろ
- 左
- 右
- 上
- 下
- 旋回

5秒発話がないとタイムアウトと判断され、自動着陸します。

操作を終了する際は、ctrl+cを押下げしてください。

## 実行環境

python 3.6以降で動作確認済み
pythonには、以下ライブラリが必要です。
- pynput
- speech_recognition
- janome
- threading
