import logging
from .api.etherscan_api_interface import EtherscanAPIInterface


class BlockCreation:

    def __init__(self, api_url: str, api_key: str, log: logging.Logger = logging):
        self.log = log
        self.etherscan_api = EtherscanAPIInterface(
            api_key=api_key, domain=api_url)

    def get_safes_creation_block(self, map: dict):
        for key in map["chains"].keys():
            addresses = map["chains"][key]
            address_block_dict = self.etherscan_api.map_address_block_creation(
                addresses)
            self.log.info(
                f"\n\nAddresses and Block Number Dictionary: \n\n{address_block_dict}")

    def get_safes_creation_block_from_list(self, addresses: list):
        addresses_block_dict = self.etherscan_api.map_address_block_creation(
            addresses)
        self.log.info(
            f"\n\nAddresses and Block Number Dictionary: \n\n{addresses_block_dict}")
        return addresses_block_dict

    def get_earliest_block_creation(self, address_block_dict: dict):
        # if len(address_block_dict) == 0 :
        #     return address_block_dict[0]
        if not address_block_dict:
            self.log.error(
                f"Empty problematic addresses list")
            raise ValueError('The provided dictionary is empty')
        earliest_key = list(address_block_dict.keys())[-1]
        return address_block_dict[earliest_key]
