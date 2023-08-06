"""
Type annotations for privatenetworks service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_privatenetworks/type_defs/)

Usage::

    ```python
    from types_aiobotocore_privatenetworks.type_defs import AcknowledgeOrderReceiptRequestRequestTypeDef

    data: AcknowledgeOrderReceiptRequestRequestTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    AcknowledgmentStatusType,
    DeviceIdentifierFilterKeysType,
    DeviceIdentifierStatusType,
    ElevationReferenceType,
    HealthStatusType,
    NetworkResourceDefinitionTypeType,
    NetworkResourceFilterKeysType,
    NetworkResourceStatusType,
    NetworkSiteStatusType,
    NetworkStatusType,
    OrderFilterKeysType,
    UpdateTypeType,
)

if sys.version_info >= (3, 9):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AcknowledgeOrderReceiptRequestRequestTypeDef",
    "ActivateDeviceIdentifierRequestRequestTypeDef",
    "DeviceIdentifierTypeDef",
    "AddressTypeDef",
    "PositionTypeDef",
    "CreateNetworkRequestRequestTypeDef",
    "NetworkTypeDef",
    "DeactivateDeviceIdentifierRequestRequestTypeDef",
    "DeleteNetworkRequestRequestTypeDef",
    "DeleteNetworkSiteRequestRequestTypeDef",
    "GetDeviceIdentifierRequestRequestTypeDef",
    "GetNetworkRequestRequestTypeDef",
    "GetNetworkResourceRequestRequestTypeDef",
    "GetNetworkSiteRequestRequestTypeDef",
    "GetOrderRequestRequestTypeDef",
    "ListDeviceIdentifiersRequestListDeviceIdentifiersPaginateTypeDef",
    "ListDeviceIdentifiersRequestRequestTypeDef",
    "ListNetworkResourcesRequestListNetworkResourcesPaginateTypeDef",
    "ListNetworkResourcesRequestRequestTypeDef",
    "ListNetworkSitesRequestListNetworkSitesPaginateTypeDef",
    "ListNetworkSitesRequestRequestTypeDef",
    "ListNetworksRequestListNetworksPaginateTypeDef",
    "ListNetworksRequestRequestTypeDef",
    "ListOrdersRequestListOrdersPaginateTypeDef",
    "ListOrdersRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "NameValuePairTypeDef",
    "TrackingInformationTypeDef",
    "PaginatorConfigTypeDef",
    "PingResponseTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateNetworkSiteRequestRequestTypeDef",
    "ActivateDeviceIdentifierResponseTypeDef",
    "DeactivateDeviceIdentifierResponseTypeDef",
    "GetDeviceIdentifierResponseTypeDef",
    "ListDeviceIdentifiersResponseTypeDef",
    "ActivateNetworkSiteRequestRequestTypeDef",
    "ReturnInformationTypeDef",
    "StartNetworkResourceUpdateRequestRequestTypeDef",
    "ConfigureAccessPointRequestRequestTypeDef",
    "CreateNetworkResponseTypeDef",
    "DeleteNetworkResponseTypeDef",
    "GetNetworkResponseTypeDef",
    "ListNetworksResponseTypeDef",
    "NetworkResourceDefinitionTypeDef",
    "OrderTypeDef",
    "NetworkResourceTypeDef",
    "SitePlanTypeDef",
    "AcknowledgeOrderReceiptResponseTypeDef",
    "GetOrderResponseTypeDef",
    "ListOrdersResponseTypeDef",
    "ConfigureAccessPointResponseTypeDef",
    "GetNetworkResourceResponseTypeDef",
    "ListNetworkResourcesResponseTypeDef",
    "StartNetworkResourceUpdateResponseTypeDef",
    "CreateNetworkSiteRequestRequestTypeDef",
    "NetworkSiteTypeDef",
    "UpdateNetworkSitePlanRequestRequestTypeDef",
    "ActivateNetworkSiteResponseTypeDef",
    "CreateNetworkSiteResponseTypeDef",
    "DeleteNetworkSiteResponseTypeDef",
    "GetNetworkSiteResponseTypeDef",
    "ListNetworkSitesResponseTypeDef",
    "UpdateNetworkSiteResponseTypeDef",
)

AcknowledgeOrderReceiptRequestRequestTypeDef = TypedDict(
    "AcknowledgeOrderReceiptRequestRequestTypeDef",
    {
        "orderArn": str,
    },
)

_RequiredActivateDeviceIdentifierRequestRequestTypeDef = TypedDict(
    "_RequiredActivateDeviceIdentifierRequestRequestTypeDef",
    {
        "deviceIdentifierArn": str,
    },
)
_OptionalActivateDeviceIdentifierRequestRequestTypeDef = TypedDict(
    "_OptionalActivateDeviceIdentifierRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class ActivateDeviceIdentifierRequestRequestTypeDef(
    _RequiredActivateDeviceIdentifierRequestRequestTypeDef,
    _OptionalActivateDeviceIdentifierRequestRequestTypeDef,
):
    pass

DeviceIdentifierTypeDef = TypedDict(
    "DeviceIdentifierTypeDef",
    {
        "createdAt": datetime,
        "deviceIdentifierArn": str,
        "iccid": str,
        "imsi": str,
        "networkArn": str,
        "orderArn": str,
        "status": DeviceIdentifierStatusType,
        "trafficGroupArn": str,
        "vendor": str,
    },
    total=False,
)

_RequiredAddressTypeDef = TypedDict(
    "_RequiredAddressTypeDef",
    {
        "city": str,
        "country": str,
        "name": str,
        "postalCode": str,
        "stateOrProvince": str,
        "street1": str,
    },
)
_OptionalAddressTypeDef = TypedDict(
    "_OptionalAddressTypeDef",
    {
        "company": str,
        "phoneNumber": str,
        "street2": str,
        "street3": str,
    },
    total=False,
)

class AddressTypeDef(_RequiredAddressTypeDef, _OptionalAddressTypeDef):
    pass

PositionTypeDef = TypedDict(
    "PositionTypeDef",
    {
        "elevation": float,
        "elevationReference": ElevationReferenceType,
        "elevationUnit": Literal["FEET"],
        "latitude": float,
        "longitude": float,
    },
    total=False,
)

_RequiredCreateNetworkRequestRequestTypeDef = TypedDict(
    "_RequiredCreateNetworkRequestRequestTypeDef",
    {
        "networkName": str,
    },
)
_OptionalCreateNetworkRequestRequestTypeDef = TypedDict(
    "_OptionalCreateNetworkRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateNetworkRequestRequestTypeDef(
    _RequiredCreateNetworkRequestRequestTypeDef, _OptionalCreateNetworkRequestRequestTypeDef
):
    pass

_RequiredNetworkTypeDef = TypedDict(
    "_RequiredNetworkTypeDef",
    {
        "networkArn": str,
        "networkName": str,
        "status": NetworkStatusType,
    },
)
_OptionalNetworkTypeDef = TypedDict(
    "_OptionalNetworkTypeDef",
    {
        "createdAt": datetime,
        "description": str,
        "statusReason": str,
    },
    total=False,
)

class NetworkTypeDef(_RequiredNetworkTypeDef, _OptionalNetworkTypeDef):
    pass

_RequiredDeactivateDeviceIdentifierRequestRequestTypeDef = TypedDict(
    "_RequiredDeactivateDeviceIdentifierRequestRequestTypeDef",
    {
        "deviceIdentifierArn": str,
    },
)
_OptionalDeactivateDeviceIdentifierRequestRequestTypeDef = TypedDict(
    "_OptionalDeactivateDeviceIdentifierRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class DeactivateDeviceIdentifierRequestRequestTypeDef(
    _RequiredDeactivateDeviceIdentifierRequestRequestTypeDef,
    _OptionalDeactivateDeviceIdentifierRequestRequestTypeDef,
):
    pass

_RequiredDeleteNetworkRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteNetworkRequestRequestTypeDef",
    {
        "networkArn": str,
    },
)
_OptionalDeleteNetworkRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteNetworkRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class DeleteNetworkRequestRequestTypeDef(
    _RequiredDeleteNetworkRequestRequestTypeDef, _OptionalDeleteNetworkRequestRequestTypeDef
):
    pass

_RequiredDeleteNetworkSiteRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteNetworkSiteRequestRequestTypeDef",
    {
        "networkSiteArn": str,
    },
)
_OptionalDeleteNetworkSiteRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteNetworkSiteRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class DeleteNetworkSiteRequestRequestTypeDef(
    _RequiredDeleteNetworkSiteRequestRequestTypeDef, _OptionalDeleteNetworkSiteRequestRequestTypeDef
):
    pass

GetDeviceIdentifierRequestRequestTypeDef = TypedDict(
    "GetDeviceIdentifierRequestRequestTypeDef",
    {
        "deviceIdentifierArn": str,
    },
)

GetNetworkRequestRequestTypeDef = TypedDict(
    "GetNetworkRequestRequestTypeDef",
    {
        "networkArn": str,
    },
)

GetNetworkResourceRequestRequestTypeDef = TypedDict(
    "GetNetworkResourceRequestRequestTypeDef",
    {
        "networkResourceArn": str,
    },
)

GetNetworkSiteRequestRequestTypeDef = TypedDict(
    "GetNetworkSiteRequestRequestTypeDef",
    {
        "networkSiteArn": str,
    },
)

GetOrderRequestRequestTypeDef = TypedDict(
    "GetOrderRequestRequestTypeDef",
    {
        "orderArn": str,
    },
)

_RequiredListDeviceIdentifiersRequestListDeviceIdentifiersPaginateTypeDef = TypedDict(
    "_RequiredListDeviceIdentifiersRequestListDeviceIdentifiersPaginateTypeDef",
    {
        "networkArn": str,
    },
)
_OptionalListDeviceIdentifiersRequestListDeviceIdentifiersPaginateTypeDef = TypedDict(
    "_OptionalListDeviceIdentifiersRequestListDeviceIdentifiersPaginateTypeDef",
    {
        "filters": Mapping[DeviceIdentifierFilterKeysType, Sequence[str]],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListDeviceIdentifiersRequestListDeviceIdentifiersPaginateTypeDef(
    _RequiredListDeviceIdentifiersRequestListDeviceIdentifiersPaginateTypeDef,
    _OptionalListDeviceIdentifiersRequestListDeviceIdentifiersPaginateTypeDef,
):
    pass

_RequiredListDeviceIdentifiersRequestRequestTypeDef = TypedDict(
    "_RequiredListDeviceIdentifiersRequestRequestTypeDef",
    {
        "networkArn": str,
    },
)
_OptionalListDeviceIdentifiersRequestRequestTypeDef = TypedDict(
    "_OptionalListDeviceIdentifiersRequestRequestTypeDef",
    {
        "filters": Mapping[DeviceIdentifierFilterKeysType, Sequence[str]],
        "maxResults": int,
        "startToken": str,
    },
    total=False,
)

class ListDeviceIdentifiersRequestRequestTypeDef(
    _RequiredListDeviceIdentifiersRequestRequestTypeDef,
    _OptionalListDeviceIdentifiersRequestRequestTypeDef,
):
    pass

_RequiredListNetworkResourcesRequestListNetworkResourcesPaginateTypeDef = TypedDict(
    "_RequiredListNetworkResourcesRequestListNetworkResourcesPaginateTypeDef",
    {
        "networkArn": str,
    },
)
_OptionalListNetworkResourcesRequestListNetworkResourcesPaginateTypeDef = TypedDict(
    "_OptionalListNetworkResourcesRequestListNetworkResourcesPaginateTypeDef",
    {
        "filters": Mapping[NetworkResourceFilterKeysType, Sequence[str]],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListNetworkResourcesRequestListNetworkResourcesPaginateTypeDef(
    _RequiredListNetworkResourcesRequestListNetworkResourcesPaginateTypeDef,
    _OptionalListNetworkResourcesRequestListNetworkResourcesPaginateTypeDef,
):
    pass

_RequiredListNetworkResourcesRequestRequestTypeDef = TypedDict(
    "_RequiredListNetworkResourcesRequestRequestTypeDef",
    {
        "networkArn": str,
    },
)
_OptionalListNetworkResourcesRequestRequestTypeDef = TypedDict(
    "_OptionalListNetworkResourcesRequestRequestTypeDef",
    {
        "filters": Mapping[NetworkResourceFilterKeysType, Sequence[str]],
        "maxResults": int,
        "startToken": str,
    },
    total=False,
)

class ListNetworkResourcesRequestRequestTypeDef(
    _RequiredListNetworkResourcesRequestRequestTypeDef,
    _OptionalListNetworkResourcesRequestRequestTypeDef,
):
    pass

_RequiredListNetworkSitesRequestListNetworkSitesPaginateTypeDef = TypedDict(
    "_RequiredListNetworkSitesRequestListNetworkSitesPaginateTypeDef",
    {
        "networkArn": str,
    },
)
_OptionalListNetworkSitesRequestListNetworkSitesPaginateTypeDef = TypedDict(
    "_OptionalListNetworkSitesRequestListNetworkSitesPaginateTypeDef",
    {
        "filters": Mapping[Literal["STATUS"], Sequence[str]],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListNetworkSitesRequestListNetworkSitesPaginateTypeDef(
    _RequiredListNetworkSitesRequestListNetworkSitesPaginateTypeDef,
    _OptionalListNetworkSitesRequestListNetworkSitesPaginateTypeDef,
):
    pass

_RequiredListNetworkSitesRequestRequestTypeDef = TypedDict(
    "_RequiredListNetworkSitesRequestRequestTypeDef",
    {
        "networkArn": str,
    },
)
_OptionalListNetworkSitesRequestRequestTypeDef = TypedDict(
    "_OptionalListNetworkSitesRequestRequestTypeDef",
    {
        "filters": Mapping[Literal["STATUS"], Sequence[str]],
        "maxResults": int,
        "startToken": str,
    },
    total=False,
)

class ListNetworkSitesRequestRequestTypeDef(
    _RequiredListNetworkSitesRequestRequestTypeDef, _OptionalListNetworkSitesRequestRequestTypeDef
):
    pass

ListNetworksRequestListNetworksPaginateTypeDef = TypedDict(
    "ListNetworksRequestListNetworksPaginateTypeDef",
    {
        "filters": Mapping[Literal["STATUS"], Sequence[str]],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListNetworksRequestRequestTypeDef = TypedDict(
    "ListNetworksRequestRequestTypeDef",
    {
        "filters": Mapping[Literal["STATUS"], Sequence[str]],
        "maxResults": int,
        "startToken": str,
    },
    total=False,
)

_RequiredListOrdersRequestListOrdersPaginateTypeDef = TypedDict(
    "_RequiredListOrdersRequestListOrdersPaginateTypeDef",
    {
        "networkArn": str,
    },
)
_OptionalListOrdersRequestListOrdersPaginateTypeDef = TypedDict(
    "_OptionalListOrdersRequestListOrdersPaginateTypeDef",
    {
        "filters": Mapping[OrderFilterKeysType, Sequence[str]],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListOrdersRequestListOrdersPaginateTypeDef(
    _RequiredListOrdersRequestListOrdersPaginateTypeDef,
    _OptionalListOrdersRequestListOrdersPaginateTypeDef,
):
    pass

_RequiredListOrdersRequestRequestTypeDef = TypedDict(
    "_RequiredListOrdersRequestRequestTypeDef",
    {
        "networkArn": str,
    },
)
_OptionalListOrdersRequestRequestTypeDef = TypedDict(
    "_OptionalListOrdersRequestRequestTypeDef",
    {
        "filters": Mapping[OrderFilterKeysType, Sequence[str]],
        "maxResults": int,
        "startToken": str,
    },
    total=False,
)

class ListOrdersRequestRequestTypeDef(
    _RequiredListOrdersRequestRequestTypeDef, _OptionalListOrdersRequestRequestTypeDef
):
    pass

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredNameValuePairTypeDef = TypedDict(
    "_RequiredNameValuePairTypeDef",
    {
        "name": str,
    },
)
_OptionalNameValuePairTypeDef = TypedDict(
    "_OptionalNameValuePairTypeDef",
    {
        "value": str,
    },
    total=False,
)

class NameValuePairTypeDef(_RequiredNameValuePairTypeDef, _OptionalNameValuePairTypeDef):
    pass

TrackingInformationTypeDef = TypedDict(
    "TrackingInformationTypeDef",
    {
        "trackingNumber": str,
    },
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
)

PingResponseTypeDef = TypedDict(
    "PingResponseTypeDef",
    {
        "status": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateNetworkSiteRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateNetworkSiteRequestRequestTypeDef",
    {
        "networkSiteArn": str,
    },
)
_OptionalUpdateNetworkSiteRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateNetworkSiteRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
    },
    total=False,
)

class UpdateNetworkSiteRequestRequestTypeDef(
    _RequiredUpdateNetworkSiteRequestRequestTypeDef, _OptionalUpdateNetworkSiteRequestRequestTypeDef
):
    pass

ActivateDeviceIdentifierResponseTypeDef = TypedDict(
    "ActivateDeviceIdentifierResponseTypeDef",
    {
        "deviceIdentifier": DeviceIdentifierTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeactivateDeviceIdentifierResponseTypeDef = TypedDict(
    "DeactivateDeviceIdentifierResponseTypeDef",
    {
        "deviceIdentifier": DeviceIdentifierTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetDeviceIdentifierResponseTypeDef = TypedDict(
    "GetDeviceIdentifierResponseTypeDef",
    {
        "deviceIdentifier": DeviceIdentifierTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDeviceIdentifiersResponseTypeDef = TypedDict(
    "ListDeviceIdentifiersResponseTypeDef",
    {
        "deviceIdentifiers": List[DeviceIdentifierTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredActivateNetworkSiteRequestRequestTypeDef = TypedDict(
    "_RequiredActivateNetworkSiteRequestRequestTypeDef",
    {
        "networkSiteArn": str,
        "shippingAddress": AddressTypeDef,
    },
)
_OptionalActivateNetworkSiteRequestRequestTypeDef = TypedDict(
    "_OptionalActivateNetworkSiteRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class ActivateNetworkSiteRequestRequestTypeDef(
    _RequiredActivateNetworkSiteRequestRequestTypeDef,
    _OptionalActivateNetworkSiteRequestRequestTypeDef,
):
    pass

ReturnInformationTypeDef = TypedDict(
    "ReturnInformationTypeDef",
    {
        "replacementOrderArn": str,
        "returnReason": str,
        "shippingAddress": AddressTypeDef,
        "shippingLabel": str,
    },
    total=False,
)

_RequiredStartNetworkResourceUpdateRequestRequestTypeDef = TypedDict(
    "_RequiredStartNetworkResourceUpdateRequestRequestTypeDef",
    {
        "networkResourceArn": str,
        "updateType": UpdateTypeType,
    },
)
_OptionalStartNetworkResourceUpdateRequestRequestTypeDef = TypedDict(
    "_OptionalStartNetworkResourceUpdateRequestRequestTypeDef",
    {
        "returnReason": str,
        "shippingAddress": AddressTypeDef,
    },
    total=False,
)

class StartNetworkResourceUpdateRequestRequestTypeDef(
    _RequiredStartNetworkResourceUpdateRequestRequestTypeDef,
    _OptionalStartNetworkResourceUpdateRequestRequestTypeDef,
):
    pass

_RequiredConfigureAccessPointRequestRequestTypeDef = TypedDict(
    "_RequiredConfigureAccessPointRequestRequestTypeDef",
    {
        "accessPointArn": str,
    },
)
_OptionalConfigureAccessPointRequestRequestTypeDef = TypedDict(
    "_OptionalConfigureAccessPointRequestRequestTypeDef",
    {
        "cpiSecretKey": str,
        "cpiUserId": str,
        "cpiUserPassword": str,
        "cpiUsername": str,
        "position": PositionTypeDef,
    },
    total=False,
)

class ConfigureAccessPointRequestRequestTypeDef(
    _RequiredConfigureAccessPointRequestRequestTypeDef,
    _OptionalConfigureAccessPointRequestRequestTypeDef,
):
    pass

CreateNetworkResponseTypeDef = TypedDict(
    "CreateNetworkResponseTypeDef",
    {
        "network": NetworkTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteNetworkResponseTypeDef = TypedDict(
    "DeleteNetworkResponseTypeDef",
    {
        "network": NetworkTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetNetworkResponseTypeDef = TypedDict(
    "GetNetworkResponseTypeDef",
    {
        "network": NetworkTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListNetworksResponseTypeDef = TypedDict(
    "ListNetworksResponseTypeDef",
    {
        "networks": List[NetworkTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredNetworkResourceDefinitionTypeDef = TypedDict(
    "_RequiredNetworkResourceDefinitionTypeDef",
    {
        "count": int,
        "type": NetworkResourceDefinitionTypeType,
    },
)
_OptionalNetworkResourceDefinitionTypeDef = TypedDict(
    "_OptionalNetworkResourceDefinitionTypeDef",
    {
        "options": List[NameValuePairTypeDef],
    },
    total=False,
)

class NetworkResourceDefinitionTypeDef(
    _RequiredNetworkResourceDefinitionTypeDef, _OptionalNetworkResourceDefinitionTypeDef
):
    pass

OrderTypeDef = TypedDict(
    "OrderTypeDef",
    {
        "acknowledgmentStatus": AcknowledgmentStatusType,
        "createdAt": datetime,
        "networkArn": str,
        "networkSiteArn": str,
        "orderArn": str,
        "shippingAddress": AddressTypeDef,
        "trackingInformation": List[TrackingInformationTypeDef],
    },
    total=False,
)

NetworkResourceTypeDef = TypedDict(
    "NetworkResourceTypeDef",
    {
        "attributes": List[NameValuePairTypeDef],
        "createdAt": datetime,
        "description": str,
        "health": HealthStatusType,
        "model": str,
        "networkArn": str,
        "networkResourceArn": str,
        "networkSiteArn": str,
        "orderArn": str,
        "position": PositionTypeDef,
        "returnInformation": ReturnInformationTypeDef,
        "serialNumber": str,
        "status": NetworkResourceStatusType,
        "statusReason": str,
        "type": Literal["RADIO_UNIT"],
        "vendor": str,
    },
    total=False,
)

SitePlanTypeDef = TypedDict(
    "SitePlanTypeDef",
    {
        "options": List[NameValuePairTypeDef],
        "resourceDefinitions": List[NetworkResourceDefinitionTypeDef],
    },
    total=False,
)

AcknowledgeOrderReceiptResponseTypeDef = TypedDict(
    "AcknowledgeOrderReceiptResponseTypeDef",
    {
        "order": OrderTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetOrderResponseTypeDef = TypedDict(
    "GetOrderResponseTypeDef",
    {
        "order": OrderTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListOrdersResponseTypeDef = TypedDict(
    "ListOrdersResponseTypeDef",
    {
        "nextToken": str,
        "orders": List[OrderTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ConfigureAccessPointResponseTypeDef = TypedDict(
    "ConfigureAccessPointResponseTypeDef",
    {
        "accessPoint": NetworkResourceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetNetworkResourceResponseTypeDef = TypedDict(
    "GetNetworkResourceResponseTypeDef",
    {
        "networkResource": NetworkResourceTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListNetworkResourcesResponseTypeDef = TypedDict(
    "ListNetworkResourcesResponseTypeDef",
    {
        "networkResources": List[NetworkResourceTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartNetworkResourceUpdateResponseTypeDef = TypedDict(
    "StartNetworkResourceUpdateResponseTypeDef",
    {
        "networkResource": NetworkResourceTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateNetworkSiteRequestRequestTypeDef = TypedDict(
    "_RequiredCreateNetworkSiteRequestRequestTypeDef",
    {
        "networkArn": str,
        "networkSiteName": str,
    },
)
_OptionalCreateNetworkSiteRequestRequestTypeDef = TypedDict(
    "_OptionalCreateNetworkSiteRequestRequestTypeDef",
    {
        "availabilityZone": str,
        "availabilityZoneId": str,
        "clientToken": str,
        "description": str,
        "pendingPlan": SitePlanTypeDef,
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateNetworkSiteRequestRequestTypeDef(
    _RequiredCreateNetworkSiteRequestRequestTypeDef, _OptionalCreateNetworkSiteRequestRequestTypeDef
):
    pass

_RequiredNetworkSiteTypeDef = TypedDict(
    "_RequiredNetworkSiteTypeDef",
    {
        "networkArn": str,
        "networkSiteArn": str,
        "networkSiteName": str,
        "status": NetworkSiteStatusType,
    },
)
_OptionalNetworkSiteTypeDef = TypedDict(
    "_OptionalNetworkSiteTypeDef",
    {
        "availabilityZone": str,
        "availabilityZoneId": str,
        "createdAt": datetime,
        "currentPlan": SitePlanTypeDef,
        "description": str,
        "pendingPlan": SitePlanTypeDef,
        "statusReason": str,
    },
    total=False,
)

class NetworkSiteTypeDef(_RequiredNetworkSiteTypeDef, _OptionalNetworkSiteTypeDef):
    pass

_RequiredUpdateNetworkSitePlanRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateNetworkSitePlanRequestRequestTypeDef",
    {
        "networkSiteArn": str,
        "pendingPlan": SitePlanTypeDef,
    },
)
_OptionalUpdateNetworkSitePlanRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateNetworkSitePlanRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class UpdateNetworkSitePlanRequestRequestTypeDef(
    _RequiredUpdateNetworkSitePlanRequestRequestTypeDef,
    _OptionalUpdateNetworkSitePlanRequestRequestTypeDef,
):
    pass

ActivateNetworkSiteResponseTypeDef = TypedDict(
    "ActivateNetworkSiteResponseTypeDef",
    {
        "networkSite": NetworkSiteTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateNetworkSiteResponseTypeDef = TypedDict(
    "CreateNetworkSiteResponseTypeDef",
    {
        "networkSite": NetworkSiteTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteNetworkSiteResponseTypeDef = TypedDict(
    "DeleteNetworkSiteResponseTypeDef",
    {
        "networkSite": NetworkSiteTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetNetworkSiteResponseTypeDef = TypedDict(
    "GetNetworkSiteResponseTypeDef",
    {
        "networkSite": NetworkSiteTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListNetworkSitesResponseTypeDef = TypedDict(
    "ListNetworkSitesResponseTypeDef",
    {
        "networkSites": List[NetworkSiteTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateNetworkSiteResponseTypeDef = TypedDict(
    "UpdateNetworkSiteResponseTypeDef",
    {
        "networkSite": NetworkSiteTypeDef,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
