# -*- coding: utf-8 -*-
"""
cron: 1 9,12,18 * * *

new Env('微信阅读の从零开始');
地址: http://dst1ya655g.qqaas.fun/app/main?openId=oiDdr50cvXog64PlMEvSfy3V31Hs#/
微信捉包 http://xxxxxx/read/get 域名请求头里的 cookie

青龙变量 export wxread="authtoken=eyJ0eXAiOiJKV1QiLCJhbxxxxx; snapshot=0" 多账号@隔开

注意:
154行 和 156行 两个参数需换为你自己的
WxPusher官网: https://wxpusher.zjiecode.com/admin/main/app/appInfo
后台新建应用，获取appToken   微信扫描关注后在公众号获取uuid

"""
import requests
import logging
import time
import os, re
import json
import random
from notify import send

# 创建日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad
    from base64 import b64encode
except:
    logger.info(
        "\n未检测到pycryptodome\n需要Python依赖里安装pycryptodome\n安装失败先linux依赖里安装gcc、python3-dev、libc-dev\n如果还是失败,重启容器,或者重启docker就能解决")
    exit(0)

cookies = []
try:
    if "wxread" in os.environ:
        cookies = os.environ["wxread"].split("@")
        if len(cookies) > 0:
            logger.info(f"共找到{len(cookies)}个账号 已获取并使用Env环境Cookie")
            logger.info("声明：本脚本为学习python 请勿用于非法用途")
    else:
        logger.info("【提示】变量格式: authtoken=eyJ0eXAiOiJKV1QiLCJhbxxxxx; snapshot=0\n环境变量添加: wxread")
        exit(3)
except Exception as e:
    logger.error(f"发生错误：{e}")
    exit(3)


# -------------------------分割线------------------------
class miniso:
    @staticmethod
    def setHeaders(i):
        headers = {
            "X-Requested-With": "com.tencent.mm",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Linux; Android 12; V2203A Build/SP1A.210812.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 XWEB/5197 MMWEBSDK/20230405 MMWEBID/9296 MicroMessenger/8.0.35.2360(0x2800235D) WeChat/arm64 Weixin NetType/WIFI Language/zh_CN ABI/arm64",
            "Cookie": cookies[i],
        }
        return headers

    @staticmethod
    def geturl(headers, detection):
        try:
            url = f'http://nqyt2plpvv.qqaas.fun/app/read/get'
            response = requests.get(url=url, headers=headers)
            result = response.json()
            id = re.search(r'u=(\w+)', result['data']['location']).group(1)
            res = f"获取阅读url: 成功"
            logger.info(res)
            log_list.append(res)
            time.sleep(5)
            miniso.doRead(headers, id, detection)
        except Exception as e:
            print(e)

    @staticmethod
    def doRead(headers, id, detection):
        try:
            url = f'https://sss.mvvv.fun/app/task/doRead?u={id}&type=1'
            response = requests.get(url=url, headers=headers)
            result = response.json()
            if result['data']['taskKey'] is not None:
                taskKey = result['data']['taskKey']
                taskUrl = result['data']['taskUrl']
                miniso.Intercept(headers, taskUrl, detection)
                time.sleep(10)
                miniso.Read(headers, id, taskKey, detection)
            else:
                res = f"获取参数: 获取阅读参数失败！"
                logger.info(res)
                log_list.append(res)
        except Exception as e:
            print(e)

    @staticmethod
    def Read(headers, id, taskKey, detection):
        try:
            url = f'https://sss.mvvv.fun/app/task/doRead?u={id}&type=1&key={taskKey}'
            response = requests.get(url=url, headers=headers)
            result = response.json()
            if result['data']['detail'] == '检测中':
                miniso.doRead(headers, id, detection)
            elif result['code'] == 0 and result['data']['taskKey'] is not None:
                taskKey = result['data']['taskKey']
                taskUrl = result['data']['taskUrl']
                miniso.Intercept(headers, taskUrl, detection)
                sleeptime = random.randint(10, 15)
                res = f"阅读: {result['data']['detail']} -- 随机等待{sleeptime}秒后继续...."
                logger.info(res)
                time.sleep(sleeptime)
                miniso.Read(headers, id, taskKey, detection)
            else:
                res = f"阅读: 没获取到文章id,可能本轮阅读已完成 或 此账号已被限制!"
                logger.info(res)
                log_list.append(res)
        except Exception as e:
            print(e)

    @staticmethod
    def Intercept(headers, taskUrl, detection):
        try:
            url = f'{taskUrl}'
            response = requests.get(url=url, headers=headers)
            match = re.search(r'_g.msg_link = "(.*?)";', response.text)
            if match:
                msg_link = match.group(1)
            match = re.search(r'biz\s*=\s*""\s*\|\|\s*"([^"]+)"', response.text)
            if match:
                biz_value = match.group(1)
                logger.info('biz_value:', biz_value)
                if biz_value in detection:
                    res = f"获取参数: 成功 --是检测文章请在10秒内点击！"
                    logger.info(res)
                    miniso.Push(headers, msg_link)
                else:
                    pass
        except Exception as e:
            print(e)

    @staticmethod
    def Push(headers, msg_link):
        try:
            url = f'https://wxpusher.zjiecode.com/api/send/message'
            data = {
                "appToken": '你的WxPusher后台创建应用的appToken',
                "content": f'<meta http-equiv="refresh" content="0; url={msg_link}">',
                "summary": '从零开始阅读检测',
                "contentType": 2,
                "uids": ['你的WxPusher的UID'],
                "verifyPay": 'False'
            }
            response = requests.post(url=url, headers=headers, json=data)
        except Exception as e:
            print(e)

    @staticmethod
    def my(headers):
        try:
            url = f'http://qmctk1sfcw.qqaas.fun/app/user/myInfo'
            response = requests.get(url=url, headers=headers)
            return response.json()
        except Exception as e:
            print(e)

    @staticmethod
    def myPickInfo(headers):
        try:
            url = f'http://qmctk1sfcw.qqaas.fun/app/user/myPickInfo'
            response = requests.get(url=url, headers=headers)
            return response.json()
        except Exception as e:
            print(e)

    @staticmethod
    def pickAuto(headers, sign):
        try:
            data = sign
            url = 'http://mhxbn1se67.qqaas.fun/app/user/pickAuto'
            response = requests.post(url, headers=headers, data=data)
            result = response.json()
            if result['code'] == 0:
                res = f"提现: 拔毛成功！"
                logger.info(res)
                log_list.append(res)
            else:
                res = f"提现: {result['msg']}"
                logger.info(res)
                log_list.append(res)
        except Exception as e:
            print(e)

def encrypt(plaintext):
    key = b'5e4332761103722eb20bb1ad53907c6e'
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
    return b64encode(ciphertext).decode()

if __name__ == '__main__':
    log_list = []  # 存储日志信息的全局变量
    biz_value = f"\n⏰请积极参与收集检测文章,如果阅读失败了,请将biz_value加入detection里,顺便提交给脚本作者,谢谢合作！\n"
    logger.info(biz_value)
    log_list.append(biz_value)
    for i in range(len(cookies)):
        head = f"\n------------开始第[{i + 1}]个账号------------"
        detection = {'Mzg4MDU1MTc0NA==', 'MzU5MDc0NjU4Mg==', 'MzA3Njk1NzAyNA==', 'MzI2ODcwOTQzMg==', 'MzU5ODU0MzM4Mg==',
                     'Mzg2OTcwOTQzNQ==', 'MzI0NTgyOTYxOQ==', 'MzI3MTY2OTYyNA==', 'MjM5NTY1OTI0MQ==', 'MzU3ODEyNTgyNQ==',
                     'MzkyNDIxMzE4OA==', 'MzI1NjY4Njc0Mw==', 'MzU4OTg3Njg1Nw=='}
        logger.info(head)
        log_list.append(head)
        headers = miniso.setHeaders(i)

        result = miniso.my(headers)
        if result['code'] == 0:
            res = f"账号: {result['data']['nameNick']} 今日已读:{result['data']['completeTodayCount']}次 金币:{result['data']['goldNow']}"
            logger.info(res)
            log_list.append(res)
            if result['data']['remainSec'] == 0:
                miniso.geturl(headers, detection)
            else:
                res = f"状态: 距离下次阅读还有{result['data']['remainSec']//60}分钟"
                logger.info(res)
                log_list.append(res)

            result = miniso.myPickInfo(headers)
            if result['data']['goldNow'] >= 0.4:
                result = miniso.myPickInfo(headers)
                data = result['data']['goldNow']
                body = f'{{"moneyPick":{data:.1f}}}'
                sign = encrypt(body)
                miniso.pickAuto(headers,sign)
        else:
            res = f"账号: {result['msg']}"
            logger.info(res)
            log_list.append(res)

    logger.info("\n============== 推送 ==============")
    send("微信阅读の从零开始", '\n'.join(log_list))