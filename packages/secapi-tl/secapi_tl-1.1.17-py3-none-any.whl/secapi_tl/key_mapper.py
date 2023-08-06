from typing import List
from .request import sec_request

# a file maintained by the sec that holds all ticker symbols and their corresponding cik
SEC_CIK_TICKERS_DATA = r"https://www.sec.gov/files/company_tickers.json"


def ticker_to_cik(ticker_symbol: str) -> str:
    # returns the cik that belongs to the company with the given ticker symbol
    ticker = ticker_symbol.upper()
    response = sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()

    for entry in data.values():
        if entry['ticker'] == ticker:
            return str(entry['cik_str'])
    raise ValueError(f'ticker symbol {ticker} not found')


def is_registered(ticker_symbol: str) -> bool:
    # proofs whether the company with the given ticker symbol is registered at the sec or not
    ticker = ticker_symbol.upper()
    response = sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()

    for entry in data.values():
        if entry['ticker'] == ticker:
            return True
    else:
        return False


def filter_tickers(tickers: List[str]) -> List[str]:
    tickers = [ticker.upper() for ticker in tickers]
    response = sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()
    tickers_registered = [entry["ticker"] for entry in data.values()]

    return [ticker for ticker in tickers if ticker in tickers_registered]


def get_registered_tickers() -> List[str]:
    response = sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()
    return [entry["ticker"] for entry in data.values()]


def get_registered_ciks() -> List[str]:
    response = sec_request(SEC_CIK_TICKERS_DATA)
    data = response.json()
    return [str(entry["cik_str"]) for entry in data.values()]