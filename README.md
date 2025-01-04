# 商品信息管理系统-MySQL -python -Flask
适用于大作业以及课设

(!!!含报告!!!)

基于python语言和MySQL，并结合Flask前端实现商品信息管理系统

效果请看images文件夹

前后端分离

后端采用pymysql库实现对MySQL数据库的操作

数据库建立了四张表，三个视图，四个触发器，若干索引

           实现复杂查询（嵌套，多表连接），删除，插入，更新
           
前端采用Flask框架实现Web可视化，同时包含登录和注册

from flask import Flask, render_template, request, redirect, url_for, flash, session

from product_pack import ProductManager

import os

import pymysql

需要导入上述库

有需要的可以加qq：2317595392



