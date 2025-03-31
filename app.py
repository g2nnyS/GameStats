'''
Date: 2025-03-27 22:24:05
LastEditors: Wang Xiaomei XianYuPigeon@outlook.com
LastEditTime: 2025-03-27 22:43:25
FilePath: /gamestats/app.py
'''
# -*- coding: utf-8 -*-
from fastapi import FastAPI
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

@app.get("/")
def read_root():
    return {"message": "Gamestats API by @g2nnyS - Status: OK✔"}

@app.post("/maimai")
def maimai_status():
    