import random
import string
import hashlib
from ctypes import *
import iota
from pkg_resources import resource_filename
from iota.crypto.kerl import Kerl
from iota.crypto import Curl
from iota.transaction.types import BundleHash
import math
import time
from trxn import Trxn
from iota.transaction.types import Fragment
from typing import MutableSequence
from iota.transaction.types import TransactionHash
from iota.types import TryteString

import logging
from sys import stderr
logger = logging.getLogger(__name__)

libccurl_path = resource_filename("pow","libccurl.so")

# Load ccurl lib
_libccurl = CDLL(libccurl_path)

# Return and argument types for our c functions
_libccurl.ccurl_pow.restype = POINTER(c_char)
_libccurl.ccurl_pow.argtypes = [c_char_p, c_int]
_libccurl.ccurl_digest_transaction.restype = POINTER(c_char)
_libccurl.ccurl_digest_transaction.argtypes = [c_char_p]

# Represents physical network node and hashing power
class IOTANode:

    def __init__(self,name,sig,initBal=100):
        self.name = name
        self.sig = sig
        self.bal = initBal
        self.seed = iota.crypto.types.Seed.random() # Generates random 81 character string


    # Node gets data (ex: iot node gets data from sensor), will work for now in simulation
    def get_random_string(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(5))

    # Calculate hash from bundle for each trxn
    def calc_hash(self,bundle):
        Trxn_HASH_Trytes = 81
        HASH_LENGTH = Trxn_HASH_Trytes * 3 # Trits conversion
        # Generate bundle hash. (taken from python API client)
        while True:
            sponge = Kerl()
            last_index = len(bundle) - 1

            for i, txn in enumerate(bundle):
                txn.current_index = i
                txn.last_index = last_index

                sponge.absorb(txn.get_bundle_essence_trits()) #TODO

            bundle_hash_trits = [0] * HASH_LENGTH
            sponge.squeeze(bundle_hash_trits)

            bundle_hash = BundleHash.from_trits(bundle_hash_trits) # Convert trits to ascii Trytes
            bundle.bundle_hash = bundle_hash
            # Check that we generated a secure bundle hash.
            # https://github.com/iotaledger/iota.py/issues/84
            #TODO
            # if any(13 in part for part in normalize(bundle_hash)):
            #     # Increment the legacy tag and try again.
            #     tail_transaction: ProposedTransaction = (
            #         self.tail_transaction
            #     )
            #     tail_transaction.increment_legacy_tag()
            # else:
            #     break
            break

        # Copy bundle hash to individual transactions.
        for txn in bundle:
            txn.bundle_hash = bundle_hash

            # Initialize signature/message fragment.
            txn.signature_message_fragment = Fragment('9' * 2187) # Fragment Length TODO

        return self.conductPOW(bundle)

    def __str__(self):
        return self.name+self.sig

    def conductPOW(self,bundle):
        HASH_LENGTH = 243
        mwm = 14 # minimum weight on mainnet tangle (TODO: why 14?)
        trailing_zeros = [0] * mwm # For checking transaction hash

        previoustx = None
        max_iter = 5
        i = 0

        branch_transaction_hash = bundle.branchObj.bundle_hash
        trunk_transaction_hash = bundle.trunkObj.bundle_hash
        for trxn in reversed(bundle.trxns):

            trxn.attachment_timestamp = int(round(time.time() * 1000))

            while i != max_iter:
                if (not previoustx):
                    if trxn.current_index == trxn.last_index:
                        trxn.branch_transaction_hash = branch_transaction_hash
                        trxn.trunk_transaction_hash = trunk_transaction_hash
                    else:
                        raise ValueError('Head transaction is inconsistent in bundle')

                else:  # It is not the head transaction (For clarity, see bundle figure in report)
                    trxn.branch_transaction_hash = trunk_transaction_hash
                    trxn.trunk_transaction_hash = previoustx

                # Let's do the pow locally
                trxn_string = trxn.as_tryte_string().__str__() # TODO
                # returns a python unicode string
                powed_trytes = _libccurl.ccurl_pow(trxn_string.encode('utf-8'), mwm)
                # construct trytestring from python string
                powed_trytes_bytes = powed_trytes[:2673]
                # Let's decode into unicode
                powed_txn_trytes = powed_trytes_bytes.decode('utf-8')
                powed_txn_trytes = TryteString(powed_txn_trytes)

                # Create powed txn hash
                hash_trits: MutableSequence[int] = [0] * HASH_LENGTH
                sponge = Curl()
                sponge.absorb(powed_txn_trytes.as_trits())
                sponge.squeeze(hash_trits)
                hash = TransactionHash.from_trits(hash_trits)
                # powed_txn = Trxn.from_tryte_string(trytes=powed_txn_trytes)
                trxn.hash = hash
                previoustx = hash
                # # put that back in the bundle
                # bundle.transactions[trxn.current_index] = powed_txn

                # # Check for inconsistency in hash
                # hash_trits = powed_txn.hash.as_trits() # TODO

                # powed_trytes = _libccurl.ccurl_pow(trytes.encode('utf-8'), mwm)

                if hash_trits[-mwm:] == trailing_zeros:
                    # We are good to go, exit from while loop
                    break
                else:
                    i = i + 1
                    logger.info('Ooops, wrong hash detected in try'
                        ' #{rounds}. Recalculating pow... '.format(rounds= i))

        return bundle.bundle_hash