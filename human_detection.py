#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ai
# flaskモジュールの直下のFlaskとrequestとioのインポート
from flask import Flask, request,render_template,make_response,jsonify
from numpy import *
import io, os
# PIL.Imageのことを今度からIって呼びます
import PIL.Image as I
# 起動開始時のまじない
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1
# http://127.0.0.1:5000をルートとして、("")の中でアクセスポイント指定
# @app.route("hoge")などで指定すると、http://127.0.0.1:5000/hogeでの動作を記述できる。
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    if 'uploadFile' not in request.files:
        make_response(jsonify({'result': 'uploadFile is required.'}))
    file = request.files['uploadFile']
    fileName = file.filename
        # failenameが空だったら
    if '' == fileName:
        make_response(jsonify({'result':'filename must not empty.'}))
        # ioはモジュール binaryは人が読めない形になってる != テキストファイル
    binary = io.BytesIO()
    file.save(binary)
    # bainaryファイルを読み込んでセーブしてる
    img = I.open(binary)
    # lenは配列
    if len(img.split()) == 4:
        background = I.new('RGB', img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[3])
        img = background

    img.save('static/image.jpg', 'JPEG')
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    ai.segmentation("static/image.jpg", "static/result.jpg")
    return render_template('result.html')


@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.context_processor
def utility_processor():
    def add_query(line):
        line += "?{:06d}"
        line =  line.format(random.randint(100000))
        print(line)
        return line
    return dict(add_query=add_query)

if __name__ == "__main__":
    # webサーバー立ち上げ
    app.debug = True
    app.run(host = '0.0.0.0',port = 80)


