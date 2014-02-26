#!/usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import requests

# Default server
SERVER_URL = 'http://localhost:8000/partnerprovisioning/v1/'
DEFAULT_COLL = 'log'
DEFAULT_URL = '{}{}'.format(SERVER_URL, DEFAULT_COLL)


class Client(object):
    """ Client class with all requests methods implemented
    """

    def get(self, args):
        """ Retrieve all data or getting selected one
        :args: log id. Optional
        """
        if args:
            r = requests.get('{}/{}'.format(DEFAULT_URL, args), verify=False)
        else:
            r = requests.get(DEFAULT_URL, verify=False)

        if r.status_code == 200:
            return r.json()
        else:
            return 'ERROR: {0}. REASON: {1}'.format(r.status_code, r.text)

    def post(self, data):
        """ Post data log
        :data: data to send to server
        """
        r = requests.post(DEFAULT_URL, verify=False)
        return r

    def put(self, data):
        """ Put data
        :data: log id and data to update it
        """
        r = requests.put(DEFAULT_URL, verify=False)
        return r

    def delete(self, id):
        """ Delete log
        :id: log id to be deleted
        """
        r = requests.delete(DEFAULT_URL, verify=False)
        return r

if __name__ == "__main__":

    parser = ArgumentParser(description="REST client script")
    parser.add_argument('-g', '--get', help='GET collection or log data information. Default collection: %(default)s',
                        default='log')
    parser.add_argument('--post', help='POST log data')
    parser.add_argument('--put', help='Modify existing log data')
    parser.add_argument('-d', '--delete', help='DELETE log')
    args = parser.parse_args()

    # Client instance
    client = Client()
    # Returning result to console
    print client.get(args.get)
