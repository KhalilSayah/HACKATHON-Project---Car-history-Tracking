//SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <=0.9.0;

import "./Car.sol";

contract CarFactory{

    Car car;

    mapping(string => Car) listCars;
    mapping(string => bool) isNivTaken;

    function createCar(string memory _niv, string memory _infos) public{
        require(!isNivTaken[_niv], "Please try another NIV as the provided one has already been used");
        car = new Car(_niv, _infos);
        isNivTaken[_niv] = true;
        listCars[_niv] = car;
    }

    function destroyCar(string memory _niv) public{
        car = carListMapping(_niv);
        car.destroyCar();
    }

    function carListMapping(string memory _niv) public view returns(Car){
        return Car(address(listCars[_niv]));
    }

    function getNivAvaibility(string memory _niv) public view returns(bool){
        return isNivTaken[_niv];
    }


}