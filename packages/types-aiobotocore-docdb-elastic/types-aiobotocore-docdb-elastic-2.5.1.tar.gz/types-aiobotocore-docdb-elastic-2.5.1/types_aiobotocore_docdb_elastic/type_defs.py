"""
Type annotations for docdb-elastic service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_docdb_elastic/type_defs/)

Usage::

    ```python
    from types_aiobotocore_docdb_elastic.type_defs import ClusterInListTypeDef

    data: ClusterInListTypeDef = {...}
    ```
"""
import sys
from typing import Dict, List, Mapping, Sequence

from .literals import AuthType, StatusType

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "ClusterInListTypeDef",
    "ClusterSnapshotInListTypeDef",
    "ClusterSnapshotTypeDef",
    "ClusterTypeDef",
    "CreateClusterInputRequestTypeDef",
    "CreateClusterSnapshotInputRequestTypeDef",
    "DeleteClusterInputRequestTypeDef",
    "DeleteClusterSnapshotInputRequestTypeDef",
    "GetClusterInputRequestTypeDef",
    "GetClusterSnapshotInputRequestTypeDef",
    "ListClusterSnapshotsInputListClusterSnapshotsPaginateTypeDef",
    "ListClusterSnapshotsInputRequestTypeDef",
    "ListClustersInputListClustersPaginateTypeDef",
    "ListClustersInputRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreClusterFromSnapshotInputRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateClusterInputRequestTypeDef",
    "ListClustersOutputTypeDef",
    "ListClusterSnapshotsOutputTypeDef",
    "CreateClusterSnapshotOutputTypeDef",
    "DeleteClusterSnapshotOutputTypeDef",
    "GetClusterSnapshotOutputTypeDef",
    "CreateClusterOutputTypeDef",
    "DeleteClusterOutputTypeDef",
    "GetClusterOutputTypeDef",
    "RestoreClusterFromSnapshotOutputTypeDef",
    "UpdateClusterOutputTypeDef",
)

ClusterInListTypeDef = TypedDict(
    "ClusterInListTypeDef",
    {
        "clusterArn": str,
        "clusterName": str,
        "status": StatusType,
    },
)

ClusterSnapshotInListTypeDef = TypedDict(
    "ClusterSnapshotInListTypeDef",
    {
        "clusterArn": str,
        "snapshotArn": str,
        "snapshotCreationTime": str,
        "snapshotName": str,
        "status": StatusType,
    },
)

ClusterSnapshotTypeDef = TypedDict(
    "ClusterSnapshotTypeDef",
    {
        "adminUserName": str,
        "clusterArn": str,
        "clusterCreationTime": str,
        "kmsKeyId": str,
        "snapshotArn": str,
        "snapshotCreationTime": str,
        "snapshotName": str,
        "status": StatusType,
        "subnetIds": List[str],
        "vpcSecurityGroupIds": List[str],
    },
)

ClusterTypeDef = TypedDict(
    "ClusterTypeDef",
    {
        "adminUserName": str,
        "authType": AuthType,
        "clusterArn": str,
        "clusterEndpoint": str,
        "clusterName": str,
        "createTime": str,
        "kmsKeyId": str,
        "preferredMaintenanceWindow": str,
        "shardCapacity": int,
        "shardCount": int,
        "status": StatusType,
        "subnetIds": List[str],
        "vpcSecurityGroupIds": List[str],
    },
)

_RequiredCreateClusterInputRequestTypeDef = TypedDict(
    "_RequiredCreateClusterInputRequestTypeDef",
    {
        "adminUserName": str,
        "adminUserPassword": str,
        "authType": AuthType,
        "clusterName": str,
        "shardCapacity": int,
        "shardCount": int,
    },
)
_OptionalCreateClusterInputRequestTypeDef = TypedDict(
    "_OptionalCreateClusterInputRequestTypeDef",
    {
        "clientToken": str,
        "kmsKeyId": str,
        "preferredMaintenanceWindow": str,
        "subnetIds": Sequence[str],
        "tags": Mapping[str, str],
        "vpcSecurityGroupIds": Sequence[str],
    },
    total=False,
)


class CreateClusterInputRequestTypeDef(
    _RequiredCreateClusterInputRequestTypeDef, _OptionalCreateClusterInputRequestTypeDef
):
    pass


_RequiredCreateClusterSnapshotInputRequestTypeDef = TypedDict(
    "_RequiredCreateClusterSnapshotInputRequestTypeDef",
    {
        "clusterArn": str,
        "snapshotName": str,
    },
)
_OptionalCreateClusterSnapshotInputRequestTypeDef = TypedDict(
    "_OptionalCreateClusterSnapshotInputRequestTypeDef",
    {
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateClusterSnapshotInputRequestTypeDef(
    _RequiredCreateClusterSnapshotInputRequestTypeDef,
    _OptionalCreateClusterSnapshotInputRequestTypeDef,
):
    pass


DeleteClusterInputRequestTypeDef = TypedDict(
    "DeleteClusterInputRequestTypeDef",
    {
        "clusterArn": str,
    },
)

DeleteClusterSnapshotInputRequestTypeDef = TypedDict(
    "DeleteClusterSnapshotInputRequestTypeDef",
    {
        "snapshotArn": str,
    },
)

GetClusterInputRequestTypeDef = TypedDict(
    "GetClusterInputRequestTypeDef",
    {
        "clusterArn": str,
    },
)

GetClusterSnapshotInputRequestTypeDef = TypedDict(
    "GetClusterSnapshotInputRequestTypeDef",
    {
        "snapshotArn": str,
    },
)

ListClusterSnapshotsInputListClusterSnapshotsPaginateTypeDef = TypedDict(
    "ListClusterSnapshotsInputListClusterSnapshotsPaginateTypeDef",
    {
        "clusterArn": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListClusterSnapshotsInputRequestTypeDef = TypedDict(
    "ListClusterSnapshotsInputRequestTypeDef",
    {
        "clusterArn": str,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListClustersInputListClustersPaginateTypeDef = TypedDict(
    "ListClustersInputListClustersPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListClustersInputRequestTypeDef = TypedDict(
    "ListClustersInputRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

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

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": int,
        "PageSize": int,
        "StartingToken": str,
    },
    total=False,
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

_RequiredRestoreClusterFromSnapshotInputRequestTypeDef = TypedDict(
    "_RequiredRestoreClusterFromSnapshotInputRequestTypeDef",
    {
        "clusterName": str,
        "snapshotArn": str,
    },
)
_OptionalRestoreClusterFromSnapshotInputRequestTypeDef = TypedDict(
    "_OptionalRestoreClusterFromSnapshotInputRequestTypeDef",
    {
        "kmsKeyId": str,
        "subnetIds": Sequence[str],
        "tags": Mapping[str, str],
        "vpcSecurityGroupIds": Sequence[str],
    },
    total=False,
)


class RestoreClusterFromSnapshotInputRequestTypeDef(
    _RequiredRestoreClusterFromSnapshotInputRequestTypeDef,
    _OptionalRestoreClusterFromSnapshotInputRequestTypeDef,
):
    pass


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

_RequiredUpdateClusterInputRequestTypeDef = TypedDict(
    "_RequiredUpdateClusterInputRequestTypeDef",
    {
        "clusterArn": str,
    },
)
_OptionalUpdateClusterInputRequestTypeDef = TypedDict(
    "_OptionalUpdateClusterInputRequestTypeDef",
    {
        "adminUserPassword": str,
        "authType": AuthType,
        "clientToken": str,
        "preferredMaintenanceWindow": str,
        "shardCapacity": int,
        "shardCount": int,
        "subnetIds": Sequence[str],
        "vpcSecurityGroupIds": Sequence[str],
    },
    total=False,
)


class UpdateClusterInputRequestTypeDef(
    _RequiredUpdateClusterInputRequestTypeDef, _OptionalUpdateClusterInputRequestTypeDef
):
    pass


ListClustersOutputTypeDef = TypedDict(
    "ListClustersOutputTypeDef",
    {
        "clusters": List[ClusterInListTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListClusterSnapshotsOutputTypeDef = TypedDict(
    "ListClusterSnapshotsOutputTypeDef",
    {
        "nextToken": str,
        "snapshots": List[ClusterSnapshotInListTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateClusterSnapshotOutputTypeDef = TypedDict(
    "CreateClusterSnapshotOutputTypeDef",
    {
        "snapshot": ClusterSnapshotTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteClusterSnapshotOutputTypeDef = TypedDict(
    "DeleteClusterSnapshotOutputTypeDef",
    {
        "snapshot": ClusterSnapshotTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetClusterSnapshotOutputTypeDef = TypedDict(
    "GetClusterSnapshotOutputTypeDef",
    {
        "snapshot": ClusterSnapshotTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateClusterOutputTypeDef = TypedDict(
    "CreateClusterOutputTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteClusterOutputTypeDef = TypedDict(
    "DeleteClusterOutputTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetClusterOutputTypeDef = TypedDict(
    "GetClusterOutputTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RestoreClusterFromSnapshotOutputTypeDef = TypedDict(
    "RestoreClusterFromSnapshotOutputTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateClusterOutputTypeDef = TypedDict(
    "UpdateClusterOutputTypeDef",
    {
        "cluster": ClusterTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)
