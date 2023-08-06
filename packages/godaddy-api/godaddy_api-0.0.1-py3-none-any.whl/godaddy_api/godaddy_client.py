from dataclasses import asdict
import requests
import os
from typing import Union
from godaddy_api.data.domain_available import DomainAvailable
from godaddy_api.data.domain_record import DomainRecord


class GodaddyClient:

    def __init__(self,
                 api_key: str,
                 api_secret: str,
                 api_url: str = "https://api.godaddy.com/"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = api_url

    def domains_available(self, domain: str) -> Union[DomainAvailable, None]:
        response = requests.get(f"{self.api_url}v1/domains/available",
                                params={
                                    "domain": domain
                                },
                                headers={
                                    "Authorization":
                                    f"sso-key {self.api_key}:{self.api_secret}"
                                }).json()

        try:
            return DomainAvailable(response["available"], response["currency"],
                                   response["definitive"], response["domain"],
                                   response["period"], response["price"])
        except Exception:
            return None

    def add_records(self, domain: str, records: list[DomainRecord]):
        """
        Returns entire response.
        """

        record_dictionaries = [asdict(record) for record in records]
        response = requests.patch(
            f"{self.api_url}v1/domains/{domain}/records",
            json=record_dictionaries,
            headers={
                "Authorization": f"sso-key {self.api_key}:{self.api_secret}"
            })

        return response

    def add_a_record(self, domain: str, record_name: str, ip_address: str):
        """
        Returns entire response.
        Status code `200` means it's successful.
        Status code `422` means record already exists.

        Example:

        ```py
        client.add_a_record("something.com", "@", "123.123.123.123")
        ```

        Example for `one.something.com` subdomain:
        ```py
        client.add_a_record("something.com", "one", "123.123.123.123")
        ```
        """

        record = DomainRecord(ip_address, record_name, 1, 1, "", "", 600, "A",
                              1)
        return self.add_records(domain, [record])

    def remove_a_record(self, domain: str, record_name: str):
        """
        Returns entire response.
        Status code `204` means it's successful.
        Status code `404` means record didn't exist.
        """
        record_type = 'A'
        response = requests.delete(
            f"{self.api_url}v1/domains/{domain}/records/{record_type}/{record_name}",
            headers={
                "Authorization": f"sso-key {self.api_key}:{self.api_secret}"
            })

        return response

    def set_a_record(self, domain: str, record_name: str, ip_address: str):
        """
        Removes the record and adds it again. Returns response from
        request that adds the record, so successful status code is `200`. 
        """
        self.remove_a_record(domain, record_name)
        response = self.add_a_record(domain, record_name, ip_address)
        return response
