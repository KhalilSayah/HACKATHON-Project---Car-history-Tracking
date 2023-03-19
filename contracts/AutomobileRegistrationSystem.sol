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

    modifier doesExist(string memory _niv){
        require(carFactory.carListMapping(_niv).doesExist(), "This car doesn't exist anymore");
        _;
    }

    modifier isNotBlank(string memory _niv){
        require(keccak256(bytes(_niv)) != keccak256(bytes("")), "Please enter a NIV");
        _;
    }


    address systemDeployer;

    CarFactory carFactory;

    mapping(address => mapping(Role => bool)) canAccess; //Instead of creating a mapping for each role, I thought it could be a great idea to create only one mapping of a mapping that sets the role of every address given

    mapping(string => address) createCarAddress;
    
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

    function isNivUsed(string memory _niv) public view isManufacturer(msg.sender, Role.Manufacturer) returns(bool){
        bool avaibility = carFactory.getNivAvaibility(_niv);
        return avaibility;
    }

    function createNewCar(string memory _niv, string memory _infos) public isManufacturer(msg.sender, Role.Manufacturer) isNotBlank(_niv){
        require(keccak256(bytes(_infos)) != keccak256(bytes("")), "The infos section cannot be blank");
        carFactory.createCar(_niv, _infos);
    }

    function storeCarAddress(string memory _niv, address _addingCar) public{
        createCarAddress[_niv] = _addingCar;
    }

    function getStoredAddress(string memory _niv) public view returns(address){
        return createCarAddress[_niv];
    }

    function getCar(string memory _niv) public view isNotBlank(_niv) returns(Car){
        Car car = carFactory.carListMapping(_niv);
        return car;
    }

    function setCarOwner(string memory _niv, address _owner, string memory _transactionInfo, string memory _matriculation) public isNotBlank(_niv) doesExist(_niv) isState(msg.sender, Role.State){
        require(_owner != address(0), "The infos section cannot be blank");
        require(keccak256(bytes(_transactionInfo)) != keccak256(bytes("")), "Please fill the transaction infos section");
        require(keccak256(bytes(_matriculation)) != keccak256(bytes("")), "The matriculation section cannot be blank");

        Car car = getCar(_niv);
        car.setOwner(_owner);
        car.setTransaction(_transactionInfo);
        car.setMatriculation(_matriculation);
    }

    function getCarOwner(string memory _niv) public view isNotBlank(_niv) returns(address[] memory){
        return getCar(_niv).getOwnerList();
    }

    function getCarPreviousTransactions(string memory _niv) public view isNotBlank(_niv) returns(string[] memory){
        return getCar(_niv).getPreviousTransactions();
    }

    function setCarSignalisation(string memory _niv, string memory _signalisation) public isNotBlank(_niv) doesExist(_niv) isDeployer{
        getCar(_niv).setSignalisation(_signalisation);
    }

    function getCarSignalisation(string memory _niv) public view isNotBlank(_niv) returns(string[] memory){
        return getCar(_niv).getSignalisation();
    }

    function addAccident(string memory _niv, string memory _accident) public isNotBlank(_niv) doesExist(_niv) isInsurance(msg.sender, Role.Insurance){
        require(keccak256(bytes(_accident)) != keccak256(bytes("")), "Please provide more infos");
        Car car = getCar(_niv);
        car.addAccident(_accident);
    }

    function getAccidentsList(string memory _niv) public view isNotBlank(_niv) returns (string[] memory){
        Car car = getCar(_niv);        
        return car.accidentsList();
    }

    function addCarReport(string memory _niv, string memory _report) public isNotBlank(_niv) doesExist(_niv) isCenter(msg.sender, Role.Center){
        require(keccak256(bytes(_report)) != keccak256(bytes("")), "Please provide a correct report");
        Car car = getCar(_niv);
        car.addReport(_report);
    }

    function getCarReport(string memory _niv) public view isNotBlank(_niv) returns(string[] memory){
        Car car = getCar(_niv);        
        return car.getReport();
    }

    function getCarInfos(string memory _niv) public view isNotBlank(_niv) returns(string memory){
        Car car = getCar(_niv);        
        return car.getInfos();        
    }

    function getCarAllInfos(string memory _niv) public view isNotBlank(_niv) returns(bool, string memory, string[] memory, address[] memory, string[] memory, string[] memory, string[] memory, string[] memory){
        return getCar(_niv).getAllInfos();
    }

    function destroyCar(string memory _niv) public isNotBlank(_niv) doesExist(_niv) isManufacturer(msg.sender, Role.Manufacturer){
        return getCar(_niv).destroyCar();
    }

}