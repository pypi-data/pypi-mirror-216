from dcentrapi.Base import Base
from dcentrapi.requests_dappi import requests_get


class HackMitigation(Base):

    def are_addresses_blacklisted(self, addresses: [str]):
        url = self.url + "generic_freeze_signal/are_addresses_blacklisted"
        data = {
            "addresses": addresses,
        }
        response = requests_get(url, json=data, headers=self.headers)
        return response
