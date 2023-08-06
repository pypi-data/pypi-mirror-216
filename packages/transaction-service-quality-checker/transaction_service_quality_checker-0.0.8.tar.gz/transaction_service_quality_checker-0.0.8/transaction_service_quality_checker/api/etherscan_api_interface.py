import requests
import logging
import time


class EtherscanAPIInterface:
    def __init__(self, domain: str = "https://api.etherscan.io", api_key: str = "YourApiKeyToken", log: logging.Logger = logging):
        self.base_url = f"{domain}/api"
        self.api_key = api_key
        self.log = log

    async def get_contract_creation(self, contract_addresses: list):
        results = []
        i = 0
        for i in range(0, len(contract_addresses), 5):
            batch = contract_addresses[i:i+5]
            addresses_str = ','.join(batch)
            self.log.debug(f"\n\nBatch Addresses of Problematic Contract Address: \n\n{addresses_str}")

            params = {
                "module": "contract",
                "action": "getcontractcreation",
                "contractaddresses": addresses_str,
                "apikey": self.api_key
            }
            
            while True:
                res = requests.get(self.base_url, params=params)
                data = res.json()
                self.log.debug(f"\n\nEtherscan API Response get_contract_creation Data JSON While: \n\n{data}")
                time.sleep(0.2)
                
                if data.get("status") == "1" and data.get("message") == "OK":
                    break
                
                if data.get("status") == "0" and data.get("message") == "NOTOK":
                    time.sleep(0.2)
            
            if data.get("status") == "1" and data.get("message") == "OK":
                parsed_results = [
                    {
                        "contractAddress": item.get("contractAddress"),
                        "contractCreator": item.get("contractCreator"),
                        "txHash": item.get("txHash")
                    } for item in data.get("result", [])
                ]
                self.log.debug(f"\n\nEtherscan API Response get_contract_creation parsed_results: \n\n{parsed_results}")
                results.extend(parsed_results)

        return results

    async def get_block_number_by_hash(self, tx_hash: str):
        params = {
            "module": "proxy",
            "action": "eth_getTransactionByHash",
            "txhash": tx_hash,
            "apikey": self.api_key
        }
        res = requests.get(self.base_url, params=params)
        data = res.json()
        self.log.debug(f"\n\nEtherscan API Response get_block_number_by_hash Data JSON: \n\n{data}")
        time.sleep(0.2)
        
        if data.get("result"):
            block_number = int(data["result"]["blockNumber"], 16)  # Convert hex string to integer
            return block_number
        else:
            return None

    async def map_address_block_creation(self, contract_addresses: list):
        self.log.debug(f"\n\nEtherscan API Response map_address_block_creation contract_addresses: \n\n{contract_addresses}")
        creation_data = await self.get_contract_creation(contract_addresses)
        time.sleep(1)
        address_block_dict = {}
        self.log.debug(f"\n\nEtherscan API Response map_address_block_creation creation_data: \n\n{creation_data}")
        for item in creation_data:
            address = item["contractAddress"]
            tx_hash = item["txHash"]
            block_number = await self.get_block_number_by_hash(tx_hash)
            address_block_dict[address] = block_number
            time.sleep(0.2)

        # Sort address_block_dict by decreasing block number
        sorted_address_block_dict = dict(sorted(address_block_dict.items(), key=lambda item: item[1], reverse=True))
        self.log.debug(f"\n\nSorted Addresses and Block Number Dictionary: \n\n{sorted_address_block_dict}")

        return sorted_address_block_dict
