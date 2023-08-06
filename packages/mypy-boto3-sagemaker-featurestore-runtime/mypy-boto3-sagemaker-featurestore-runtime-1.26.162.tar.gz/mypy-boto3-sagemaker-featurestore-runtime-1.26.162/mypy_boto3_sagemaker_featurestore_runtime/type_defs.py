"""
Type annotations for sagemaker-featurestore-runtime service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_sagemaker_featurestore_runtime/type_defs/)

Usage::

    ```python
    from mypy_boto3_sagemaker_featurestore_runtime.type_defs import BatchGetRecordErrorTypeDef

    data: BatchGetRecordErrorTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Sequence

from .literals import (
    DeletionModeType,
    ExpirationTimeResponseType,
    TargetStoreType,
    TtlDurationUnitType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "BatchGetRecordErrorTypeDef",
    "BatchGetRecordIdentifierTypeDef",
    "ResponseMetadataTypeDef",
    "FeatureValueTypeDef",
    "DeleteRecordRequestRequestTypeDef",
    "GetRecordRequestRequestTypeDef",
    "TtlDurationTypeDef",
    "BatchGetRecordRequestRequestTypeDef",
    "EmptyResponseMetadataTypeDef",
    "BatchGetRecordResultDetailTypeDef",
    "GetRecordResponseTypeDef",
    "PutRecordRequestRequestTypeDef",
    "BatchGetRecordResponseTypeDef",
)

BatchGetRecordErrorTypeDef = TypedDict(
    "BatchGetRecordErrorTypeDef",
    {
        "FeatureGroupName": str,
        "RecordIdentifierValueAsString": str,
        "ErrorCode": str,
        "ErrorMessage": str,
    },
)

_RequiredBatchGetRecordIdentifierTypeDef = TypedDict(
    "_RequiredBatchGetRecordIdentifierTypeDef",
    {
        "FeatureGroupName": str,
        "RecordIdentifiersValueAsString": Sequence[str],
    },
)
_OptionalBatchGetRecordIdentifierTypeDef = TypedDict(
    "_OptionalBatchGetRecordIdentifierTypeDef",
    {
        "FeatureNames": Sequence[str],
    },
    total=False,
)


class BatchGetRecordIdentifierTypeDef(
    _RequiredBatchGetRecordIdentifierTypeDef, _OptionalBatchGetRecordIdentifierTypeDef
):
    pass


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

FeatureValueTypeDef = TypedDict(
    "FeatureValueTypeDef",
    {
        "FeatureName": str,
        "ValueAsString": str,
    },
)

_RequiredDeleteRecordRequestRequestTypeDef = TypedDict(
    "_RequiredDeleteRecordRequestRequestTypeDef",
    {
        "FeatureGroupName": str,
        "RecordIdentifierValueAsString": str,
        "EventTime": str,
    },
)
_OptionalDeleteRecordRequestRequestTypeDef = TypedDict(
    "_OptionalDeleteRecordRequestRequestTypeDef",
    {
        "TargetStores": Sequence[TargetStoreType],
        "DeletionMode": DeletionModeType,
    },
    total=False,
)


class DeleteRecordRequestRequestTypeDef(
    _RequiredDeleteRecordRequestRequestTypeDef, _OptionalDeleteRecordRequestRequestTypeDef
):
    pass


_RequiredGetRecordRequestRequestTypeDef = TypedDict(
    "_RequiredGetRecordRequestRequestTypeDef",
    {
        "FeatureGroupName": str,
        "RecordIdentifierValueAsString": str,
    },
)
_OptionalGetRecordRequestRequestTypeDef = TypedDict(
    "_OptionalGetRecordRequestRequestTypeDef",
    {
        "FeatureNames": Sequence[str],
        "ExpirationTimeResponse": ExpirationTimeResponseType,
    },
    total=False,
)


class GetRecordRequestRequestTypeDef(
    _RequiredGetRecordRequestRequestTypeDef, _OptionalGetRecordRequestRequestTypeDef
):
    pass


TtlDurationTypeDef = TypedDict(
    "TtlDurationTypeDef",
    {
        "Unit": TtlDurationUnitType,
        "Value": int,
    },
)

_RequiredBatchGetRecordRequestRequestTypeDef = TypedDict(
    "_RequiredBatchGetRecordRequestRequestTypeDef",
    {
        "Identifiers": Sequence[BatchGetRecordIdentifierTypeDef],
    },
)
_OptionalBatchGetRecordRequestRequestTypeDef = TypedDict(
    "_OptionalBatchGetRecordRequestRequestTypeDef",
    {
        "ExpirationTimeResponse": ExpirationTimeResponseType,
    },
    total=False,
)


class BatchGetRecordRequestRequestTypeDef(
    _RequiredBatchGetRecordRequestRequestTypeDef, _OptionalBatchGetRecordRequestRequestTypeDef
):
    pass


EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredBatchGetRecordResultDetailTypeDef = TypedDict(
    "_RequiredBatchGetRecordResultDetailTypeDef",
    {
        "FeatureGroupName": str,
        "RecordIdentifierValueAsString": str,
        "Record": List[FeatureValueTypeDef],
    },
)
_OptionalBatchGetRecordResultDetailTypeDef = TypedDict(
    "_OptionalBatchGetRecordResultDetailTypeDef",
    {
        "ExpiresAt": str,
    },
    total=False,
)


class BatchGetRecordResultDetailTypeDef(
    _RequiredBatchGetRecordResultDetailTypeDef, _OptionalBatchGetRecordResultDetailTypeDef
):
    pass


GetRecordResponseTypeDef = TypedDict(
    "GetRecordResponseTypeDef",
    {
        "Record": List[FeatureValueTypeDef],
        "ExpiresAt": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)

_RequiredPutRecordRequestRequestTypeDef = TypedDict(
    "_RequiredPutRecordRequestRequestTypeDef",
    {
        "FeatureGroupName": str,
        "Record": Sequence[FeatureValueTypeDef],
    },
)
_OptionalPutRecordRequestRequestTypeDef = TypedDict(
    "_OptionalPutRecordRequestRequestTypeDef",
    {
        "TargetStores": Sequence[TargetStoreType],
        "TtlDuration": TtlDurationTypeDef,
    },
    total=False,
)


class PutRecordRequestRequestTypeDef(
    _RequiredPutRecordRequestRequestTypeDef, _OptionalPutRecordRequestRequestTypeDef
):
    pass


BatchGetRecordResponseTypeDef = TypedDict(
    "BatchGetRecordResponseTypeDef",
    {
        "Records": List[BatchGetRecordResultDetailTypeDef],
        "Errors": List[BatchGetRecordErrorTypeDef],
        "UnprocessedIdentifiers": List[BatchGetRecordIdentifierTypeDef],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
