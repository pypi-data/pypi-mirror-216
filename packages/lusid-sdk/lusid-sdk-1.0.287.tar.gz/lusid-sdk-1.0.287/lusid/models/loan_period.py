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


class LoanPeriod(object):
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
        'payment_date': 'datetime',
        'notional': 'float',
        'interest_amount': 'float'
    }

    attribute_map = {
        'payment_date': 'paymentDate',
        'notional': 'notional',
        'interest_amount': 'interestAmount'
    }

    required_map = {
        'payment_date': 'required',
        'notional': 'required',
        'interest_amount': 'required'
    }

    def __init__(self, payment_date=None, notional=None, interest_amount=None, local_vars_configuration=None):  # noqa: E501
        """LoanPeriod - a model defined in OpenAPI"
        
        :param payment_date:  (required)
        :type payment_date: datetime
        :param notional:  (required)
        :type notional: float
        :param interest_amount:  (required)
        :type interest_amount: float

        """  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._payment_date = None
        self._notional = None
        self._interest_amount = None
        self.discriminator = None

        self.payment_date = payment_date
        self.notional = notional
        self.interest_amount = interest_amount

    @property
    def payment_date(self):
        """Gets the payment_date of this LoanPeriod.  # noqa: E501


        :return: The payment_date of this LoanPeriod.  # noqa: E501
        :rtype: datetime
        """
        return self._payment_date

    @payment_date.setter
    def payment_date(self, payment_date):
        """Sets the payment_date of this LoanPeriod.


        :param payment_date: The payment_date of this LoanPeriod.  # noqa: E501
        :type payment_date: datetime
        """
        if self.local_vars_configuration.client_side_validation and payment_date is None:  # noqa: E501
            raise ValueError("Invalid value for `payment_date`, must not be `None`")  # noqa: E501

        self._payment_date = payment_date

    @property
    def notional(self):
        """Gets the notional of this LoanPeriod.  # noqa: E501


        :return: The notional of this LoanPeriod.  # noqa: E501
        :rtype: float
        """
        return self._notional

    @notional.setter
    def notional(self, notional):
        """Sets the notional of this LoanPeriod.


        :param notional: The notional of this LoanPeriod.  # noqa: E501
        :type notional: float
        """
        if self.local_vars_configuration.client_side_validation and notional is None:  # noqa: E501
            raise ValueError("Invalid value for `notional`, must not be `None`")  # noqa: E501

        self._notional = notional

    @property
    def interest_amount(self):
        """Gets the interest_amount of this LoanPeriod.  # noqa: E501


        :return: The interest_amount of this LoanPeriod.  # noqa: E501
        :rtype: float
        """
        return self._interest_amount

    @interest_amount.setter
    def interest_amount(self, interest_amount):
        """Sets the interest_amount of this LoanPeriod.


        :param interest_amount: The interest_amount of this LoanPeriod.  # noqa: E501
        :type interest_amount: float
        """
        if self.local_vars_configuration.client_side_validation and interest_amount is None:  # noqa: E501
            raise ValueError("Invalid value for `interest_amount`, must not be `None`")  # noqa: E501

        self._interest_amount = interest_amount

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
        if not isinstance(other, LoanPeriod):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, LoanPeriod):
            return True

        return self.to_dict() != other.to_dict()
