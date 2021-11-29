import argparse
import inspect
import json
import os
import subprocess
import sys
import time
from web3 import Web3
from web3.middleware import geth_poa_middleware

sys.path.append(os.path.join(os.getcwd(), "monitor"))
from monitor_tx import start_monitor


global web3


def build_args_list(args):
    """
    """
    args_list = []
    for k, v in args.items():
        args_list.append("--" + str(k))
        args_list.append(str(v))
    return args_list


def test_single_successful_bet(cmd, script, base_args):
    """
    Execute a single successful bet

    Expect: success
    Output: single transaction receipt
    """

    print("\n\n[{}]\n".format(inspect.getframeinfo(inspect.currentframe()).function))
    print("Expect: {}\nOutput: {}\n".format("success", "single transaction receipt"))

    args = base_args
    args["guess"] = 1
    args["bet"] = 0.01

    args = build_args_list(args)

    proc = subprocess.Popen([cmd, script] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    tx_hashes = []
    if not stderr:
        result = json.loads(stdout.decode("ascii"))
        tx_hashes.append(result["hash"])
        start_monitor(web3, tx_hashes, outdir="./output", verbose=True)
    else:
        raise Exception("Unexpected error occurred:\n{}".format(stderr.decode("ascii")))


def test_multiple_successful_bets(cmd, script, base_args):
    """
    Execute a series of consecutive successful bets

    Expect: success
    Output: transaction receipt for each transaction
    """

    print("\n\n[{}]\n".format(inspect.getframeinfo(inspect.currentframe()).function))
    print("Expect: {}\nOutput: {}\n".format("success", "transaction receipt for each transaction"))

    tx_hashes = []

    # Transaction 1
    args = base_args
    args["guess"] = 1
    args["bet"] = 0.01

    args = build_args_list(args)

    proc = subprocess.Popen([cmd, script] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout1, stderr1 = proc.communicate()

    if not stderr1:
        result1 = json.loads(stdout1.decode("ascii"))
        tx_hashes.append(result1["hash"])
        nonce1 = result1["nonce"]
    else:
        raise Exception("Unexpected error occurred:\n{}".format(stderr1.decode("ascii")))

    # Transaction 2
    args = base_args
    args["guess"] = 1
    args["bet"] = 0.01
    args["nonce"] = nonce1 + 1

    args = build_args_list(args)

    proc = subprocess.Popen([cmd, script] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout2, stderr2 = proc.communicate()

    if not stderr2:
        result2 = json.loads(stdout2.decode("ascii"))
        tx_hashes.append(result2["hash"])
    else:
        raise Exception("Unexpected error occurred:\n{}".format(stderr2.decode("ascii")))

    start_monitor(web3, tx_hashes, outdir="./output", verbose=True)


def test_insufficient_wallet_balance(cmd, script, base_args):
    """
    Execute a transaction specifying a bet larger than the account wallet balance

    Expect: failed transaction
    Output: error string
    """

    print("\n\n[{}]\n".format(inspect.getframeinfo(inspect.currentframe()).function))
    print("Expect: {}\nOutput: {}\n".format("failed transaction", "error string"))

    args = base_args
    args["guess"] = 1
    args["bet"] = web3.fromWei(web3.eth.get_balance(args["address"]), "ether") + 1

    args = build_args_list(args)

    proc = subprocess.Popen([cmd, script] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    if not stderr:
        print(stdout.decode("ascii"))
    else:
        raise Exception("Unexpected error occurred:\n{}".format(stderr.decode("ascii")))


def test_insufficient_pool_balance(cmd, script, base_args):
    """
    Execute a transaction specifying a bet larger than the contract payable (pool) balance

    Expect: revert transaction
    Output: error string
    """

    print("\n\n[{}]\n".format(inspect.getframeinfo(inspect.currentframe()).function))
    print("Expect: {}\nOutput: {}\n".format("revert transaction", "error string"))

    args = base_args
    args["guess"] = 1
    # bet must be less than contract balance / 10
    args["bet"] = web3.fromWei(web3.eth.get_balance(args["contract"]), "ether")

    args = build_args_list(args)

    proc = subprocess.Popen([cmd, script] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    if not stderr:
        print(stdout.decode("ascii"))
    else:
        raise Exception("Unexpected error occurred:\n{}".format(stderr.decode("ascii")))


def test_guess_out_of_range(cmd, script, base_args):
    """
    Execute a transaction specify a guess outside of the range 1-10

    Expect: revert transaction
    Output: error string
    """

    print("\n\n[{}]\n".format(inspect.getframeinfo(inspect.currentframe()).function))
    print("Expect: {}\nOutput: {}\n".format("revert transaction", "error string"))

    args = base_args
    args["guess"] = 11
    args["bet"] = web3.fromWei(web3.eth.get_balance(args["contract"]), "ether") / 100

    args = build_args_list(args)

    proc = subprocess.Popen([cmd, script] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    if not stderr:
        print(stdout.decode("ascii"))
    else:
        raise Exception("Unexpected error occurred:\n{}".format(stderr.decode("ascii")))


def test_replace_bet_success(cmd, script, base_args):
    """
    Execute two bets in sequence, the latter to replace the former

    Expect: partial success
    Output:
        Transaction 1: transaction timeout error string after default 120 seconds
        Transaction 2: transaction receipt for successful (replacement) transaction
    """

    print("\n\n[{}]\n".format(inspect.getframeinfo(inspect.currentframe()).function))
    print("Expect: {}\nOutput:\n\t{}\n\t{}\n".format(
            "partial success",
            "Transaction 1: (failure) transaction timeout error string after default 120 seconds",
            "Transaction 2: (success) transaction receipt for successful (replacement) transaction"
    ))

    tx_hashes = []

    # Transaction 1
    args = base_args
    args["guess"] = 1
    args["bet"] = 0.01
    args["nonce"] = web3.eth.get_transaction_count(args["address"])

    args = build_args_list(args)

    proc = subprocess.Popen([cmd, script] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout1, stderr1 = proc.communicate()

    if not stderr1:
        result1 = json.loads(stdout1.decode("ascii"))
        tx_hashes.append(result1["hash"])
        nonce1 = result1["nonce"]
        gas1 = result1["gasPrice"]
    else:
        raise Exception("Unexpected error occurred:\n{}".format(stderr1.decode("ascii")))

    # Transaction 2
    args = base_args
    args["guess"] = 1
    args["bet"] = 0.01
    args["nonce"] = nonce1 # same nonce to replace previous transaction
    args["gas"] = int(gas1 * 1.2) # higher gasPrice to increase priority

    args = build_args_list(args)

    proc = subprocess.Popen([cmd, script] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout2, stderr2 = proc.communicate()

    if not stderr2:
        result2 = json.loads(stdout2.decode("ascii"))
        tx_hashes.append(result2["hash"])
    else:
        raise Exception("Unexpected error occurred:\n{}".format(stderr2.decode("ascii")))

    start_monitor(web3, tx_hashes, outdir="./output", verbose=True)


def test_replace_bet_fail(cmd, script, base_args):
    """
    Execute two bets in sequence, the latter to replace the former with insufficient gas

    Expect: partial success
    Output:
        Transaction 1: transaction receipt for successful (replacement) transaction
        Transaction 2: transaction fail
    """

    print("\n\n[{}]\n".format(inspect.getframeinfo(inspect.currentframe()).function))
    print("Expect: {}\nOutput:\n\t{}\n\t{}\n".format(
            "partial success",
            "Transaction 1: (success) transaction receipt for successful (replacement) transaction",
            "Transaction 2: (failure) transaction fail"
    ))

    tx_hashes = []

    # Transaction 1
    args = base_args
    args["guess"] = 1
    args["bet"] = 0.01
    args["nonce"] = web3.eth.get_transaction_count(args["address"])

    args = build_args_list(args)

    proc = subprocess.Popen([cmd, script] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout1, stderr1 = proc.communicate()

    if not stderr1:
        result1 = json.loads(stdout1.decode("ascii"))
        tx_hashes.append(result1["hash"])
        nonce1 = result1["nonce"]
        gas1 = result1["gasPrice"]
    else:
        raise Exception("Unexpected error occurred:\n{}".format(stderr1.decode("ascii")))

    # Transaction 2
    args = base_args
    args["guess"] = 1
    args["bet"] = 0.01
    args["nonce"] = nonce1 # same nonce to replace previous transaction
    args["gas"] = int(gas1 * 0.9) # lower gasPrice to induce failed submission

    args = build_args_list(args)

    proc = subprocess.Popen([cmd, script] + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout2, stderr2 = proc.communicate()

    start_monitor(web3, tx_hashes, outdir="./output", verbose=True)

    if not stderr2:
        print(stdout2.decode("ascii"))
    else:
        raise Exception("Unexpected error occurred:\n{}".format(stderr2.decode("ascii")))


def run_all_tests(cmd, script, base_args):
    """
    Execute the full suite of tests in succession
    """

    test_single_successful_bet(cmd, script, base_args)
    test_multiple_successful_bets(cmd, script, base_args)
    test_insufficient_wallet_balance(cmd, script, base_args)
    test_insufficient_pool_balance(cmd, script, base_args)
    test_guess_out_of_range(cmd, script, base_args)
    test_replace_bet_success(cmd, script, base_args)
    test_replace_bet_fail(cmd, script, base_args)


if __name__ == "__main__":
    """
    Run the suite of test transactions to demonstrate the network and contract.

    Usage:
    
        run_tests.py [-h] -a ADDRESS -k KEYFILE [-p PASSPHRASE] -c CONTRACT --abi ABI --config CONFIG --python PYTHON

    Required Arguments:

        -a ADDRESS, --address ADDRESS
                                account address of transaction owner
        -k KEYFILE, --keyfile KEYFILE
                                path to account keyfile
        -p PASSPHRASE, --passphrase PASSPHRASE
                                path to file containing account keyfile passphrase (will prompt if not provided)
        -c CONTRACT, --contract CONTRACT
                                contract address
        --abi ABI               contract ABI or full path to .abi file
        --config CONFIG         path to network provider RPC server config.json
        --python PYTHON         path to python executable

    Optional Arguments:

        -h, --help            show this help message and exit

    """

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
        "--abi",
        help="contract ABI or full path to .abi file",
        type=str,
        required=True
    )
    parser.add_argument(
        "--config",
        help="path to network provider RPC server config.json",
        type=str,
        required=True
    )
    parser.add_argument(
        "--python",
        help="path to python executable",
        type=str,
        required=True
    )

    args = parser.parse_args()

    cmd = args.python

    # Relative path to script for submitting bet transactions
    script = "tests/submit_bet.py"

    base_args = {
        "config": args.config,
        "address": args.address,
        "keyfile": args.keyfile,
        "contract": args.contract,
        "passphrase": args.passphrase,
        "abi": args.abi
    }

    try:

        # Load provider config.json
        if os.path.exists(os.path.normpath(args.config)):
            with open(os.path.normpath(args.config)) as f:
                provider = json.loads(f.read())
        else:
            raise FileNotFoundError()
        web3 = Web3(Web3.HTTPProvider(provider["url"] + ":" + str(provider["port"])))
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        # Execute suite of tests
        run_all_tests(cmd, script, base_args)

    except Exception as e:
        print("[ERROR] Exception encountered: {}".format(e))
