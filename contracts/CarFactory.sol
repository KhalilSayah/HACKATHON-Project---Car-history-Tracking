//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <=0.9.0;

import "./Car.sol";

contract CarFactory{

    Car car;
    string niv;
    //Using mapping

    mapping(string => Car) listCars;

    function createCar(string memory _niv, string memory _infos) public{
        car = new Car(_niv, _infos);
        listCars[_niv] = car;
    }

    function destroyCar(string memory _niv) public{
        car = carListMapping(_niv);
        car.destroyCar();
    }

    function carListMapping(string memory _niv) public view returns(Car){
        return Car(address(listCars[_niv]));
    }
    
}