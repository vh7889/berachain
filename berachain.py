from web3 import Web3
from loguru import logger
web3 = Web3(Web3.HTTPProvider('https://bartio.rpc.berachain.com/'))
dex_address = Web3.to_checksum_address('0x21e2C0AFd058A89FCf7caf3aEA3cB84Ae977B73D')
dex_abi = '''[
  {
    "type": "constructor",
    "inputs": [
      {
        "name": "_crocSwapDex",
        "type": "address",
        "internalType": "address"
      },
      {
        "name": "_crocImpact",
        "type": "address",
        "internalType": "address"
      },
      {
        "name": "_crocQuery",
        "type": "address",
        "internalType": "address"
      }
    ],
    "stateMutability": "nonpayable"
  },
  {
    "type": "receive",
    "stateMutability": "payable"
  },
  {
    "type": "function",
    "name": "crocSwapDex",
    "inputs": [],
    "outputs": [
      {
        "name": "",
        "type": "address",
        "internalType": "contract CrocSwapDex"
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "multiSwap",
    "inputs": [
      {
        "name": "_steps",
        "type": "tuple[]",
        "internalType": "struct SwapHelpers.SwapStep[]",
        "components": [
          {
            "name": "poolIdx",
            "type": "uint256",
            "internalType": "uint256"
          },
          {
            "name": "base",
            "type": "address",
            "internalType": "address"
          },
          {
            "name": "quote",
            "type": "address",
            "internalType": "address"
          },
          {
            "name": "isBuy",
            "type": "bool",
            "internalType": "bool"
          }
        ]
      },
      {
        "name": "_amount",
        "type": "uint128",
        "internalType": "uint128"
      },
      {
        "name": "_minOut",
        "type": "uint128",
        "internalType": "uint128"
      }
    ],
    "outputs": [
      {
        "name": "out",
        "type": "uint128",
        "internalType": "uint128"
      }
    ],
    "stateMutability": "payable"
  },
  {
    "type": "function",
    "name": "previewMultiSwap",
    "inputs": [
      {
        "name": "_steps",
        "type": "tuple[]",
        "internalType": "struct SwapHelpers.SwapStep[]",
        "components": [
          {
            "name": "poolIdx",
            "type": "uint256",
            "internalType": "uint256"
          },
          {
            "name": "base",
            "type": "address",
            "internalType": "address"
          },
          {
            "name": "quote",
            "type": "address",
            "internalType": "address"
          },
          {
            "name": "isBuy",
            "type": "bool",
            "internalType": "bool"
          }
        ]
      },
      {
        "name": "_amount",
        "type": "uint128",
        "internalType": "uint128"
      }
    ],
    "outputs": [
      {
        "name": "out",
        "type": "uint128",
        "internalType": "uint128"
      },
      {
        "name": "predictedQty",
        "type": "uint256",
        "internalType": "uint256"
      }
    ],
    "stateMutability": "view"
  },
  {
    "type": "function",
    "name": "retire",
    "inputs": [],
    "outputs": [],
    "stateMutability": "nonpayable"
  }
]'''
dex_contract = web3.eth.contract(address=dex_address, abi=dex_abi)

mint_honey_address = Web3.to_checksum_address('0xAd1782b2a7020631249031618fB1Bd09CD926b31')
mint_honey_abi = '''[
  {
    "constant": false,
    "inputs": [
      {
        "name": "vault",
        "type": "address"
      },
      {
        "name": "shares",
        "type": "uint256"
      },
      {
        "name": "receiver",
        "type": "address"
      }
    ],
    "name": "mint",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  }
]'''
mint_honey_contract = web3.eth.contract(address=mint_honey_address, abi=mint_honey_abi)

bend_address = Web3.to_checksum_address('0x30A3039675E5b5cbEA49d9a5eacbc11f9199B86D')
bend_abi = '''[
  {
    "constant": false,
    "inputs": [
      {
        "name": "asset",
        "type": "address"
      },
      {
        "name": "amount",
        "type": "uint256"
      },
      {
        "name": "interestRateMode",
        "type": "uint256"
      },
      {
        "name": "referralCode",
        "type": "uint16"
      },
      {
        "name": "onBehalfOf",
        "type": "address"
      }
    ],
    "name": "borrow",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "asset",
        "type": "address"
      },
      {
        "name": "amount",
        "type": "uint256"
      },
      {
        "name": "onBehalfOf",
        "type": "address"
      },
      {
        "name": "referralCode",
        "type": "uint16"
      }
    ],
    "name": "supply",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": true,
    "inputs": [
      {
        "name": "user",
        "type": "address"
      }
    ],
    "name": "getUserAccountData",
    "outputs": [
      {
        "name": "totalCollateralETH",
        "type": "uint256"
      },
      {
        "name": "totalDebtETH",
        "type": "uint256"
      },
      {
        "name": "availableBorrowsETH",
        "type": "uint256"
      },
      {
        "name": "currentLiquidationThreshold",
        "type": "uint256"
      },
      {
        "name": "ltv",
        "type": "uint256"
      },
      {
        "name": "healthFactor",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  }
]'''
bend_contract = web3.eth.contract(address=bend_address, abi=bend_abi)

usdc_address = Web3.to_checksum_address('0xd6d83af58a19cd14ef3cf6fe848c9a4d21e5727c')
usdc_abi = '''[
  {
    "constant": true,
    "inputs": [
      {
        "name": "account",
        "type": "address"
      }
    ],
    "name": "balanceOf",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "spender",
        "type": "address"
      },
      {
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "approve",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  }
]'''
usdc_contract = web3.eth.contract(address=usdc_address, abi=usdc_abi)

honey_address = Web3.to_checksum_address('0x0E4aaF1351de4c0264C5c7056Ef3777b41BD8e03')
honey_abi='''[
  {
    "constant": true,
    "inputs": [
      {
        "name": "account",
        "type": "address"
      }
    ],
    "name": "balanceOf",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "spender",
        "type": "address"
      },
      {
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "approve",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  }
]'''
honey_contract = web3.eth.contract(address=honey_address, abi=honey_abi)

bgt_address = Web3.to_checksum_address('0xbDa130737BDd9618301681329bF2e46A016ff9Ad')
bgt_abi = '''[
  {
    "constant": true,
    "inputs": [
      {
        "name": "account",
        "type": "address"
      }
    ],
    "name": "balanceOf",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "spender",
        "type": "address"
      },
      {
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "approve",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  }
]'''
bgt_contract = web3.eth.contract(address=bgt_address, abi=bgt_abi)
wbtc_address =Web3.to_checksum_address('0x286F1C3f0323dB9c91D1E8f45c8DF2d065AB5fae')
wbtc_abi = '''[
  {
    "constant": true,
    "inputs": [
      {
        "name": "account",
        "type": "address"
      }
    ],
    "name": "balanceOf",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": false,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": false,
    "inputs": [
      {
        "name": "spender",
        "type": "address"
      },
      {
        "name": "amount",
        "type": "uint256"
      }
    ],
    "name": "approve",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  }
]'''
wbtc_contract = web3.eth.contract(address=wbtc_address, abi=wbtc_abi)
getBgt_address = Web3.to_checksum_address('0x2E8410239bB4b099EE2d5683e3EF9d6f04E321CC')
getBgt_abi = '''[
  {
    "constant": false,
    "inputs": [
      {
        "name": "_claimer",
        "type": "address"
      }
    ],
    "name": "getReward",
    "outputs": [],
    "payable": false,
    "stateMutability": "nonpayable",
    "type": "function"
  }
]'''
getBgt_contract = web3.eth.contract(address=getBgt_address, abi=getBgt_abi)
class Bera:
    def __init__(self,dex_contract,mint_honey_contract,bend_contract,usdc_contract,honey_contract,wbtc_contract,getBgt_contract,bgt_contract):
        self.dex_contract = dex_contract
        self.mint_honey_contract = mint_honey_contract
        self.bend_contract = bend_contract
        self.usdc_contract = usdc_contract
        self.honey_contract = honey_contract
        self.wbtc_contract = wbtc_contract
        self.getBgt_contract = getBgt_contract
        self.bgt_contract = bgt_contract
        self.address = None
        self.private_key = None
    def swapUsdc(self,amount):
        steps_read = [
            {
                "poolIdx": 36000,
                "base": Web3.to_checksum_address('0x7507c1dc16935b82698e4c63f2746a2fcf994df8'),
                "quote": Web3.to_checksum_address('0xd6d83af58a19cd14ef3cf6fe848c9a4d21e5727c'),
                "isBuy": True
            }
        ]
        amount_read = 1000000000000000000
        output = self.dex_contract.functions.previewMultiSwap(steps_read, amount_read).call()
        _minOut = int(output[0] * 0.9 * amount)
        bear_address_checksum = Web3.to_checksum_address('0x0000000000000000000000000000000000000000')
        quote_address_checksum = Web3.to_checksum_address('0xd6d83af58a19cd14ef3cf6fe848c9a4d21e5727c')
        _steps = [
            {
                "poolIdx": 36000,  # 解析后的值
                "base": bear_address_checksum,  # ETH 地址 (零地址)
                "quote": quote_address_checksum,  # USDT 合约地址
                "isBuy": True,
            }
        ]
        _amount = web3.to_wei(amount, 'ether')
        tx = {
            'nonce': web3.eth.get_transaction_count(self.address),
            'chainId': web3.eth.chain_id,
            'gasPrice': int(web3.eth.gas_price * 1.1),
            'gas': 2000000,
            'value': _amount
        }
        info = dex_contract.functions.multiSwap(_steps, _amount, _minOut)
        txn = info.build_transaction(tx)
        signed_tx = web3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        logger.success(f'Swap-USDC ✅ Swap数量：{amount}--- 哈希：{tx_hash.hex()} ')
    def mintHoney(self):
        amount = usdc_contract.functions.balanceOf(self.address).call()
        tx = {
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(self.address),
            'chainId': web3.eth.chain_id,
            'gas': 2000000
        }
        spender_address = Web3.to_checksum_address('0xAd1782b2a7020631249031618fB1Bd09CD926b31')
        info = usdc_contract.functions.approve(spender_address,amount)
        txn = info.build_transaction(tx)
        signed_tx = web3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        logger.success(f'授权USDC ✅ 授权数量：{amount/10 **6}--- 哈希：{tx_hash.hex()} ')
        tx['nonce'] = web3.eth.get_transaction_count(self.address)
        info = mint_honey_contract.functions.mint(usdc_address,amount, self.address)
        txn = info.build_transaction(tx)
        signed_tx = web3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        logger.success(f'Mint-Honey ✅ 消耗Usdc数量：{amount/10**6}--- 哈希：{tx_hash.hex()} ')
    def bend(self):
        steps_read = [
            (
                36002,  # poolIdx
                Web3.to_checksum_address('0x286f1c3f0323db9c91d1e8f45c8df2d065ab5fae'),  # base
                Web3.to_checksum_address('0x7507c1dc16935b82698e4c63f2746a2fcf994df8'),  # quote
                False  # isBuy
            )
        ]
        amount_read = 1000000000000000000  # 1 ETH
        output = dex_contract.functions.previewMultiSwap(steps_read, amount_read).call()
        tx = {
            'nonce': web3.eth.get_transaction_count(self.address),
            'chainId': web3.eth.chain_id,
            'gasPrice': web3.eth.gas_price,
            'gas': 2000000,
            'value': web3.to_wei(0.1, 'ether')
        }
        _steps = [
            {
                "poolIdx": 36002,  # 解析后的值
                "base": wbtc_address,  #
                "quote": Web3.to_checksum_address('0x0000000000000000000000000000000000000000'),  #
                "isBuy": False
            }
        ]
        _amount = web3.to_wei(0.1, 'ether')
        _minOut = int(output[0] * 0.09)
        info = dex_contract.functions.multiSwap(_steps, _amount, _minOut)
        txn = info.build_transaction(tx)
        signed_tx = web3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        logger.success(f'Swap-WBTC ✅ Swap数量：0.1--- 哈希：{tx_hash.hex()} ')
        amount = wbtc_contract.functions.balanceOf(self.address).call()
        spender_address = Web3.to_checksum_address('0x30A3039675E5b5cbEA49d9a5eacbc11f9199B86D')
        info = wbtc_contract.functions.approve(spender_address,amount)
        tx = {
            'nonce': web3.eth.get_transaction_count(self.address),
            'chainId': web3.eth.chain_id,
            'gasPrice': web3.eth.gas_price,
            'gas': 2000000
        }
        txn = info.build_transaction(tx)
        signed_tx = web3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        formatted_amount = "{:.8f}".format(amount / 10 ** 8)  # 保留8位小数
        logger.success(f'授权-WBTC ✅ 授权数量：{formatted_amount}--- 哈希：{tx_hash.hex()}')
        tx = {
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(self.address),
            'chainId': web3.eth.chain_id,
            'gas': 2000000
        }
        info = bend_contract.functions.supply(wbtc_address, amount, self.address, 8)
        txn = info.build_transaction(tx)
        signed_tx = web3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        logger.success(f'Supply-WBTC ✅ Supply数量：{formatted_amount}--- 哈希：{tx_hash.hex()} ')
        amount = honey_contract.functions.balanceOf(self.address).call()
        tx = {
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(self.address),
            'chainId': web3.eth.chain_id,
            'gas': 2000000
        }
        spender_address = Web3.to_checksum_address('0x30A3039675E5b5cbEA49d9a5eacbc11f9199B86D')
        info = honey_contract.functions.approve(spender_address, amount)
        txn = info.build_transaction(tx)
        signed_tx = web3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        logger.success(f'授权-Honey ✅ 授权数量：{web3.from_wei(amount,'ether')}--- 哈希：{tx_hash.hex()}')
        tx = {
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(self.address),
            'chainId': web3.eth.chain_id,
            'gas': 2000000
        }
        info = bend_contract.functions.supply(honey_address, amount, self.address, 18)
        txn = info.build_transaction(tx)
        signed_tx = web3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        logger.success(f'Supply-Honey ✅ Supply数量：{web3.from_wei(amount,'ether')}--- 哈希：{tx_hash.hex()}')
        output = bend_contract.functions.getUserAccountData(self.address).call()
        tx = {
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(self.address),
            'chainId': web3.eth.chain_id,
            'gas': 2000000
        }
        borrow_addr1 = Web3.to_checksum_address('0x0E4aaF1351de4c0264C5c7056Ef3777b41BD8e03')
        info = bend_contract.functions.borrow(borrow_addr1,int(output[2]*9*10**9), 2, 0, self.address)
        txn = info.build_transaction(tx)
        signed_tx = web3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        logger.success(f'Borrow-Honey ✅ Borrow数量：{output[2]*0.9/10**8}--- 哈希：{tx_hash.hex()}')
        output = bend_contract.functions.getUserAccountData(self.address).call()
        logger.info(f'当前地址:{self.address}---总借出额度：{output[1]/10**8} HONEY')
    def getBgt(self):
        tx = {
            'gasPrice': web3.eth.gas_price,
            'nonce': web3.eth.get_transaction_count(self.address),
            'chainId': web3.eth.chain_id,
            'gas': 2000000
        }
        info = getBgt_contract.functions.getReward(self.address)
        txn = info.build_transaction(tx)
        signed_tx = web3.eth.account.sign_transaction(txn, self.private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        logger.success(f'获取Bgt成功 ✅ 哈希:{tx_hash.hex()}')
        usdc_balance = usdc_contract.functions.balanceOf(self.address).call()
        honey_balance = honey_contract.functions.balanceOf(self.address).call()
        wbtc_balance = wbtc_contract.functions.balanceOf(self.address).call()
        bgt_balance = bgt_contract.functions.balanceOf(self.address).call()
        bera_balance = web3.eth.get_balance(self.address)
        logger.info(f'当前账户:{self.address}-余额：{web3.from_wei(bera_balance,'ether'):.2f} -Bera | {web3.from_wei(honey_balance,'ether'):.5f} -Honey | {(usdc_balance/10*6):.4f} -Usdc | {wbtc_balance/10*8:.6f} -WBTC | {web3.from_wei(bgt_balance,'ether'):.6f} -BGT')
bera = Bera(dex_contract=dex_contract,mint_honey_contract=mint_honey_contract,bend_contract=bend_contract,usdc_contract=usdc_contract,honey_contract=honey_contract,wbtc_contract=wbtc_contract,getBgt_contract=getBgt_contract,bgt_contract=bgt_contract)
