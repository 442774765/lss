import requests
import json
import time
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 禁用警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



def main():
    timestamp1 = int(time.time())
    ten_digit_timestamp = timestamp1 // 10
    Origins = f'https://b{ten_digit_timestamp}-1304258503.cos.ap-beijing.myqcloud.com'
    print(Origins)

    method = "GET"

    url1 = "https://nsr.zsf2023e458.cloud/yunonline/v1/do_read?uk=a0d782334bd3af666ba2856cd8c300c0"
    headers1 = {
        'Origin': Origins,
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Host': 'nsr.zsf2023e458.cloud',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.39(0x18002733) NetType/4G Language/zh_CN',
        'Accept-Language': 'zh-CN,zh-Hans;q=0.9'
    }
    body1 = ""

    response1 = requests.request(method, url1, headers=headers1, data=body1)
    print(response1)
    jsonData = json.loads(response1.text)
    
    link = jsonData['data']['link']
    print("Link: " + link)

    matches = re.search(r'\/\/([^\/]+)\/', link)
    if matches and len(matches.groups()) > 0:
        matchedText = matches.group(1)
        print("Matched text: " + matchedText)

        time.sleep(10)

        url2 = link + "?/"
        headers2 = {
            'Cookie': 'ysm_uid=oZdBp03T0YHEGAgssGfr8hCCRo1M; ejectCode=1',
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

        time.sleep(10)

        timestamp = str(int(time.time()))
        url3 = f'https://nsr.zsf2023e458.cloud/yunonline/v1/get_read_gold?uk=a0d782334bd3af666ba2856cd8c300c0&time=12&timestamp={timestamp}'
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

if __name__ == "__main__":
    main()
