import argparse
import asyncio
import json
import os
from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
from web3.middleware import geth_poa_middleware


global web3
global provider


def deploy_contract(contract, account, value):
    """
    Deploy the smart contract from the specified account, and transfer the
    given amount of ether into the contract as the starting pool balance
    """
    transaction = {
        "from": account["address"],
        "value": web3.toWei(value, "ether"),
        "gasPrice": web3.eth.gas_price,
        "nonce": web3.eth.get_transaction_count(account["address"]),
        "chainId": provider["chainId"],
    }
    transaction["gas"] = contract.constructor().estimateGas()

    # Build and sign transaction
    tx = contract.constructor().buildTransaction(transaction)
    signed_tx = web3.eth.account.sign_transaction(tx, account["private_key"])

    # Send transaction (raw due to locally hosted network node)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_receipt


def build_contract(abi, bytecode):
    """
    Build and return contract object
    """
    # Load contract ABI
    if os.path.exists(os.path.normpath(abi)):
        with open(os.path.normpath(abi)) as f:
            abi = json.load(f)
    # Load contract bytecode
    if os.path.exists(os.path.normpath(bytecode)):
        with open(os.path.normpath(bytecode)) as f:
            bytecode = f.read()

    return web3.eth.contract(abi=abi, bytecode=bytecode)


def build_account(address, keyfile, passphrase=None):
    """
    Build and return account dict
    """
    account = {"address": address}
    if os.path.exists(os.path.normpath(keyfile)):
        with open(os.path.normpath(keyfile)) as f:
            encrypted_key = f.read()
    else:
        raise FileNotFoundError()
    if passphrase is not None and os.path.exists(os.path.normpath(passphrase)):
        with open(os.path.normpath(passphrase)) as f:
            passphrase = f.read()
    else:
        passphrase = getpass.getpass("Passphrase: ")
    account["private_key"] = web3.eth.account.decrypt(encrypted_key, passphrase)

    return account


if __name__ == "__main__":
    """
    Script to deploy a smart contract to a private node from a given address.

    Usage:
    
        deploy_contract.py [-h] -a ADDRESS -k KEYFILE [-p PASSPHRASE] -v VALUE --abi ABI --bytecode BYTECODE --config CONFIG

    Required Arguments:

        -a ADDRESS, --address ADDRESS
                                account address of contract creator
        -k KEYFILE, --keyfile KEYFILE
                                path to account keyfile
        -v VALUE, --value VALUE
                                amount of ether to send to contract (this is the starting pool balance)
        --abi ABI               contract ABI or full path to .abi file
        --bytecode BYTECODE     contract bytecode or full path to .bin file
        --config CONFIG         path to network provider RPC server config.json

    Optional Arguments:

        -h, --help              show this help message and exit
        -p PASSPHRASE, --passphrase PASSPHRASE
                                path to file containing account keyfile passphrase (will prompt if not provided)

    """

    # TODO: No error catching or validation happening

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--address",
        help="account address of contract creator",
        type=str,
        required=True
    )
    parser.add_argument(
        "-k", "--keyfile",
        help="path to account keyfile",
        type=str,
        required=True
    )
    parser.add_argument(
        "-p", "--passphrase",
        help="path to file containing account keyfile passphrase (will prompt if not provided)",
        type=str,
        required=False
    )
    parser.add_argument(
        "-v", "--value",
        help="amount of ether to send to contract (this is the starting pool balance)",
        type=float,
        required=True
    )
    parser.add_argument(
        "--abi",
        help="contract ABI or full path to .abi file",
        type=str,
        required=True
    )
    parser.add_argument(
        "--bytecode",
        help="contract bytecode or full path to .bin file",
        type=str,
        required=True
    )
    parser.add_argument(
        "--config",
        help="path to network provider RPC server config.json",
        type=str,
        required=True
    )

    args = parser.parse_args()

    try:

        # Load provider config.json
        if os.path.exists(os.path.normpath(args.config)):
            with open(os.path.normpath(args.config)) as f:
                provider = json.loads(f.read())
        else:
            raise FileNotFoundError()
        web3 = Web3(Web3.HTTPProvider(provider["url"] + ":" + str(provider["port"])))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        # Build contract object
        contract = build_contract(args.abi, args.bytecode)

        # Build account dict (account must be hosted on local node)
        account = build_account(args.address, args.keyfile, args.passphrase)

        # Call contract deployment
        receipt = deploy_contract(contract, account, args.value)

        print(receipt)

    except Exception as e:
        print(e)
