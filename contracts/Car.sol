//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <=0.9.0;

contract Car{

    string niv;
    bool exists;
    string[] accidents;
    string infos;
    string[] rapports;

    constructor(string memory _niv, string memory _infos){
        niv = _niv;
        exists = true;
        infos = _infos;
    }

    function getInfos() public view returns(string memory){
        return infos;
    }

    function addAccident(string memory _accident) public {
        accidents.push(_accident);
    }

    function accidentsList() public view returns (string[] memory) {
        return accidents;
    }

    function addRapport(string memory _rapport) public{
        rapports.push(_rapport);
    }

    function getRapport() public view returns(string[] memory){
        return rapports;
    }
}