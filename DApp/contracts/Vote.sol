pragma solidity ^0.4.23;

contract Share {
    function getShare(address addr) public constant returns(uint256);
    
    function addShare(address addr, uint256 amount) public returns(uint256);
    
    function totalShare() public constant returns(uint256);
}

contract Vote {

    Share s;

    function s_getShare(address addr) public constant returns (uint256) {
        return s.getShare(addr);
    }

    function s_addShare(address addr, uint256 amount) public returns (uint256) {
        return s.addShare(addr, amount);
    }

    function s_totalShare() public constant returns(uint256) {
        return s.totalShare();
    }

    constructor(address callee) public {
        s = Share(callee);
    }

}