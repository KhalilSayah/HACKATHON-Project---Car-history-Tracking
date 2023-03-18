from brownie import network, config, accounts, AutomobileRegistrationSystem,Car,CarFactory, helpful_scripts
from web3 import Web3
import os,requests,json
from pathlib import Path

def deploy_system():
    account = get_account()
    system = AutomobileRegistrationSystem.deploy(
        {
        "from" : account
        }
    )
    print('Automobile Regestration system contract Deployed')


def main():
    pass


