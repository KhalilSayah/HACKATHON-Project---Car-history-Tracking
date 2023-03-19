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

def createInfoCar(_NIV,_date,_fabrication,_modele,_carro,_annee,_carburant,_transmition,_moteur):
    output = {
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
    output['NIV'] = _NIV
    output['Date'] = _date
    output['Fabrication'] = _fabrication
    output['Modele'] = _modele
    output['Type_Carrosserie'] = _carro
    output['Annee_Production'] = _annee
    output['Carburant'] = _carburant
    output['Transmition'] = _transmition
    output['Transmition'] = _moteur
    return output

def createcrash(_NIV,_date,_where,_damage,_price):
    output = {
    "NIV":"11",
    "Date":"26/06/2001",
    "Where":"Algerie",
    "Damage_emp":"Par-brise",
    "Estimated_Price":"10000"
    }
    output['NIV'] = _NIV
    output['Date'] = _date
    output['Where'] = _where
    output['Damage_emp'] = _damage
    output['Estimated_Price'] = _price
    
    return output

def createRepport(_NIV,_date,_km,_entretiens,_time):
    output = {
    "NIV":"11",
    "Date":"27/06/2001",
    "KM":"10000",
    "Entretiens":['Entretien Vidange','Pression Pneux'],
    "Timestamp":"30 min"
}
    output['NIV'] = _NIV
    output['Date'] = _date
    output['KM'] = _km
    output['Entretiens'] = _entretiens
    output['Timestamp'] = _time
    
    return output

def createSignalisation(_NIV,_date,_where,_source,_status):
    output = {
    "NIV":"11",
    "Date":"28/06/2001",
    "Where":"Algeria",
    "Source":"Police",
    "Status":"True"
}
    output['NIV'] = _NIV
    output['Date'] = _date
    output['Where'] = _where
    output['Source'] = _source
    output['Status'] = _status
    
    return output

def createTransfere(_NIV,_date,_amount,_devise,_previous,_new):
    output = {
    "NIV":"11",
    "Date":"31/12/2001",
    "Amount" :"1000000",
    "Devise":"DZ",
    "Previous_Owner":"0x123456789",
    "New_Owner":"0x963852741"  
    }
    output['NIV'] = _NIV
    output['Date'] = _date
    output['Amount'] = _amount
    output['Devise'] = _devise
    output['Previous_Owner'] = _previous
    output['New_Owner'] = _new
    
    return output



def main():
    
    ###############################

    system = Contract.from_abi('AutomobileRegistrationSystem', SYS_ADD, AutomobileRegistrationSystem.abi)

    account = get_account()
    setup_roles(system,account)

    Maccount = setup_account('0')
    InfoCar = createInfoCar('11','25/06/2001','Renault','R6','Berlin','2018','Diesel','Auto','Puissant')
    Car1 = AddCar(system, Maccount, InfoCar,create_car_template)
    ## FROM FORMS
    
    #system.storeCarAddress(InfoCar["NIV"],Car1.new_contracts,{"from":account})
    
    Iaccount = setup_account('3')
    Crashdata = createcrash('11','25/29/2018','Algerie','Par-Brise','10000')
    Crash1 = AddCrash(system, Iaccount, Crashdata,create_car_template)
    Crashdata2 = createcrash('11','01/01/2023','Algerie','Carrosserie','12000')
    Crash2 = AddCrash(system, Iaccount, Crashdata2,create_car_template)
    Crashdata3 = createcrash('11','01/06/2023','Algerie','Feux','3000')
    Crash3 = AddCrash(system, Iaccount, Crashdata3,create_car_template)
    
    

    account = get_account()
    SignalisationData=createSignalisation('11','31/12/2001','Algeria','Police','True')
    Signalisation1 = UpdateSignalisation(system,account,SignalisationData,create_car_template)
    SignalisationData2=createSignalisation('11','04/04/2012','Roumanie','Gendarmerie','True')
    Signalisation2 = UpdateSignalisation(system,account,SignalisationData2,create_car_template)
    
    

    Caccount = setup_account('2')
    RepportData = createRepport('11','13/04/2009','10000',['Entretien Vidange','Pression Pneux'],'30 min')
    Rapport1 = AddRapport(system,Caccount,RepportData,create_car_template)
    RepportData2 = createRepport('11','13/04/2010','12000',['Entretien Vidange','Equilibrage'],'15 min')
    Rapport2 = AddRapport(system,Caccount,RepportData2,create_car_template)
    RepportData3 = createRepport('11','13/09/2012','10000',['Entretien Vidange','Pression Pneux','scaner'],'30 min')
    Rapport3 = AddRapport(system,Caccount,RepportData3,create_car_template)
    

    Saccount = setup_account('1')
    TransferData = createTransfere('11','13/04/2016','100000','DZ','0x123456789','0x963852741')
    Transfer1 = TransfereCar(system,Saccount,data=TransferData,Owner='0x52C9a652a12800Fe804dB8673d34936BaD9250E7',_matriculation='221222-113-13',template=create_car_template)
    TransferData2 = createTransfere('11','13/04/2018','250000','DZ','0x123456789','0x963852741')
    Transfer2 = TransfereCar(system,Saccount,data=TransferData2,Owner='0xA0Be6213F7f951B7E2f9d625Ad8a76D675E80e3D',_matriculation='25852-113-13',template=create_car_template)
    TransferData3 = createTransfere('11','13/04/2018','688000','DZ','0x123456789','0x963852741')
    Transfer3 = TransfereCar(system,Saccount,data=TransferData3,Owner='0x8678D83e01F227F40A049C40ca9ec4fdB9608c54',_matriculation='221222-113-13',template=create_car_template)

    #Crash2 = AddCrash(system, account, data1,create_car_template)
    #Car2 = AddCar(system, account, data2,create_car_template)
    #Car2Crash2 = AddCrash(system, account, data2,create_car_template)
    #returnCarAdd(system,data1)
    #returnCarAdd(system,data2)
    #Crashlist1 = returnCarCrashes(system,InfoCar)
    #Crashlist2 = returnCarCrashes(system,data2)
    #print(f'List of crash for the first car : {Crashlist1}')
    #print(f'List of crash for the second car : {Crashlist2}')




