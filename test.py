from flask import Flask, render_template, request, url_for, jsonify
from web3 import Web3
import json
import os
from pathlib import Path
import requests
import ast

file_path = './build/contracts/AutomobileRegistrationSystem.json'
with open(file_path,'r') as f:
    raw = json.loads(f.read())

abi = raw["abi"]

SYS_ADD = '0x47267A8a0076Da12E13D36DA1627885085dbEcBA'
print(SYS_ADD)

    # Create a Web3 object and connect to the Mumbai testnet
w3 = Web3(Web3.HTTPProvider('https://rpc-mumbai.maticvigil.com'))
contract = w3.eth.contract(address=SYS_ADD, abi=abi)
print(contract)

_NIV='11'
car = contract.functions.getCarInfos(_NIV).call()
print(car)


