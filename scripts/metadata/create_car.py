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

# linktofile = 'https://gateway.pinata.cloud/ipfs/'+IpfsHash
# print(linktofile)


def main():
    json_template = gettemplate(template_json_file)
    data = addinfo_data('11111',json_template)
    filename = upload_json_file(data)
    IpfsHash = jsontoipfs(data)
    print(f'Ipfshack is :{IpfsHash}')


main()