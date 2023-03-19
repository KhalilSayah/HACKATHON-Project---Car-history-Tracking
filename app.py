from flask import Flask, render_template, request, url_for, jsonify
from web3 import Web3
import json
import os
from pathlib import Path
import requests
import ast



def returnCarAdd(system,_NIV):
    
    add = system.functions.getCarInfos(_NIV).call()
    #print(f'Voici laddress de la voiture : {add}')
    return add

def returnCarCrashes(system,_NIV):
     
     _CrashList = system.functions.getAccidentsList(_NIV).call()
     
     return _CrashList

def returnRapport(system,_NIV):
    
    _RapportList = system.functions.getCarReport(_NIV).call()
    return _RapportList

def returnTransactions(system,_NIV):
    
    _TransactionsList = system.functions.getCarPreviousTransactions(_NIV).call()
    print(_TransactionsList)
    return _TransactionsList

def returnSignalisation(system,_NIV):
    _Signalisation = system.functions.getCarSignalisation(_NIV).call()
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
    #print(response.text)
    data = json.loads(response.text)
    return data

def getlistdatad(List):
    data = []
    for link in List:
        data.append(requestdata(link))
    return data

def getdata(_NIV,system):
    Links= {
        "InfoCar":'',
        "Crashdata": [],
        "RepportData" : [],
        "SignalisationData" : [],
        "TransferData" : [],
        "Car_Address" : ''
    }
    
    cars = returnCarAdd(system,_NIV)
    print(cars)
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
    #dump["Car_Address"] = system.getStoredAddress(_NIV)

    return dump



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/rapport', methods =['post', 'get'])
def rapport():
    file_path = './build/contracts/AutomobileRegistrationSystem.json'
    with open(file_path,'r') as f:
        raw = json.loads(f.read())

    abi = raw["abi"]

    SYS_ADD = '0x47267A8a0076Da12E13D36DA1627885085dbEcBA'

    # Create a Web3 object and connect to the Mumbai testnet
    w3 = Web3(Web3.HTTPProvider('https://rpc-mumbai.maticvigil.com'))
    system = w3.eth.contract(address=SYS_ADD, abi=abi)
    _NIV = request.form.get('identifier')
        
    data = getdata(_NIV,system)
    print(data)


    
    

    return render_template('rapport.html', data = data)

if __name__ == '__main__':
    app.run(debug =True)