pragma solidity ^0.4.23;

contract Info {
	mapping (address => uint256) internal addr_share;

	string public current_strategy = "Multi_Factor";

    uint256 internal total_share = 0;

    function getStrategy() public constant returns(string) {
    	return current_strategy;
    }

    function updateStrategy(string winningProposal) public returns(string) {
    	current_strategy = winningProposal;
    	return current_strategy;
    }
    
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