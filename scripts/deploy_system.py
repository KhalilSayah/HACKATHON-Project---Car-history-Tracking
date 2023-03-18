from brownie import network, config, accounts, AutomobileRegistrationSystem,Car,CarFactory
from web3 import Web3
import os
import json
from pathlib import Path
import requests

template_json_file = 'scripts\metadata\CreateCar.json'

def gettemplate(template_json_file):
    with open(template_json_file,"r") as jt:
        json_template = json.load(jt)
    print('json template is done !')
    return json_template

def addinfo_data(_NIV,json_template):
    data = json_template
    #get N+IV from Contract
    NIV = _NIV
    Fabrication = 'renault'
    Modele = 'GTLine'
    Type_Carrosserie = 'Berlin'
    Annee_Production = '2015'
    Carburant = 'Gasoil'
    Transmition = 'Auto'
    Moteur = 'Hme9'

    data['NIV'] = NIV
    data['Fabrication']= Fabrication
    data['Modele']= Modele
    data['Type_Carrosserie']= Type_Carrosserie
    data['Annee_Production']= Annee_Production
    data['Carburant']= Carburant
    data['Transmition']= Transmition
    data['Moteur']= Moteur

    print('DATA is done !')

    return data

def upload_json_file(data):
    filename= data['NIV'] + "_creation.json"
    if not os.path.exists(filename):
        with open(filename, "w") as outfile:
            json.dump(data, outfile)
    print('json uploaded is done !')        
    return filename

################### PINATA ###################
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

json_template = gettemplate(template_json_file)

def deploytest():
    account = get_account()
    system = AutomobileRegistrationSystem.deploy(
        {
        "from" : account
        }
    )
    print('Automobile Regestration system contract Deployed')


    print('Adding first car')
    create_first_car = system.createCar('111111',{"from":account})
    create_first_car.wait(1)
    data_car1 = addinfo_data('111111',json_template)
    filename1 = upload_json_file(data_car1)
    IpfsHash11 = jsontoipfs(data_car1)
    print(f'Ipfshack is :{IpfsHash11}')
    linktofile = 'https://gateway.pinata.cloud/ipfs/'+IpfsHash11
    print(linktofile)


    print('Adding first accident for the first car')
    add_accident_first_car = system.addAccident('111111',IpfsHash11,{"from":account})
    add_accident_first_car.wait(1)

    IpfsHash12 = jsontoipfs(data_car1)
    print(f'Ipfshack is :{IpfsHash12}')
    linktofile = 'https://gateway.pinata.cloud/ipfs/'+IpfsHash12
    print(linktofile)

    print('Adding seconde accident for the first car')
    add_accident2_first_car = system.addAccident('111111','hash21',{"from":account})
    add_accident2_first_car.wait(1)


    print('Adding second car')
    create_seconde_car = system.createCar('222222',{"from":account})
    create_seconde_car.wait(1)

    data_car2 = addinfo_data('222222',json_template)
    IpfsHash21 = jsontoipfs(data_car2)
    print(f'Ipfshack is :{IpfsHash21}')
    linktofile = 'https://gateway.pinata.cloud/ipfs/'+IpfsHash21
    print(linktofile)

    print('Adding first accident for the second car')
    add_accident_seconde_car = system.addAccident('222222',IpfsHash21,{"from":account})
    add_accident_seconde_car.wait(1)

    first_car = system.getCar('111111')
    second_car = system.getCar('222222')
    accident1 = system.getAccidentsList('111111')
    accident2 = system.getAccidentsList('222222')


    print('***********************************')
    print(f'first car contract :{first_car}')
    print(f'list of accident for this car : {accident1}')
    print(f'Second car : {second_car}')
    print(f'accident for this car : {accident2}')


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploytest()