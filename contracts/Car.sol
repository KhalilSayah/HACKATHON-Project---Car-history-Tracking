//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <=0.9.0;

contract Car{

    string niv;
    bool exists;
    string[] accidents;

    constructor(string memory _niv){
        niv = _niv;
        exists = true;
    }

    function addAccident(string memory _accident) public {
        accidents.push(_accident);
    }

    function accidentsList() public view returns (string[] memory) {
        return accidents;
    }
}