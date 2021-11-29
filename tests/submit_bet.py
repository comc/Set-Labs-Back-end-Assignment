import argparse
import json
import os
from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
from web3.middleware import construct_sign_and_send_raw_middleware
from web3.middleware import geth_poa_middleware


global web3
global provider


def send_transaction(account, transaction, func):
    """
    Build, sign, and send a transaction

    Parameters
    ----------
    account : dict
        the account for the sender
    transaction : dict
        the transaction parameters
    func : function
        the contract function to call

    Returns
    -------
    tx_hash : uint
        the transaction hash

    """

    # TODO: add type, validity checks

    tx = func.buildTransaction(transaction)
    signed_tx = web3.eth.account.sign_transaction(tx, account["private_key"])
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    return tx_hash


def place_bet(contract, account, guess, amount, nonce=None, gas=None):
    """
    Prepare the transaction for sending
    """

    # TODO: validate inputs

    tx = {
        'from': account['address'],
        'value': web3.toWei(amount, 'ether'),
        'gasPrice': gas if gas else web3.eth.gas_price,
        'nonce': nonce if nonce else web3.eth.get_transaction_count(account['address']),
        'chainId': provider["chainId"],    # must specify this is a private network
    }

    tx_hash = send_transaction(
        account,
        tx,
        contract.functions.placeBet(guess)
    )

    return tx_hash


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
    Script to submit transactions (bets) against the NumberBet contract for testing.

    Usage:
    
        submit_bet.py [-h] -a ADDRESS -k KEYFILE [-p PASSPHRASE] -c CONTRACT -b BET -g GUESS [-n NONCE] [-w] --abi ABI --config CONFIG

    Required Arguments:

        -a ADDRESS, --address ADDRESS
                                account address of transaction owner
        -k KEYFILE, --keyfile KEYFILE
                                path to account keyfile
        -c CONTRACT, --contract CONTRACT
                                contract address
        -b BET, --bet BET       amount of ether to bet
        -g GUESS, --guess GUESS number to guess (between 1 and 10 inclusive)
        --abi ABI               contract ABI or full path to .abi file
        --config CONFIG         path to network provider RPC server config.json

    Optional Arguments:

        -h, --help              show this help message and exit
        --gas GAS               manually specify the transaction gas price to use use (e.g., for replacing a transaction)
        --nonce NONCE           manually specify the transaction nonce to use (e.g., for placing multiple bets in a row)
        -p PASSPHRASE, --passphrase PASSPHRASE
                                path to file containing account keyfile passphrase (will prompt if not provided)
        -w, --wait              wait for transaction receipt and show result

    """

    # TODO: No error catching or validation happening

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--address",
        help="account address of transaction owner",
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
        "-c", "--contract",
        help="contract address",
        type=str,
        required=True
    )
    parser.add_argument(
        "-b", "--bet",
        help="amount of ether to bet",
        type=float,
        required=True
    )
    parser.add_argument(
        "-g", "--guess",
        help="number to guess (between 1 and 10 inclusive)",
        type=int,
        required=True
    )
    parser.add_argument(
        "--gas",
        help="manually specify the transaction gas price to use use (e.g., for replacing a transaction)",
        type=int,
        required=False
    )
    parser.add_argument(
        "--nonce",
        help="manually specify the transaction nonce to use (e.g., for placing multiple bets in a row)",
        type=int,
        required=False
    )
    parser.add_argument(
        "--abi",
        help="contract ABI or full path to .abi file",
        type=str,
        required=True
    )
    parser.add_argument(
        "-w", "--wait",
        help="wait for transaction receipt and show result",
        action="store_true"
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

        # Build account dict (account must be hosted on local node)
        account = build_account(args.address, args.keyfile, args.passphrase)

        # Get contract object
        if os.path.exists(os.path.normpath(args.abi)):
            with open(os.path.normpath(args.abi)) as f:
                abi = json.load(f)
        else:
            abi = args.abi
        contract = web3.eth.contract(address=args.contract, abi=abi)

        # Locally validate bet conditions in script
        # Commenting out will result in contract reverting invalid transactions (consumes gas)
        # assert args.guess >= 1 and args.guess <= 10, "Guess must be between 1-10 inclusive."
        # assert args.bet <= web3.fromWei(web3.eth.get_balance(account["address"]), 'ether'), "Not enough ether in account."
        # assert 10 * args.bet <= web3.fromWei(web3.eth.get_balance(contract.address), 'ether'), "Insufficient pool balance ({} ETH).".format(web3.fromWei(web3.eth.get_balance(contract.address), 'ether'))
        # assert args.bet > 0, "Invalid bet amount."
        # TODO: add nonce assertion check?

        # Submit the transaction (place a bet)
        result = place_bet(contract, account, args.guess, args.bet, args.nonce, args.gas)

        tx_hash = web3.toHex(result)

        # If transaction successful and wait flag set, parse and show transaction results
        if args.wait:

            # Wait for transaction receipt
            tx_receipt = web3.eth.wait_for_transaction_receipt(result)

            # Parse contract events
            bal = contract.events.PoolBalance().processReceipt(tx_receipt, errors=DISCARD)
            bal = web3.fromWei(bal[0]['args']['amount'], 'ether')
            res = contract.events.Result().processReceipt(tx_receipt, errors=DISCARD)
            print('Result: {}\t(Guess: {}, Roll: {}, Bet: {} ETH)'.format(
                res[0]['args']['result'],
                res[0]['args']['guess'],
                res[0]['args']['roll'],
                web3.fromWei(res[0]['args']['bet'], 'ether')
            ))
            print('Pool Balance: {} ETH'.format(bal))
        
        tx = web3.eth.get_transaction(tx_hash)
        print(web3.toJSON(tx))

    except Exception as e:
        print("[ERROR] An unexpected exception has occurred: {}".format(e))
