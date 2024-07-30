import csv
import random
import time
from web3 import Web3
from berachain import Bera, bgt_contract, getBgt_contract, wbtc_contract, honey_contract, \
    usdc_contract, bend_contract, mint_honey_contract, dex_contract  # 假设 Bera 类在 bera 模块中
web3 = Web3(Web3.HTTPProvider('https://bartio.rpc.berachain.com/'))
# 读取CSV文件，获取钱包信息
def read_wallets(file_path):
    wallets = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            wallets.append({
                "number": int(row["number"]),
                "address": row["address"],
                "privateKey": row["privateKey"]
            })
    return wallets

# 执行指定方法
def execute_method(wallets, wallet_indices, method_name, delay_range, *args):
    for index in wallet_indices:
        wallet = wallets[index - 1]
        private_key = wallet["privateKey"]
        address = wallet["address"]
        account = web3.eth.account.from_key(private_key)

        bera = Bera(
            dex_contract=dex_contract,
            mint_honey_contract=mint_honey_contract,
            bend_contract=bend_contract,
            usdc_contract=usdc_contract,
            honey_contract=honey_contract,
            wbtc_contract=wbtc_contract,
            getBgt_contract=getBgt_contract,
            bgt_contract=bgt_contract
        )
        bera.account = account
        bera.address = address
        bera.private_key = private_key

        # 随机延迟
        delay = random.uniform(*delay_range)
        time.sleep(delay)

        # 执行指定的方法
        method = getattr(bera, method_name)
        method(*args)
        print(f"Executed {method_name} for wallet {wallet['number']} with delay {delay:.2f} seconds.")

# 主程序
# 主程序部分
if __name__ == "__main__":
    file_path = 'bera_wallet.csv'
    wallets = read_wallets(file_path)

    # 获取用户输入
    wallet_input = input("请输入钱包序号范围（例如 1-5）: ")
    method_name = input("请输入要执行的方法名：<swapUsdc> | <mintHoney> | <bend> | <getBgt> ; 如果输入<all>，则执行全部流程: ")
    delay_input = input("请输入延迟范围（例如 2-5）: ")

    # 解析输入
    start, end = map(int, wallet_input.split('-'))
    delay_min, delay_max = map(int, delay_input.split('-'))
    wallet_indices = list(range(start, end + 1))
    delay_range = (delay_min, delay_max)

    # 方法列表
    methods_to_execute = []
    if method_name == "all":
        methods_to_execute = [
            ("swapUsdc", (float(input("请输入要交换的 Bera 数量: ")),)),
            ("mintHoney", ()),
            ("bend", ()),
            ("getBgt", ())
        ]
    else:
        if method_name == "swapUsdc":
            amount = float(input("请输入要交换的 Bera 数量: "))
            args = (amount,)
        else:
            args = ()
        methods_to_execute = [(method_name, args)]

    # 执行指定方法
    for method, args in methods_to_execute:
        execute_method(wallets, wallet_indices, method, delay_range, *args)