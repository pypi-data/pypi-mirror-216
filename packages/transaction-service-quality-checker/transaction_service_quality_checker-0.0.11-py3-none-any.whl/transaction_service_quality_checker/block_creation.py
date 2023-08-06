import logging
from .api.etherscan_api_interface import EtherscanAPIInterface


class BlockCreation:

    def __init__(self, chainIds: list[str], api_url: str, api_key: str, log: logging.Logger = logging):
        self.log = log
        self.etherscan_api = EtherscanAPIInterface(chainIds=chainIds, api_key=api_key, domain=api_url)

    def get_safes_creation_block(self, map: dict):
        for key in map["chains"].keys():
            addresses = map["chains"][key]
            address_block_dict = self.etherscan_api.map_address_block_creation(
                addresses)
            self.log.info(
                f"\n\nAddresses and Block Number Dictionary: \n\n{address_block_dict}")

    async def get_safes_creation_block_from_list(self, addresses: list, chainId: int):
        addresses_block_dict = await self.etherscan_api.map_address_block_creation(addresses, chainId)
        self.log.info(f"\n\nAddresses and Block Number Dictionary: \n\n{addresses_block_dict}")
        return addresses_block_dict

    def get_earliest_block_creation(self, address_block_dict: dict):
        if len(address_block_dict) == 0:
            return None
        earliest_key = list(address_block_dict.keys())[-1]
        return address_block_dict[earliest_key]
