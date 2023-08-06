import logging
import os
import yaml
from dotenv import load_dotenv
from comparer import Comparer
from addresses_map import AddressesMap
from block_creation import BlockCreation
from kubernetes import watch, client, config


# Load the environment variables:
load_dotenv()
# Get LOG_LEVEL from environment variables
log_level = os.getenv("LOG_LEVEL", "INFO")
environment = os.getenv("ENVIRONMENT")
etherscan_api_key = os.getenv("ETHERSCAN_KEY")
etherscan_api_url = os.getenv("ETHERSCAN_URL")
safe_domain = os.getenv("SAFE_DOMAIN")
palmera_domain = os.getenv("PALMERA_DOMAIN")
balance_in_usd_percentage_threshold = os.getenv(
    "BALANCE_IN_USD_PERCENTAGE_THRESHOLD")
group = environment + ".palmera.xyz"


def main():
    logging.basicConfig(level=log_level)

    chain_id = 137
    addresses = ["0xc43f4d3573d72f5bb1bb53e81080f6a6342dd3b9",
                 "0xce016794f2968087f7ac614a8716bf6742d25f4b", "0xe1d32becefb8dd9161dd3043a9f56ce59a8481f2"]
    # Check addresses indexing
    problematic_addresses = check_addresses(chain_id, addresses)
    if len(problematic_addresses) == 0:
        logging.info(
            f"No need to reindex addresses: {addresses} for chain: {chain_id}")
        return

    # Get earliest creation block
    earliest_block = get_problematic_addresses_earliest_creation_block(
        etherscan_api_url, etherscan_api_key, problematic_addresses)
    logging.info(
            f"Earliest block: {earliest_block}")


def check_addresses(chain_id, addresses):
    # Compare
    comp = Comparer(domain_a=safe_domain, domain_b=palmera_domain, log=logging,
                    balance_in_usd_percentage_threshold=balance_in_usd_percentage_threshold)
    comp.compare_safes_for_chain(chain_id, addresses)
    # TODO: How to export metrics?
    # comp.export_metrics_to_json("results_test.json")

    # Return list addresses
    category = 'safe_transactions_' + str(chain_id)
    return comp.metrics.get_problematic_addresses(category)


def get_problematic_addresses_earliest_creation_block(etherscan_api_url, etherscan_api_key, addresses: list):
    creation = BlockCreation(etherscan_api_url, etherscan_api_key, log=logging)
    addresses_with_creation_blocks = creation.get_safes_creation_block_from_list(
        addresses=addresses)
    # Return minimum block number of all problematic addresses
    earliest_block = creation.get_earliest_block_creation(
        addresses_with_creation_blocks)
    return earliest_block

if __name__ == '__main__':
    main()
