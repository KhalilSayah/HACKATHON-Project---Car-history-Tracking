from brownie import network, config, accounts, Contract, AutomobileRegistrationSystem,Car,CarFactory
from web3 import Web3
import os,requests,json
from pathlib import Path



def returnCarAdd(system,data):
    _NIV = data["NIV"]
    add = system.getCar(_NIV)
    print(f'Voici laddress de la voiture : {add}')
    return add


data = {
    "NIV": "111111",
    "Fabrication": "renault",
    "Modele": "GTLine",
    "Type_Carrosserie": "Berlin",
    "Annee_Production": "2015",
    "Carburant": "Gasoil",
    "Transmition": "Auto",
    "Moteur": "Hme9"
    }

def main():
    contract_address =  '0x3A29a51B509067D5dB5d811D03A9d8246De83491'
    contract = Contract.from_abi('AutomobileRegistrationSystem', contract_address, AutomobileRegistrationSystem.abi)
    cars = returnCarAdd(contract,data)
    print(cars)

