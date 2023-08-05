"""
    Production API

    API exposing endpoints for managing well  and daily production.  # noqa: E501

    The version of the OpenAPI document: 1.0
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

import nulltype  # noqa: F401

from openapi_client.model_utils import (  # noqa: F401
    ApiTypeError,
    ModelComposed,
    ModelNormal,
    ModelSimple,
    cached_property,
    change_keys_js_to_python,
    convert_js_args_to_python_args,
    date,
    datetime,
    file_type,
    none_type,
    validate_get_composed_info,
)


class GasLiftValveInput(ModelNormal):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.

    Attributes:
      allowed_values (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          with a capitalized key describing the allowed value and an allowed
          value. These dicts store the allowed enum values.
      attribute_map (dict): The key is attribute name
          and the value is json key in definition.
      discriminator_value_class_map (dict): A dict to go from the discriminator
          variable value to the discriminator class name.
      validations (dict): The key is the tuple path to the attribute
          and the for var_name this is (var_name,). The value is a dict
          that stores validations for max_length, min_length, max_items,
          min_items, exclusive_maximum, inclusive_maximum, exclusive_minimum,
          inclusive_minimum, and regex.
      additional_properties_type (tuple): A tuple of classes accepted
          as additional properties values.
    """

    allowed_values = {
    }

    validations = {
    }

    additional_properties_type = None

    _nullable = False

    @cached_property
    def openapi_types():
        """
        This must be a method because a model may have properties that are
        of type self, this must run after the class is loaded

        Returns
            openapi_types (dict): The key is attribute name
                and the value is attribute type.
        """
        return {
            'source_well_id': (str,),  # noqa: E501
            'source_wellbore_id': (str,),  # noqa: E501
            'source_tubing_id': (str,),  # noqa: E501
            'source_id': (str,),  # noqa: E501
            'source_mandrel_id': (str,),  # noqa: E501
            'run_date': (datetime,),  # noqa: E501
            'install_md': (float,),  # noqa: E501
            'surface_open_pressure': (float,),  # noqa: E501
            'surface_close_pressure': (float,),  # noqa: E501
            'port_size': (float,),  # noqa: E501
            'pull_date': (datetime, none_type,),  # noqa: E501
            'glv_station': (int, none_type,),  # noqa: E501
            'test_rack_open_pressure': (float, none_type,),  # noqa: E501
        }

    @cached_property
    def discriminator():
        return None


    attribute_map = {
        'source_well_id': 'sourceWellId',  # noqa: E501
        'source_wellbore_id': 'sourceWellboreId',  # noqa: E501
        'source_tubing_id': 'sourceTubingId',  # noqa: E501
        'source_id': 'sourceId',  # noqa: E501
        'source_mandrel_id': 'sourceMandrelId',  # noqa: E501
        'run_date': 'runDate',  # noqa: E501
        'install_md': 'installMd',  # noqa: E501
        'surface_open_pressure': 'surfaceOpenPressure',  # noqa: E501
        'surface_close_pressure': 'surfaceClosePressure',  # noqa: E501
        'port_size': 'portSize',  # noqa: E501
        'pull_date': 'pullDate',  # noqa: E501
        'glv_station': 'glvStation',  # noqa: E501
        'test_rack_open_pressure': 'testRackOpenPressure',  # noqa: E501
    }

    _composed_schemas = {}

    required_properties = set([
        '_data_store',
        '_check_type',
        '_spec_property_naming',
        '_path_to_item',
        '_configuration',
        '_visited_composed_classes',
    ])

    @convert_js_args_to_python_args
    def __init__(self, source_well_id, source_wellbore_id, source_tubing_id, source_id, source_mandrel_id, run_date, install_md, surface_open_pressure, surface_close_pressure, port_size, *args, **kwargs):  # noqa: E501
        """GasLiftValveInput - a model defined in OpenAPI

        Args:
            source_well_id (str):
            source_wellbore_id (str):
            source_tubing_id (str):
            source_id (str):
            source_mandrel_id (str):
            run_date (datetime):
            install_md (float):
            surface_open_pressure (float):
            surface_close_pressure (float):
            port_size (float):

        Keyword Args:
            _check_type (bool): if True, values for parameters in openapi_types
                                will be type checked and a TypeError will be
                                raised if the wrong type is input.
                                Defaults to True
            _path_to_item (tuple/list): This is a list of keys or values to
                                drill down to the model in received_data
                                when deserializing a response
            _spec_property_naming (bool): True if the variable names in the input data
                                are serialized names, as specified in the OpenAPI document.
                                False if the variable names in the input data
                                are pythonic names, e.g. snake case (default)
            _configuration (Configuration): the instance to use when
                                deserializing a file_type parameter.
                                If passed, type conversion is attempted
                                If omitted no type conversion is done.
            _visited_composed_classes (tuple): This stores a tuple of
                                classes that we have traveled through so that
                                if we see that class again we will not use its
                                discriminator again.
                                When traveling through a discriminator, the
                                composed schema that is
                                is traveled through is added to this set.
                                For example if Animal has a discriminator
                                petType and we pass in "Dog", and the class Dog
                                allOf includes Animal, we move through Animal
                                once using the discriminator, and pick Dog.
                                Then in Dog, we will make an instance of the
                                Animal class but this time we won't travel
                                through its discriminator because we passed in
                                _visited_composed_classes = (Animal,)
            pull_date (datetime, none_type): [optional]  # noqa: E501
            glv_station (int, none_type): [optional]  # noqa: E501
            test_rack_open_pressure (float, none_type): [optional]  # noqa: E501
        """

        _check_type = kwargs.pop('_check_type', True)
        _spec_property_naming = kwargs.pop('_spec_property_naming', False)
        _path_to_item = kwargs.pop('_path_to_item', ())
        _configuration = kwargs.pop('_configuration', None)
        _visited_composed_classes = kwargs.pop('_visited_composed_classes', ())

        if args:
            raise ApiTypeError(
                "Invalid positional arguments=%s passed to %s. Remove those invalid positional arguments." % (
                    args,
                    self.__class__.__name__,
                ),
                path_to_item=_path_to_item,
                valid_classes=(self.__class__,),
            )

        self._data_store = {}
        self._check_type = _check_type
        self._spec_property_naming = _spec_property_naming
        self._path_to_item = _path_to_item
        self._configuration = _configuration
        self._visited_composed_classes = _visited_composed_classes + (self.__class__,)

        self.source_well_id = source_well_id
        self.source_wellbore_id = source_wellbore_id
        self.source_tubing_id = source_tubing_id
        self.source_id = source_id
        self.source_mandrel_id = source_mandrel_id
        self.run_date = run_date
        self.install_md = install_md
        self.surface_open_pressure = surface_open_pressure
        self.surface_close_pressure = surface_close_pressure
        self.port_size = port_size
        for var_name, var_value in kwargs.items():
            if var_name not in self.attribute_map and \
                        self._configuration is not None and \
                        self._configuration.discard_unknown_keys and \
                        self.additional_properties_type is None:
                # discard variable.
                continue
            setattr(self, var_name, var_value)
