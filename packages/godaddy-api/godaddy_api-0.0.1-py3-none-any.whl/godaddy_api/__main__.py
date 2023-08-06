from godaddy_api.godaddy_client import GodaddyClient
from godaddy_api import get_api_key, get_api_secret, get_api_url
from argparse import ArgumentParser


def main():
    key = get_api_key()
    secret = get_api_secret()
    url = get_api_url()
    if key == None or secret == None:
        return

    parser = ArgumentParser(prog='GoDaddy A record',
                            description='Sets A record using GoDaddy API.')

    parser.add_argument(
        "domain",
        help=
        "Domain name you wish to set A record for (example: entire-domain.com)"
    )
    parser.add_argument("record_name",
                        help="""
    Name for A record.
    @ sign is for your entire domain (example: entire-domain.com).
    some-name is for your subdomain (example: some-name.entire-domain.com
    """)
    parser.add_argument("ip_address",
                        help="IP address you want it to point to.")
    args = parser.parse_args()
    client = GodaddyClient(key, secret, url)
    res = client.set_a_record(args.domain, args.record_name, args.ip_address)

    if res.status_code == 200:
        print("A record set.")
    else:
        print("Something went wrong.")


if __name__ == "__main__":
    main()
