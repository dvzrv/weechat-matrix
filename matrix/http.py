# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import json
from enum import Enum, unique


@unique
class RequestType(Enum):
    GET    = 0
    POST   = 1
    PUT    = 2


class HttpResponse:
    def __init__(self, status, headers, body):
        self.status  = status   # type: int
        self.headers = headers  # type: Dict[str, str]
        self.body    = body     # type: bytes


class HttpRequest:
    def __init__(
            self,
            request_type,                        # type: RequestType
            host,                                # type: str
            port,                                # type: int
            location,                            # type: str
            data=None,                           # type: Dict[str, Any]
            user_agent='weechat-matrix/{version}'.format(
                version="0.1")  # type: str
    ):
        # type: (...) -> None
        host_string   = ':'.join([host, str(port)])

        user_agent    = 'User-Agent: {agent}'.format(agent=user_agent)
        host_header   = 'Host: {host}'.format(host=host_string)
        request_list  = []             # type: List[str]
        accept_header = 'Accept: */*'  # type: str
        end_separator = '\r\n'         # type: str
        payload       = None           # type: str

        if request_type == RequestType.GET:
            get = 'GET {location} HTTP/1.1'.format(location=location)
            request_list  = [get, host_header,
                             user_agent, accept_header, end_separator]

        elif (request_type == RequestType.POST or
              request_type == RequestType.PUT):

            json_data     = json.dumps(data, separators=(',', ':'))

            if request_type == RequestType.POST:
                method = "POST"
            else:
                method = "PUT"

            request_line = '{method} {location} HTTP/1.1'.format(
                method=method,
                location=location
            )

            type_header   = 'Content-Type: application/x-www-form-urlencoded'
            length_header = 'Content-Length: {length}'.format(
                length=len(json_data)
            )

            request_list  = [request_line, host_header,
                             user_agent, accept_header,
                             length_header, type_header, end_separator]
            payload       = json_data

        request = '\r\n'.join(request_list)

        self.request = request
        self.payload = payload