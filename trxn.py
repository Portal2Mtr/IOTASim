from calendar import timegm as unix_timestamp
from datetime import datetime
from iota.trits import int_from_trits, trits_from_int
from iota.types import Address, Tag, TryteString, TrytesCompatible

from iota import TransactionTrytes
import math


class Trxn:
    #TODO: add support for value trxns
    def __init__(self,bundle,value=0):
        self.bundle = bundle
        self.value = value
        self.timestamp = unix_timestamp(datetime.utcnow().timetuple())

        nonceLength = 27 # From Python iota documentation
        hashLength = 81
        noncestr = '9' * nonceLength
        hashstr = '9' * hashLength
        self.nonce = bytearray(noncestr,'utf-8')
        self.trunk_transaction_hash = bytearray(hashstr,'utf-8')
        self.branch_transaction_hash = bytearray(hashstr,'utf-8')
        """
            The position of the transaction inside the bundle.

                - If the ``current_index`` value is 0, then this is the "head transaction".
                - If it is equal to ``last_index``, then this is the "tail transaction".

            For value transfers, the "spend" transaction is generally in the
            0th position, followed by inputs, and the "change" transaction
            is last.

            :type: ``int``
        """
        self.current_index = None
        self.last_index = None
        self.value_tx = False
        self.bundle_hash = None
        self.signature_message_fragment = None
        self.attachment_timestamp = None
        self.attachment_timestamp_upper_bound = (math.pow(3, 27) - 1) // 2
        self.attachment_timestamp_lower_bound = 999999999
        self.nonce = 0 # Default Nonce
        self.legacy_tag = 'LOCALATTACHINTERFACE9999999'
        self.tag = 'LOCALATTACHINTERFACE9999999'
        self.hash = None

    # Pass back group of trxn info for PoW
    def get_bundle_essence_trits(self):

        # Format trxn features as trytes (same as python IOTA API)
        addr = self.bundle.node.seed
        value = TryteString.from_trits(trits_from_int(self.value,pad=81)) # Pad to 81 trits (27 trytes)
        tstamp = TryteString.from_trits(trits_from_int(self.timestamp,pad=27)) # Pad to 27 trits (9 trytes)
        currIdx = TryteString.from_trits(trits_from_int(self.current_index,pad=27)) # Pad to 27 trits (9 trytes)
        lastIdx = TryteString.from_trits(trits_from_int(self.last_index,pad=27)) # Pad to 27 trits (9 trytes)
        sum = addr + value + tstamp + currIdx + lastIdx

        return (sum.as_trits())

    def as_tryte_string(self):

        msgfrag= self.signature_message_fragment
        seed =TryteString(str(self.bundle.node.seed))
        value = TryteString.from_trits(trits_from_int(self.value, pad=81))
        legacytag= TryteString(self.legacy_tag)
        timestamp= TryteString.from_trits(trits_from_int(self.timestamp, pad=27))
        curridx = TryteString.from_trits(trits_from_int(self.current_index,pad=27))
        lastidx=TryteString.from_trits(trits_from_int(self.last_index, pad=27))
        bundlehash=self.bundle.bundle_hash
        branchtrxnhash= TryteString(self.trunk_transaction_hash)
        trunkhash= TryteString(self.branch_transaction_hash)
        tag= TryteString(self.tag)
        attachtime = TryteString.from_trits(trits_from_int(self.attachment_timestamp,pad=27))
        timelower= TryteString.from_trits(trits_from_int(self.attachment_timestamp_lower_bound, pad=27))
        timeupper= TryteString.from_trits(trits_from_int(self.attachment_timestamp_upper_bound, pad=27))
        nonce = TryteString.from_trits(trits_from_int(self.nonce,pad=81))
        sum = nonce + timeupper + timelower + tag + trunkhash + branchtrxnhash + bundlehash + lastidx + timestamp \
        +legacytag + value + seed + msgfrag + curridx + attachtime

        return TransactionTrytes(sum).__str__()