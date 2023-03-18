from brownie import network, config, accounts, Contract, AutomobileRegistrationSystem,Car,CarFactory
from web3 import Web3
import os,requests,json
from pathlib import Path
# from dotenv import load_dotenv
# load_dotenv()

create_car_template = 'scripts\metadata\CreateCar.json'
add_crash_template = 'scripts\metadata\AddCrash.json'
add_repport_template = 'scripts\metadata\AddRepport.json'
add_signalisation_template = 'scripts\metadata\AddSignalisation.json'
add_transfere_template = 'scripts\metadata\TransferCar.json'

SYS_ADD = os.environ.get('SYS_ADD')
print(SYS_ADD)

#SYS_ADD = '0xcdeb3CDFa43E365167f4dEFd27Bc94b7B0130191'


def gettemplate(template_json_file):
    with open(template_json_file,"r") as jt:
        json_template = json.load(jt)
    print('json template is done !')
    return json_template

def upload_json_file(data):
    filename= data['NIV'] + "_creation.json"
    if not os.path.exists(filename):
        with open(filename, "w") as outfile:
            json.dump(data, outfile)
    print('json uploaded is done !')        
    return filename

def jsontoipfs(data):
    headers = {
    "pinata_api_key": '12f7dbee4220cf56156b',
    "pinata_secret_api_key": '54d808d09c01b67afd9661871cc64c186bbf7e12b3cd1fb92c10564456c9707f'
    }
    endpoint = "https://api.pinata.cloud/pinning/pinJSONToIPFS"
    payload = data 
    response = requests.request("POST", endpoint, headers=headers, data=payload)
    response_dict = json.loads(response.text)
    ##{'IpfsHash': 'QmQCsu8HtM569MmnjKM5SHUuhmkt3JibFEqjm9hJUZVpDD', 'PinSize': 188, 'Timestamp': '2023-03-18T11:16:12.012Z', 'isDuplicate': True} 
    IpfsHash = response_dict['IpfsHash']
    print('Hash uploaded is done !')  
    return IpfsHash



def get_hash(data,template):
    json_template = gettemplate(template)
    upload_json_file(data)
    hash = jsontoipfs(data)
    print(f'*************************************** hash : {hash}')
    return hash
    
    


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_system():
    account = get_account()
    system = AutomobileRegistrationSystem.deploy(
        {
        "from" : account
        }
    )
    print('Automobile Regestration system contract Deployed')
    return system

def AddCar(system, account, data,template):
    _NIV = data["NIV"]
    _Infos = get_hash(data,template)
    _Car = system.createNewCar(_NIV,_Infos,{"from":account})
    _Car.wait(1)
    print('********* CAR ADDED ************')
    return _Car


def AddCrash(system, account, data,template):
    _NIV = data["NIV"]
    _hash = get_hash(data,template)
    _Crash = system.addAccident(_NIV,_hash,{"from":account})
    _Crash.wait(1)
    print('********* CRASH ADDED ************')
    return _Crash

def AddRapport(system,account,data,template):
    _NIV = data["NIV"]
    _hash = get_hash(data,template)
    _Rapport = system.addCarReport(_NIV,_hash,{"from":account})
    _Rapport.wait(1)
    print('********* Repport ADDED ************')
    return _Rapport

def UpdateSignalisation(system,account,data,template):
    _NIV = data["NIV"]
    _hash = get_hash(data,template)
    _Sign = system.setCarSignalisation(_NIV,_hash,{"from":account})
    _Sign.wait(1)
    print('********* Signalisation Updated ************')
    return _Sign

def TransfereCar(system,account,data,Owner,_matriculation):
    _NIV = data["NIV"]
    _Transfere = system.setCarOwner(_NIV,Owner,data,_matriculation,{"from":account})
    _Transfere.wait(1)
    print('********* Transaction Done ************')
    return _Transfere



def returnCarAdd(system,data):
    _NIV = data["NIV"]
    add = system.getCar(_NIV)
    print(f'Voici laddress de la voiture : {add}')
    return add

def returnCarCrashes(system,data):
     _NIV = data["NIV"]
     _CrashList = system.getAccidentsList(_NIV)
     
     return _CrashList

def returnRapport(system,data):
    _NIV = data["NIV"]
    _RapportList = system.getCarReport(_NIV)
    return _RapportList

def returnTransactions(system,data):
    _NIV = data["NIV"]
    _TransactionsList = system.getCarOwner(_NIV)
    return _TransactionsList


def main():
    ## FROM FORMS
    InfoCar = {
    "NIV":"7",
    "Date":"25/06/2001",
    "Fabrication":"Renault",
    "Modele":"R6",
    "Type_Carrosserie":"Berlin",
    "Annee_Production":"2018",
    "Carburant":"Diesel",
    "Transmition":"Auto",
    "Moteur":"Puissant"
    }
    Crashdata = {
    "NIV":"7",
    "Date":"26/06/2001",
    "Where":"Algerie",
    "Damage_emp":"Par-brise",
    "Estimated_Price":"10000"
}
    RepportData = {
    "NIV":"7",
    "Date":"27/06/2001",
    "KM":"10000",
    "Entretiens":['Entretien Vidange','Pression Pneux'],
    "Timestamp":"30 min"
}
    SignalisationData = {
    "NIV":"7",
    "Date":"28/06/2001",
    "Where":"Algeria",
    "Source":"Police",
    "Status":"True"
}
    TransferData = {
 "NIV":"7",
 "Date":"31/12/2001",
 "Amount" :"1000000",
 "Devise":"DZ",
 "Previous_Owner":"0x123456789",
 "New_Owner":"0x963852741"  
}
    ###############################

    system = Contract.from_abi('AutomobileRegistrationSystem', SYS_ADD, AutomobileRegistrationSystem.abi)

    account = get_account()
    Car1 = AddCar(system, account, InfoCar,create_car_template)
    Crash1 = AddCrash(system, account, Crashdata,create_car_template)
    Signalisation1 = UpdateSignalisation(system,account,SignalisationData,create_car_template)
    Rapport1 = AddRapport(system,account,RepportData,create_car_template)
    Transfer1 = TransfereCar(system,account,TransferData,'0x52C9a652a12800Fe804dB8673d34936BaD9250E7','221222-113-13')


    #Crash2 = AddCrash(system, account, data1,create_car_template)
    #Car2 = AddCar(system, account, data2,create_car_template)
    #Car2Crash2 = AddCrash(system, account, data2,create_car_template)
    #returnCarAdd(system,data1)
    #returnCarAdd(system,data2)
    #Crashlist1 = returnCarCrashes(system,InfoCar)
    #Crashlist2 = returnCarCrashes(system,data2)
    #print(f'List of crash for the first car : {Crashlist1}')
    #print(f'List of crash for the second car : {Crashlist2}')




