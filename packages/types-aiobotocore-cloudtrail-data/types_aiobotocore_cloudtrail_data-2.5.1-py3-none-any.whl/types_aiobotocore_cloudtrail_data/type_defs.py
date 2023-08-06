"""
Type annotations for cloudtrail-data service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_cloudtrail_data/type_defs/)

Usage::

    ```python
    from types_aiobotocore_cloudtrail_data.type_defs import AuditEventResultEntryTypeDef

    data: AuditEventResultEntryTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Sequence

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AuditEventResultEntryTypeDef",
    "AuditEventTypeDef",
    "ResultErrorEntryTypeDef",
    "ResponseMetadataTypeDef",
    "PutAuditEventsRequestRequestTypeDef",
    "PutAuditEventsResponseTypeDef",
)

AuditEventResultEntryTypeDef = TypedDict(
    "AuditEventResultEntryTypeDef",
    {
        "eventID": str,
        "id": str,
    },
)

_RequiredAuditEventTypeDef = TypedDict(
    "_RequiredAuditEventTypeDef",
    {
        "eventData": str,
        "id": str,
    },
)
_OptionalAuditEventTypeDef = TypedDict(
    "_OptionalAuditEventTypeDef",
    {
        "eventDataChecksum": str,
    },
    total=False,
)


class AuditEventTypeDef(_RequiredAuditEventTypeDef, _OptionalAuditEventTypeDef):
    pass


ResultErrorEntryTypeDef = TypedDict(
    "ResultErrorEntryTypeDef",
    {
        "errorCode": str,
        "errorMessage": str,
        "id": str,
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

_RequiredPutAuditEventsRequestRequestTypeDef = TypedDict(
    "_RequiredPutAuditEventsRequestRequestTypeDef",
    {
        "auditEvents": Sequence[AuditEventTypeDef],
        "channelArn": str,
    },
)
_OptionalPutAuditEventsRequestRequestTypeDef = TypedDict(
    "_OptionalPutAuditEventsRequestRequestTypeDef",
    {
        "externalId": str,
    },
    total=False,
)


class PutAuditEventsRequestRequestTypeDef(
    _RequiredPutAuditEventsRequestRequestTypeDef, _OptionalPutAuditEventsRequestRequestTypeDef
):
    pass


PutAuditEventsResponseTypeDef = TypedDict(
    "PutAuditEventsResponseTypeDef",
    {
        "failed": List[ResultErrorEntryTypeDef],
        "successful": List[AuditEventResultEntryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
