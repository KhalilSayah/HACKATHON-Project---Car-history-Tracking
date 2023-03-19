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
    listink = []
    endpoint = 'https://gateway.pinata.cloud/ipfs/'
    tuple_obj = ast.literal_eval(hash)
    for element in tuple_obj:
        link = endpoint+element
        listink.append(link)
    return listink

def requestdata(url):
    response= requests.get(url=url)
    print(response.text)
    data = json.loads(response.text)
    return data
def getlistdatad(List):
    data = []
    for link in List:
        data.append(requestdata(link))
    return data

def _wellformatedjson(Links):
    pass



def main():
    Links= {
        "InfoCar":'',
        "Crashdata": [],
        "RepportData" : [],
        "SignalisationData" : [],
        "TransferData" : []
    }
    _NIV = '10'
    system = Contract.from_abi('AutomobileRegistrationSystem', SYS_ADD, AutomobileRegistrationSystem.abi)
    cars = returnCarAdd(system,_NIV)
    Links["InfoCar"] = ('https://gateway.pinata.cloud/ipfs/'+cars)
    crashes = returnCarCrashes(system,_NIV)
    Links ["Crashdata"]= getlink(str(crashes),Links)

    repport = returnRapport(system,_NIV)
    Links["RepportData"]=getlink(str(repport),Links)
    
    transactions = returnTransactions(system,_NIV)
    Links["TransferData"] = getlink(str(transactions),Links)
    
    signalisations = returnSignalisation(system,_NIV)
    Links["SignalisationData"] = getlink(str(signalisations),Links)

    dump = Links
    dump["InfoCar"] = requestdata(Links["InfoCar"])
    dump["Crashdata"] = getlistdatad(Links["Crashdata"])
    dump["RepportData"] = getlistdatad(Links["RepportData"])
    dump["TransferData"] = getlistdatad(Links["TransferData"])
    dump["SignalisationData"] = getlistdatad(Links["SignalisationData"])

    print(dump)


    
    

