# Docket Python Client

This is a Python client API for [Docket](https://github.com/rocknsm/docket) which is a RESTful API for [Stenographer](https://github.com/google/stenographer). This library is primarily for use with [ROCK NSM](https://rocknsm.io/) to easily automate retrieval of network traffic for post-process analysis. 

# Install

```
pip install docketapi --user
```

# Usage

```python
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
```
