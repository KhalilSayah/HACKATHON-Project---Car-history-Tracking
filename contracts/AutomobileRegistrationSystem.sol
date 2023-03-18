//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <=0.9.0;

import "./CarFactory.sol";

contract AutomobileRegistrationSystem{

    //List of roles
    enum Role{
        Manufacturer, //0
        State, //1
        Center, //2
        Insurance //3
    }

    modifier isDeployer(){
        require(msg.sender == systemDeployer, "You're not the owner, aborting");
        _;
    }

    modifier isManufacturer(address _of, Role _role){ //Create or delete the car
        require(canAccess[_of][_role], "Permission denied, you must be a manufacturer!");
        _;
    }

    modifier isState(address _of, Role _role){ //Set owner (old and new) + Transaction infos
        require(canAccess[_of][_role], "You don't have the previledges, aborting");
        _;
    }

    modifier isCenter(address _of, Role _role){ //Create reports
        require(canAccess[_of][_role], "Permission denied, center only!"); 
        _;
    }

    modifier isInsurance(address _of, Role _role){ //Save accidents
        require(canAccess[_of][_role], "Permission denied, insurance only!"); 
        _;
    }

    modifier doesExist(string memory _niv) {
        require(carFactory.carListMapping(_niv).doesExist(), "This car doesn't exist anymore");
        _;
    }


    address systemDeployer;

    CarFactory carFactory;
    //Accounts account;

    mapping(address => mapping(Role => bool)) canAccess; //Instead of creating a mapping for each role, I thought it could be a great idea to create only one mapping of a mapping that sets the role of every address given

    
    constructor(){
        systemDeployer = msg.sender;    
        carFactory = new CarFactory();
    }


    function setRole(address _for, Role _role, bool _roleStatus) public isDeployer{
        canAccess[_for][_role] = _roleStatus;
    }

    //Getting the roles of the accounts
    function getAccountRole(address _of, Role _role) public view isDeployer returns(bool){
        return canAccess[_of][_role];
    }

    function createNewCar(string memory _niv, string memory _infos) public /*isManufacturer(msg.sender, Role.Manufacturer)*/{
        carFactory.createCar(_niv, _infos);
    }

    function getCar(string memory _niv) private view returns(Car){
        Car car = carFactory.carListMapping(_niv);
        return car;
    }

    function setCarOwner(string memory _niv, string memory _owner, string memory _transactionInfo, string memory _matriculation) public doesExist(_niv){
        Car car = getCar(_niv);
        car.setOwner(_owner);
        car.setTransaction(_transactionInfo);
        car.setMatriculation(_matriculation);
    }

    function getCarOwner(string memory _niv) public view returns(string[] memory){
        return getCar(_niv).getOwnerList();
    }

    function getCarPreviousTransactions(string memory _niv) public view returns(string[] memory){
        return getCar(_niv).getPreviousTransactions();
    }

    function setCarSignalisation(string memory _niv, bool _signalisation) public doesExist(_niv){
        getCar(_niv).setSignalisation(_signalisation);
    }

    function getCarSignalisation(string memory _niv) public view returns(bool){
        return getCar(_niv).getSignalisation();
    }

    function addAccident(string memory _niv, string memory _accident) public doesExist(_niv){
        Car car = getCar(_niv);
        car.addAccident(_accident);
    }

    function getAccidentsList(string memory _niv) public view returns (string[] memory){
        Car car = getCar(_niv);        
        return car.accidentsList();
    }

    function addCarReport(string memory _niv, string memory _report) public doesExist(_niv){
        Car car = getCar(_niv);
        car.addReport(_report);
    }

    function getCarReport(string memory _niv) public view returns(string[] memory){
        Car car = getCar(_niv);        
        return car.getReport();
    }

    function getCarInfos(string memory _niv) public view returns(string memory){
        Car car = getCar(_niv);        
        return car.getInfos();        
    }

    function getCarAllInfos(string memory _niv) public view returns(bool, string memory, string[] memory, string[] memory, string[] memory, string[] memory, string[] memory, bool){
        return getCar(_niv).getAllInfos();
    }

    function destroyCar(string memory _niv) public doesExist(_niv){
        return getCar(_niv).destroyCar();
    }

}