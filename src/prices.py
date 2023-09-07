#!/bin/python

from bitcoinrpc.authproxy import AuthServiceProxy
from datetime import datetime
import time
import json
import properties_main as prop

from defichain import Node

# node = Node(prop.RPC_USERNAME, prop.RPC_PASSWORD, prop.PRC_HOST, prop.RPC_PORT)
# print(node.blockchain.getblockcount())
# print(node.poolpair.getpoolpair('USDT-DFI'))

url = f'http://{prop.RPC_USERNAME}:{prop.RPC_PASSWORD}@{prop.PRC_HOST}:{prop.RPC_PORT}'
rpc_conn = AuthServiceProxy(url)

def usdPerDfi():
    try:
        usdt = rpc_conn.getpoolpair("USDT-DFI")

        for pool in usdt.values():
            usdt = pool
            break
    except:
        usdt = None

    try:
        usdc = rpc_conn.getpoolpair("USDC-DFI")
        for pool in usdc.values():
            usdc = pool
            break
    except:
        usdc = None

    total = {'usd': 0, 'dfi': 0}
    def add(ppair):
        if ppair['idTokenA'] == '0':
            total['usd'] += ppair['reserveB']
            total['dfi'] += ppair['reserveA']
        elif ppair['idTokenB'] == '0':
            total['usd'] += ppair['reserveA']
            total['dfi'] += ppair['reserveB']

    if usdt is not None:
        add(usdt)

    if usdc is not None:
        add(usdc)

    return total['usd'] / total['dfi']

def totalLiquitidyUsd(poolpair):
    usd_per_dfi = usdPerDfi()

    totalLiqUsd = 0.0
    if poolpair['idTokenA'] == '0':
        return poolpair['reserveA'] * 2 * usd_per_dfi

    if poolpair['idTokenB'] == '0':
        return poolpair['reserveB'] * 2 * usd_per_dfi

def dexPrice(poolsymbol):
    poolpair = rpc_conn.getpoolpair(poolsymbol)
    for pool in poolpair.values():
        poolpair = pool
        break

    totalUSD = totalLiquitidyUsd(poolpair)

    priceUSD = 0.0
    if poolpair['idTokenA'] == '0':
        priceUSD = totalUSD / 2 / poolpair['reserveB']

    if poolpair['idTokenB'] == '0':
        priceUSD = totalUSD / 2 / poolpair['reserveA']

    return priceUSD

def showPrice(poolsymbol):
    print(poolsymbol.split('-')[0], "in $:", round(dexPrice(poolsymbol),4))

usd_per_dfi = usdPerDfi()
print("DFI in $:", round(usd_per_dfi,4))

showPrice("BTC-DFI")
showPrice("ETH-DFI")
showPrice("DUSD-DFI")


# def getPoolpairs():
#     poolpairs = {}
#     pools = conn.listpoolpairs()
#     for pool in pools.values():
#         poolpairs[pool['symbol']] = pool
    
#     return poolpairs

# poolpairs = getPoolpairs()
# showPrice(poolpairs['DFI-BTC'])

# print(conn.getpoolpair('DFI-BTC'))
