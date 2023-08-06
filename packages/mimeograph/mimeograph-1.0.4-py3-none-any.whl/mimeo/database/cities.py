"""The Cities module.

It exports classes related to cities CSV data:
    * City
        DTO class representing a single row in cities CSV data.
    * CitiesDB
        Class exposing READ operations on cities CSV data.
"""
from __future__ import annotations

from typing import ClassVar

import pandas
from pandas import DataFrame

from mimeo import tools
from mimeo.database.exc import InvalidIndexError


class City:
    """DTO class representing a single row in cities CSV data.

    Attributes
    ----------
    id : int
        An identifier
    name : str
        A city name
    name_ascii : str
        A city name in ASCII encoding
    country : str
        A country of a city
    """

    def __init__(
            self,
            identifier: str,
            name: str,
            name_ascii: str,
            country: str,
    ):
        """Initialize City class.

        Parameters
        ----------
        identifier : str
            An identifier
        name : str
            A city name
        name_ascii : str
            A city name in ASCII encoding
        country : str
            A country of a city
        """
        self.id: int = int(identifier)
        self.name: str = name
        self.name_ascii: str = name_ascii
        self.country: str = country

    def __str__(
            self,
    ) -> str:
        """Stringify the City instance.

        Returns
        -------
        str
            A stringified `dict` representation of the City instance
        """
        return str({
            "id": self.id,
            "name": self.name,
            "name_ascii": self.name_ascii,
            "country": self.country,
        })

    def __repr__(
            self,
    ) -> str:
        """Represent the City instance.

        Returns
        -------
        str
            A python representation of the City instance
        """
        return (f"City("
                f"id='{self.id}', "
                f"name='{self.name}', "
                f"name_ascii='{self.name_ascii}', "
                f"country='{self.country}')")


class CitiesDB:
    """Class exposing READ operations on cities CSV data.

    Attributes
    ----------
    NUM_OF_RECORDS : int
        A number of rows in cities CSV data

    Methods
    -------
    get_cities() -> list[City]
        Get all cities.
    get_cities_of(country_iso3: str) -> list[City]
        Get cities of a specific country.
    get_city_at(index: int) -> City
        Get a city at `index` position.
    """

    NUM_OF_RECORDS: int = 42904
    _CITIES_DB: str = "cities.csv"
    _CITIES_DF: DataFrame = None
    _CITIES: ClassVar[list] = None
    _COUNTRY_CITIES: ClassVar[dict] = {}

    def get_city_at(
            self,
            index: int,
    ) -> City:
        """Get a city at `index` position.

        Parameters
        ----------
        index : int
            A city row index

        Returns
        -------
        City
            A specific city

        Raises
        ------
        InvalidIndexError
            If the provided `index` is out of bounds
        """
        cities = CitiesDB._get_cities()
        try:
            return cities[index]
        except IndexError:
            last_index = CitiesDB.NUM_OF_RECORDS-1
            raise InvalidIndexError(index, last_index) from IndexError

    def get_cities_of(
            self,
            country_iso3: str,
    ) -> list[City]:
        """Get cities of a specific country.

        Parameters
        ----------
        country_iso3 : str
            A country ISO3 code to filter cities

        Returns
        -------
        list[City]
            List of cities filtered by country
        """
        return CitiesDB._get_country_cities(country_iso3).copy()

    def get_cities(
            self,
    ) -> list[City]:
        """Get all cities.

        Returns
        -------
        list[City]
            List of all cities
        """
        return CitiesDB._get_cities().copy()

    @classmethod
    def _get_country_cities(
            cls,
            country_iso3: str,
    ) -> list[City]:
        """Get cities of a specific country from cache.

        The country's cities list is initialized for the first time
        and cached in internal class attribute.

        Parameters
        ----------
        country_iso3 : str
            A country ISO3 code to filter cities

        Returns
        -------
        list[City]
            List of cities filtered by country
        """
        if country_iso3 not in cls._COUNTRY_CITIES:
            cities = cls._get_cities()
            cities = filter(lambda c: c.country == country_iso3, cities)
            cls._COUNTRY_CITIES[country_iso3] = list(cities)
        return cls._COUNTRY_CITIES[country_iso3]

    @classmethod
    def _get_cities(
            cls,
    ) -> list[City]:
        """Get all cities from cache.

        The cities list is initialized for the first time and cached
        in internal class attribute.

        Returns
        -------
        list[City]
            List of all cities
        """
        if cls._CITIES is None:
            cls._CITIES = [City(row.ID, row.CITY, row.CITY_ASCII, row.COUNTRY)
                           for row in cls._get_cities_df().itertuples()]
        return cls._CITIES

    @classmethod
    def _get_cities_df(
            cls,
    ) -> pandas.DataFrame:
        """Load cities CSV data and save in internal class attribute."""
        if cls._CITIES_DF is None:
            data = tools.get_resource(cls._CITIES_DB)
            cls._CITIES_DF = pandas.read_csv(data)
        return cls._CITIES_DF
