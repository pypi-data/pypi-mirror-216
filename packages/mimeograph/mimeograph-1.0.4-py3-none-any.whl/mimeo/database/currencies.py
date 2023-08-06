"""The Countries module.

It exports classes related to currencies CSV data:
    * Currency
        DTO class representing a single row in currencies CSV data.
    * CurrenciesDB
        Class exposing READ operations on currencies CSV data.
"""
from __future__ import annotations

from typing import ClassVar

import pandas
from pandas import DataFrame

from mimeo import tools
from mimeo.database.exc import InvalidIndexError


class Currency:
    """DTO class representing a single row in currencies CSV data.

    Attributes
    ----------
    code : str
        A currency code
    name : str
        A currency name
    countries : list[str]
        A countries using the currency
    """

    def __init__(
            self,
            code: str,
            name: str,
            countries: list[str],
    ):
        """Initialize Currency class.

        Parameters
        ----------
        code : str
            A currency code
        name : str
            A currency name
        countries : list
            A countries using the currency
        """
        self.code: str = code
        self.name: str = name
        self.countries: list[str] = countries

    def __str__(
            self,
    ) -> str:
        """Stringify the Currency instance.

        Returns
        -------
        str
            A stringified `dict` representation of the Currency instance
        """
        return str({
            "code": self.code,
            "name": self.name,
            "countries": self.countries,
        })

    def __repr__(
            self,
    ) -> str:
        """Represent the Currency instance.

        Returns
        -------
        str
            A python representation of the Currency instance
        """
        return (f"Currency("
                f"code='{self.code}', "
                f"name='{self.name}', "
                f"countries={self.countries})")


class CurrenciesDB:
    """Class exposing READ operations on currencies CSV data.

    Attributes
    ----------
    NUM_OF_RECORDS : int
        A number of rows in currencies CSV data

    Methods
    -------
    get_currencies() -> list[Currency]
        Get all currencies.
    get_currency_of(country_name: str) -> Currency | None
        Get currency of a specific country.
    get_currency_at(index: int) -> Currency
        Get a currency at `index` position.
    """

    NUM_OF_RECORDS: int = 169
    _CURRENCIES_DB: str = "currencies.csv"
    _CURRENCIES_DF: DataFrame = None
    _CURRENCIES: ClassVar[list] = None
    _COUNTRY_CURRENCIES: ClassVar[dict] = {}

    def get_currency_at(
            self,
            index: int,
    ) -> Currency:
        """Get a currency at `index` position.

        Parameters
        ----------
        index : int
            A currency row index

        Returns
        -------
        Currency
            A specific currency

        Raises
        ------
        InvalidIndexError
            If the provided `index` is out of bounds
        """
        currencies = CurrenciesDB._get_currencies()
        try:
            return currencies[index]
        except IndexError:
            last_index = CurrenciesDB.NUM_OF_RECORDS-1
            raise InvalidIndexError(index, last_index) from IndexError

    def get_currency_of(
            self,
            country_name: str,
    ) -> Currency | None:
        """Get a currency of a specific country.

        Parameters
        ----------
        country_name : str
            A country name to find a currency

        Returns
        -------
        Currency | None
            A currency used in a specific country or None
        """
        return CurrenciesDB._get_country_currency(country_name)

    def get_currencies(
            self,
    ) -> list[Currency]:
        """Get all currencies.

        Returns
        -------
        list[Currency]
            List of all currencies
        """
        return CurrenciesDB._get_currencies().copy()

    @classmethod
    def _get_country_currency(
            cls,
            country_name: str,
    ) -> Currency | None:
        """Get currency of a specific country from cache.

        The country's currency is initialized for the first time and cached in internal
        class attribute.

        Parameters
        ----------
        country_name : str
            A country ISO3 code to filter currencies

        Returns
        -------
        Currency | None
            A currency used in a specific country or None
        """
        if country_name not in cls._COUNTRY_CURRENCIES:
            currencies = cls._get_currencies()
            country_currency = filter(lambda c: country_name in c.countries, currencies)
            cls._COUNTRY_CURRENCIES[country_name] = next(country_currency, None)
        return cls._COUNTRY_CURRENCIES[country_name]

    @classmethod
    def _get_currencies(
            cls,
    ) -> list[Currency]:
        """Get all currencies from cache.

        The currencies list is initialized for the first time and cached in internal
        class attribute.

        Returns
        -------
        list[Currency]
            List of all currencies
        """
        if cls._CURRENCIES is None:
            cls._CURRENCIES = [Currency(row.CODE, row.NAME, row.COUNTRIES)
                               for row in cls._get_currencies_df().itertuples()]
        return cls._CURRENCIES

    @classmethod
    def _get_currencies_df(
            cls,
    ) -> pandas.DataFrame:
        """Load currencies CSV data and save in internal class attribute."""
        if cls._CURRENCIES_DF is None:
            data = tools.get_resource(cls._CURRENCIES_DB)
            cls._CURRENCIES_DF = pandas.read_csv(data)
        return cls._CURRENCIES_DF
