#!/usr/bin/env python

from ethereum.tools import tester
from ethereum.tools.tester import TransactionFailed
from pytest import fixture, mark, lazy_fixture, raises

@fixture(scope='session')
def testerSnapshot(sessionFixture):
    sessionFixture.resetSnapshot()
    sessionFixture.uploadAndAddToController('solidity_test_helpers/ReentrancyGuardHelper.sol')
    ReentrancyGuardHelper = sessionFixture.contracts['ReentrancyGuardHelper']
    return sessionFixture.chain.snapshot()

@fixture
def testerContractsFixture(sessionFixture, testerSnapshot):
    sessionFixture.chain.revert(testerSnapshot)
    return sessionFixture

def test_nonReentrant(testerContractsFixture): 
    ReentrancyGuardHelper = testerContractsFixture.contracts['ReentrancyGuardHelper']
    assert ReentrancyGuardHelper.testerCanReentrant()

    with raises(TransactionFailed):
        ReentrancyGuardHelper.testerCanNotReentrant()
