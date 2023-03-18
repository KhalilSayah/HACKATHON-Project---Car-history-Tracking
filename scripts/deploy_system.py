from brownie import network, config, accounts, AutomobileRegistrationSystem,Car,CarFactory
from web3 import Web3
import os
import json
from pathlib import Path
import requests




def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy():
    account = get_account()
    system = AutomobileRegistrationSystem.deploy(
        {
        "from" : account
        }
    )
    print('Automobile Regestration system contract Deployed')
    return system

def main():
    system = deploy()

    variable_name = 'SYS_ADD'
    new_value = system.address

    with open('.env', 'r') as f:
        
        lines = f.readlines()

    # Modify the line with the specified variable name
    for i, line in enumerate(lines):
        if line.startswith(f'export {variable_name}='):
            lines[i] = f'export {variable_name}={new_value}\n'
            break

    # Save the changes back to the .env file
    with open('.env', 'w') as f:
        f.writelines(lines)

    
