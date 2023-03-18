//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <=0.9.0;

contract Car{

    string niv;
    bool exists;

    constructor(string memory _niv){
        niv = _niv;
        exists = true;
    }
    
}