//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <=0.9.0;

import "./CarFactory.sol";
//import "Accounts.sol";

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
        //account = new Accounts();
    }


    function setRole(address _for, Role _role, bool _roleStatus) public isDeployer{
        canAccess[_for][_role] = _roleStatus;
    }

    //Getting the roles of the accounts
    function getAccountRole(address _of, Role _role) public view isDeployer returns(bool){
        return canAccess[_of][_role];
    }

    function createCar(string memory _niv) public isManufacturer(canAccess[msg.sender][Role.Manufacturer]){
        carFactory.createCarMapping(_niv);
    }

    function getCar(string memory _niv) public view returns(Car){
        Car car = carFactory.carListMapping(_niv);
        return car;
    }


}