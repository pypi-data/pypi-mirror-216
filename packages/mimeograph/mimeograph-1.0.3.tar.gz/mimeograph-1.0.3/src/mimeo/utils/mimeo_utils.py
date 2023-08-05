"""The Mimeo Utils module.

This module contains all Mimeo Utils. It exports the following classes:
    * MimeoUtil
        A superclass for all Mimeo Utils.
    * RandomStringUtil
        A MimeoUtil implementation rendering a random string value.
    * RandomIntegerUtil
        A MimeoUtil implementation rendering a random integer value.
    * RandomItemUtil
        A MimeoUtil implementation rendering a random item.
    * DateUtil
        A MimeoUtil implementation rendering a stringified date value.
    * DateTimeUtil
        A MimeoUtil implementation rendering a stringified date time value.
    * AutoIncrementUtil
        A MimeoUtil implementation rendering an auto incremented ID.
    * CurrentIterationUtil
        A MimeoUtil implementation rendering a current iteration ID.
    * KeyUtil
        A MimeoUtil implementation rendering a unique identifier.
    * CityUtil
        A MimeoUtil implementation rendering city names.
    * CountryUtil
        A MimeoUtil implementation rendering country details.
    * CurrencyUtil
        A MimeoUtil implementation rendering currency details.
    * FirstNameUtil
        A MimeoUtil implementation rendering forenames.
    * LastNameUtil
        A MimeoUtil implementation rendering surnames.
"""
from __future__ import annotations

import random
import string
from abc import ABCMeta, abstractmethod
from datetime import date, datetime, timedelta
from typing import Any

from mimeo.context import MimeoContext, MimeoContextManager
from mimeo.context.decorators import mimeo_context
from mimeo.database import Country, Currency, MimeoDB
from mimeo.database.exc import DataNotFoundError, InvalidSexError
from mimeo.utils.exc import InvalidValueError


class MimeoUtil(metaclass=ABCMeta):
    """A superclass for all Mimeo Utils.

    It defines abstract methods to be implemented in each subclass.

    Methods
    -------
    render
        Render a value.
    """

    @classmethod
    def __subclasshook__(
            cls,
            subclass: MimeoUtil,
    ):
        """Verify if a subclass implements all abstract methods.

        Parameters
        ----------
        subclass : MimeoUtil
            A MimeoUtil subclass

        Returns
        -------
        bool
            True if the subclass includes the render method and KEY
            attribute
        """
        return ("KEY" in subclass.__dict__ and
                not callable(subclass.KEY) and
                "render" in subclass.__dict__ and
                callable(subclass.render))

    @abstractmethod
    def render(
            self,
    ) -> Any:
        """Render a value.

        It is an abstract method to implement in subclasses
        """
        raise NotImplementedError


class RandomStringUtil(MimeoUtil):
    """A MimeoUtil implementation rendering a random string value.

    Methods
    -------
    render
        Render a random string value.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY: str = "random_str"

    def __init__(
            self,
            length: int = 20,
            **kwargs,
    ):
        """Initialize RandomStringUtil class.

        Parameters
        ----------
        length : int, default 20
            A length of a string to render
        kwargs : dict
            Arbitrary keyword arguments (ignored).
        """
        self._length: int = length

    def render(
            self,
    ) -> str:
        """Render a random string value.

        Returns
        -------
        str
            A random string value

        Raises
        ------
        InvalidValueError
            If the length param is negative
        """
        if self._length < 0:
            raise InvalidValueError(InvalidValueError.Code.ERR_1,
                                    util=self.KEY,
                                    length=self._length)
        return "".join(random.choice(string.ascii_letters) for _ in range(self._length))


class RandomIntegerUtil(MimeoUtil):
    """A MimeoUtil implementation rendering a random integer value.

    Methods
    -------
    render
        Render a random integer value.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY: str = "random_int"

    def __init__(
            self,
            start: int = 1,
            limit: int = 100,
            **kwargs,
    ):
        """Initialize RandomIntegerUtil class.

        Parameters
        ----------
        start : int, default 1
            A lower bound for integers (inclusive)
        limit : int, default 100
            An upper bound for integers (inclusive)
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._start: int = start
        self._limit: int = limit

    def render(
            self,
    ) -> int:
        """Render a random integer value.

        Returns
        -------
        int
            A random integer value

        Raises
        ------
        InvalidValueError
            If the limit param is lower than start
        """
        if self._start > self._limit:
            raise InvalidValueError(InvalidValueError.Code.ERR_2,
                                    util=self.KEY,
                                    limit=self._limit,
                                    start=self._start)
        return random.randrange(self._start, self._limit + 1)


class RandomItemUtil(MimeoUtil):
    """A MimeoUtil implementation rendering a random item.

    Methods
    -------
    render
        Render a random item.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY: str = "random_item"

    def __init__(
            self,
            items: list | None = None,
            **kwargs,
    ):
        """Initialize RandomItemUtil class.

        Parameters
        ----------
        items : int, default ['']
            A list of items from which a value will be picked up
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._items: list = items if items is not None and len(items) != 0 else [""]

    def render(
            self,
    ) -> Any:
        """Render a random item.

        Returns
        -------
        Any
            A random item
        """
        length = len(self._items)
        return self._items[random.randrange(0, length)]


class DateUtil(MimeoUtil):
    """A MimeoUtil implementation rendering a stringified date value.

    Methods
    -------
    render
        Render a stringified date value.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY: str = "date"

    def __init__(
            self,
            days_delta: int = 0,
            **kwargs,
    ):
        """Initialize DateUtil class.

        Parameters
        ----------
        days_delta : int, default 0
            An integer value of days to add or subtract from today
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._days_delta: int = days_delta

    def render(
            self,
    ) -> str:
        """Render a stringified date value.

        Returns
        -------
        str
            A stringified date value in format %Y-%m-%d
        """
        if self._days_delta == 0:
            date_value = date.today()
        else:
            date_value = date.today() + timedelta(days=self._days_delta)
        return date_value.strftime("%Y-%m-%d")


class DateTimeUtil(MimeoUtil):
    """A MimeoUtil implementation rendering a stringified date time value.

    Methods
    -------
    render
        Render a stringified date time value.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY: str = "date_time"

    def __init__(self,
                 days_delta: int = 0,
                 hours_delta: int = 0,
                 minutes_delta: int = 0,
                 seconds_delta: int = 0,
                 **kwargs):
        """Initialize DateTimeUtil class.

        Parameters
        ----------
        days_delta : int, default 0
            An integer value of days to add or subtract from now
        hours_delta : int, default 0
            An integer value of hours to add or subtract from now
        minutes_delta : int, default 0
            An integer value of minutes to add or subtract from now
        seconds_delta : int, default 0
            An integer value of seconds to add or subtract from now
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._days_delta: int = days_delta
        self._hours_delta: int = hours_delta
        self._minutes_delta: int = minutes_delta
        self._seconds_delta: int = seconds_delta

    def render(
            self,
    ) -> str:
        """Render a stringified date time value.

        Returns
        -------
        str
            A stringified date time value in format %Y-%m-%dT%H:%M:%S
        """
        time_value = datetime.now() + timedelta(days=self._days_delta,
                                                hours=self._hours_delta,
                                                minutes=self._minutes_delta,
                                                seconds=self._seconds_delta)
        return time_value.strftime("%Y-%m-%dT%H:%M:%S")


class AutoIncrementUtil(MimeoUtil):
    """A MimeoUtil implementation rendering an auto incremented ID.

    It is a Mimeo Context-dependent Mimeo Util. Rendered ID value is
    pulled from the Context.

    Methods
    -------
    render
        Render an auto incremented identifier.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY: str = "auto_increment"

    def __init__(
            self,
            pattern: str = "{:05d}",
            **kwargs,
    ):
        """Initialize AutoIncrementUtil class.

        Parameters
        ----------
        pattern : str, default '{:05d}'
            A pattern to inject incremented ID
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._pattern: str = pattern

    @mimeo_context
    def render(
            self,
            context: MimeoContext | None = None,
    ) -> str:
        """Render an auto incremented identifier.

        Parameters
        ----------
        context : MimeoContext, default None
            A current Mimeo Context injected by a decorator

        Returns
        -------
        str
            An auto incremented identifier in a parametrized format

        Raises
        ------
        InvalidValueError
            If the pattern is not a string value
        """
        try:
            identifier = context.next_id()
            return self._pattern.format(identifier)
        except AttributeError:
            context.prev_id()
            raise InvalidValueError(InvalidValueError.Code.ERR_3,
                                    util=self.KEY,
                                    type="string",
                                    param_name="pattern",
                                    param_val=self._pattern) from AttributeError


class CurrentIterationUtil(MimeoUtil):
    """A MimeoUtil implementation rendering a current iteration ID.

    It is a Mimeo Context-dependent Mimeo Util. Rendered ID value is
    pulled from the Context.

    Methods
    -------
    render
        Render a current iteration ID.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY: str = "curr_iter"

    def __init__(
            self,
            context: str | None = None,
            **kwargs,
    ):
        """Initialize CurrentIterationUtil class.

        Parameters
        ----------
        context : str, default None
            A context name to reach the current iteration
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._context_name: str = context

    @mimeo_context
    def render(
            self,
            context: MimeoContext | None = None,
    ) -> int:
        """Render a current iteration ID.

        Parameters
        ----------
        context : MimeoContext, default None
            A current Mimeo Context injected by a decorator

        Returns
        -------
        int
            A specific Mimeo Context's current iteration ID
        """
        if self._context_name is not None:
            context = MimeoContextManager().get_context(self._context_name)
        return context.curr_iteration().id


class KeyUtil(MimeoUtil):
    """A MimeoUtil implementation rendering a unique identifier.

    It is a Mimeo Context-dependent Mimeo Util. Rendered identifiers
    are stored in a MimeoContext and pulled from it when the Mimeo
    Util is parametrized to do so.

    Methods
    -------
    render
        Render a unique identifier.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY: str = "key"

    def __init__(
            self,
            context: str | None = None,
            iteration: int | None = None,
            **kwargs,
    ):
        """Initialize KeyUtil class.

        Parameters
        ----------
        context : str, default None
            A context name to reach already generated identifier
        iteration : int, default None
            A iteration id to reach already generated identifier
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._context_name: str = context
        self._iteration: int = iteration

    @mimeo_context
    def render(
            self,
            context: MimeoContext | None = None,
    ) -> str:
        """Render a unique identifier.

        By default, Key Mimeo Util renders identifier from the current
        iteration of the current Mimeo Context.
        If the context name is parametrized and iteration is not, then
        identifier is pulled from the current iteration of THIS
        context. If the iteration is parametrized, then the identifier
        is pulled from the specific iteration of Mimeo Context (current
        or parametrized).

        Parameters
        ----------
        context : MimeoContext, default None
            A current Mimeo Context injected by a decorator

        Returns
        -------
        str
            A unique identifier
        """
        if self._context_name is not None:
            context = MimeoContextManager().get_context(self._context_name)
        if self._iteration is None:
            iteration = context.curr_iteration()
        else:
            iteration = context.get_iteration(self._iteration)
        return iteration.key


class CityUtil(MimeoUtil):
    """A MimeoUtil implementation rendering city names.

    It is a Mimeo Context-dependent Mimeo Util only when parametrized
    to generate unique city names.

    Methods
    -------
    render
        Render a city name.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY: str = "city"
    _MIMEO_DB: MimeoDB = MimeoDB()

    def __init__(
            self,
            unique: bool = True,
            country: str | None = None,
            **kwargs,
    ):
        """Initialize CityUtil class.

        Parameters
        ----------
        unique : bool, default True
            Indicates if rendered city names will be unique across
            a Mimeo Context
        country : str, default None
            A country limiting city names that can be rendered
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._unique: bool = unique
        self._country: str = country

    @mimeo_context
    def render(
            self,
            context: MimeoContext | None = None,
    ) -> str:
        """Render a city name.

        By default, City Mimeo Util generates a unique city name across
        a Mimeo Context without `country` limitation. If `country` is
        parametrized, then this Mimeo Util will render only those
        city names that lie in the specific country.

        Parameters
        ----------
        context : MimeoContext, default None
            A current Mimeo Context injected by a decorator

        Returns
        -------
        str
            A city name

        Raises
        ------
        OutOfStockError
            If all unique cities have been consumed already
        DataNotFoundError
            If database does not contain any cities for the provided
            `country`
        """
        if self._country is None:
            if self._unique:
                index = context.next_city_index()
            else:
                index = random.randrange(MimeoDB.NUM_OF_CITIES)
            city = self._MIMEO_DB.get_city_at(index)
        else:
            country_cities = self._MIMEO_DB.get_cities_of(self._country)
            country_cities_count = len(country_cities)
            if country_cities_count == 0:
                raise DataNotFoundError(DataNotFoundError.Code.ERR_2,
                                        data="city",
                                        param_name="country",
                                        param_val=self._country)

            if self._unique:
                index = context.next_city_index(self._country)
            else:
                index = random.randrange(country_cities_count)
            city = country_cities[index]

        return city.name_ascii


class CountryUtil(MimeoUtil):
    """A MimeoUtil implementation rendering country details.

    It is a Mimeo Context-dependent Mimeo Util only when parametrized
    to generate unique country names.

    Methods
    -------
    render
        Render a country detail (name, ISO3 or ISO2 code).

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY: str = "country"

    _VALUE_NAME: str = "name"
    _VALUE_ISO3: str = "iso3"
    _VALUE_ISO2: str = "iso2"
    _SUPPORTED_VALUES: tuple = (_VALUE_NAME, _VALUE_ISO3, _VALUE_ISO2)
    _MIMEO_DB: MimeoDB = MimeoDB()

    def __init__(
            self,
            value: str | None = None,
            unique: bool = True,
            country: str | None = None,
            **kwargs,
    ):
        """Initialize CountryUtil class.

        Parameters
        ----------
        value : str, default 'name'
            Indicates which country detail should be rendered:
            name, ISO3 code or ISO2 code.
        unique : bool, default True
            Indicates if rendered country names will be unique across
            a Mimeo Context
        country : str, default None
            A one country detail to get its other detail
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._value: str = value if value is not None else self._VALUE_NAME
        self._unique: bool = unique
        self._country: str = country

    @mimeo_context
    def render(
            self,
            context: MimeoContext | None = None,
    ) -> str:
        """Render a country name.

        By default, Country Mimeo Util generates a unique country name
        across a Mimeo Context. If `value` is parametrized, then it
        will render a specific country detail (name, ISO3 code or ISO2
        code). This Mimeo Util allows you to provide a `country` detail
        (e.g. ISO3 code) to get another detail (e.g. name).
        When `country` is parametrized, then the unique parameter is
        ignored.

        Parameters
        ----------
        context : MimeoContext, default None
            A current Mimeo Context injected by a decorator

        Returns
        -------
        str
            A country detail

        Raises
        ------
        InvalidValueError
            If the `value` parameter value is not supported
        OutOfStockError
            If all unique countries have been consumed already
        DataNotFoundError
            If database does not contain the provided `country`
        """
        if self._value == self._VALUE_NAME:
            return self._get_country(context).name
        if self._value == self._VALUE_ISO3:
            return self._get_country(context).iso_3
        if self._value == self._VALUE_ISO2:
            return self._get_country(context).iso_2
        raise InvalidValueError(InvalidValueError.Code.ERR_4,
                                util=self.KEY,
                                value=self._value,
                                supported_values=self._SUPPORTED_VALUES)

    def _get_country(
            self,
            context: MimeoContext,
    ) -> Country:
        if self._country is not None:
            countries = self._MIMEO_DB.get_countries()
            country_found = next(
                filter(lambda c: self._country in [c.name, c.iso_3, c.iso_2],
                       countries),
                None,
            )
            if country_found is None:
                raise DataNotFoundError(DataNotFoundError.Code.ERR_1,
                                        data="country",
                                        value=self._country)
            return country_found

        if self._unique:
            index = context.next_country_index()
        else:
            index = random.randrange(MimeoDB.NUM_OF_COUNTRIES)
        return self._MIMEO_DB.get_country_at(index)


class CurrencyUtil(MimeoUtil):
    """A MimeoUtil implementation rendering currency details.

    It is a Mimeo Context-dependent Mimeo Util only when parametrized
    to generate unique currency codes.

    Methods
    -------
    render
        Render a currency detail (code or name).

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY: str = "currency"

    _VALUE_CODE: str = "code"
    _VALUE_NAME: str = "name"
    _SUPPORTED_VALUES: tuple = (_VALUE_CODE, _VALUE_NAME)
    _MIMEO_DB: MimeoDB = MimeoDB()

    def __init__(
            self,
            value: str | None = None,
            unique: bool = False,
            country: str | None = None,
            **kwargs,
    ):
        """Initialize CurrencyUtil class.

        Parameters
        ----------
        value : str, default 'code'
            Indicates which currency detail should be rendered:
            code or name.
        unique : bool, default False
            Indicates if rendered currency codes will be unique across
            a Mimeo Context
        country : str, default None
            A country of which the currency should be rendered
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._value: str = value if value is not None else self._VALUE_CODE
        self._unique: bool = unique
        self._country: str = country

    @mimeo_context
    def render(
            self,
            context: MimeoContext | None = None,
    ) -> str:
        """Render a currency code.

        By default, Currency Mimeo Util generates a non-unique currency code across
        a Mimeo Context. If `value` is parametrized, then it will render a specific
        currency detail (code or name). This Mimeo Util allows you to provide
        a `country` to get a currency being used there. When `country` is parametrized,
        then the 'unique' parameter is ignored.

        Parameters
        ----------
        context : MimeoContext, default None
            A current Mimeo Context injected by a decorator

        Returns
        -------
        str
            A currency code

        Raises
        ------
        InvalidValueError
            If the `value` parameter value is not supported
        OutOfStockError
            If all unique currencies have been consumed already
        DataNotFoundError
            If database does not contain a currency of the provided `country`
        """
        if self._value == self._VALUE_CODE:
            return self._get_currency(context).code
        if self._value == self._VALUE_NAME:
            return self._get_currency(context).name
        raise InvalidValueError(InvalidValueError.Code.ERR_4,
                                util=self.KEY,
                                value=self._value,
                                supported_values=self._SUPPORTED_VALUES)

    def _get_currency(
            self,
            context: MimeoContext,
    ) -> Currency:
        if self._country is None:
            if self._unique:
                index = context.next_currency_index()
            else:
                index = random.randrange(MimeoDB.NUM_OF_CURRENCIES)
            currency = self._MIMEO_DB.get_currency_at(index)
        else:
            currency = self._MIMEO_DB.get_currency_of(self._country)
            if currency is None:
                raise DataNotFoundError(DataNotFoundError.Code.ERR_2,
                                        data="currency",
                                        param_name="country",
                                        param_val=self._country)
        return currency


class FirstNameUtil(MimeoUtil):
    """A MimeoUtil implementation rendering forenames.

    It is a Mimeo Context-dependent Mimeo Util only when parametrized
    to generate unique forenames.

    Methods
    -------
    render
        Render a first name.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY: str = "first_name"
    __MIMEO_DB: MimeoDB = MimeoDB()

    def __init__(
            self,
            unique: bool = True,
            sex: str | None = None,
            **kwargs,
    ):
        """Initialize FirstNameUtil class.

        Parameters
        ----------
        unique : bool, default True
            Indicates if rendered forenames will be unique across
            a Mimeo Context
        sex : str, default None
            A sex to limit forenames
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._unique: bool = unique
        self._sex: str = self._standardize_sex(sex)

    @mimeo_context
    def render(
            self,
            context: MimeoContext | None = None,
    ) -> str:
        """Render a first name.

        By default, First Name Mimeo Util generates a unique forename
        across a Mimeo Context without sex limitation. If `sex` is
        parametrized, then this Mimeo Util will render only those
        first names that are assigned to the specific sex.

        Parameters
        ----------
        context : MimeoContext, default None
            A current Mimeo Context injected by a decorator

        Returns
        -------
        str
            A first name

        Raises
        ------
        OutOfStockError
            If all unique first names have been consumed already
        InvalidSexError
            If the `sex` parameter value is not supported
        """
        if self._sex is None:
            if self._unique:
                index = context.next_first_name_index()
            else:
                index = random.randrange(MimeoDB.NUM_OF_FIRST_NAMES)
            first_name = self.__MIMEO_DB.get_first_name_at(index)
        else:
            first_name_for_sex = self.__MIMEO_DB.get_first_names_by_sex(self._sex)
            first_name_for_sex_count = len(first_name_for_sex)

            if self._unique:
                index = context.next_first_name_index(self._sex)
            else:
                index = random.randrange(first_name_for_sex_count)
            first_name = first_name_for_sex[index]

        return first_name.name

    @classmethod
    def _standardize_sex(
            cls,
            sex: str,
    ):
        if sex is None:
            return sex
        if sex.upper() in ["M", "MALE"]:
            return "M"
        if sex.upper() in ["F", "FEMALE"]:
            return "F"
        raise InvalidSexError(("M", "F", "Male", "Female"))


class LastNameUtil(MimeoUtil):
    """A MimeoUtil implementation rendering surnames.

    It is a Mimeo Context-dependent Mimeo Util only when parametrized
    to generate unique surnames.

    Methods
    -------
    render
        Render a last name.

    Attributes
    ----------
    KEY : str
        A Mimeo Util key
    """

    KEY: str = "last_name"
    __MIMEO_DB: MimeoDB = MimeoDB()

    def __init__(
            self,
            unique: bool = True,
            **kwargs,
    ):
        """Initialize LastNameUtil class.

        Parameters
        ----------
        unique : bool, default True
            Indicates if rendered forenames will be unique across
            a Mimeo Context
        kwargs : dict
            Arbitrary keyword arguments (ignored)
        """
        self._unique: bool = unique

    @mimeo_context
    def render(
            self,
            context: MimeoContext | None = None,
    ) -> str:
        """Render a last name.

        By default, First Name Mimeo Util generates a unique surname
        across a Mimeo Context.

        Parameters
        ----------
        context : MimeoContext, default None
            A current Mimeo Context injected by a decorator

        Returns
        -------
        str
            A last name

        Raises
        ------
        OutOfStockError
            If all unique last names have been consumed already
        """
        if self._unique:
            index = context.next_first_name_index()
        else:
            index = random.randrange(MimeoDB.NUM_OF_FIRST_NAMES)
        return self.__MIMEO_DB.get_last_name_at(index)
