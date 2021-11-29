// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.10;

/// Contract for guessing a random number from 1-10 with a 10x bet reward
contract NumberBet {

    // State variables
    uint private randNonce;

    // Events to trigger
    event Result(string result, address account, uint bet, uint guess, uint roll);
    event PoolBalance(uint amount);
    event PoolExhausted(string gameover);

    // Errors
    error InsufficientBet(uint amount);

    constructor() payable {}

    // Defining a function to generate a random number
    // https://www.geeksforgeeks.org/random-number-generator-in-solidity-using-keccak256/
    function randMod(uint modulus) internal returns (uint result) {
        randNonce++;
        result = uint(keccak256(
            abi.encodePacked(block.timestamp, block.difficulty, msg.sender, randNonce)
        )) % modulus; // range 0-9
        result++; // range 1-10
    }

    /// Take a guess between 1 and 10 (inclusive) and win 10x the bet amount
    /// on match or lose the bet
    function placeBet(uint guess) payable public {
        require(guess >= 1 && guess <= 10, "Guess must be from 1-10.");
        require(10 * msg.value <= address(this).balance, "Insufficient pool balance.");
        if (msg.value <= 0)
            revert InsufficientBet({
                amount: msg.value
            });
        uint roll = randMod(10);
        if (guess == roll) {
            emit Result("Winner", msg.sender, msg.value, guess, roll);
            if (address(this).balance == 10 * msg.value) {
                emit PoolExhausted("Pool funds exhausted. Game Over.");
                selfdestruct(payable(msg.sender));
            } else {
                payable(msg.sender).transfer(10 * msg.value);
            }
        } else {
            emit Result("Loser", msg.sender, msg.value, guess, roll);
        }
        emit PoolBalance(address(this).balance);
    }

}