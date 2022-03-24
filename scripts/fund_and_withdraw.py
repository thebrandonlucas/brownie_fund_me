from brownie import FundMe
from scripts.helpful_scripts import get_account
from scripts.deploy import deploy_fund_me

def fund():
    fund_me_contract = deploy_fund_me()
    account = get_account()
    entrance_fee = fund_me_contract.getEntranceFee()
    print(entrance_fee)
    print(f"The current entry fee is {entrance_fee}")
    fund_me_contract.fund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me_contract = FundMe[-1]
    account = get_account()
    fund_me_contract.withdraw({"from": account})


def main():
    fund()
    withdraw()
