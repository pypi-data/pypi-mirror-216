from dcentrapi.Base import Base
from dcentrapi.modules.requests_dappi import requests_get


class GasMonitor(Base):

    def get_optimal_gas_price(self, network_name, minutes, stats=None, values=None):
        url = self.url + "gas_monitor/optimal_gas_price_for_network"
        data = {
            "network_name": network_name,
            "minutes": minutes,
            "stats": stats,
            "values": values,
        }
        response = requests_get(url, params=data, headers=self.headers)
        return response.json()
