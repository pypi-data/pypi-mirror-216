"""
This module provides the sec_request function which must be used
for all requests to the  sec.gov domain to ensure that the amount
of requests stays in the boundaries set by the sec.
"""
import requests
from faker import Faker
from ratelimit import limits, sleep_and_retry
from threading import Semaphore

SEC_REQUEST_COUNT = 1
SEC_PERIOD = 0.101

SEMAPHORE = Semaphore(value=1)
SESSION = requests.Session()
FAKER = Faker()


def sec_request(url: str):
    """
    I dont provide the sec_request_decorated function because for some reason the ratelimit decorator does not
    work when some function calls to the decorated function are done locally in this python package and others are
    done from outside the package. I dont know why this is the case but it is. For example using sec_request_decorated
    and get_filings in the same project can cause problems. So I provide this function instead which is just a wrapper
    """
    return sec_request_decorated(url)


@sleep_and_retry
@limits(calls=SEC_REQUEST_COUNT, period=SEC_PERIOD)
def sec_request_decorated(url: str):
    header = {"User-Agent": create_user_agent()}
    try:
        response = SESSION.get(url=url, headers=header)
    except Exception as err:
        raise err

    if response.status_code != 200:
        raise ConnectionError(f"invalid response status code {response.status_code}")
    return response


def create_user_agent() -> str:
    ua = f"{FAKER.first_name()} {FAKER.last_name()} {FAKER.email()}"
    return ua
