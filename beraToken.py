import time
import requests
from web3 import Web3
import pandas as pd

wallet_path = 'bera_wallet.csv'
outputPath = 'breaTokenOutput.txt'
proxy = "" #你的代理ip填这里
proxyVerified = False
capsolverVerified = False
api_key = ""  # 你的capsolver API密钥
site_key = "0x4AAAAAAARdAuciFArKhVwt"
site_url = "https://bartio.faucet.berachain.com/"

def checkIP(ip):
    proxyVerified = False
    proxies = {
        "http": ip,
        "https": ip
    }
    ipUrl = "https://myip.ipip.net"
    print("开始检测IP是否代理成功...")
    try:
        response = requests.get(ipUrl, proxies=proxies)
        print(response.text)
        proxyVerified = True
        print("IP代理成功 ✅ ...")
        return proxyVerified
    except Exception as e:
        print(f"代理失败: {e}")
        proxyVerified = False
        return proxyVerified

def capsolver():
    payload = {
        "clientKey": api_key,
        "task": {
            "type": 'AntiTurnstileTaskProxyLess',
            "websiteKey": site_key,
            "websiteURL": site_url,
            "metadata": {
                "action": ""  # 可选
            }
        }
    }
    res = requests.post("https://api.capsolver.com/createTask", json=payload)
    resp = res.json()
    task_id = resp.get("taskId")
    if not task_id:
        print("创建任务失败:", res.text)
        return
    print(f"获得任务ID: {task_id} / 获取结果中...")

    while True:
        time.sleep(1)  # 延迟
        payload = {"clientKey": api_key, "taskId": task_id}
        res = requests.post("https://api.capsolver.com/getTaskResult", json=payload)
        resp = res.json()
        status = resp.get("status")
        if status == "ready":
            return resp.get("solution", {}).get('token')
        if status == "failed" or resp.get("errorId"):
            print("解决失败! 响应:", res.text)
            return

def getBearToken(token, gzy_address):
    url = f"https://bartio-faucet.berachain-devnet.com/api/claim?address={gzy_address}"
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "authorization": f"Bearer {token}",
        "content-type": "text/plain;charset=UTF-8",
        "priority": "u=1, i",
        "sec-ch-ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site"
    }
    data = {
        "address": gzy_address
    }

    proxies = {
        "http": proxy,
        "https": proxy
    }

    response = requests.post(url, headers=headers, json=data, proxies=proxies)
    return response.json()

def checkEthBalance(gzy_address):
    print(f'当前钱包地址：{gzy_address}')
    ethProvider = Web3(Web3.HTTPProvider('https://node.onekey.so/eth'))
    balance = ethProvider.eth.get_balance(gzy_address)
    etherBalance = ethProvider.from_wei(balance, 'ether')
    return etherBalance

def main():
    walletList = pd.read_csv(wallet_path)
    addresses = walletList['address']

    with open(outputPath, 'a') as file:
        for gzy_address in addresses:
            etherBalance = checkEthBalance(gzy_address)
            if etherBalance >= 0.001:
                print(f"当前地址 {gzy_address} : 主网余额满足条件 ✅ --- 当前余额：{etherBalance}")
                result = checkIP(proxy)
                if result:
                    token = capsolver()
                    print(f'人机验证Token：{token}')
                    if token:
                        resultJson = getBearToken(token, gzy_address)
                        print(f"地址 {gzy_address} : 任务完成 ✅ 消息：{resultJson['msg']}")
                        file.write(f"地址 {gzy_address} : 任务完成 ✅ 消息：{resultJson['msg']}\n")
                    else:
                        print(f"任务终止：原因：人机验证失败，capsolver：{capsolverVerified}")
            else:
                print(f"当前地址 {gzy_address} : 主网余额不足 0.001 --- 当前余额：{etherBalance}")
            time.sleep(3)

main()
