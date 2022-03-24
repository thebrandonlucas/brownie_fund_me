from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    fund_me_contract = deploy_fund_me()
    account = get_account()
    entrance_fee = fund_me_contract.getEntranceFee() + 100
    tx = fund_me_contract.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me_contract.addressToAmountFunded(account.address) == entrance_fee
    tx2 = fund_me_contract.withdraw({"from": account})
    tx2.wait(1)
    assert fund_me_contract.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")
    account = get_account()
    fund_me = deploy_fund_me()
    # Add a random "bad actor" account to ensure that it is different than the account
    # that deployed the smart contract
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withdraw({"from": bad_actor})
