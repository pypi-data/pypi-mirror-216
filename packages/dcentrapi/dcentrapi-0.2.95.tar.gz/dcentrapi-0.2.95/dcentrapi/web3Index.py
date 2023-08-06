from dcentrapi.Base import Base
from dcentrapi.requests_dappi import requests_get


class Web3Index(Base):
    def get_pairs(self, network_name: str, token_address: str):
        url = self.web3index_url + "pairs" + f"/{network_name}/{token_address}"
        response = requests_get(url, headers=self.headers)
        return response.json()

    def get_factories(self):
        url = self.web3index_url + "factories"
        response = requests_get(url, headers=self.headers)
        return response.json()

    def get_token_price_snapshot(self, info):
        # Currently info is token symbol (str), e.g. "XCAD"
        # In future, might also have the base token id (int)
        url = self.web3index_url + "token_price_snapshot" + f"/{info}"
        response = requests_get(url, headers=self.headers)
        return response.json()
