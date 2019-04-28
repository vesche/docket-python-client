Docket Python Client
====================

.. image:: https://img.shields.io/pypi/v/docketapi.svg
    :target: https://pypi.python.org/pypi/docketapi
.. image:: https://img.shields.io/pypi/pyversions/docketapi.svg
    :target: https://pypi.python.org/pypi/docketapi
.. image:: https://readthedocs.org/projects/docket-python-client/badge/?version=latest
    :target: http://docket-python-client.readthedocs.io/

This is a Python client API for `Docket`_ which is a RESTful API for `Stenographer`_.

.. _Docket: https://github.com/rocknsm/docket
.. _Stenographer: https://github.com/google/stenographer

This library is primarily for use with `ROCK NSM`_ to easily automate retrieval of network traffic for post-process analysis.

.. _ROCK NSM: https://rocknsm.io/


Installation
------------

::

    pip install docketapi --user


Example
-------

.. code-block:: python

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


Documentation
-------------

See the `Docs on RTD`_ for full documentation.

.. _Docs on RTD: http://docket-python-client.readthedocs.io/
