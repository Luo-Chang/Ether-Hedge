pragma solidity ^0.4.23;

contract Share {
	mapping (address => uint256) internal addr_share;
    uint256 internal total_share = 0;
    
	function getShare(address addr) public constant returns(uint256) {
		return addr_share[addr];
	}

	function addShare(address addr, uint256 amount) public returns(uint256) {
		addr_share[addr] += amount;
		total_share += amount;
		return addr_share[addr];
	}
	
	function totalShare() public constant returns(uint256) {
	    return total_share;
	}
}