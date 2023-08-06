"""
Type annotations for m2 service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_m2/type_defs/)

Usage::

    ```python
    from types_aiobotocore_m2.type_defs import AlternateKeyTypeDef

    data: AlternateKeyTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ApplicationDeploymentLifecycleType,
    ApplicationLifecycleType,
    ApplicationVersionLifecycleType,
    BatchJobExecutionStatusType,
    BatchJobTypeType,
    DataSetTaskLifecycleType,
    DeploymentLifecycleType,
    EngineTypeType,
    EnvironmentLifecycleType,
)

if sys.version_info >= (3, 9):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "AlternateKeyTypeDef",
    "ApplicationSummaryTypeDef",
    "ApplicationVersionSummaryTypeDef",
    "FileBatchJobDefinitionTypeDef",
    "ScriptBatchJobDefinitionTypeDef",
    "FileBatchJobIdentifierTypeDef",
    "ScriptBatchJobIdentifierTypeDef",
    "CancelBatchJobExecutionRequestRequestTypeDef",
    "DefinitionTypeDef",
    "CreateApplicationResponseTypeDef",
    "CreateDataSetImportTaskResponseTypeDef",
    "CreateDeploymentRequestRequestTypeDef",
    "CreateDeploymentResponseTypeDef",
    "HighAvailabilityConfigTypeDef",
    "CreateEnvironmentResponseTypeDef",
    "ExternalLocationTypeDef",
    "DataSetImportSummaryTypeDef",
    "DataSetSummaryTypeDef",
    "RecordLengthTypeDef",
    "GdgDetailAttributesTypeDef",
    "PoDetailAttributesTypeDef",
    "PsDetailAttributesTypeDef",
    "GdgAttributesTypeDef",
    "PoAttributesTypeDef",
    "PsAttributesTypeDef",
    "DeleteApplicationFromEnvironmentRequestRequestTypeDef",
    "DeleteApplicationRequestRequestTypeDef",
    "DeleteEnvironmentRequestRequestTypeDef",
    "DeployedVersionSummaryTypeDef",
    "DeploymentSummaryTypeDef",
    "EfsStorageConfigurationTypeDef",
    "EngineVersionsSummaryTypeDef",
    "EnvironmentSummaryTypeDef",
    "FsxStorageConfigurationTypeDef",
    "GetApplicationRequestRequestTypeDef",
    "LogGroupSummaryTypeDef",
    "GetApplicationVersionRequestRequestTypeDef",
    "GetApplicationVersionResponseTypeDef",
    "GetBatchJobExecutionRequestRequestTypeDef",
    "GetDataSetDetailsRequestRequestTypeDef",
    "GetDataSetImportTaskRequestRequestTypeDef",
    "GetDeploymentRequestRequestTypeDef",
    "GetDeploymentResponseTypeDef",
    "GetEnvironmentRequestRequestTypeDef",
    "ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef",
    "ListApplicationVersionsRequestRequestTypeDef",
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    "ListApplicationsRequestRequestTypeDef",
    "ListBatchJobDefinitionsRequestListBatchJobDefinitionsPaginateTypeDef",
    "ListBatchJobDefinitionsRequestRequestTypeDef",
    "ListBatchJobExecutionsRequestListBatchJobExecutionsPaginateTypeDef",
    "ListBatchJobExecutionsRequestRequestTypeDef",
    "ListDataSetImportHistoryRequestListDataSetImportHistoryPaginateTypeDef",
    "ListDataSetImportHistoryRequestRequestTypeDef",
    "ListDataSetsRequestListDataSetsPaginateTypeDef",
    "ListDataSetsRequestRequestTypeDef",
    "ListDeploymentsRequestListDeploymentsPaginateTypeDef",
    "ListDeploymentsRequestRequestTypeDef",
    "ListEngineVersionsRequestListEngineVersionsPaginateTypeDef",
    "ListEngineVersionsRequestRequestTypeDef",
    "ListEnvironmentsRequestListEnvironmentsPaginateTypeDef",
    "ListEnvironmentsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MaintenanceScheduleTypeDef",
    "PaginatorConfigTypeDef",
    "PrimaryKeyTypeDef",
    "ResponseMetadataTypeDef",
    "StartApplicationRequestRequestTypeDef",
    "StartBatchJobResponseTypeDef",
    "StopApplicationRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateApplicationResponseTypeDef",
    "UpdateEnvironmentRequestRequestTypeDef",
    "UpdateEnvironmentResponseTypeDef",
    "ListApplicationsResponseTypeDef",
    "ListApplicationVersionsResponseTypeDef",
    "BatchJobDefinitionTypeDef",
    "BatchJobIdentifierTypeDef",
    "CreateApplicationRequestRequestTypeDef",
    "UpdateApplicationRequestRequestTypeDef",
    "DataSetImportTaskTypeDef",
    "GetDataSetImportTaskResponseTypeDef",
    "ListDataSetsResponseTypeDef",
    "ListDeploymentsResponseTypeDef",
    "ListEngineVersionsResponseTypeDef",
    "ListEnvironmentsResponseTypeDef",
    "StorageConfigurationTypeDef",
    "GetApplicationResponseTypeDef",
    "PendingMaintenanceTypeDef",
    "VsamAttributesTypeDef",
    "VsamDetailAttributesTypeDef",
    "ListBatchJobDefinitionsResponseTypeDef",
    "BatchJobExecutionSummaryTypeDef",
    "GetBatchJobExecutionResponseTypeDef",
    "StartBatchJobRequestRequestTypeDef",
    "ListDataSetImportHistoryResponseTypeDef",
    "CreateEnvironmentRequestRequestTypeDef",
    "GetEnvironmentResponseTypeDef",
    "DatasetOrgAttributesTypeDef",
    "DatasetDetailOrgAttributesTypeDef",
    "ListBatchJobExecutionsResponseTypeDef",
    "DataSetTypeDef",
    "GetDataSetDetailsResponseTypeDef",
    "DataSetImportItemTypeDef",
    "DataSetImportConfigTypeDef",
    "CreateDataSetImportTaskRequestRequestTypeDef",
)

_RequiredAlternateKeyTypeDef = TypedDict(
    "_RequiredAlternateKeyTypeDef",
    {
        "length": int,
        "offset": int,
    },
)
_OptionalAlternateKeyTypeDef = TypedDict(
    "_OptionalAlternateKeyTypeDef",
    {
        "allowDuplicates": bool,
        "name": str,
    },
    total=False,
)


class AlternateKeyTypeDef(_RequiredAlternateKeyTypeDef, _OptionalAlternateKeyTypeDef):
    pass


_RequiredApplicationSummaryTypeDef = TypedDict(
    "_RequiredApplicationSummaryTypeDef",
    {
        "applicationArn": str,
        "applicationId": str,
        "applicationVersion": int,
        "creationTime": datetime,
        "engineType": EngineTypeType,
        "name": str,
        "status": ApplicationLifecycleType,
    },
)
_OptionalApplicationSummaryTypeDef = TypedDict(
    "_OptionalApplicationSummaryTypeDef",
    {
        "deploymentStatus": ApplicationDeploymentLifecycleType,
        "description": str,
        "environmentId": str,
        "lastStartTime": datetime,
        "roleArn": str,
        "versionStatus": ApplicationVersionLifecycleType,
    },
    total=False,
)


class ApplicationSummaryTypeDef(
    _RequiredApplicationSummaryTypeDef, _OptionalApplicationSummaryTypeDef
):
    pass


_RequiredApplicationVersionSummaryTypeDef = TypedDict(
    "_RequiredApplicationVersionSummaryTypeDef",
    {
        "applicationVersion": int,
        "creationTime": datetime,
        "status": ApplicationVersionLifecycleType,
    },
)
_OptionalApplicationVersionSummaryTypeDef = TypedDict(
    "_OptionalApplicationVersionSummaryTypeDef",
    {
        "statusReason": str,
    },
    total=False,
)


class ApplicationVersionSummaryTypeDef(
    _RequiredApplicationVersionSummaryTypeDef, _OptionalApplicationVersionSummaryTypeDef
):
    pass


_RequiredFileBatchJobDefinitionTypeDef = TypedDict(
    "_RequiredFileBatchJobDefinitionTypeDef",
    {
        "fileName": str,
    },
)
_OptionalFileBatchJobDefinitionTypeDef = TypedDict(
    "_OptionalFileBatchJobDefinitionTypeDef",
    {
        "folderPath": str,
    },
    total=False,
)


class FileBatchJobDefinitionTypeDef(
    _RequiredFileBatchJobDefinitionTypeDef, _OptionalFileBatchJobDefinitionTypeDef
):
    pass


ScriptBatchJobDefinitionTypeDef = TypedDict(
    "ScriptBatchJobDefinitionTypeDef",
    {
        "scriptName": str,
    },
)

_RequiredFileBatchJobIdentifierTypeDef = TypedDict(
    "_RequiredFileBatchJobIdentifierTypeDef",
    {
        "fileName": str,
    },
)
_OptionalFileBatchJobIdentifierTypeDef = TypedDict(
    "_OptionalFileBatchJobIdentifierTypeDef",
    {
        "folderPath": str,
    },
    total=False,
)


class FileBatchJobIdentifierTypeDef(
    _RequiredFileBatchJobIdentifierTypeDef, _OptionalFileBatchJobIdentifierTypeDef
):
    pass


ScriptBatchJobIdentifierTypeDef = TypedDict(
    "ScriptBatchJobIdentifierTypeDef",
    {
        "scriptName": str,
    },
)

CancelBatchJobExecutionRequestRequestTypeDef = TypedDict(
    "CancelBatchJobExecutionRequestRequestTypeDef",
    {
        "applicationId": str,
        "executionId": str,
    },
)

DefinitionTypeDef = TypedDict(
    "DefinitionTypeDef",
    {
        "content": str,
        "s3Location": str,
    },
    total=False,
)

CreateApplicationResponseTypeDef = TypedDict(
    "CreateApplicationResponseTypeDef",
    {
        "applicationArn": str,
        "applicationId": str,
        "applicationVersion": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateDataSetImportTaskResponseTypeDef = TypedDict(
    "CreateDataSetImportTaskResponseTypeDef",
    {
        "taskId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateDeploymentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDeploymentRequestRequestTypeDef",
    {
        "applicationId": str,
        "applicationVersion": int,
        "environmentId": str,
    },
)
_OptionalCreateDeploymentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDeploymentRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class CreateDeploymentRequestRequestTypeDef(
    _RequiredCreateDeploymentRequestRequestTypeDef, _OptionalCreateDeploymentRequestRequestTypeDef
):
    pass


CreateDeploymentResponseTypeDef = TypedDict(
    "CreateDeploymentResponseTypeDef",
    {
        "deploymentId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

HighAvailabilityConfigTypeDef = TypedDict(
    "HighAvailabilityConfigTypeDef",
    {
        "desiredCapacity": int,
    },
)

CreateEnvironmentResponseTypeDef = TypedDict(
    "CreateEnvironmentResponseTypeDef",
    {
        "environmentId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ExternalLocationTypeDef = TypedDict(
    "ExternalLocationTypeDef",
    {
        "s3Location": str,
    },
    total=False,
)

DataSetImportSummaryTypeDef = TypedDict(
    "DataSetImportSummaryTypeDef",
    {
        "failed": int,
        "inProgress": int,
        "pending": int,
        "succeeded": int,
        "total": int,
    },
)

_RequiredDataSetSummaryTypeDef = TypedDict(
    "_RequiredDataSetSummaryTypeDef",
    {
        "dataSetName": str,
    },
)
_OptionalDataSetSummaryTypeDef = TypedDict(
    "_OptionalDataSetSummaryTypeDef",
    {
        "creationTime": datetime,
        "dataSetOrg": str,
        "format": str,
        "lastReferencedTime": datetime,
        "lastUpdatedTime": datetime,
    },
    total=False,
)


class DataSetSummaryTypeDef(_RequiredDataSetSummaryTypeDef, _OptionalDataSetSummaryTypeDef):
    pass


RecordLengthTypeDef = TypedDict(
    "RecordLengthTypeDef",
    {
        "max": int,
        "min": int,
    },
)

GdgDetailAttributesTypeDef = TypedDict(
    "GdgDetailAttributesTypeDef",
    {
        "limit": int,
        "rollDisposition": str,
    },
    total=False,
)

PoDetailAttributesTypeDef = TypedDict(
    "PoDetailAttributesTypeDef",
    {
        "encoding": str,
        "format": str,
    },
)

PsDetailAttributesTypeDef = TypedDict(
    "PsDetailAttributesTypeDef",
    {
        "encoding": str,
        "format": str,
    },
)

GdgAttributesTypeDef = TypedDict(
    "GdgAttributesTypeDef",
    {
        "limit": int,
        "rollDisposition": str,
    },
    total=False,
)

_RequiredPoAttributesTypeDef = TypedDict(
    "_RequiredPoAttributesTypeDef",
    {
        "format": str,
        "memberFileExtensions": Sequence[str],
    },
)
_OptionalPoAttributesTypeDef = TypedDict(
    "_OptionalPoAttributesTypeDef",
    {
        "encoding": str,
    },
    total=False,
)


class PoAttributesTypeDef(_RequiredPoAttributesTypeDef, _OptionalPoAttributesTypeDef):
    pass


_RequiredPsAttributesTypeDef = TypedDict(
    "_RequiredPsAttributesTypeDef",
    {
        "format": str,
    },
)
_OptionalPsAttributesTypeDef = TypedDict(
    "_OptionalPsAttributesTypeDef",
    {
        "encoding": str,
    },
    total=False,
)


class PsAttributesTypeDef(_RequiredPsAttributesTypeDef, _OptionalPsAttributesTypeDef):
    pass


DeleteApplicationFromEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteApplicationFromEnvironmentRequestRequestTypeDef",
    {
        "applicationId": str,
        "environmentId": str,
    },
)

DeleteApplicationRequestRequestTypeDef = TypedDict(
    "DeleteApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)

DeleteEnvironmentRequestRequestTypeDef = TypedDict(
    "DeleteEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)

_RequiredDeployedVersionSummaryTypeDef = TypedDict(
    "_RequiredDeployedVersionSummaryTypeDef",
    {
        "applicationVersion": int,
        "status": DeploymentLifecycleType,
    },
)
_OptionalDeployedVersionSummaryTypeDef = TypedDict(
    "_OptionalDeployedVersionSummaryTypeDef",
    {
        "statusReason": str,
    },
    total=False,
)


class DeployedVersionSummaryTypeDef(
    _RequiredDeployedVersionSummaryTypeDef, _OptionalDeployedVersionSummaryTypeDef
):
    pass


_RequiredDeploymentSummaryTypeDef = TypedDict(
    "_RequiredDeploymentSummaryTypeDef",
    {
        "applicationId": str,
        "applicationVersion": int,
        "creationTime": datetime,
        "deploymentId": str,
        "environmentId": str,
        "status": DeploymentLifecycleType,
    },
)
_OptionalDeploymentSummaryTypeDef = TypedDict(
    "_OptionalDeploymentSummaryTypeDef",
    {
        "statusReason": str,
    },
    total=False,
)


class DeploymentSummaryTypeDef(
    _RequiredDeploymentSummaryTypeDef, _OptionalDeploymentSummaryTypeDef
):
    pass


EfsStorageConfigurationTypeDef = TypedDict(
    "EfsStorageConfigurationTypeDef",
    {
        "fileSystemId": str,
        "mountPoint": str,
    },
)

EngineVersionsSummaryTypeDef = TypedDict(
    "EngineVersionsSummaryTypeDef",
    {
        "engineType": str,
        "engineVersion": str,
    },
)

EnvironmentSummaryTypeDef = TypedDict(
    "EnvironmentSummaryTypeDef",
    {
        "creationTime": datetime,
        "engineType": EngineTypeType,
        "engineVersion": str,
        "environmentArn": str,
        "environmentId": str,
        "instanceType": str,
        "name": str,
        "status": EnvironmentLifecycleType,
    },
)

FsxStorageConfigurationTypeDef = TypedDict(
    "FsxStorageConfigurationTypeDef",
    {
        "fileSystemId": str,
        "mountPoint": str,
    },
)

GetApplicationRequestRequestTypeDef = TypedDict(
    "GetApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)

LogGroupSummaryTypeDef = TypedDict(
    "LogGroupSummaryTypeDef",
    {
        "logGroupName": str,
        "logType": str,
    },
)

GetApplicationVersionRequestRequestTypeDef = TypedDict(
    "GetApplicationVersionRequestRequestTypeDef",
    {
        "applicationId": str,
        "applicationVersion": int,
    },
)

GetApplicationVersionResponseTypeDef = TypedDict(
    "GetApplicationVersionResponseTypeDef",
    {
        "applicationVersion": int,
        "creationTime": datetime,
        "definitionContent": str,
        "description": str,
        "name": str,
        "status": ApplicationVersionLifecycleType,
        "statusReason": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetBatchJobExecutionRequestRequestTypeDef = TypedDict(
    "GetBatchJobExecutionRequestRequestTypeDef",
    {
        "applicationId": str,
        "executionId": str,
    },
)

GetDataSetDetailsRequestRequestTypeDef = TypedDict(
    "GetDataSetDetailsRequestRequestTypeDef",
    {
        "applicationId": str,
        "dataSetName": str,
    },
)

GetDataSetImportTaskRequestRequestTypeDef = TypedDict(
    "GetDataSetImportTaskRequestRequestTypeDef",
    {
        "applicationId": str,
        "taskId": str,
    },
)

GetDeploymentRequestRequestTypeDef = TypedDict(
    "GetDeploymentRequestRequestTypeDef",
    {
        "applicationId": str,
        "deploymentId": str,
    },
)

GetDeploymentResponseTypeDef = TypedDict(
    "GetDeploymentResponseTypeDef",
    {
        "applicationId": str,
        "applicationVersion": int,
        "creationTime": datetime,
        "deploymentId": str,
        "environmentId": str,
        "status": DeploymentLifecycleType,
        "statusReason": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetEnvironmentRequestRequestTypeDef = TypedDict(
    "GetEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)

_RequiredListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef = TypedDict(
    "_RequiredListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef = TypedDict(
    "_OptionalListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef(
    _RequiredListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef,
    _OptionalListApplicationVersionsRequestListApplicationVersionsPaginateTypeDef,
):
    pass


_RequiredListApplicationVersionsRequestRequestTypeDef = TypedDict(
    "_RequiredListApplicationVersionsRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalListApplicationVersionsRequestRequestTypeDef = TypedDict(
    "_OptionalListApplicationVersionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListApplicationVersionsRequestRequestTypeDef(
    _RequiredListApplicationVersionsRequestRequestTypeDef,
    _OptionalListApplicationVersionsRequestRequestTypeDef,
):
    pass


ListApplicationsRequestListApplicationsPaginateTypeDef = TypedDict(
    "ListApplicationsRequestListApplicationsPaginateTypeDef",
    {
        "environmentId": str,
        "names": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListApplicationsRequestRequestTypeDef = TypedDict(
    "ListApplicationsRequestRequestTypeDef",
    {
        "environmentId": str,
        "maxResults": int,
        "names": Sequence[str],
        "nextToken": str,
    },
    total=False,
)

_RequiredListBatchJobDefinitionsRequestListBatchJobDefinitionsPaginateTypeDef = TypedDict(
    "_RequiredListBatchJobDefinitionsRequestListBatchJobDefinitionsPaginateTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalListBatchJobDefinitionsRequestListBatchJobDefinitionsPaginateTypeDef = TypedDict(
    "_OptionalListBatchJobDefinitionsRequestListBatchJobDefinitionsPaginateTypeDef",
    {
        "prefix": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListBatchJobDefinitionsRequestListBatchJobDefinitionsPaginateTypeDef(
    _RequiredListBatchJobDefinitionsRequestListBatchJobDefinitionsPaginateTypeDef,
    _OptionalListBatchJobDefinitionsRequestListBatchJobDefinitionsPaginateTypeDef,
):
    pass


_RequiredListBatchJobDefinitionsRequestRequestTypeDef = TypedDict(
    "_RequiredListBatchJobDefinitionsRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalListBatchJobDefinitionsRequestRequestTypeDef = TypedDict(
    "_OptionalListBatchJobDefinitionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "prefix": str,
    },
    total=False,
)


class ListBatchJobDefinitionsRequestRequestTypeDef(
    _RequiredListBatchJobDefinitionsRequestRequestTypeDef,
    _OptionalListBatchJobDefinitionsRequestRequestTypeDef,
):
    pass


_RequiredListBatchJobExecutionsRequestListBatchJobExecutionsPaginateTypeDef = TypedDict(
    "_RequiredListBatchJobExecutionsRequestListBatchJobExecutionsPaginateTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalListBatchJobExecutionsRequestListBatchJobExecutionsPaginateTypeDef = TypedDict(
    "_OptionalListBatchJobExecutionsRequestListBatchJobExecutionsPaginateTypeDef",
    {
        "executionIds": Sequence[str],
        "jobName": str,
        "startedAfter": Union[datetime, str],
        "startedBefore": Union[datetime, str],
        "status": BatchJobExecutionStatusType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListBatchJobExecutionsRequestListBatchJobExecutionsPaginateTypeDef(
    _RequiredListBatchJobExecutionsRequestListBatchJobExecutionsPaginateTypeDef,
    _OptionalListBatchJobExecutionsRequestListBatchJobExecutionsPaginateTypeDef,
):
    pass


_RequiredListBatchJobExecutionsRequestRequestTypeDef = TypedDict(
    "_RequiredListBatchJobExecutionsRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalListBatchJobExecutionsRequestRequestTypeDef = TypedDict(
    "_OptionalListBatchJobExecutionsRequestRequestTypeDef",
    {
        "executionIds": Sequence[str],
        "jobName": str,
        "maxResults": int,
        "nextToken": str,
        "startedAfter": Union[datetime, str],
        "startedBefore": Union[datetime, str],
        "status": BatchJobExecutionStatusType,
    },
    total=False,
)


class ListBatchJobExecutionsRequestRequestTypeDef(
    _RequiredListBatchJobExecutionsRequestRequestTypeDef,
    _OptionalListBatchJobExecutionsRequestRequestTypeDef,
):
    pass


_RequiredListDataSetImportHistoryRequestListDataSetImportHistoryPaginateTypeDef = TypedDict(
    "_RequiredListDataSetImportHistoryRequestListDataSetImportHistoryPaginateTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalListDataSetImportHistoryRequestListDataSetImportHistoryPaginateTypeDef = TypedDict(
    "_OptionalListDataSetImportHistoryRequestListDataSetImportHistoryPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListDataSetImportHistoryRequestListDataSetImportHistoryPaginateTypeDef(
    _RequiredListDataSetImportHistoryRequestListDataSetImportHistoryPaginateTypeDef,
    _OptionalListDataSetImportHistoryRequestListDataSetImportHistoryPaginateTypeDef,
):
    pass


_RequiredListDataSetImportHistoryRequestRequestTypeDef = TypedDict(
    "_RequiredListDataSetImportHistoryRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalListDataSetImportHistoryRequestRequestTypeDef = TypedDict(
    "_OptionalListDataSetImportHistoryRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListDataSetImportHistoryRequestRequestTypeDef(
    _RequiredListDataSetImportHistoryRequestRequestTypeDef,
    _OptionalListDataSetImportHistoryRequestRequestTypeDef,
):
    pass


_RequiredListDataSetsRequestListDataSetsPaginateTypeDef = TypedDict(
    "_RequiredListDataSetsRequestListDataSetsPaginateTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalListDataSetsRequestListDataSetsPaginateTypeDef = TypedDict(
    "_OptionalListDataSetsRequestListDataSetsPaginateTypeDef",
    {
        "prefix": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListDataSetsRequestListDataSetsPaginateTypeDef(
    _RequiredListDataSetsRequestListDataSetsPaginateTypeDef,
    _OptionalListDataSetsRequestListDataSetsPaginateTypeDef,
):
    pass


_RequiredListDataSetsRequestRequestTypeDef = TypedDict(
    "_RequiredListDataSetsRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalListDataSetsRequestRequestTypeDef = TypedDict(
    "_OptionalListDataSetsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "prefix": str,
    },
    total=False,
)


class ListDataSetsRequestRequestTypeDef(
    _RequiredListDataSetsRequestRequestTypeDef, _OptionalListDataSetsRequestRequestTypeDef
):
    pass


_RequiredListDeploymentsRequestListDeploymentsPaginateTypeDef = TypedDict(
    "_RequiredListDeploymentsRequestListDeploymentsPaginateTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalListDeploymentsRequestListDeploymentsPaginateTypeDef = TypedDict(
    "_OptionalListDeploymentsRequestListDeploymentsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListDeploymentsRequestListDeploymentsPaginateTypeDef(
    _RequiredListDeploymentsRequestListDeploymentsPaginateTypeDef,
    _OptionalListDeploymentsRequestListDeploymentsPaginateTypeDef,
):
    pass


_RequiredListDeploymentsRequestRequestTypeDef = TypedDict(
    "_RequiredListDeploymentsRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalListDeploymentsRequestRequestTypeDef = TypedDict(
    "_OptionalListDeploymentsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)


class ListDeploymentsRequestRequestTypeDef(
    _RequiredListDeploymentsRequestRequestTypeDef, _OptionalListDeploymentsRequestRequestTypeDef
):
    pass


ListEngineVersionsRequestListEngineVersionsPaginateTypeDef = TypedDict(
    "ListEngineVersionsRequestListEngineVersionsPaginateTypeDef",
    {
        "engineType": EngineTypeType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEngineVersionsRequestRequestTypeDef = TypedDict(
    "ListEngineVersionsRequestRequestTypeDef",
    {
        "engineType": EngineTypeType,
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

ListEnvironmentsRequestListEnvironmentsPaginateTypeDef = TypedDict(
    "ListEnvironmentsRequestListEnvironmentsPaginateTypeDef",
    {
        "engineType": EngineTypeType,
        "names": Sequence[str],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListEnvironmentsRequestRequestTypeDef = TypedDict(
    "ListEnvironmentsRequestRequestTypeDef",
    {
        "engineType": EngineTypeType,
        "maxResults": int,
        "names": Sequence[str],
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

MaintenanceScheduleTypeDef = TypedDict(
    "MaintenanceScheduleTypeDef",
    {
        "endTime": datetime,
        "startTime": datetime,
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

_RequiredPrimaryKeyTypeDef = TypedDict(
    "_RequiredPrimaryKeyTypeDef",
    {
        "length": int,
        "offset": int,
    },
)
_OptionalPrimaryKeyTypeDef = TypedDict(
    "_OptionalPrimaryKeyTypeDef",
    {
        "name": str,
    },
    total=False,
)


class PrimaryKeyTypeDef(_RequiredPrimaryKeyTypeDef, _OptionalPrimaryKeyTypeDef):
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

StartApplicationRequestRequestTypeDef = TypedDict(
    "StartApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)

StartBatchJobResponseTypeDef = TypedDict(
    "StartBatchJobResponseTypeDef",
    {
        "executionId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredStopApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredStopApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
    },
)
_OptionalStopApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalStopApplicationRequestRequestTypeDef",
    {
        "forceStop": bool,
    },
    total=False,
)


class StopApplicationRequestRequestTypeDef(
    _RequiredStopApplicationRequestRequestTypeDef, _OptionalStopApplicationRequestRequestTypeDef
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

UpdateApplicationResponseTypeDef = TypedDict(
    "UpdateApplicationResponseTypeDef",
    {
        "applicationVersion": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateEnvironmentRequestRequestTypeDef",
    {
        "environmentId": str,
    },
)
_OptionalUpdateEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateEnvironmentRequestRequestTypeDef",
    {
        "applyDuringMaintenanceWindow": bool,
        "desiredCapacity": int,
        "engineVersion": str,
        "instanceType": str,
        "preferredMaintenanceWindow": str,
    },
    total=False,
)


class UpdateEnvironmentRequestRequestTypeDef(
    _RequiredUpdateEnvironmentRequestRequestTypeDef, _OptionalUpdateEnvironmentRequestRequestTypeDef
):
    pass


UpdateEnvironmentResponseTypeDef = TypedDict(
    "UpdateEnvironmentResponseTypeDef",
    {
        "environmentId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListApplicationsResponseTypeDef = TypedDict(
    "ListApplicationsResponseTypeDef",
    {
        "applications": List[ApplicationSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListApplicationVersionsResponseTypeDef = TypedDict(
    "ListApplicationVersionsResponseTypeDef",
    {
        "applicationVersions": List[ApplicationVersionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchJobDefinitionTypeDef = TypedDict(
    "BatchJobDefinitionTypeDef",
    {
        "fileBatchJobDefinition": FileBatchJobDefinitionTypeDef,
        "scriptBatchJobDefinition": ScriptBatchJobDefinitionTypeDef,
    },
    total=False,
)

BatchJobIdentifierTypeDef = TypedDict(
    "BatchJobIdentifierTypeDef",
    {
        "fileBatchJobIdentifier": FileBatchJobIdentifierTypeDef,
        "scriptBatchJobIdentifier": ScriptBatchJobIdentifierTypeDef,
    },
    total=False,
)

_RequiredCreateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredCreateApplicationRequestRequestTypeDef",
    {
        "definition": DefinitionTypeDef,
        "engineType": EngineTypeType,
        "name": str,
    },
)
_OptionalCreateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalCreateApplicationRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "kmsKeyId": str,
        "roleArn": str,
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateApplicationRequestRequestTypeDef(
    _RequiredCreateApplicationRequestRequestTypeDef, _OptionalCreateApplicationRequestRequestTypeDef
):
    pass


_RequiredUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateApplicationRequestRequestTypeDef",
    {
        "applicationId": str,
        "currentApplicationVersion": int,
    },
)
_OptionalUpdateApplicationRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateApplicationRequestRequestTypeDef",
    {
        "definition": DefinitionTypeDef,
        "description": str,
    },
    total=False,
)


class UpdateApplicationRequestRequestTypeDef(
    _RequiredUpdateApplicationRequestRequestTypeDef, _OptionalUpdateApplicationRequestRequestTypeDef
):
    pass


DataSetImportTaskTypeDef = TypedDict(
    "DataSetImportTaskTypeDef",
    {
        "status": DataSetTaskLifecycleType,
        "summary": DataSetImportSummaryTypeDef,
        "taskId": str,
    },
)

GetDataSetImportTaskResponseTypeDef = TypedDict(
    "GetDataSetImportTaskResponseTypeDef",
    {
        "status": DataSetTaskLifecycleType,
        "summary": DataSetImportSummaryTypeDef,
        "taskId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDataSetsResponseTypeDef = TypedDict(
    "ListDataSetsResponseTypeDef",
    {
        "dataSets": List[DataSetSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListDeploymentsResponseTypeDef = TypedDict(
    "ListDeploymentsResponseTypeDef",
    {
        "deployments": List[DeploymentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEngineVersionsResponseTypeDef = TypedDict(
    "ListEngineVersionsResponseTypeDef",
    {
        "engineVersions": List[EngineVersionsSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListEnvironmentsResponseTypeDef = TypedDict(
    "ListEnvironmentsResponseTypeDef",
    {
        "environments": List[EnvironmentSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StorageConfigurationTypeDef = TypedDict(
    "StorageConfigurationTypeDef",
    {
        "efs": EfsStorageConfigurationTypeDef,
        "fsx": FsxStorageConfigurationTypeDef,
    },
    total=False,
)

GetApplicationResponseTypeDef = TypedDict(
    "GetApplicationResponseTypeDef",
    {
        "applicationArn": str,
        "applicationId": str,
        "creationTime": datetime,
        "deployedVersion": DeployedVersionSummaryTypeDef,
        "description": str,
        "engineType": EngineTypeType,
        "environmentId": str,
        "kmsKeyId": str,
        "lastStartTime": datetime,
        "latestVersion": ApplicationVersionSummaryTypeDef,
        "listenerArns": List[str],
        "listenerPorts": List[int],
        "loadBalancerDnsName": str,
        "logGroups": List[LogGroupSummaryTypeDef],
        "name": str,
        "roleArn": str,
        "status": ApplicationLifecycleType,
        "statusReason": str,
        "tags": Dict[str, str],
        "targetGroupArns": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PendingMaintenanceTypeDef = TypedDict(
    "PendingMaintenanceTypeDef",
    {
        "engineVersion": str,
        "schedule": MaintenanceScheduleTypeDef,
    },
    total=False,
)

_RequiredVsamAttributesTypeDef = TypedDict(
    "_RequiredVsamAttributesTypeDef",
    {
        "format": str,
    },
)
_OptionalVsamAttributesTypeDef = TypedDict(
    "_OptionalVsamAttributesTypeDef",
    {
        "alternateKeys": Sequence[AlternateKeyTypeDef],
        "compressed": bool,
        "encoding": str,
        "primaryKey": PrimaryKeyTypeDef,
    },
    total=False,
)


class VsamAttributesTypeDef(_RequiredVsamAttributesTypeDef, _OptionalVsamAttributesTypeDef):
    pass


VsamDetailAttributesTypeDef = TypedDict(
    "VsamDetailAttributesTypeDef",
    {
        "alternateKeys": List[AlternateKeyTypeDef],
        "cacheAtStartup": bool,
        "compressed": bool,
        "encoding": str,
        "primaryKey": PrimaryKeyTypeDef,
        "recordFormat": str,
    },
    total=False,
)

ListBatchJobDefinitionsResponseTypeDef = TypedDict(
    "ListBatchJobDefinitionsResponseTypeDef",
    {
        "batchJobDefinitions": List[BatchJobDefinitionTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredBatchJobExecutionSummaryTypeDef = TypedDict(
    "_RequiredBatchJobExecutionSummaryTypeDef",
    {
        "applicationId": str,
        "executionId": str,
        "startTime": datetime,
        "status": BatchJobExecutionStatusType,
    },
)
_OptionalBatchJobExecutionSummaryTypeDef = TypedDict(
    "_OptionalBatchJobExecutionSummaryTypeDef",
    {
        "batchJobIdentifier": BatchJobIdentifierTypeDef,
        "endTime": datetime,
        "jobId": str,
        "jobName": str,
        "jobType": BatchJobTypeType,
        "returnCode": str,
    },
    total=False,
)


class BatchJobExecutionSummaryTypeDef(
    _RequiredBatchJobExecutionSummaryTypeDef, _OptionalBatchJobExecutionSummaryTypeDef
):
    pass


GetBatchJobExecutionResponseTypeDef = TypedDict(
    "GetBatchJobExecutionResponseTypeDef",
    {
        "applicationId": str,
        "batchJobIdentifier": BatchJobIdentifierTypeDef,
        "endTime": datetime,
        "executionId": str,
        "jobId": str,
        "jobName": str,
        "jobType": BatchJobTypeType,
        "jobUser": str,
        "returnCode": str,
        "startTime": datetime,
        "status": BatchJobExecutionStatusType,
        "statusReason": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredStartBatchJobRequestRequestTypeDef = TypedDict(
    "_RequiredStartBatchJobRequestRequestTypeDef",
    {
        "applicationId": str,
        "batchJobIdentifier": BatchJobIdentifierTypeDef,
    },
)
_OptionalStartBatchJobRequestRequestTypeDef = TypedDict(
    "_OptionalStartBatchJobRequestRequestTypeDef",
    {
        "jobParams": Mapping[str, str],
    },
    total=False,
)


class StartBatchJobRequestRequestTypeDef(
    _RequiredStartBatchJobRequestRequestTypeDef, _OptionalStartBatchJobRequestRequestTypeDef
):
    pass


ListDataSetImportHistoryResponseTypeDef = TypedDict(
    "ListDataSetImportHistoryResponseTypeDef",
    {
        "dataSetImportTasks": List[DataSetImportTaskTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateEnvironmentRequestRequestTypeDef = TypedDict(
    "_RequiredCreateEnvironmentRequestRequestTypeDef",
    {
        "engineType": EngineTypeType,
        "instanceType": str,
        "name": str,
    },
)
_OptionalCreateEnvironmentRequestRequestTypeDef = TypedDict(
    "_OptionalCreateEnvironmentRequestRequestTypeDef",
    {
        "clientToken": str,
        "description": str,
        "engineVersion": str,
        "highAvailabilityConfig": HighAvailabilityConfigTypeDef,
        "kmsKeyId": str,
        "preferredMaintenanceWindow": str,
        "publiclyAccessible": bool,
        "securityGroupIds": Sequence[str],
        "storageConfigurations": Sequence[StorageConfigurationTypeDef],
        "subnetIds": Sequence[str],
        "tags": Mapping[str, str],
    },
    total=False,
)


class CreateEnvironmentRequestRequestTypeDef(
    _RequiredCreateEnvironmentRequestRequestTypeDef, _OptionalCreateEnvironmentRequestRequestTypeDef
):
    pass


GetEnvironmentResponseTypeDef = TypedDict(
    "GetEnvironmentResponseTypeDef",
    {
        "actualCapacity": int,
        "creationTime": datetime,
        "description": str,
        "engineType": EngineTypeType,
        "engineVersion": str,
        "environmentArn": str,
        "environmentId": str,
        "highAvailabilityConfig": HighAvailabilityConfigTypeDef,
        "instanceType": str,
        "kmsKeyId": str,
        "loadBalancerArn": str,
        "name": str,
        "pendingMaintenance": PendingMaintenanceTypeDef,
        "preferredMaintenanceWindow": str,
        "publiclyAccessible": bool,
        "securityGroupIds": List[str],
        "status": EnvironmentLifecycleType,
        "statusReason": str,
        "storageConfigurations": List[StorageConfigurationTypeDef],
        "subnetIds": List[str],
        "tags": Dict[str, str],
        "vpcId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DatasetOrgAttributesTypeDef = TypedDict(
    "DatasetOrgAttributesTypeDef",
    {
        "gdg": GdgAttributesTypeDef,
        "po": PoAttributesTypeDef,
        "ps": PsAttributesTypeDef,
        "vsam": VsamAttributesTypeDef,
    },
    total=False,
)

DatasetDetailOrgAttributesTypeDef = TypedDict(
    "DatasetDetailOrgAttributesTypeDef",
    {
        "gdg": GdgDetailAttributesTypeDef,
        "po": PoDetailAttributesTypeDef,
        "ps": PsDetailAttributesTypeDef,
        "vsam": VsamDetailAttributesTypeDef,
    },
    total=False,
)

ListBatchJobExecutionsResponseTypeDef = TypedDict(
    "ListBatchJobExecutionsResponseTypeDef",
    {
        "batchJobExecutions": List[BatchJobExecutionSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredDataSetTypeDef = TypedDict(
    "_RequiredDataSetTypeDef",
    {
        "datasetName": str,
        "datasetOrg": DatasetOrgAttributesTypeDef,
        "recordLength": RecordLengthTypeDef,
    },
)
_OptionalDataSetTypeDef = TypedDict(
    "_OptionalDataSetTypeDef",
    {
        "relativePath": str,
        "storageType": str,
    },
    total=False,
)


class DataSetTypeDef(_RequiredDataSetTypeDef, _OptionalDataSetTypeDef):
    pass


GetDataSetDetailsResponseTypeDef = TypedDict(
    "GetDataSetDetailsResponseTypeDef",
    {
        "blocksize": int,
        "creationTime": datetime,
        "dataSetName": str,
        "dataSetOrg": DatasetDetailOrgAttributesTypeDef,
        "lastReferencedTime": datetime,
        "lastUpdatedTime": datetime,
        "location": str,
        "recordLength": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DataSetImportItemTypeDef = TypedDict(
    "DataSetImportItemTypeDef",
    {
        "dataSet": DataSetTypeDef,
        "externalLocation": ExternalLocationTypeDef,
    },
)

DataSetImportConfigTypeDef = TypedDict(
    "DataSetImportConfigTypeDef",
    {
        "dataSets": Sequence[DataSetImportItemTypeDef],
        "s3Location": str,
    },
    total=False,
)

_RequiredCreateDataSetImportTaskRequestRequestTypeDef = TypedDict(
    "_RequiredCreateDataSetImportTaskRequestRequestTypeDef",
    {
        "applicationId": str,
        "importConfig": DataSetImportConfigTypeDef,
    },
)
_OptionalCreateDataSetImportTaskRequestRequestTypeDef = TypedDict(
    "_OptionalCreateDataSetImportTaskRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)


class CreateDataSetImportTaskRequestRequestTypeDef(
    _RequiredCreateDataSetImportTaskRequestRequestTypeDef,
    _OptionalCreateDataSetImportTaskRequestRequestTypeDef,
):
    pass
