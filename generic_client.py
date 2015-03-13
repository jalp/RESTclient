#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import requests.exceptions
import json
from requests.auth import HTTPBasicAuth

FORM = "application/x-www-form-urlencoded; charset=utf-8"
JSON = "application/json"


class Client:
    """ API generic client """

    def __init__(self, url, timeout=1):
        self.timeout = timeout
        self.url = url

    def get_api_allowed_methods(self):
        """
         Get allowed methods
        :param url: url to get methods
        :return: headers string list
        """
        verbs = requests.options(self.url)
        return verbs.headers["allow"]

    def request(self, method="GET", **kwargs):
        """
         Generic request requester
        :param url: server url
        :param method: method
        :param kwargs: all kind of information: data, auth,...
        :return: data
        """
        timeout = kwargs.get("timeout", None)
        if not timeout:
            timeout = self.timeout

        headers = kwargs.get("headers", None)
        if not headers:
            headers = {"content-type": JSON}

        query_params = kwargs.get("params", None)

        data = kwargs.get("data", None)

        auth = kwargs.get("auth", None)

        stream = kwargs.get("stream", False)

        kwargs = {"headers": headers,
                  "json": data,
                  "timeout": timeout,
                  "auth": auth,
                  "params": query_params,
                  "stream": stream}

        try:
            response = requests.request(method, self.url, **kwargs)

            if response.status_code <= 399:
                if stream:
                    result = []
                    for element in self._stream_treatment(response):
                        result.append(element)
                    return result
                return response.json()
            else:
                return response.reason
        except requests.exceptions.ReadTimeout as rex:
            print("Reading data bytes exception: {}".format(str(rex)))
        except requests.exceptions.ConnectionError as connex:
            print("Connection error: {}".format(str(connex)))
        except requests.exceptions.HTTPError as httpex:
            print("HTTP error: {}".format(httpex))

    def _stream_treatment(self, response):
        for line in response.iter_lines():
            if line:
                yield json.loads(line.decode("UTF-8"))


if __name__ == "__main__":
    url = "http://httpbin.org/get"
    # Testing GET
    c = Client(url)
    print("METHODS: {}".format(c.get_api_allowed_methods()))

    params = {"isBoolean": True, "number": 12}
    print("\nGET\n===\n{}".format(c.request(params=params)))

    # Testing POST
    post_url = "{}{}".format(url[:-3], "post")
    c1 = Client(post_url)
    payload = {"key1": "value1", "key2": "value2"}
    print("\nPOST\n====\n{}".format(c1.request("POST", data=payload)))

    # Testing authentication
    auth = HTTPBasicAuth("ad@min.com", "admin")
    print("\nPOST with auth\n==============\n{}".format(c1.request("POST", data=payload, auth=auth)))

    # Testing auth in path
    auth_url = "{}basic-auth/{}/{}".format(url[:-3], "ad@min.com", "admin")
    c2 = Client(auth_url)
    print("\nPOST with auth URL\n=================\n{}".format(c2.request(data=payload)))

    # Testing stream
    stream_url = "{}stream/20".format(url[:-3], "ad@min.com", "admin")
    c3 = Client(stream_url)
    print("\nUsing Stream\n============\n{}".format(c3.request(stream=True)))

    # Testing DELETE
    delete_url = "{}delete".format(url[:-3])
    c4 = Client(delete_url)
    print("\nDelete URL\n============\n{}".format(c4.request("DELETE")))

    # Testing Internal server error
    url_500 = "{}status/500".format(url[:-3])
    c5 = Client(url_500)
    print("\n500 URL\n============\n{}".format(c5.request()))