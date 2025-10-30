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

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)  # 调试模式启动（开发环境用）