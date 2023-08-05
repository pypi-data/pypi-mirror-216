"""The Mimeo Database module.

It exports a class related to all Mimeo CSV data:
    * MimeoDB
        Facade class exposing READ operations on all Mimeo CSV data.
"""
from __future__ import annotations

from mimeo.database import (CitiesDB, City, CountriesDB, Country, CurrenciesDB,
                            Currency, FirstName, FirstNamesDB, LastNamesDB)


class MimeoDB:
    """Facade class exposing READ operations on all Mimeo CSV data.

    It combines all attributes and methods exposed by downstream
    classes:
    - CitiesDB
    - CountriesDB
    - CurrenciesDB
    - FirstNamesDB
    - LastNamesDB

    Attributes
    ----------
    NUM_OF_CITIES : int
        A number of rows in cities CSV data
    NUM_OF_COUNTRIES : int
        A number of rows in countries CSV data
    NUM_OF_CURRENCIES : int
        A number of rows in currencies CSV data
    NUM_OF_FIRST_NAMES : int
        A number of rows in forenames CSV data
    NUM_OF_LAST_NAMES : int
        A number of rows in surnames CSV data

    Methods
    -------
    get_cities() -> list[City]
        Get all cities.
    get_cities_of(country: str) -> list[City]
        Get cities of a specific country.
    get_city_at(index: int) -> City
        Get a city at `index` position.
    get_currencies() -> list[Currency]
        Get all currencies.
    get_currency_at(index: int) -> Currency
        Get a currency at `index` position.
    get_currency_of(country: str) -> Currency | None
        Get a currency at `index` position.
    get_countries() -> list[Country]
        Get all countries.
    get_country_at(index: int) -> Country
        Get a country at `index` position.
    get_country_by_iso_3(iso_3: str) -> Country
        Get a country having a specific ISO3 code.
    get_country_by_iso_3(iso_2: str) -> Country
        Get a country having a specific ISO2 code.
    get_country_by_name(name: str) -> Country
        Get a country having a specific name.
    get_first_names() -> list[FirstName]
        Get all first names.
    get_first_names_by_sex(sex: str) -> list[FirstName]
        Get first names for a specific sex.
    get_first_name_at(index: int) -> FirstName
        Get a first name at `index` position.
    get_last_names() -> list[str]
        Get all last names.
    get_last_name_at(index: int) -> str
        Get a last name at `index` position.
    """

    NUM_OF_CITIES: int = CitiesDB.NUM_OF_RECORDS
    NUM_OF_COUNTRIES: int = CountriesDB.NUM_OF_RECORDS
    NUM_OF_CURRENCIES: int = CurrenciesDB.NUM_OF_RECORDS
    NUM_OF_FIRST_NAMES: int = FirstNamesDB.NUM_OF_RECORDS
    NUM_OF_LAST_NAMES: int = LastNamesDB.NUM_OF_RECORDS

    def __init__(
            self,
    ):
        self._cities_db = CitiesDB()
        self._countries_db = CountriesDB()
        self._currencies_db = CurrenciesDB()
        self._first_names_db = FirstNamesDB()
        self._last_names_db = LastNamesDB()

    def get_cities(
            self,
    ) -> list[City]:
        """Get all cities.

        Returns
        -------
        list[City]
            List of all cities
        """
        return self._cities_db.get_cities()

    def get_cities_of(
            self,
            country: str,
    ) -> list[City]:
        """Get cities of a specific country.

        In contrast to CitiesDB.get_cities_of() method it combines
        CitiesDB and CountriesDB to allow for any country detail
        providing. It can be ISO3 code, ISO2 code and name.
        First it will find the specific country and extract its
        ISO3 code to use in CitiesDB.get_cities_of() call.

        Parameters
        ----------
        country : str
            A country ISO3 / ISO2 code or name to filter cities

        Returns
        -------
        list[City]
            List of cities filtered by country
        """
        countries = filter(
            lambda c: country in [c.iso_3, c.iso_2, c.name],
            self.get_countries())
        country = next(countries, None)
        if country is None:
            return []
        return self._cities_db.get_cities_of(country.iso_3)

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
        return self._cities_db.get_city_at(index)

    def get_currencies(
            self,
    ) -> list[Currency]:
        """Get all currencies.

        Returns
        -------
        list[Currency]
            List of all currencies
        """
        return self._currencies_db.get_currencies()

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
        return self._currencies_db.get_currency_at(index)

    def get_currency_of(
            self,
            country: str,
    ) -> Currency | None:
        """Get a currency of a specific country.

        In contrast to CurrenciesDB.get_currency_of() method it combines
        CurrenciesDB and CountriesDB to allow for any country detail
        providing. It can be ISO3 code, ISO2 code and name.
        First it will find the specific country and extract its
        name to use in CurrenciesDB.get_currency_of() call.

        Parameters
        ----------
        country : str
            A country ISO3 / ISO2 code or name to filter currency

        Returns
        -------
        Currency
            A currency used in a specific country
        """
        countries = filter(
            lambda c: country in [c.iso_3, c.iso_2, c.name],
            self.get_countries())
        country = next(countries, None)
        if country is None:
            return None
        return self._currencies_db.get_currency_of(country.name)

    def get_countries(
            self,
    ) -> list[Country]:
        """Get all countries.

        Returns
        -------
        list[Country]
            List of all countries
        """
        return self._countries_db.get_countries()

    def get_country_at(
            self,
            index: int,
    ) -> Country:
        """Get a country at `index` position.

        Parameters
        ----------
        index : int
            A country row index

        Returns
        -------
        Country
            A specific country

        Raises
        ------
        InvalidIndexError
            If the provided `index` is out of bounds
        """
        return self._countries_db.get_country_at(index)

    def get_country_by_iso_3(
            self,
            iso_3: str,
    ) -> Country:
        """Get a country having a specific ISO3 code.

        Parameters
        ----------
        iso_3 : str
            An ISO3 code to find a country

        Returns
        -------
        Country
            A specific country or None
        """
        return self._countries_db.get_country_by_iso_3(iso_3)

    def get_country_by_iso_2(
            self,
            iso_2: str,
    ) -> Country:
        """Get a country having a specific ISO2 code.

        Parameters
        ----------
        iso_2 : str
            An ISO2 code to find a country

        Returns
        -------
        Country
            A specific country or None
        """
        return self._countries_db.get_country_by_iso_2(iso_2)

    def get_country_by_name(
            self,
            name: str,
    ) -> Country:
        """Get a country having a specific name.

        Parameters
        ----------
        name : str
            A name to find a country

        Returns
        -------
        Country
            A specific country or None
        """
        return self._countries_db.get_country_by_name(name)

    def get_first_names(
            self,
    ) -> list[FirstName]:
        """Get all first names.

        Returns
        -------
        list[FirstName]
            List of all first names
        """
        return self._first_names_db.get_first_names()

    def get_first_names_by_sex(
            self,
            sex: str,
    ) -> list[FirstName]:
        """Get first names for a specific sex.

        Parameters
        ----------
        sex : str
            A sex value to filter first names

        Returns
        -------
        list[FirstName]
            List of first names filtered by sex

        Raises
        ------
        InvalidSexError
            If the provided `sex` value is not supported
        """
        return self._first_names_db.get_first_names_by_sex(sex)

    def get_first_name_at(
            self,
            index: int,
    ) -> FirstName:
        """Get a first name at `index` position.

        Parameters
        ----------
        index : int
            A first name row index

        Returns
        -------
        FirstName
            A specific first name

        Raises
        ------
        InvalidIndexError
            If the provided `index` is out of bounds
        """
        return self._first_names_db.get_first_name_at(index)

    def get_last_names(
            self,
    ) -> list[str]:
        """Get all last names.

        Returns
        -------
        list[str]
            List of all last names
        """
        return self._last_names_db.get_last_names()

    def get_last_name_at(
            self,
            index: int,
    ) -> str:
        """Get a last name at `index` position.

        Parameters
        ----------
        index : int
            A last name row index

        Returns
        -------
        str
            A last name

        Raises
        ------
        InvalidIndexError
            If the provided `index` is out of bounds
        """
        return self._last_names_db.get_last_name_at(index)
