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


def setup_account(role):


    if network.show_active() == "development":
        return accounts[0]
    else:
        if role == '0':
            account = accounts.add(config["wallets"]["Manufacture"])
    
        elif role =='1':
            account =  accounts.add(config["wallets"]["State"])

        elif role =='2':
            account =  accounts.add(config["wallets"]["Center"])

        elif role =='3':
            account =  accounts.add(config["wallets"]["Insurance"])


    return account


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

def TransfereCar(system,account,data,Owner,_matriculation,template):
    _NIV = data["NIV"]
    _hash = get_hash(data,template)
    _Transfere = system.setCarOwner(_NIV,Owner,_hash,_matriculation,{"from":account})
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

def setup_roles(system,account):
    print(config["wallets"]["public_keys"]['Manufacture'])

    system.setRole(config["wallets"]["public_keys"]['Manufacture'],0,1,{"from":account})
    system.setRole(config["wallets"]["public_keys"]['State'],1,1,{"from":account})
    system.setRole(config["wallets"]["public_keys"]['Center'],2,1,{"from":account})
    system.setRole(config["wallets"]["public_keys"]['Insurance'],3,1,{"from":account})
    print("********** Accounts have a Roles now ! **************")



def main():
    ## FROM FORMS
    InfoCar = {
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
    Crashdata = {
    "NIV":"11",
    "Date":"26/06/2001",
    "Where":"Algerie",
    "Damage_emp":"Par-brise",
    "Estimated_Price":"10000"
}
    RepportData = {
    "NIV":"11",
    "Date":"27/06/2001",
    "KM":"10000",
    "Entretiens":['Entretien Vidange','Pression Pneux'],
    "Timestamp":"30 min"
}
    SignalisationData = {
    "NIV":"11",
    "Date":"28/06/2001",
    "Where":"Algeria",
    "Source":"Police",
    "Status":"True"
}
    TransferData = {
    "NIV":"11",
    "Date":"31/12/2001",
    "Amount" :"1000000",
    "Devise":"DZ",
    "Previous_Owner":"0x123456789",
    "New_Owner":"0x963852741"  
    }
    ###############################

    system = Contract.from_abi('AutomobileRegistrationSystem', SYS_ADD, AutomobileRegistrationSystem.abi)

    account = get_account()
    setup_roles(system,account)

    Maccount = setup_account('0')
    Car1 = AddCar(system, Maccount, InfoCar,create_car_template)
    #system.storeCarAddress(InfoCar["NIV"],Car1.new_contracts,{"from":account})
    
    Iaccount = setup_account('3')
    Crash1 = AddCrash(system, Iaccount, Crashdata,create_car_template)

    account = get_account()
    Signalisation1 = UpdateSignalisation(system,account,SignalisationData,create_car_template)

    Caccount = setup_account('2')
    Rapport1 = AddRapport(system,Caccount,RepportData,create_car_template)

    Saccount = setup_account('1')
    Transfer1 = TransfereCar(system,Saccount,data=TransferData,Owner='0x52C9a652a12800Fe804dB8673d34936BaD9250E7',_matriculation='221222-113-13',template=create_car_template)
   

    #Crash2 = AddCrash(system, account, data1,create_car_template)
    #Car2 = AddCar(system, account, data2,create_car_template)
    #Car2Crash2 = AddCrash(system, account, data2,create_car_template)
    #returnCarAdd(system,data1)
    #returnCarAdd(system,data2)
    #Crashlist1 = returnCarCrashes(system,InfoCar)
    #Crashlist2 = returnCarCrashes(system,data2)
    #print(f'List of crash for the first car : {Crashlist1}')
    #print(f'List of crash for the second car : {Crashlist2}')




