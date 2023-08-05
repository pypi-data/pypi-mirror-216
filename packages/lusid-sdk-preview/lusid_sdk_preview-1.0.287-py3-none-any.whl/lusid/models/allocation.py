# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    The version of the OpenAPI document: 1.0.287
    Contact: info@finbourne.com
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from lusid.configuration import Configuration


class Allocation(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
      required_map (dict): The key is attribute name
                           and the value is whether it is 'required' or 'optional'.
    """
    openapi_types = {
        'id': 'ResourceId',
        'allocated_order_id': 'ResourceId',
        'portfolio_id': 'ResourceId',
        'quantity': 'float',
        'instrument_identifiers': 'dict(str, str)',
        'version': 'Version',
        'properties': 'dict(str, PerpetualProperty)',
        'instrument_scope': 'str',
        'lusid_instrument_id': 'str',
        'placement_ids': 'list[ResourceId]',
        'state': 'str',
        'side': 'str',
        'type': 'str',
        'settlement_date': 'datetime',
        'date': 'datetime',
        'price': 'CurrencyAndAmount',
        'settlement_currency': 'str',
        'settlement_currency_fx_rate': 'float',
        'counterparty': 'str',
        'execution_ids': 'list[ResourceId]',
        'links': 'list[Link]'
    }

    attribute_map = {
        'id': 'id',
        'allocated_order_id': 'allocatedOrderId',
        'portfolio_id': 'portfolioId',
        'quantity': 'quantity',
        'instrument_identifiers': 'instrumentIdentifiers',
        'version': 'version',
        'properties': 'properties',
        'instrument_scope': 'instrumentScope',
        'lusid_instrument_id': 'lusidInstrumentId',
        'placement_ids': 'placementIds',
        'state': 'state',
        'side': 'side',
        'type': 'type',
        'settlement_date': 'settlementDate',
        'date': 'date',
        'price': 'price',
        'settlement_currency': 'settlementCurrency',
        'settlement_currency_fx_rate': 'settlementCurrencyFxRate',
        'counterparty': 'counterparty',
        'execution_ids': 'executionIds',
        'links': 'links'
    }

    required_map = {
        'id': 'required',
        'allocated_order_id': 'required',
        'portfolio_id': 'required',
        'quantity': 'required',
        'instrument_identifiers': 'required',
        'version': 'optional',
        'properties': 'optional',
        'instrument_scope': 'optional',
        'lusid_instrument_id': 'required',
        'placement_ids': 'optional',
        'state': 'optional',
        'side': 'optional',
        'type': 'optional',
        'settlement_date': 'optional',
        'date': 'optional',
        'price': 'optional',
        'settlement_currency': 'optional',
        'settlement_currency_fx_rate': 'optional',
        'counterparty': 'optional',
        'execution_ids': 'optional',
        'links': 'optional'
    }

    def __init__(self, id=None, allocated_order_id=None, portfolio_id=None, quantity=None, instrument_identifiers=None, version=None, properties=None, instrument_scope=None, lusid_instrument_id=None, placement_ids=None, state=None, side=None, type=None, settlement_date=None, date=None, price=None, settlement_currency=None, settlement_currency_fx_rate=None, counterparty=None, execution_ids=None, links=None, local_vars_configuration=None):  # noqa: E501
        """Allocation - a model defined in OpenAPI"
        
        :param id:  (required)
        :type id: lusid.ResourceId
        :param allocated_order_id:  (required)
        :type allocated_order_id: lusid.ResourceId
        :param portfolio_id:  (required)
        :type portfolio_id: lusid.ResourceId
        :param quantity:  The quantity of given instrument allocated. (required)
        :type quantity: float
        :param instrument_identifiers:  The instrument allocated. (required)
        :type instrument_identifiers: dict(str, str)
        :param version: 
        :type version: lusid.Version
        :param properties:  Client-defined properties associated with this allocation.
        :type properties: dict[str, lusid.PerpetualProperty]
        :param instrument_scope:  The scope in which the instrument lies
        :type instrument_scope: str
        :param lusid_instrument_id:  The LUSID instrument id for the instrument allocated. (required)
        :type lusid_instrument_id: str
        :param placement_ids:  A placement - also known as an order placed in the market - associated with this allocation.
        :type placement_ids: list[lusid.ResourceId]
        :param state:  The state of this allocation.
        :type state: str
        :param side:  The side of this allocation (examples: Buy, Sell, ...).
        :type side: str
        :param type:  The type of order associated with this allocation (examples: Limit, Market, ...).
        :type type: str
        :param settlement_date:  The settlement date for this allocation.
        :type settlement_date: datetime
        :param date:  The date of this allocation.
        :type date: datetime
        :param price: 
        :type price: lusid.CurrencyAndAmount
        :param settlement_currency:  The settlement currency of this allocation.
        :type settlement_currency: str
        :param settlement_currency_fx_rate:  The settlement currency to allocation currency FX rate.
        :type settlement_currency_fx_rate: float
        :param counterparty:  The counterparty for this allocation.
        :type counterparty: str
        :param execution_ids:  The executions associated with this allocation
        :type execution_ids: list[lusid.ResourceId]
        :param links: 
        :type links: list[lusid.Link]

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._id = None
        self._allocated_order_id = None
        self._portfolio_id = None
        self._quantity = None
        self._instrument_identifiers = None
        self._version = None
        self._properties = None
        self._instrument_scope = None
        self._lusid_instrument_id = None
        self._placement_ids = None
        self._state = None
        self._side = None
        self._type = None
        self._settlement_date = None
        self._date = None
        self._price = None
        self._settlement_currency = None
        self._settlement_currency_fx_rate = None
        self._counterparty = None
        self._execution_ids = None
        self._links = None
        self.discriminator = None

        self.id = id
        self.allocated_order_id = allocated_order_id
        self.portfolio_id = portfolio_id
        self.quantity = quantity
        self.instrument_identifiers = instrument_identifiers
        if version is not None:
            self.version = version
        self.properties = properties
        self.instrument_scope = instrument_scope
        self.lusid_instrument_id = lusid_instrument_id
        self.placement_ids = placement_ids
        self.state = state
        self.side = side
        self.type = type
        self.settlement_date = settlement_date
        if date is not None:
            self.date = date
        if price is not None:
            self.price = price
        self.settlement_currency = settlement_currency
        self.settlement_currency_fx_rate = settlement_currency_fx_rate
        self.counterparty = counterparty
        self.execution_ids = execution_ids
        self.links = links

    @property
    def id(self):
        """Gets the id of this Allocation.  # noqa: E501


        :return: The id of this Allocation.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Allocation.


        :param id: The id of this Allocation.  # noqa: E501
        :type id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and id is None:  # noqa: E501
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def allocated_order_id(self):
        """Gets the allocated_order_id of this Allocation.  # noqa: E501


        :return: The allocated_order_id of this Allocation.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._allocated_order_id

    @allocated_order_id.setter
    def allocated_order_id(self, allocated_order_id):
        """Sets the allocated_order_id of this Allocation.


        :param allocated_order_id: The allocated_order_id of this Allocation.  # noqa: E501
        :type allocated_order_id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and allocated_order_id is None:  # noqa: E501
            raise ValueError("Invalid value for `allocated_order_id`, must not be `None`")  # noqa: E501

        self._allocated_order_id = allocated_order_id

    @property
    def portfolio_id(self):
        """Gets the portfolio_id of this Allocation.  # noqa: E501


        :return: The portfolio_id of this Allocation.  # noqa: E501
        :rtype: lusid.ResourceId
        """
        return self._portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, portfolio_id):
        """Sets the portfolio_id of this Allocation.


        :param portfolio_id: The portfolio_id of this Allocation.  # noqa: E501
        :type portfolio_id: lusid.ResourceId
        """
        if self.local_vars_configuration.client_side_validation and portfolio_id is None:  # noqa: E501
            raise ValueError("Invalid value for `portfolio_id`, must not be `None`")  # noqa: E501

        self._portfolio_id = portfolio_id

    @property
    def quantity(self):
        """Gets the quantity of this Allocation.  # noqa: E501

        The quantity of given instrument allocated.  # noqa: E501

        :return: The quantity of this Allocation.  # noqa: E501
        :rtype: float
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this Allocation.

        The quantity of given instrument allocated.  # noqa: E501

        :param quantity: The quantity of this Allocation.  # noqa: E501
        :type quantity: float
        """
        if self.local_vars_configuration.client_side_validation and quantity is None:  # noqa: E501
            raise ValueError("Invalid value for `quantity`, must not be `None`")  # noqa: E501

        self._quantity = quantity

    @property
    def instrument_identifiers(self):
        """Gets the instrument_identifiers of this Allocation.  # noqa: E501

        The instrument allocated.  # noqa: E501

        :return: The instrument_identifiers of this Allocation.  # noqa: E501
        :rtype: dict(str, str)
        """
        return self._instrument_identifiers

    @instrument_identifiers.setter
    def instrument_identifiers(self, instrument_identifiers):
        """Sets the instrument_identifiers of this Allocation.

        The instrument allocated.  # noqa: E501

        :param instrument_identifiers: The instrument_identifiers of this Allocation.  # noqa: E501
        :type instrument_identifiers: dict(str, str)
        """
        if self.local_vars_configuration.client_side_validation and instrument_identifiers is None:  # noqa: E501
            raise ValueError("Invalid value for `instrument_identifiers`, must not be `None`")  # noqa: E501

        self._instrument_identifiers = instrument_identifiers

    @property
    def version(self):
        """Gets the version of this Allocation.  # noqa: E501


        :return: The version of this Allocation.  # noqa: E501
        :rtype: lusid.Version
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this Allocation.


        :param version: The version of this Allocation.  # noqa: E501
        :type version: lusid.Version
        """

        self._version = version

    @property
    def properties(self):
        """Gets the properties of this Allocation.  # noqa: E501

        Client-defined properties associated with this allocation.  # noqa: E501

        :return: The properties of this Allocation.  # noqa: E501
        :rtype: dict[str, lusid.PerpetualProperty]
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """Sets the properties of this Allocation.

        Client-defined properties associated with this allocation.  # noqa: E501

        :param properties: The properties of this Allocation.  # noqa: E501
        :type properties: dict[str, lusid.PerpetualProperty]
        """

        self._properties = properties

    @property
    def instrument_scope(self):
        """Gets the instrument_scope of this Allocation.  # noqa: E501

        The scope in which the instrument lies  # noqa: E501

        :return: The instrument_scope of this Allocation.  # noqa: E501
        :rtype: str
        """
        return self._instrument_scope

    @instrument_scope.setter
    def instrument_scope(self, instrument_scope):
        """Sets the instrument_scope of this Allocation.

        The scope in which the instrument lies  # noqa: E501

        :param instrument_scope: The instrument_scope of this Allocation.  # noqa: E501
        :type instrument_scope: str
        """

        self._instrument_scope = instrument_scope

    @property
    def lusid_instrument_id(self):
        """Gets the lusid_instrument_id of this Allocation.  # noqa: E501

        The LUSID instrument id for the instrument allocated.  # noqa: E501

        :return: The lusid_instrument_id of this Allocation.  # noqa: E501
        :rtype: str
        """
        return self._lusid_instrument_id

    @lusid_instrument_id.setter
    def lusid_instrument_id(self, lusid_instrument_id):
        """Sets the lusid_instrument_id of this Allocation.

        The LUSID instrument id for the instrument allocated.  # noqa: E501

        :param lusid_instrument_id: The lusid_instrument_id of this Allocation.  # noqa: E501
        :type lusid_instrument_id: str
        """
        if self.local_vars_configuration.client_side_validation and lusid_instrument_id is None:  # noqa: E501
            raise ValueError("Invalid value for `lusid_instrument_id`, must not be `None`")  # noqa: E501
        if (self.local_vars_configuration.client_side_validation and
                lusid_instrument_id is not None and len(lusid_instrument_id) < 1):
            raise ValueError("Invalid value for `lusid_instrument_id`, length must be greater than or equal to `1`")  # noqa: E501

        self._lusid_instrument_id = lusid_instrument_id

    @property
    def placement_ids(self):
        """Gets the placement_ids of this Allocation.  # noqa: E501

        A placement - also known as an order placed in the market - associated with this allocation.  # noqa: E501

        :return: The placement_ids of this Allocation.  # noqa: E501
        :rtype: list[lusid.ResourceId]
        """
        return self._placement_ids

    @placement_ids.setter
    def placement_ids(self, placement_ids):
        """Sets the placement_ids of this Allocation.

        A placement - also known as an order placed in the market - associated with this allocation.  # noqa: E501

        :param placement_ids: The placement_ids of this Allocation.  # noqa: E501
        :type placement_ids: list[lusid.ResourceId]
        """

        self._placement_ids = placement_ids

    @property
    def state(self):
        """Gets the state of this Allocation.  # noqa: E501

        The state of this allocation.  # noqa: E501

        :return: The state of this Allocation.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this Allocation.

        The state of this allocation.  # noqa: E501

        :param state: The state of this Allocation.  # noqa: E501
        :type state: str
        """

        self._state = state

    @property
    def side(self):
        """Gets the side of this Allocation.  # noqa: E501

        The side of this allocation (examples: Buy, Sell, ...).  # noqa: E501

        :return: The side of this Allocation.  # noqa: E501
        :rtype: str
        """
        return self._side

    @side.setter
    def side(self, side):
        """Sets the side of this Allocation.

        The side of this allocation (examples: Buy, Sell, ...).  # noqa: E501

        :param side: The side of this Allocation.  # noqa: E501
        :type side: str
        """

        self._side = side

    @property
    def type(self):
        """Gets the type of this Allocation.  # noqa: E501

        The type of order associated with this allocation (examples: Limit, Market, ...).  # noqa: E501

        :return: The type of this Allocation.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Allocation.

        The type of order associated with this allocation (examples: Limit, Market, ...).  # noqa: E501

        :param type: The type of this Allocation.  # noqa: E501
        :type type: str
        """

        self._type = type

    @property
    def settlement_date(self):
        """Gets the settlement_date of this Allocation.  # noqa: E501

        The settlement date for this allocation.  # noqa: E501

        :return: The settlement_date of this Allocation.  # noqa: E501
        :rtype: datetime
        """
        return self._settlement_date

    @settlement_date.setter
    def settlement_date(self, settlement_date):
        """Sets the settlement_date of this Allocation.

        The settlement date for this allocation.  # noqa: E501

        :param settlement_date: The settlement_date of this Allocation.  # noqa: E501
        :type settlement_date: datetime
        """

        self._settlement_date = settlement_date

    @property
    def date(self):
        """Gets the date of this Allocation.  # noqa: E501

        The date of this allocation.  # noqa: E501

        :return: The date of this Allocation.  # noqa: E501
        :rtype: datetime
        """
        return self._date

    @date.setter
    def date(self, date):
        """Sets the date of this Allocation.

        The date of this allocation.  # noqa: E501

        :param date: The date of this Allocation.  # noqa: E501
        :type date: datetime
        """

        self._date = date

    @property
    def price(self):
        """Gets the price of this Allocation.  # noqa: E501


        :return: The price of this Allocation.  # noqa: E501
        :rtype: lusid.CurrencyAndAmount
        """
        return self._price

    @price.setter
    def price(self, price):
        """Sets the price of this Allocation.


        :param price: The price of this Allocation.  # noqa: E501
        :type price: lusid.CurrencyAndAmount
        """

        self._price = price

    @property
    def settlement_currency(self):
        """Gets the settlement_currency of this Allocation.  # noqa: E501

        The settlement currency of this allocation.  # noqa: E501

        :return: The settlement_currency of this Allocation.  # noqa: E501
        :rtype: str
        """
        return self._settlement_currency

    @settlement_currency.setter
    def settlement_currency(self, settlement_currency):
        """Sets the settlement_currency of this Allocation.

        The settlement currency of this allocation.  # noqa: E501

        :param settlement_currency: The settlement_currency of this Allocation.  # noqa: E501
        :type settlement_currency: str
        """

        self._settlement_currency = settlement_currency

    @property
    def settlement_currency_fx_rate(self):
        """Gets the settlement_currency_fx_rate of this Allocation.  # noqa: E501

        The settlement currency to allocation currency FX rate.  # noqa: E501

        :return: The settlement_currency_fx_rate of this Allocation.  # noqa: E501
        :rtype: float
        """
        return self._settlement_currency_fx_rate

    @settlement_currency_fx_rate.setter
    def settlement_currency_fx_rate(self, settlement_currency_fx_rate):
        """Sets the settlement_currency_fx_rate of this Allocation.

        The settlement currency to allocation currency FX rate.  # noqa: E501

        :param settlement_currency_fx_rate: The settlement_currency_fx_rate of this Allocation.  # noqa: E501
        :type settlement_currency_fx_rate: float
        """

        self._settlement_currency_fx_rate = settlement_currency_fx_rate

    @property
    def counterparty(self):
        """Gets the counterparty of this Allocation.  # noqa: E501

        The counterparty for this allocation.  # noqa: E501

        :return: The counterparty of this Allocation.  # noqa: E501
        :rtype: str
        """
        return self._counterparty

    @counterparty.setter
    def counterparty(self, counterparty):
        """Sets the counterparty of this Allocation.

        The counterparty for this allocation.  # noqa: E501

        :param counterparty: The counterparty of this Allocation.  # noqa: E501
        :type counterparty: str
        """

        self._counterparty = counterparty

    @property
    def execution_ids(self):
        """Gets the execution_ids of this Allocation.  # noqa: E501

        The executions associated with this allocation  # noqa: E501

        :return: The execution_ids of this Allocation.  # noqa: E501
        :rtype: list[lusid.ResourceId]
        """
        return self._execution_ids

    @execution_ids.setter
    def execution_ids(self, execution_ids):
        """Sets the execution_ids of this Allocation.

        The executions associated with this allocation  # noqa: E501

        :param execution_ids: The execution_ids of this Allocation.  # noqa: E501
        :type execution_ids: list[lusid.ResourceId]
        """

        self._execution_ids = execution_ids

    @property
    def links(self):
        """Gets the links of this Allocation.  # noqa: E501


        :return: The links of this Allocation.  # noqa: E501
        :rtype: list[lusid.Link]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this Allocation.


        :param links: The links of this Allocation.  # noqa: E501
        :type links: list[lusid.Link]
        """

        self._links = links

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Allocation):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, Allocation):
            return True

        return self.to_dict() != other.to_dict()
