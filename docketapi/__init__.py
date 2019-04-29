"""docketapi"""

import json
import requests

__version__ = '0.0.4'

QUERY_URI = 'app/docket/api/'
GET_PCAP_URI = 'results/{pcap_id}/merged.pcap'


class DocketClient:
    """Docket API Client

    Core class used for interacting with the Docket RESTful API.

    Args:
        base_url (str): URL pointing to the ROCK NSM (or Docket) instance
        username (str): Authentication username
        password (str): Authentication password
        verify (bool): Verify SSL (ignored on HTTP). Disable to use self-signed certificates
        proxies (dict): Optional requests-style proxies dict

    Attributes:
        base_url (str): Full RFC-1738 URL pointing to the ROCK NSM (or Docket) instance
        query_url (str): URL pointing to Docket query endpoint
        username (str): Authentication username
        session (requests.sessions.Session): Requests session used for all outbound requests

    Examples:

        ::

            from docketapi import DocketClient

            # create a client
            docket = DocketClient('https://rock_nsm_url', 'username', 'password', verify=False)

            # perform a query
            my_query = docket.query(
                after='2019-04-20T21:07:59.689Z',
                before='2019-04-30T21:07:59.689Z',
                host=['151.101.68.223'],
                proto_name='TCP',
                port=['443']
            )

            # retrieve pcap
            pcap = docket.get_pcap(my_query)

            # save pcap
            docket.save_pcap(pcap, filename='my_traffic.pcap')

    """
    def __init__(self, base_url, username, password, verify=True, proxies=None):
        self.base_url = base_url if base_url.endswith('/') else base_url + '/'
        self.query_url = self.base_url + QUERY_URI
        self.username = username

        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.verify = verify
        self.session.proxies = proxies
        self.session.headers['Accept'] = 'application/json'
        self.session.headers['Content-Type'] = 'application/json'

    def __repr__(self):
        return '<{cls}: {user}@{host} v{ver}>'.format(
            cls=self.__class__.__name__,
            user=self.username,
            host=self.base_url,
            ver=__version__
        )

    def _get(self, uri):
        """GET request for retrieving PCAP

        Args:
            uri (str): URI to GET, this will be the PCAP endpoint
        """
        r = self.session.request('GET', self.base_url + uri)
        r.raise_for_status()
        return r.content

    def _post(self, data):
        """POST request for performing queries

        Args:
            data (dict): JSON payload query data to POST
        """
        r = self.session.request('POST', self.query_url, data=json.dumps(data))
        r.raise_for_status()
        return r.json()

    def query(self, **kwargs):
        """Docket query

        Args:
            after (str): After datetime in ISO-8601 format (e.g. '2019-04-20T21:07:59.689Z')
            before (str): Before datetime in ISO-8601 format (e.g. '2019-04-20T21:07:59.689Z')
            host (list): List of IP addresses to filter on (e.g. ['192.168.1.1'])
            net (list): List of CIDR notation networks to filter on (e.g. ['192.168.1.0/24'])
            port (list): List of Ports to filter on (e.g. ['22'])
            proto_name (str): TCP, UDP, or ICMP
        """
        data = dict(**kwargs)
        # handle kwarg key rename
        for k in data.keys():
            if '_' in k:
                new_key = k.replace('_', '-')
                data[new_key] = data.pop(k)
        return self._post(data)

    def get_pcap(self, query_result):
        """Docket get PCAP, returns raw data

        Args:
            query_result (dict): Response from a docket query
        """
        pcap_id = query_result['id']
        uri = GET_PCAP_URI.format(pcap_id=pcap_id)
        return self._get(uri)

    def save_pcap(self, pcap, filename='merged.pcap'):
        """Docket save PCAP to disk

        Args:
            pcap (str): Raw pcap data, response from docket get PCAP
            filename (str): Optional filename to save as, default is merged.pcap
        """
        with open(filename, 'wb+') as f:
            f.write(pcap)
