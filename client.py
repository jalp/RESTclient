#!/usr/bin/env python
# -*- coding: utf-8 -*-
from argparse import ArgumentParser
import requests

# Default server
SERVER_URL = 'http://localhost/partnerprovisioning/v1/'
# Default secured server
SECURE_SERVER_URL = 'https://localhost/partnerprovisioning/v1/'
DEFAULT_COLL = 'log/'
COLLECTION = 'collection/'
DEFAULT_URL = '{}{}'.format(SERVER_URL, DEFAULT_COLL)
DEFAULT_SECURE_URL = '{}{}'.format(SECURE_SERVER_URL, DEFAULT_COLL)
DEFAULT_HEADER = {'content-type': 'application/json'}


class Client(object):
    """ Client class with all requests methods implemented
    We use verify=False because we use self-signed certs
    """

    def get(self, args):
        """ Retrieve all data or getting selected one
        :args: log id. Optional
        """
        if args:
            r = requests.get('{}{}'.format(DEFAULT_URL, args), verify=False)
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
        r = requests.post(DEFAULT_SECURE_URL, data=data, headers=DEFAULT_HEADER, verify=False)
        if r.status_code == 201:
            return r.json()
        else:
            return 'ERROR: {0}. REASON: {1}'.format(r.status_code, r.text)

    def put(self, data):
        """ Put data
        :data: log id and data to update it in a list
        """
        # WARNING!! Final slash needed in order not to have redirection
        r = requests.put("{}{}/".format(DEFAULT_SECURE_URL, data[0]), data=data[1], headers=DEFAULT_HEADER,
                         verify=False)
        if r.status_code == 200:
            return r.text
        else:
            return 'ERROR: {0}. REASON: {1}'.format(r.status_code, r.text)

    def delete(self, id):
        """ Delete log
        :id: log id to be deleted
        """
        r = requests.delete("{}{}".format(DEFAULT_SECURE_URL, id), verify=False)
        if r.status_code == 204:
            return True
        else:
            return False

    def getcollection(self, collection):
        """ Get collection data
        :collection: Collection to get. Optional param
        """
        if 'collection' in collection:
            r = requests.get("{}{}".format(SERVER_URL, COLLECTION), verify=False)
        else:
            r = requests.get("{}{}{}".format(SERVER_URL, COLLECTION, collection), verify=False)

        if r.status_code == 200:
            return r.json()
        else:
            return 'ERROR: {0}. REASON: {1}'.format(r.status_code, r.text)


if __name__ == "__main__":

    parser = ArgumentParser(description="REST client script")
    # Log client
    parser.add_argument('-g', '--get', help='GET log data information. Get all or unique data log', nargs='?')
    parser.add_argument('--post', help='POST log data')
    parser.add_argument('--put', help='Modify existing log data. First param log id, second data info', nargs=2)
    parser.add_argument('-d', '--delete', help='DELETE log')
    # Collection client
    parser.add_argument('-gc', help='GET collection data information', const='collection', nargs='?')

    args = parser.parse_args()

    # Client instance
    client = Client()
    # Returning result to console
    if args.get:
        print client.get(args.get)
    elif args.post:
        print client.post(args.post)
    elif args.put:
        print client.put(args.put)
    elif args.delete:
        print client.delete(args.delete)
    elif args.gc:
        print client.getcollection(args.gc)
    else:
        # Default, get all logs
        print client.get(args.get)
