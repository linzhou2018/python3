#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/21 17:20
# @Author : Mr.L
# @File : main.py

# -*- coding: UTF-8 -*-
# 导入数据库模块
import pymysql
# 导入Flask框架，这个框架可以快捷地实现了一个WSGI应用
from flask import Flask
# 默认情况下，flask在程序文件夹中的templates子文件夹中寻找模块
from flask import render_template
# 导入前台请求的request模块
from flask import request,Response
import traceback

import flask

# 传递根目录
app = Flask(__name__)


# 默认路径访问登录页面
@app.route('/')
def login():
    return render_template('login.html')


# 默认路径访问注册页面
@app.route('/regist')
def regist():
    return render_template('regist.html')


# 设置响应头
def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


# 获取注册请求及处理
@app.route('/registuser')
def getRigistRequest():
    # 把用户名和密码注册到数据库中

    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect("localhost", "root", "root", "TESTDB")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    sql = "INSERT INTO user(name, password) VALUES (" +"'"+ request.args.get('name') +"'"+ ", " +"'"+ request.args.get(
        'password') + "'"+")"
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        # 注册成功之后跳转到登录页面
        return render_template('login.html')
    except:
        # 抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        return '注册失败'
    # 关闭数据库连接
    db.close()


# 获取登录参数及处理
@app.route('/login')
def getLoginRequest():
    # 查询用户名及密码是否匹配及存在
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect("localhost", "root", "root", "TESTDB")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "select * from user where name=" +"'"+ request.args.get('name') + "'"+" and password=" + request.args.get(
        'password') + ""
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        print(len(results))
        if len(results) == 1:
            return '登录成功'
        else:
            return '用户名或密码不正确'
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
    # 关闭数据库连接
    db.close()


@app.route('/list')
def getAll():
    # 查询用户名及密码是否匹配及存在
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect("localhost", "root", "root", "TESTDB")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    sql = "select * from user "
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        if len(results) >= 1:
            return render_template('list.html', users=results)
        else:
            return '查无此信息'
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
    # 关闭数据库连接
    db.close()


@app.route('/delete')
def getDel():
    # 查询用户名及密码是否匹配及存在
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect("localhost", "root", "root", "TESTDB")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    print(request.args.get('id'))
    sql = "delete from user where id=" + request.args.get('id')
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        return '删除成功'
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
    # 关闭数据库连接
    db.close()

@app.route('/edit')
def getEdit():
    id=request.args.get('id')
    name = request.args.get('name')
    password=request.args.get('password')
    user = [id,name, password]
    print('update:%s' % user)
    return render_template('update.html', user=user)

@app.route('/eidtS',methods = ['POST'])
def getUpd():
    # 查询用户名及密码是否匹配及存在
    # 连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect("localhost", "root", "root", "TESTDB")
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 查询语句
    # print(request.args.get('id'))
    params = request.args if request.method == 'GET' else request.form


    sql = "update  user  set name="+   "'"+params.get('name') +"'"      +  " where id=" + params.get('id')
    print(sql)
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        return '更新成功'
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
    # 关闭数据库连接
    db.close()


# 使用__name__ == '__main__'是 Python 的惯用法，确保直接执行此脚本时才
# 启动服务器，若其他程序调用该脚本可能父级程序会启动不同的服务器
if __name__ == '__main__':
    app.run(debug=True)