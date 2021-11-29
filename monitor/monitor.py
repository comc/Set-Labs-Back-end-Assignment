import argparse
import asyncio
import json
import os
from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
from web3.middleware import geth_poa_middleware


global web3


def handler_pending(event, contract):
    """
    Pending block handler that filters on contract address
    """
    tx = web3.eth.get_transaction(event)
    if (tx["to"] == contract.address):
        return web3.eth.get_transaction(event)


def handler_event(event, contract):
    """
    Event handler for the contract events; simply returns event for writing
    """
    return event


def record_log(data, outfile, verbose=False):
    """
    Dump output to file, one JSON object per line
    """

    # TODO: File contents should ideally be a single JSON object

    if verbose:
        print(web3.toJSON(data))

    with open(outfile, "a+") as f:
        f.write(web3.toJSON(data) + "\n")


async def log_loop(
        event_filter=None,
        handler=None,
        contract=None,
        outfile=None,
        poll_interval=5,
        verbose=False
):
    """
    Continuously monitor filters and pass results for writing to file
    """
    while True:
        for event in event_filter.get_new_entries():
            result = handler(event, contract)
            if isinstance(result, tuple):
                for item in result:
                    record_log(item, outfile, verbose)
            else:
                record_log(result, outfile, verbose)
        await asyncio.sleep(poll_interval)


def start_monitor(contract=None, outdir=None, verbose=False):
    """
    Create filters and start asynchronous monitoring
    """
    pending_filter = web3.eth.filter("pending")
    pool_exhausted_filter = contract.events.PoolExhausted.createFilter(fromBlock="latest")
    pool_balance_filter = contract.events.PoolBalance.createFilter(fromBlock="latest")
    result_filter = contract.events.Result.createFilter(fromBlock="latest")

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(
                    pool_balance_filter,
                    handler_event,
                    contract,
                    os.path.join(outdir, "event.log"),
                    2,
                    verbose
                ),
                log_loop(
                    pending_filter,
                    handler_pending,
                    contract,
                    os.path.join(outdir, "pending.log"),
                    2.5,
                    verbose
                ),
                log_loop(
                    result_filter,
                    handler_event,
                    contract,
                    os.path.join(outdir, "event.log"),
                    3,
                    verbose
                ),
                log_loop(
                    pool_exhausted_filter,
                    handler_event,
                    contract,
                    os.path.join(outdir, "event.log"),
                    3.5
                ),
            )
        )
    except Exception as e:
        print(e)
    finally:
        loop.close()


if __name__ == "__main__":
    """
    Script to asynchronously monitor for contract activity in pending and
    latest blocks of local private network node, writing filter events to
    "pending.log" and "event.log" output files.

    Usage:
    
        monitor.py [-h] -a ADDRESS --abi ABI --config CONFIG [-o OUTPUT]

    Required Arguments:

        -c CONTRACT, --contract CONTRACT
                                contract address to monitor
        --abi ABI               contract ABI or full path to ABI file
        --config CONFIG         path to network provider RPC server config.json

    Optional Arguments:

        -h, --help              show this help message and exit
        -o OUTPUT, --output OUTPUT
                                path to folder for storing output logs (default: ./output/)
        -v, --verbose           additionally log to command line

    """

    # TODO: No error catching or validation happening

    # TODO: Fails and exits if tx hash not found (e.g., for some multi-
    #       transaction tests submitted across mined block)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-c", "--contract",
        help="contract address to monitor",
        type=str,
        required=True
    )
    parser.add_argument(
        "-o", "--output",
        help="path to folder for storing output logs (default: ./output/)",
        type=str,
        required=False,
        default="./output"
    )
    parser.add_argument(
        "--abi",
        help="contract ABI or full path to ABI file",
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
        "-v", "--verbose",
        help="additionally log to command line",
        action="store_true"
    )

    args = parser.parse_args()

    # Load provider config.json
    if os.path.exists(os.path.normpath(args.config)):
        with open(os.path.normpath(args.config)) as f:
            provider = json.loads(f.read())
    else:
        raise FileNotFoundError()
    web3 = Web3(Web3.HTTPProvider(provider["url"] + ":" + str(provider["port"])))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    # Load contract
    if os.path.exists(os.path.normpath(args.abi)):
        with open(os.path.normpath(args.abi)) as f:
            contract = web3.eth.contract(address=args.address, abi=f.read())
    else:
        contract = web3.eth.contract(address=args.address, abi=args.abi)

    # Create output path if required
    if not os.path.isdir(args.output):
        os.makedirs(args.output)
    # DEBUG: Uncomment below to clear output files on each run
    # else:
    #     if os.path.exists(os.path.join(args.output, "event.log")):
    #         os.remove(os.path.join(args.output, "event.log"))
    #     if os.path.exists(os.path.join(args.output, "pending.log")):
    #         os.remove(os.path.join(args.output, "pending.log"))

    #  Start the monitor
    start_monitor(contract, args.output, args.verbose)
