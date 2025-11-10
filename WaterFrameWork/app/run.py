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


from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_cors import CORS
from WaterFrameWork.core.Debugger import Debugger


app = Flask(__name__)
CORS(app)

debugger = Debugger()

# 首页路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_debugger_info', methods=['GET'])
def get_debugger_info():
    if request.method == 'GET':
        return debugger.viriables

@app.route('/get_stacktrace_info', methods=['GET'])
def get_stacktrace_info():
    if request.method == 'GET':
        return debugger.stacktrace

@app.route('/post_breakpoints', methods=['POST'])
def post_breakpoints():
    front_breakpoints = request.get_json()
    print(f"* 断点列表：{front_breakpoints}")
    debugger.breakpoints = front_breakpoints
    return jsonify({"code":"back get breakpoints list"})

@app.route('/get_currunt_line', methods=['GET'])
def get_currunt_line():
        # TODO 这里需要写 debugger.currrunt_line
        return jsonify({"curruntline": debugger.currunt_line})

@app.route('/step', methods=['GET'])
def step():
    """
    step 方法只负责更新后端调试器实例的信息，而消息的获取仍然通过之前的接口
    """
    debugger.step()
    return jsonify({"code": "next success!"})

if __name__ == '__main__':
    app.run(debug=True)  # 调试模式启动（开发环境用）