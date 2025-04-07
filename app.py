'''
Date: 2025-03-27 22:24:05
LastEditors: Wang Xiaomei XianYuPigeon@outlook.com
LastEditTime: 2025-04-07 23:01:50
FilePath: /gamestats/app.py
'''
# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)

#配置服务器监听地址端口

@app.get("/")
def read_root():
    return {
        "status": "OK ✔",
        "copyright": "© 2025 Wang Xiaomei (XianYuPigeon@outlook.com)",
        "message": "GameStats API is running"
    }

uvicorn.run(app, host="0.0.0.0", port="8080")