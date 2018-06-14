pragma solidity ^0.4.23;

contract Info {
    function getShare(address addr) public constant returns(uint256);

    function updateStrategy(string winningProposal) public returns(string);

    // function addShare(address addr, uint256 amount) public returns(uint256);
    
    // function totalShare() public constant returns(uint256);

    // function update_strategy(string name, string md5) public returns(bool) ;
}

contract Vote {
    Info s;
    uint[] proposals = [0, 1, 2];
    string[] names = ["Multi_Factor", "Machine_Learning", "Turtle_Trading"];
    // // string[] md5;
    // uint[] scores;
    
    struct Voter {
        uint weight;
        bool voted;
        uint8 vote;
    }
        
    mapping(address => Voter) public voters;

    function s_getShare(address addr) internal constant returns (uint256) {
        return s.getShare(addr);
    }

    function s_updateStrategy(string winningProposal) internal returns(string) {
        return s.updateStrategy(winningProposal);
    }

    constructor(address callee) public {
        // Initialize Info contract through its address.
        s = Info(callee);
    }
    
    function vote(address addr, uint8 toProposal) public {
        Voter storage sender = voters[addr];
        sender.weight = s_getShare(addr);
        if (sender.voted || toProposal >proposals.length || sender.weight == 0) revert();
        sender.voted = true;
        sender.vote = toProposal;
        proposals[toProposal] += sender.weight;
    }
    
    // function push_proposal(string name, string _md5) public {
    //     if (msg.sender != chairman) revert();
    //     proposals.push(name);
    //     md5.push(_md5);
    // }

    function winningProposal() public returns (string) {
        uint256 winningVoteCount = 0;
        uint8 _winningProposal = 0;
        for (uint8 prop = 0; prop < proposals.length; prop++)
            if (proposals[prop] > winningVoteCount) {
                winningVoteCount = proposals[prop];
                _winningProposal = prop;
            }
        s_updateStrategy(names[_winningProposal]);
        return names[_winningProposal];
    }


}