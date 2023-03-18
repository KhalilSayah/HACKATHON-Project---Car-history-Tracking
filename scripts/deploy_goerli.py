from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
import json

load_dotenv()

install_solc("0.6.0")

with open("./contracts/AutomobileRegistrationSystem.sol", "r") as file:
    contract_file = file.read()

with open("./build/contracts//AutomobileRegistrationSystem.json", "r") as file:
    compiled_sol  = json.loads(file.read())


bytecode = compiled_sol['bytecode']
abi = compiled_sol['abi']


    






