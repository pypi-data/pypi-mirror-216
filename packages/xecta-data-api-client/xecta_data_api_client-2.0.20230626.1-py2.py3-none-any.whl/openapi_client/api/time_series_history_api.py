"""
    Production API

    API exposing endpoints for managing well  and daily production.  # noqa: E501

    The version of the OpenAPI document: 1.0
    Generated by: https://openapi-generator.tech
"""


import re  # noqa: F401
import sys  # noqa: F401

from openapi_client.api_client import ApiClient, Endpoint
from openapi_client.model_utils import (  # noqa: F401
    check_allowed_values,
    check_validations,
    date,
    datetime,
    file_type,
    none_type,
    validate_and_convert_types
)
from openapi_client.model.time_series_history import TimeSeriesHistory
from openapi_client.model.time_series_history_input import TimeSeriesHistoryInput


class TimeSeriesHistoryApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        def __get_time_series_history_by_well(
            self,
            source_well_id,
            **kwargs
        ):
            """Get time series configuration by well source id  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_time_series_history_by_well(source_well_id, async_req=True)
            >>> result = thread.get()

            Args:
                source_well_id (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                [TimeSeriesHistory]
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['source_well_id'] = \
                source_well_id
            return self.call_with_http_info(**kwargs)

        self.get_time_series_history_by_well = Endpoint(
            settings={
                'response_type': ([TimeSeriesHistory],),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/well/{sourceWellId}/ts',
                'operation_id': 'get_time_series_history_by_well',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'source_well_id',
                ],
                'required': [
                    'source_well_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'source_well_id':
                        (str,),
                },
                'attribute_map': {
                    'source_well_id': 'sourceWellId',
                },
                'location_map': {
                    'source_well_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json',
                    'application/x-ndjson'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__get_time_series_history_by_well
        )

        def __get_time_series_history_by_well1(
            self,
            source_well_id,
            source_time_series_id,
            **kwargs
        ):
            """Get time series configuration by well source id  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_time_series_history_by_well1(source_well_id, source_time_series_id, async_req=True)
            >>> result = thread.get()

            Args:
                source_well_id (str):
                source_time_series_id (str):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                [TimeSeriesHistory]
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['source_well_id'] = \
                source_well_id
            kwargs['source_time_series_id'] = \
                source_time_series_id
            return self.call_with_http_info(**kwargs)

        self.get_time_series_history_by_well1 = Endpoint(
            settings={
                'response_type': ([TimeSeriesHistory],),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/well/{sourceWellId}/timeseries/{sourceTimeSeriesId}/ts',
                'operation_id': 'get_time_series_history_by_well1',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'source_well_id',
                    'source_time_series_id',
                ],
                'required': [
                    'source_well_id',
                    'source_time_series_id',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'source_well_id':
                        (str,),
                    'source_time_series_id':
                        (str,),
                },
                'attribute_map': {
                    'source_well_id': 'sourceWellId',
                    'source_time_series_id': 'sourceTimeSeriesId',
                },
                'location_map': {
                    'source_well_id': 'path',
                    'source_time_series_id': 'path',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json',
                    'application/x-ndjson'
                ],
                'content_type': [],
            },
            api_client=api_client,
            callable=__get_time_series_history_by_well1
        )

        def __upsert_time_series_history(
            self,
            time_series_history_input,
            **kwargs
        ):
            """Bulk Add / Update Time Series Data  # noqa: E501

            This operation will add or update multiple time series records using batching for efficiency  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.upsert_time_series_history(time_series_history_input, async_req=True)
            >>> result = thread.get()

            Args:
                time_series_history_input ([TimeSeriesHistoryInput]):

            Keyword Args:
                _return_http_data_only (bool): response data without head status
                    code and headers. Default is True.
                _preload_content (bool): if False, the urllib3.HTTPResponse object
                    will be returned without reading/decoding response data.
                    Default is True.
                _request_timeout (float/tuple): timeout setting for this request. If one
                    number provided, it will be total request timeout. It can also
                    be a pair (tuple) of (connection, read) timeouts.
                    Default is None.
                _check_input_type (bool): specifies if type checking
                    should be done one the data sent to the server.
                    Default is True.
                _check_return_type (bool): specifies if type checking
                    should be done one the data received from the server.
                    Default is True.
                _host_index (int/None): specifies the index of the server
                    that we want to use.
                    Default is read from the configuration.
                async_req (bool): execute request asynchronously

            Returns:
                int
                    If the method is called asynchronously, returns the request
                    thread.
            """
            kwargs['async_req'] = kwargs.get(
                'async_req', False
            )
            kwargs['_return_http_data_only'] = kwargs.get(
                '_return_http_data_only', True
            )
            kwargs['_preload_content'] = kwargs.get(
                '_preload_content', True
            )
            kwargs['_request_timeout'] = kwargs.get(
                '_request_timeout', None
            )
            kwargs['_check_input_type'] = kwargs.get(
                '_check_input_type', True
            )
            kwargs['_check_return_type'] = kwargs.get(
                '_check_return_type', True
            )
            kwargs['_host_index'] = kwargs.get('_host_index')
            kwargs['time_series_history_input'] = \
                time_series_history_input
            return self.call_with_http_info(**kwargs)

        self.upsert_time_series_history = Endpoint(
            settings={
                'response_type': (int,),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/ts',
                'operation_id': 'upsert_time_series_history',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'time_series_history_input',
                ],
                'required': [
                    'time_series_history_input',
                ],
                'nullable': [
                ],
                'enum': [
                ],
                'validation': [
                ]
            },
            root_map={
                'validations': {
                },
                'allowed_values': {
                },
                'openapi_types': {
                    'time_series_history_input':
                        ([TimeSeriesHistoryInput],),
                },
                'attribute_map': {
                },
                'location_map': {
                    'time_series_history_input': 'body',
                },
                'collection_format_map': {
                }
            },
            headers_map={
                'accept': [
                    'application/json',
                    'application/x-ndjson'
                ],
                'content_type': [
                    'application/json'
                ]
            },
            api_client=api_client,
            callable=__upsert_time_series_history
        )
