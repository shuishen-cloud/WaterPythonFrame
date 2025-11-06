'''
Filename:  run.py
Project:   app
Author:    lwy
***
Created:   2025/10/30 Thursday 21:04:26
Modified:  2025/10/30 Thursday 21:04:31
***
Description: 启动 Flask 服务
'''


from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from WaterFrameWork.core.Debugger import Debugger


app = Flask(__name__)
CORS(app)

debugger = Debugger()

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

# 问候页面路由（支持 GET 和 POST 方法）
@app.route('/greet', methods=['GET', 'POST'])
def greet():
    if request.method == 'POST':
        # 获取表单提交的用户名
        name = request.form.get('name', '匿名用户')
        return render_template('greet.html', name=name)
    # GET 请求时返回表单页面
    return render_template('greet.html')

@app.route('/get_debugger_info', methods=['GET', 'POST'])
def get_debugger_info():
    if request.method == 'GET':
        # return "the string from flask_debugger"
        return debugger.viriables

@app.route('/get_stacktrace_info', methods=['GET', 'POST'])
def get_stacktrace_info():
    if request.method == 'GET':
        return debugger.stacktrace


if __name__ == '__main__':
    app.run(debug=True)  # 调试模式启动（开发环境用）