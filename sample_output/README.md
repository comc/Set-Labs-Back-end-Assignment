# Sample Output

Provides examples of expected output from this code base.

## Monitoring

Sample outputs from the back-end monitor can be found in the following files in this folder:

- `event.log`: contract events `Result()` and `PoolBalance()`
- `pending.log`: pending transactions monitored in the pending block
- `transaction.log`: transactions discovered from monitoring the latest block


## run_tests.py

The following demonstrates sample output from the `tests/run_tests.py` script (note the script logs only to STDOUT on the command line):

```sh
[test_single_successful_bet]

Expect: success
Output: single transaction receipt

{"blockHash": "0x8c315f70592cf5bdeb9d8e19633e361c5c82f3707930fbd39196425d4354cb6b", "blockNumber": 268, "contractAddress": null, "cumulativeGasUsed": 42403, "effectiveGasPrice": 1000000000, "from": "0xD019848F4D19E17a328EAD5075b4BFdcf7CCa52A", "gasUsed": 42403, "logs": [{"address": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "topics": ["0x7a02f1d2dd71151fb3b62793fdca6a76eb5ec512bce4b7f8a2950dfe231b0eba"], "data": "0x00000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000d019848f4d19e17a328ead5075b4bfdcf7cca52a000000000000000000000000000000000000000000000000002386f26fc1000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000657696e6e65720000000000000000000000000000000000000000000000000000", "blockNumber": 268, "transactionHash": "0xba329499e5e5f9d340d797a2fd2f6c7391d9ec58da0378d1345c0b20c476fc88", "transactionIndex": 0, "blockHash": "0x8c315f70592cf5bdeb9d8e19633e361c5c82f3707930fbd39196425d4354cb6b", "logIndex": 0, "removed": false}, {"address": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "topics": ["0x1729767272c3fd78218fbe2a8e63bf9ad7227ce637b442eafe52cf715920d474"], "data": "0x0000000000000000000000000000000000000000000000000ad31dde0cce0000", "blockNumber": 268, "transactionHash": "0xba329499e5e5f9d340d797a2fd2f6c7391d9ec58da0378d1345c0b20c476fc88", "transactionIndex": 0, "blockHash": "0x8c315f70592cf5bdeb9d8e19633e361c5c82f3707930fbd39196425d4354cb6b", "logIndex": 1, "removed": false}], "logsBloom": "0x00000000001000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000010000000000000000000000000000000000020000000020000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000", "status": 1, "to": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "transactionHash": "0xba329499e5e5f9d340d797a2fd2f6c7391d9ec58da0378d1345c0b20c476fc88", "transactionIndex": 0, "type": "0x0"}


[test_multiple_successful_bets]

Expect: success
Output: transaction receipt for each transaction

{"blockHash": "0x213dedd175af89de243712bf9d104ecb52821ccf7b8e99d2596219513380a0e7", "blockNumber": 269, "contractAddress": null, "cumulativeGasUsed": 42403, "effectiveGasPrice": 1000000000, "from": "0xD019848F4D19E17a328EAD5075b4BFdcf7CCa52A", "gasUsed": 42403, "logs": [{"address": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "topics": ["0x7a02f1d2dd71151fb3b62793fdca6a76eb5ec512bce4b7f8a2950dfe231b0eba"], "data": "0x00000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000d019848f4d19e17a328ead5075b4bfdcf7cca52a000000000000000000000000000000000000000000000000002386f26fc1000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000657696e6e65720000000000000000000000000000000000000000000000000000", "blockNumber": 269, "transactionHash": "0xbd49e08c017a810e2919d13a8a43fcd7d92a0d18a20dc7dd1ebeecdb721a71f5", "transactionIndex": 0, "blockHash": "0x213dedd175af89de243712bf9d104ecb52821ccf7b8e99d2596219513380a0e7", "logIndex": 0, "removed": false}, {"address": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "topics": ["0x1729767272c3fd78218fbe2a8e63bf9ad7227ce637b442eafe52cf715920d474"], "data": "0x00000000000000000000000000000000000000000000000009935f581f050000", "blockNumber": 269, "transactionHash": "0xbd49e08c017a810e2919d13a8a43fcd7d92a0d18a20dc7dd1ebeecdb721a71f5", "transactionIndex": 0, "blockHash": "0x213dedd175af89de243712bf9d104ecb52821ccf7b8e99d2596219513380a0e7", "logIndex": 1, "removed": false}], "logsBloom": "0x00000000001000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000010000000000000000000000000000000000020000000020000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000", "status": 1, "to": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "transactionHash": "0xbd49e08c017a810e2919d13a8a43fcd7d92a0d18a20dc7dd1ebeecdb721a71f5", "transactionIndex": 0, "type": "0x0"}
{"blockHash": "0x213dedd175af89de243712bf9d104ecb52821ccf7b8e99d2596219513380a0e7", "blockNumber": 269, "contractAddress": null, "cumulativeGasUsed": 76847, "effectiveGasPrice": 1000000000, "from": "0xD019848F4D19E17a328EAD5075b4BFdcf7CCa52A", "gasUsed": 34444, "logs": [{"address": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "topics": ["0x7a02f1d2dd71151fb3b62793fdca6a76eb5ec512bce4b7f8a2950dfe231b0eba"], "data": "0x00000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000d019848f4d19e17a328ead5075b4bfdcf7cca52a000000000000000000000000000000000000000000000000002386f26fc100000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000300000000000000000000000000000000000000000000000000000000000000054c6f736572000000000000000000000000000000000000000000000000000000", "blockNumber": 269, "transactionHash": "0x5d475a41e49cfaa2c0e294c1637581ce93ec1a9b5f7c7d1f868353c3403668fc", "transactionIndex": 1, "blockHash": "0x213dedd175af89de243712bf9d104ecb52821ccf7b8e99d2596219513380a0e7", "logIndex": 2, "removed": false}, {"address": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "topics": ["0x1729767272c3fd78218fbe2a8e63bf9ad7227ce637b442eafe52cf715920d474"], "data": "0x00000000000000000000000000000000000000000000000009b6e64a8ec60000", "blockNumber": 269, "transactionHash": "0x5d475a41e49cfaa2c0e294c1637581ce93ec1a9b5f7c7d1f868353c3403668fc", "transactionIndex": 1, "blockHash": "0x213dedd175af89de243712bf9d104ecb52821ccf7b8e99d2596219513380a0e7", "logIndex": 3, "removed": false}], "logsBloom": "0x00000000001000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000010000000000000000000000000000000000020000000020000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000", "status": 1, "to": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "transactionHash": "0x5d475a41e49cfaa2c0e294c1637581ce93ec1a9b5f7c7d1f868353c3403668fc", "transactionIndex": 1, "type": "0x0"}


[test_insufficient_wallet_balance]

Expect: failed transaction
Output: error string

[ERROR] An unexpected exception has occurred: {'code': -32000, 'message': 'insufficient funds for transfer'}



[test_insufficient_pool_balance]

Expect: revert transaction
Output: error string

[ERROR] An unexpected exception has occurred: execution reverted: Insufficient pool balance.



[test_guess_out_of_range]

Expect: revert transaction
Output: error string

[ERROR] An unexpected exception has occurred: execution reverted: Guess must be from 1-10.



[test_replace_bet_success]

Expect: partial success
Output:
        Transaction 1: (failure) transaction timeout error string after default 120 seconds
        Transaction 2: (success) transaction receipt for successful (replacement) transaction

{"blockHash": "0xc23132fc5eecefb79ff9a5a33bc10fe0980968d55b931f2d1fb35305a4b70955", "blockNumber": 270, "contractAddress": null, "cumulativeGasUsed": 34444, "effectiveGasPrice": 1200000000, "from": "0xD019848F4D19E17a328EAD5075b4BFdcf7CCa52A", "gasUsed": 34444, "logs": [{"address": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "topics": ["0x7a02f1d2dd71151fb3b62793fdca6a76eb5ec512bce4b7f8a2950dfe231b0eba"], "data": "0x00000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000d019848f4d19e17a328ead5075b4bfdcf7cca52a000000000000000000000000000000000000000000000000002386f26fc100000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000400000000000000000000000000000000000000000000000000000000000000054c6f736572000000000000000000000000000000000000000000000000000000", "blockNumber": 270, "transactionHash": "0x8259bca8d99562460917db22269185b75c395c190796b6f35ef3e14e76a18eb1", "transactionIndex": 0, "blockHash": "0xc23132fc5eecefb79ff9a5a33bc10fe0980968d55b931f2d1fb35305a4b70955", "logIndex": 0, "removed": false}, {"address": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "topics": ["0x1729767272c3fd78218fbe2a8e63bf9ad7227ce637b442eafe52cf715920d474"], "data": "0x00000000000000000000000000000000000000000000000009da6d3cfe870000", "blockNumber": 270, "transactionHash": "0x8259bca8d99562460917db22269185b75c395c190796b6f35ef3e14e76a18eb1", "transactionIndex": 0, "blockHash": "0xc23132fc5eecefb79ff9a5a33bc10fe0980968d55b931f2d1fb35305a4b70955", "logIndex": 1, "removed": false}], "logsBloom": "0x00000000001000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000010000000000000000000000000000000000020000000020000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000", "status": 1, "to": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "transactionHash": "0x8259bca8d99562460917db22269185b75c395c190796b6f35ef3e14e76a18eb1", "transactionIndex": 0, "type": "0x0"}
Transaction HexBytes('0xb404f0b02806397433961463fa6eb0f9870aca8c649b95550ee3440f867e0aa2') is not in the chain, after 120 seconds


[test_replace_bet_fail]

Expect: partial success
Output:
        Transaction 1: (success) transaction receipt for successful (replacement) transaction
        Transaction 2: (failure) transaction fail

{"blockHash": "0x5e9e5a03e3154502d3aecee35ecc990ff2168c2b0e9bd937120155f062543fd4", "blockNumber": 279, "contractAddress": null, "cumulativeGasUsed": 34444, "effectiveGasPrice": 1200000000, "from": "0xD019848F4D19E17a328EAD5075b4BFdcf7CCa52A", "gasUsed": 34444, "logs": [{"address": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "topics": ["0x7a02f1d2dd71151fb3b62793fdca6a76eb5ec512bce4b7f8a2950dfe231b0eba"], "data": "0x00000000000000000000000000000000000000000000000000000000000000a0000000000000000000000000d019848f4d19e17a328ead5075b4bfdcf7cca52a000000000000000000000000000000000000000000000000002386f26fc100000000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000054c6f736572000000000000000000000000000000000000000000000000000000", "blockNumber": 279, "transactionHash": "0x460bc9aa102fbef8e6b667e1ac01e5b1df6b1c82f427df66ba896b0c41f9460f", "transactionIndex": 0, "blockHash": "0x5e9e5a03e3154502d3aecee35ecc990ff2168c2b0e9bd937120155f062543fd4", "logIndex": 0, "removed": false}, {"address": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "topics": ["0x1729767272c3fd78218fbe2a8e63bf9ad7227ce637b442eafe52cf715920d474"], "data": "0x00000000000000000000000000000000000000000000000009fdf42f6e480000", "blockNumber": 279, "transactionHash": "0x460bc9aa102fbef8e6b667e1ac01e5b1df6b1c82f427df66ba896b0c41f9460f", "transactionIndex": 0, "blockHash": "0x5e9e5a03e3154502d3aecee35ecc990ff2168c2b0e9bd937120155f062543fd4", "logIndex": 1, "removed": false}], "logsBloom": "0x00000000001000000000000000000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000020000000000010000000000000000000000000000000000020000000020000000000000000000000000000000000000000000000000000000000000000000010000000000000000000000", "status": 1, "to": "0xa283Ecc3a250B05afB1344b5B1fcd2B152F99268", "transactionHash": "0x460bc9aa102fbef8e6b667e1ac01e5b1df6b1c82f427df66ba896b0c41f9460f", "transactionIndex": 0, "type": "0x0"}
[ERROR] An unexpected exception has occurred: {'code': -32000, 'message': 'replacement transaction underpriced'}
```