from brownie import network, accounts, exceptions, Contract, config, AutomobileRegistrationSystem,Car,CarFactory
from web3 import Web3
import os
import json
from pathlib import Path
import requests
import pytest

def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])
    
def setup_admin_connexion():

    SYS_ADD = os.environ.get('SYS_ADD')
    system = Contract.from_abi('AutomobileRegistrationSystem', SYS_ADD, AutomobileRegistrationSystem.abi)
    account = get_account()
    return system,account

def deploy():
    account = get_account()
     
    system = AutomobileRegistrationSystem.deploy(
        {
        "from" : account
        })
    
    return account,system


def setup_account(role):


    if network.show_active() == "development":
        return accounts[0]
    else:
        if role == '0':
            account = accounts.add(config["wallets"]["Manufacture"])

    return account
    



    
def test_deploy_correctly():
    account = get_account()
    try: 
        system = AutomobileRegistrationSystem.deploy(
        {
        "from" : account
        })
        print('Automobile Regestration system contract Deployed')
    except Exception as e:
        print('Not deployed correctly')

def test_Modify_without_roles():
    account,system = deploy()
    data = {
    "NIV":"11",
    "Date":"25/06/2001",
    "Fabrication":"Renault",
    "Modele":"R6",
    "Type_Carrosserie":"Berlin",
    "Annee_Production":"2018",
    "Carburant":"Diesel",
    "Transmition":"Auto",
    "Moteur":"Puissant"
    }
    
    assert system.createNewCar('212212',data,{"from":account}), " YOU DONT HAVE THE PERMISSION"
    

    

def test_with_given_role():
    account,system = deploy()
    data = {
    "NIV":"11",
    "Date":"25/06/2001",
    "Fabrication":"Renault",
    "Modele":"R6",
    "Type_Carrosserie":"Berlin",
    "Annee_Production":"2018",
    "Carburant":"Diesel",
    "Transmition":"Auto",
    "Moteur":"Puissant"
    }
    Maccount = setup_account('0')
    system.setRole(config["wallets"]["public_keys"]['Manufacture'],0,1,{"from":account})
    assert system.createNewCar('212212',data,{"from":Maccount}), "ONLY Manifacture can add cars"


    


    





