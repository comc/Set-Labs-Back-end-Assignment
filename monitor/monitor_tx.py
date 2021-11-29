import asyncio
import json
import os
from web3 import Web3
from web3.logs import STRICT, IGNORE, DISCARD, WARN
from web3.middleware import geth_poa_middleware


def record_log(web3, data, outfile, verbose=False):
    """
    Dump output to file, one JSON object per line
    """

    # TODO: File contents should ideally be a single JSON object

    if verbose:
        print(web3.toJSON(data))

    with open(outfile, "a+") as f:
        f.write(web3.toJSON(data) + "\n")


async def handler_tx(web3, address, outfile, verbose):
    """
    Transaction handler that waits for transaction receipt and write results
    """
    while True:
        receipt = web3.eth.wait_for_transaction_receipt(address)
        record_log(web3, receipt, outfile, verbose)
        return receipt


async def main(web3, addresses, handler, outfile, verbose):
    """
    Set up the async tasks to monitor
    """
    tasks = []
    for address in addresses:
        tasks.append(handler(web3, address, outfile, verbose))

    await asyncio.gather(*tasks)


def start_monitor(web3=None, addresses=[], outdir=None, verbose=False):
    """
    Start asynchronous monitoring for a set of transaction hashes
    """
    # Create output path if required
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    try:
        asyncio.run(main(
            web3,
            addresses,
            handler_tx,
            os.path.join(outdir, "transaction.log"),
            verbose
        ))
    except Exception as e:
        print(e)
