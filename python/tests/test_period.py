# standard imports
import os
import unittest
import json
import logging

# external imports
from chainlib.eth.constant import ZERO_ADDRESS
from chainlib.eth.nonce import RPCNonceOracle
from chainlib.eth.tx import receipt

# local imports
from erc20_demurrage_token import DemurrageToken

# test imports
from tests.base import TestDemurrageDefault

logging.basicConfig(level=logging.DEBUG)
logg = logging.getLogger()

testdir = os.path.dirname(__file__)

class TestPeriod(TestDemurrageDefault):

    def test_period(self):
        nonce_oracle = RPCNonceOracle(self.accounts[0], self.rpc)
        c = DemurrageToken(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.mint_to(self.address, self.accounts[0], self.accounts[1], 1024)
        r = self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        self.backend.time_travel(self.start_time + 61)

        c = DemurrageToken(self.chain_spec, signer=self.signer, nonce_oracle=nonce_oracle)
        (tx_hash, o) = c.change_period(self.address, self.accounts[0])
        r = self.rpc.do(o)
        o = receipt(tx_hash)
        r = self.rpc.do(o)
        self.assertEqual(r['status'], 1)

        o = c.redistributions(self.address, 1, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        redistribution = c.parse_redistributions(r)

        o = c.to_redistribution_period(self.address, redistribution, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        period = c.parse_to_redistribution_period(r)
        self.assertEqual(2, period)

        o = c.redistributions(self.address, 1, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        redistribution = c.parse_redistributions(r)

        o = c.to_redistribution_period(self.address, redistribution, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        period = c.parse_to_redistribution_period(r)
        self.assertEqual(2, period)

        o = c.actual_period(self.address, sender_address=self.accounts[0])
        r = self.rpc.do(o)
        period = c.parse_actual_period(r)
        self.assertEqual(2, period)


if __name__ == '__main__':
    unittest.main()
