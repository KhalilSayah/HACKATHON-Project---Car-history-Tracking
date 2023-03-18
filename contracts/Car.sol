//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <=0.9.0;

contract Car{

    string niv;
    bool exists;
    string[] accidents;
    string owner;
    string[] cacheOwnersList;
    string infos;
    string[] rapports;
    uint price;
    uint[] listPreviousPrices;
    bool signalisation;


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

    function setOwner(string memory _owner) public{
        owner = _owner;
        cacheOwnersList.push(owner);
    }

    function getOwnerList() public view returns(string[] memory){
        return cacheOwnersList;
    }

    function setPrice(uint _price) public{
        price = _price;
        listPreviousPrices.push(price);
    }

    function getPreviousPrices() public view returns(uint[] memory){
        return listPreviousPrices;
    }

    function setSignalisation(bool _signalisation) public{
        signalisation = _signalisation;
    }

    function getSignalisation() public view returns(bool){
        return signalisation;
    }

}


