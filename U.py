import os
import requests
import json
import re
import time
import random

# 初始化 Origins 变量，只在第一次迭代中赋值
timestamp1 = int(time.time())
ten_digit_timestamp = timestamp1 // 10
Origins = f'https://b{ten_digit_timestamp}-1304258503.cos.ap-beijing.myqcloud.com'

def main():
    method = "GET"

    cookies = []  # 存储多个Cookie
    uks = []  # 存储多个uk值
    i = 1

    # 读取环境变量中的Cookie和uk值，直到找不到为止
    while True:
        cookie_key = f'COOKIE_{i}'
        uk_key = f'UK_{i}'

        if cookie_key in os.environ and uk_key in os.environ:
            cookies.append(os.environ[cookie_key])
            uks.append(os.environ[uk_key])
            i += 1
        else:
            break

    for i in range(len(cookies)):
        # 使用 cookies[i] 和 uks[i] 构建对应的请求
        url1 = f"https://nsr.zsf2023e458.cloud/yunonline/v1/do_read?uk={uks[i]}"
        headers1 = {
            'Origin': Origins,
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Host': 'nsr.zsf2023e458.cloud',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.39(0x18002733) NetType/4G Language/zh_CN',
            'Accept-Language': 'zh-CN,zh-Hans;q=0.9',
            'Cookie': cookies[i],  # 使用对应的Cookie
        }
        body1 = ""

        response1 = requests.request(method, url1, headers=headers1, data=body1)
        jsonData = json.loads(response1.text)
        link = jsonData['data']['link']
        print("Link: " + link)

        matches = re.search(r'\/\/([^\/]+)\/', link)
        if matches and len(matches.groups()) > 0:
            matchedText = matches.group(1)
            print("Matched text: " + matchedText)

            sleep_time1 = random.randint(10, 15)  # 随机等待时间
            print(f"Sleeping for {sleep_time1} seconds...")
            time.sleep(sleep_time1)

            url2 = link + "?/"
            headers2 = {
                'Cookie': 'ysm_uid=non1312141d3d7e1e28650b515a6aa18043',
                'Accept-Encoding': 'gzip, deflate',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Connection': 'keep-alive',
                'Host': matchedText,
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.39(0x18002733) NetType/4G Language/zh_CN',
                'Upgrade-Insecure-Requests': '1',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
            }
            body2 = ""

            response2 = requests.request(method, url2, headers=headers2, data=body2)
            print(response2.text)

            sleep_time2 = random.randint(10, 15)  # 随机等待时间
            print(f"Sleeping for {sleep_time2} seconds...")
            time.sleep(sleep_time2)

            timestamp = str(int(time.time()))
            url3 = f'https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk={uks[i]}&time=12&timestamp={timestamp}'
            headers3 = {
                'Origin': Origins,
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Host': 'nsr.zsf2023e458.cloud',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.39(0x18002733) NetType/4G Language/zh_CN',
                'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
            }
            body3 = ""

            response3 = requests.request(method, url3, headers=headers3, data=body3)
            print(response3.text)

            # 检查返回体中是否包含'再来阅读'，如果包含则退出循环
            if '再来阅读' in response3.text:
                print("检测到 '再来阅读'，停止运行")
                break

if __name__ == "__main__":
    main()

