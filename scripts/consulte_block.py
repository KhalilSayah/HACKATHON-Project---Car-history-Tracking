from brownie import network, config, accounts, Contract, AutomobileRegistrationSystem,Car,CarFactory
from web3 import Web3
import os
import json
from pathlib import Path
import requests
import ast



SYS_ADD = os.environ.get('SYS_ADD')
print(SYS_ADD)

def returnCarAdd(system,_NIV):
    
    add = system.getCarInfos(_NIV)
    #print(f'Voici laddress de la voiture : {add}')
    return add

def returnCarCrashes(system,_NIV):
     
     _CrashList = system.getAccidentsList(_NIV)
     
     return _CrashList

def returnRapport(system,_NIV):
    
    _RapportList = system.getCarReport(_NIV)
    return _RapportList

def returnTransactions(system,_NIV):
    
    _TransactionsList = system.getCarOwner(_NIV)
    return _TransactionsList

def returnSignalisation(system,_NIV):
    _Signalisation = system.getCarSignalisation(_NIV)
    return _Signalisation

def getlink(hash,Lists):
    listink = Lists
    endpoint = 'https://gateway.pinata.cloud/ipfs/'
    tuple_obj = ast.literal_eval(hash)
    for element in tuple_obj:
        link = endpoint+element
        listink.append(link)
    return listink


def main():
    Links= []
    _NIV = '7'
    system = Contract.from_abi('AutomobileRegistrationSystem', SYS_ADD, AutomobileRegistrationSystem.abi)
    cars = returnCarAdd(system,_NIV)
    Links.append('https://gateway.pinata.cloud/ipfs/'+cars)
    crashes = returnCarCrashes(system,_NIV)
    Links= getlink(str(crashes),Links)

    repport = returnRapport(system,_NIV)
    Links= getlink(str(repport),Links)
    
    transactions = returnTransactions(system,_NIV)
    Links= getlink(str(transactions),Links)
    
    signalisations = returnSignalisation(system,_NIV)
    Links= getlink(str(signalisations),Links)
    
    print(Links)

