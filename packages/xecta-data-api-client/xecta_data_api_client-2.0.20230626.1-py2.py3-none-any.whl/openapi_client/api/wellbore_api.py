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
from openapi_client.model.wellbore import Wellbore
from openapi_client.model.wellbore_input import WellboreInput


class WellboreApi(object):
    """NOTE: This class is auto generated by OpenAPI Generator
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    def __init__(self, api_client=None):
        if api_client is None:
            api_client = ApiClient()
        self.api_client = api_client

        def __delete_wellbore_by_source(
            self,
            source_well_id,
            source_wellbore_id,
            **kwargs
        ):
            """Delete a single wellbore  # noqa: E501

            This operation will delete a single wellbore by its uwi and wellbore index.              This operation will also cascade delete all dependent wellbore entities that have been added             to the system.               # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.delete_wellbore_by_source(source_well_id, source_wellbore_id, async_req=True)
            >>> result = thread.get()

            Args:
                source_well_id (str):
                source_wellbore_id (str):

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
            kwargs['source_well_id'] = \
                source_well_id
            kwargs['source_wellbore_id'] = \
                source_wellbore_id
            return self.call_with_http_info(**kwargs)

        self.delete_wellbore_by_source = Endpoint(
            settings={
                'response_type': (int,),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/well/{sourceWellId}/wellbore/{sourceWellboreId}',
                'operation_id': 'delete_wellbore_by_source',
                'http_method': 'DELETE',
                'servers': None,
            },
            params_map={
                'all': [
                    'source_well_id',
                    'source_wellbore_id',
                ],
                'required': [
                    'source_well_id',
                    'source_wellbore_id',
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
                    'source_wellbore_id':
                        (str,),
                },
                'attribute_map': {
                    'source_well_id': 'sourceWellId',
                    'source_wellbore_id': 'sourceWellboreId',
                },
                'location_map': {
                    'source_well_id': 'path',
                    'source_wellbore_id': 'path',
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
            callable=__delete_wellbore_by_source
        )

        def __delete_wellbore_by_source_well(
            self,
            source_well_id,
            **kwargs
        ):
            """Delete a single wellbore  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.delete_wellbore_by_source_well(source_well_id, async_req=True)
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
            kwargs['source_well_id'] = \
                source_well_id
            return self.call_with_http_info(**kwargs)

        self.delete_wellbore_by_source_well = Endpoint(
            settings={
                'response_type': (int,),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/well/{sourceWellId}/wellbore',
                'operation_id': 'delete_wellbore_by_source_well',
                'http_method': 'DELETE',
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
            callable=__delete_wellbore_by_source_well
        )

        def __get_wellbor_by_source(
            self,
            source_well_id,
            source_wellbore_id,
            **kwargs
        ):
            """Get wellbores by wellbore source id  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_wellbor_by_source(source_well_id, source_wellbore_id, async_req=True)
            >>> result = thread.get()

            Args:
                source_well_id (str):
                source_wellbore_id (str):

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
                Wellbore
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
            kwargs['source_wellbore_id'] = \
                source_wellbore_id
            return self.call_with_http_info(**kwargs)

        self.get_wellbor_by_source = Endpoint(
            settings={
                'response_type': (Wellbore,),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/well/{sourceWellId}/wellbore/{sourceWellboreId}',
                'operation_id': 'get_wellbor_by_source',
                'http_method': 'GET',
                'servers': None,
            },
            params_map={
                'all': [
                    'source_well_id',
                    'source_wellbore_id',
                ],
                'required': [
                    'source_well_id',
                    'source_wellbore_id',
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
                    'source_wellbore_id':
                        (str,),
                },
                'attribute_map': {
                    'source_well_id': 'sourceWellId',
                    'source_wellbore_id': 'sourceWellboreId',
                },
                'location_map': {
                    'source_well_id': 'path',
                    'source_wellbore_id': 'path',
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
            callable=__get_wellbor_by_source
        )

        def __get_wellbores_by_source_well(
            self,
            source_well_id,
            **kwargs
        ):
            """Get wellbores by well source id  # noqa: E501

            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.get_wellbores_by_source_well(source_well_id, async_req=True)
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
                [Wellbore]
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

        self.get_wellbores_by_source_well = Endpoint(
            settings={
                'response_type': ([Wellbore],),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/well/{sourceWellId}/wellbore',
                'operation_id': 'get_wellbores_by_source_well',
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
            callable=__get_wellbores_by_source_well
        )

        def __upsert_wellbores(
            self,
            wellbore_input,
            **kwargs
        ):
            """Bulk Add / Update Wellbore Data  # noqa: E501

            This operation will add or update multiple wellbores using batching for efficiency  # noqa: E501
            This method makes a synchronous HTTP request by default. To make an
            asynchronous HTTP request, please pass async_req=True

            >>> thread = api.upsert_wellbores(wellbore_input, async_req=True)
            >>> result = thread.get()

            Args:
                wellbore_input ([WellboreInput]):

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
                [Wellbore]
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
            kwargs['wellbore_input'] = \
                wellbore_input
            return self.call_with_http_info(**kwargs)

        self.upsert_wellbores = Endpoint(
            settings={
                'response_type': ([Wellbore],),
                'auth': [
                    'bearerAuth'
                ],
                'endpoint_path': '/api/production/wellbore',
                'operation_id': 'upsert_wellbores',
                'http_method': 'POST',
                'servers': None,
            },
            params_map={
                'all': [
                    'wellbore_input',
                ],
                'required': [
                    'wellbore_input',
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
                    'wellbore_input':
                        ([WellboreInput],),
                },
                'attribute_map': {
                },
                'location_map': {
                    'wellbore_input': 'body',
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
            callable=__upsert_wellbores
        )
