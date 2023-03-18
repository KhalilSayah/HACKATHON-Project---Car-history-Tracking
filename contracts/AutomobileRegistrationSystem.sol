//SPDX-License-Identifier: MIT

import "./CarFactory.sol";
pragma solidity >=0.6.0 <=0.9.0;


contract AutomobileRegistrationSystem{

    //List of roles
    enum Role{
        Manufacturer, //0
        State, //1
        Center, //2
        Insurance //3
    }

    modifier isDeployer(){
        require(systemDeployer == msg.sender, "You're not the owner, aborting");
        _;
    }

    modifier isManufacturer(bool hasAccess){
        require(hasAccess, "Permission denied, you must be a manifactor!");
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

    function createCar(string memory _niv, string memory _infos) public /*isManufacturer(canAccess[msg.sender][Role.Manufacturer])*/{
        carFactory.createCarMapping(_niv, _infos);
    }

    function addAccident(string memory _niv, string memory _accident) public {
        Car car = getCar(_niv);
        car.addAccident(_accident);
    }

    function getAccidentsList(string memory _niv) public view returns (string[] memory){
        Car car = getCar(_niv);        
        return car.accidentsList();
    }

    function addCarRapport(string memory _niv, string memory _rapport) public{
        Car car = getCar(_niv);
        car.addRapport(_rapport);
    }

    function getCarRapport(string memory _niv) public view returns(string[] memory){
        Car car = getCar(_niv);        
        return car.getRapport();
    }

    function getCarInfos(string memory _niv) public view returns(string memory){
        Car car = getCar(_niv);        
        return car.getInfos();        
    }

    function getCar(string memory _niv) public view returns(Car){
        Car car = carFactory.carListMapping(_niv);
        return car;
    }
}