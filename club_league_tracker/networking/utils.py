import time

from dataclasses import dataclass
from enum import Enum

import requests

@dataclass
class RetryOptions:
    max_retries: int
    retry_buffer_seconds: int

@dataclass
class RequestContents:
    url: str
    headers: dict
    timeout_seconds: int
    proxy: dict = None
    data: str = None

class RequestType(Enum):
    POST = "POST"
    GET = "GET"
    PUT = "PUT"
    DELETE = "DELETE"

def do_retryable_request(request_type: RequestType,
                        request_contents: RequestContents,
                        retry_options: RetryOptions):
    query_response = None
    for i in range(retry_options.max_retries):
        if query_response:
            break

        if i>0:
            print(f"Failed to get response from {request_contents.url}")
            print(f"Trying again in {retry_options.retry_buffer_seconds} seconds")
            time.sleep(retry_options.retry_buffer_seconds)

        # TODO: proper logging
        print(f"Making {request_type.value} request to {request_contents.url}")
        if RequestType.POST == request_type:
            query_response = requests.post(url=request_contents.url,
                                            data=request_contents.data,
                                            headers=request_contents.headers,
                                            timeout=request_contents.timeout_seconds,
                                            proxies=request_contents.proxy)
        elif RequestType.GET == request_type:
            query_response = requests.get(url=request_contents.url,
                                            headers=request_contents.headers,
                                            timeout=request_contents.timeout_seconds,
                                            proxies=request_contents.proxy)
        elif RequestType.PUT == request_type:
            query_response = requests.put(url=request_contents.url,
                                            data=request_contents.data,
                                            headers=request_contents.headers,
                                            timeout=request_contents.timeout_seconds,
                                            proxies=request_contents.proxy)
        elif RequestType.DELETE == request_type:
            query_response = requests.delete(url=request_contents.url,
                                                headers=request_contents.headers,
                                                timeout=request_contents.timeout_seconds,
                                                proxies=request_contents.proxy)
        print(f"Request response: {query_response}")

    if not query_response:
        raise RuntimeError(f"Max retries exceeded sending {request_type} to {request_contents.url}. Got {query_response.text}")

    return query_response
