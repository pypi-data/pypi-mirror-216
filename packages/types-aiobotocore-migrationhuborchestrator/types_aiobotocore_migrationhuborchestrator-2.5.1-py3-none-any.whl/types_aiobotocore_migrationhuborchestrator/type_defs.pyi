"""
Type annotations for migrationhuborchestrator service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_migrationhuborchestrator/type_defs/)

Usage::

    ```python
    from types_aiobotocore_migrationhuborchestrator.type_defs import StepInputTypeDef

    data: StepInputTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence

from .literals import (
    DataTypeType,
    MigrationWorkflowStatusEnumType,
    OwnerType,
    PluginHealthType,
    RunEnvironmentType,
    StepActionTypeType,
    StepGroupStatusType,
    StepStatusType,
    TargetTypeType,
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
    "StepInputTypeDef",
    "CreateWorkflowStepGroupRequestRequestTypeDef",
    "ToolTypeDef",
    "CreateWorkflowStepResponseTypeDef",
    "DeleteMigrationWorkflowRequestRequestTypeDef",
    "DeleteMigrationWorkflowResponseTypeDef",
    "DeleteWorkflowStepGroupRequestRequestTypeDef",
    "DeleteWorkflowStepRequestRequestTypeDef",
    "GetMigrationWorkflowRequestRequestTypeDef",
    "GetMigrationWorkflowTemplateRequestRequestTypeDef",
    "TemplateInputTypeDef",
    "GetTemplateStepGroupRequestRequestTypeDef",
    "GetTemplateStepRequestRequestTypeDef",
    "StepOutputTypeDef",
    "GetWorkflowStepGroupRequestRequestTypeDef",
    "GetWorkflowStepRequestRequestTypeDef",
    "ListMigrationWorkflowTemplatesRequestListTemplatesPaginateTypeDef",
    "ListMigrationWorkflowTemplatesRequestRequestTypeDef",
    "TemplateSummaryTypeDef",
    "ListMigrationWorkflowsRequestListWorkflowsPaginateTypeDef",
    "ListMigrationWorkflowsRequestRequestTypeDef",
    "MigrationWorkflowSummaryTypeDef",
    "ListPluginsRequestListPluginsPaginateTypeDef",
    "ListPluginsRequestRequestTypeDef",
    "PluginSummaryTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTemplateStepGroupsRequestListTemplateStepGroupsPaginateTypeDef",
    "ListTemplateStepGroupsRequestRequestTypeDef",
    "TemplateStepGroupSummaryTypeDef",
    "ListTemplateStepsRequestListTemplateStepsPaginateTypeDef",
    "ListTemplateStepsRequestRequestTypeDef",
    "TemplateStepSummaryTypeDef",
    "ListWorkflowStepGroupsRequestListWorkflowStepGroupsPaginateTypeDef",
    "ListWorkflowStepGroupsRequestRequestTypeDef",
    "WorkflowStepGroupSummaryTypeDef",
    "ListWorkflowStepsRequestListWorkflowStepsPaginateTypeDef",
    "ListWorkflowStepsRequestRequestTypeDef",
    "WorkflowStepSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "PlatformCommandTypeDef",
    "PlatformScriptKeyTypeDef",
    "ResponseMetadataTypeDef",
    "RetryWorkflowStepRequestRequestTypeDef",
    "RetryWorkflowStepResponseTypeDef",
    "StartMigrationWorkflowRequestRequestTypeDef",
    "StartMigrationWorkflowResponseTypeDef",
    "StopMigrationWorkflowRequestRequestTypeDef",
    "StopMigrationWorkflowResponseTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateWorkflowStepGroupRequestRequestTypeDef",
    "UpdateWorkflowStepResponseTypeDef",
    "WorkflowStepOutputUnionTypeDef",
    "CreateMigrationWorkflowRequestRequestTypeDef",
    "CreateMigrationWorkflowResponseTypeDef",
    "UpdateMigrationWorkflowRequestRequestTypeDef",
    "UpdateMigrationWorkflowResponseTypeDef",
    "CreateWorkflowStepGroupResponseTypeDef",
    "GetMigrationWorkflowResponseTypeDef",
    "GetTemplateStepGroupResponseTypeDef",
    "GetWorkflowStepGroupResponseTypeDef",
    "UpdateWorkflowStepGroupResponseTypeDef",
    "GetMigrationWorkflowTemplateResponseTypeDef",
    "ListMigrationWorkflowTemplatesResponseTypeDef",
    "ListMigrationWorkflowsResponseTypeDef",
    "ListPluginsResponseTypeDef",
    "ListTemplateStepGroupsResponseTypeDef",
    "ListTemplateStepsResponseTypeDef",
    "ListWorkflowStepGroupsResponseTypeDef",
    "ListWorkflowStepsResponseTypeDef",
    "StepAutomationConfigurationTypeDef",
    "WorkflowStepAutomationConfigurationTypeDef",
    "WorkflowStepOutputTypeDef",
    "GetTemplateStepResponseTypeDef",
    "CreateWorkflowStepRequestRequestTypeDef",
    "GetWorkflowStepResponseTypeDef",
    "UpdateWorkflowStepRequestRequestTypeDef",
)

StepInputTypeDef = TypedDict(
    "StepInputTypeDef",
    {
        "integerValue": int,
        "stringValue": str,
        "listOfStringsValue": Sequence[str],
        "mapOfStringValue": Mapping[str, str],
    },
    total=False,
)

_RequiredCreateWorkflowStepGroupRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWorkflowStepGroupRequestRequestTypeDef",
    {
        "workflowId": str,
        "name": str,
    },
)
_OptionalCreateWorkflowStepGroupRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWorkflowStepGroupRequestRequestTypeDef",
    {
        "description": str,
        "next": Sequence[str],
        "previous": Sequence[str],
    },
    total=False,
)

class CreateWorkflowStepGroupRequestRequestTypeDef(
    _RequiredCreateWorkflowStepGroupRequestRequestTypeDef,
    _OptionalCreateWorkflowStepGroupRequestRequestTypeDef,
):
    pass

ToolTypeDef = TypedDict(
    "ToolTypeDef",
    {
        "name": str,
        "url": str,
    },
    total=False,
)

CreateWorkflowStepResponseTypeDef = TypedDict(
    "CreateWorkflowStepResponseTypeDef",
    {
        "id": str,
        "stepGroupId": str,
        "workflowId": str,
        "name": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteMigrationWorkflowRequestRequestTypeDef = TypedDict(
    "DeleteMigrationWorkflowRequestRequestTypeDef",
    {
        "id": str,
    },
)

DeleteMigrationWorkflowResponseTypeDef = TypedDict(
    "DeleteMigrationWorkflowResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "status": MigrationWorkflowStatusEnumType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteWorkflowStepGroupRequestRequestTypeDef = TypedDict(
    "DeleteWorkflowStepGroupRequestRequestTypeDef",
    {
        "workflowId": str,
        "id": str,
    },
)

DeleteWorkflowStepRequestRequestTypeDef = TypedDict(
    "DeleteWorkflowStepRequestRequestTypeDef",
    {
        "id": str,
        "stepGroupId": str,
        "workflowId": str,
    },
)

GetMigrationWorkflowRequestRequestTypeDef = TypedDict(
    "GetMigrationWorkflowRequestRequestTypeDef",
    {
        "id": str,
    },
)

GetMigrationWorkflowTemplateRequestRequestTypeDef = TypedDict(
    "GetMigrationWorkflowTemplateRequestRequestTypeDef",
    {
        "id": str,
    },
)

TemplateInputTypeDef = TypedDict(
    "TemplateInputTypeDef",
    {
        "inputName": str,
        "dataType": DataTypeType,
        "required": bool,
    },
    total=False,
)

GetTemplateStepGroupRequestRequestTypeDef = TypedDict(
    "GetTemplateStepGroupRequestRequestTypeDef",
    {
        "templateId": str,
        "id": str,
    },
)

GetTemplateStepRequestRequestTypeDef = TypedDict(
    "GetTemplateStepRequestRequestTypeDef",
    {
        "id": str,
        "templateId": str,
        "stepGroupId": str,
    },
)

StepOutputTypeDef = TypedDict(
    "StepOutputTypeDef",
    {
        "name": str,
        "dataType": DataTypeType,
        "required": bool,
    },
    total=False,
)

GetWorkflowStepGroupRequestRequestTypeDef = TypedDict(
    "GetWorkflowStepGroupRequestRequestTypeDef",
    {
        "id": str,
        "workflowId": str,
    },
)

GetWorkflowStepRequestRequestTypeDef = TypedDict(
    "GetWorkflowStepRequestRequestTypeDef",
    {
        "workflowId": str,
        "stepGroupId": str,
        "id": str,
    },
)

ListMigrationWorkflowTemplatesRequestListTemplatesPaginateTypeDef = TypedDict(
    "ListMigrationWorkflowTemplatesRequestListTemplatesPaginateTypeDef",
    {
        "name": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListMigrationWorkflowTemplatesRequestRequestTypeDef = TypedDict(
    "ListMigrationWorkflowTemplatesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "name": str,
    },
    total=False,
)

TemplateSummaryTypeDef = TypedDict(
    "TemplateSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "arn": str,
        "description": str,
    },
    total=False,
)

ListMigrationWorkflowsRequestListWorkflowsPaginateTypeDef = TypedDict(
    "ListMigrationWorkflowsRequestListWorkflowsPaginateTypeDef",
    {
        "templateId": str,
        "adsApplicationConfigurationName": str,
        "status": MigrationWorkflowStatusEnumType,
        "name": str,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListMigrationWorkflowsRequestRequestTypeDef = TypedDict(
    "ListMigrationWorkflowsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "templateId": str,
        "adsApplicationConfigurationName": str,
        "status": MigrationWorkflowStatusEnumType,
        "name": str,
    },
    total=False,
)

MigrationWorkflowSummaryTypeDef = TypedDict(
    "MigrationWorkflowSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "templateId": str,
        "adsApplicationConfigurationName": str,
        "status": MigrationWorkflowStatusEnumType,
        "creationTime": datetime,
        "endTime": datetime,
        "statusMessage": str,
        "completedSteps": int,
        "totalSteps": int,
    },
    total=False,
)

ListPluginsRequestListPluginsPaginateTypeDef = TypedDict(
    "ListPluginsRequestListPluginsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListPluginsRequestRequestTypeDef = TypedDict(
    "ListPluginsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

PluginSummaryTypeDef = TypedDict(
    "PluginSummaryTypeDef",
    {
        "pluginId": str,
        "hostname": str,
        "status": PluginHealthType,
        "ipAddress": str,
        "version": str,
        "registeredTime": str,
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

_RequiredListTemplateStepGroupsRequestListTemplateStepGroupsPaginateTypeDef = TypedDict(
    "_RequiredListTemplateStepGroupsRequestListTemplateStepGroupsPaginateTypeDef",
    {
        "templateId": str,
    },
)
_OptionalListTemplateStepGroupsRequestListTemplateStepGroupsPaginateTypeDef = TypedDict(
    "_OptionalListTemplateStepGroupsRequestListTemplateStepGroupsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListTemplateStepGroupsRequestListTemplateStepGroupsPaginateTypeDef(
    _RequiredListTemplateStepGroupsRequestListTemplateStepGroupsPaginateTypeDef,
    _OptionalListTemplateStepGroupsRequestListTemplateStepGroupsPaginateTypeDef,
):
    pass

_RequiredListTemplateStepGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListTemplateStepGroupsRequestRequestTypeDef",
    {
        "templateId": str,
    },
)
_OptionalListTemplateStepGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListTemplateStepGroupsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListTemplateStepGroupsRequestRequestTypeDef(
    _RequiredListTemplateStepGroupsRequestRequestTypeDef,
    _OptionalListTemplateStepGroupsRequestRequestTypeDef,
):
    pass

TemplateStepGroupSummaryTypeDef = TypedDict(
    "TemplateStepGroupSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "previous": List[str],
        "next": List[str],
    },
    total=False,
)

_RequiredListTemplateStepsRequestListTemplateStepsPaginateTypeDef = TypedDict(
    "_RequiredListTemplateStepsRequestListTemplateStepsPaginateTypeDef",
    {
        "templateId": str,
        "stepGroupId": str,
    },
)
_OptionalListTemplateStepsRequestListTemplateStepsPaginateTypeDef = TypedDict(
    "_OptionalListTemplateStepsRequestListTemplateStepsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListTemplateStepsRequestListTemplateStepsPaginateTypeDef(
    _RequiredListTemplateStepsRequestListTemplateStepsPaginateTypeDef,
    _OptionalListTemplateStepsRequestListTemplateStepsPaginateTypeDef,
):
    pass

_RequiredListTemplateStepsRequestRequestTypeDef = TypedDict(
    "_RequiredListTemplateStepsRequestRequestTypeDef",
    {
        "templateId": str,
        "stepGroupId": str,
    },
)
_OptionalListTemplateStepsRequestRequestTypeDef = TypedDict(
    "_OptionalListTemplateStepsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListTemplateStepsRequestRequestTypeDef(
    _RequiredListTemplateStepsRequestRequestTypeDef, _OptionalListTemplateStepsRequestRequestTypeDef
):
    pass

TemplateStepSummaryTypeDef = TypedDict(
    "TemplateStepSummaryTypeDef",
    {
        "id": str,
        "stepGroupId": str,
        "templateId": str,
        "name": str,
        "stepActionType": StepActionTypeType,
        "targetType": TargetTypeType,
        "owner": OwnerType,
        "previous": List[str],
        "next": List[str],
    },
    total=False,
)

_RequiredListWorkflowStepGroupsRequestListWorkflowStepGroupsPaginateTypeDef = TypedDict(
    "_RequiredListWorkflowStepGroupsRequestListWorkflowStepGroupsPaginateTypeDef",
    {
        "workflowId": str,
    },
)
_OptionalListWorkflowStepGroupsRequestListWorkflowStepGroupsPaginateTypeDef = TypedDict(
    "_OptionalListWorkflowStepGroupsRequestListWorkflowStepGroupsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListWorkflowStepGroupsRequestListWorkflowStepGroupsPaginateTypeDef(
    _RequiredListWorkflowStepGroupsRequestListWorkflowStepGroupsPaginateTypeDef,
    _OptionalListWorkflowStepGroupsRequestListWorkflowStepGroupsPaginateTypeDef,
):
    pass

_RequiredListWorkflowStepGroupsRequestRequestTypeDef = TypedDict(
    "_RequiredListWorkflowStepGroupsRequestRequestTypeDef",
    {
        "workflowId": str,
    },
)
_OptionalListWorkflowStepGroupsRequestRequestTypeDef = TypedDict(
    "_OptionalListWorkflowStepGroupsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListWorkflowStepGroupsRequestRequestTypeDef(
    _RequiredListWorkflowStepGroupsRequestRequestTypeDef,
    _OptionalListWorkflowStepGroupsRequestRequestTypeDef,
):
    pass

WorkflowStepGroupSummaryTypeDef = TypedDict(
    "WorkflowStepGroupSummaryTypeDef",
    {
        "id": str,
        "name": str,
        "owner": OwnerType,
        "status": StepGroupStatusType,
        "previous": List[str],
        "next": List[str],
    },
    total=False,
)

_RequiredListWorkflowStepsRequestListWorkflowStepsPaginateTypeDef = TypedDict(
    "_RequiredListWorkflowStepsRequestListWorkflowStepsPaginateTypeDef",
    {
        "workflowId": str,
        "stepGroupId": str,
    },
)
_OptionalListWorkflowStepsRequestListWorkflowStepsPaginateTypeDef = TypedDict(
    "_OptionalListWorkflowStepsRequestListWorkflowStepsPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class ListWorkflowStepsRequestListWorkflowStepsPaginateTypeDef(
    _RequiredListWorkflowStepsRequestListWorkflowStepsPaginateTypeDef,
    _OptionalListWorkflowStepsRequestListWorkflowStepsPaginateTypeDef,
):
    pass

_RequiredListWorkflowStepsRequestRequestTypeDef = TypedDict(
    "_RequiredListWorkflowStepsRequestRequestTypeDef",
    {
        "workflowId": str,
        "stepGroupId": str,
    },
)
_OptionalListWorkflowStepsRequestRequestTypeDef = TypedDict(
    "_OptionalListWorkflowStepsRequestRequestTypeDef",
    {
        "nextToken": str,
        "maxResults": int,
    },
    total=False,
)

class ListWorkflowStepsRequestRequestTypeDef(
    _RequiredListWorkflowStepsRequestRequestTypeDef, _OptionalListWorkflowStepsRequestRequestTypeDef
):
    pass

WorkflowStepSummaryTypeDef = TypedDict(
    "WorkflowStepSummaryTypeDef",
    {
        "stepId": str,
        "name": str,
        "stepActionType": StepActionTypeType,
        "owner": OwnerType,
        "previous": List[str],
        "next": List[str],
        "status": StepStatusType,
        "statusMessage": str,
        "noOfSrvCompleted": int,
        "noOfSrvFailed": int,
        "totalNoOfSrv": int,
        "description": str,
        "scriptLocation": str,
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

PlatformCommandTypeDef = TypedDict(
    "PlatformCommandTypeDef",
    {
        "linux": str,
        "windows": str,
    },
    total=False,
)

PlatformScriptKeyTypeDef = TypedDict(
    "PlatformScriptKeyTypeDef",
    {
        "linux": str,
        "windows": str,
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

RetryWorkflowStepRequestRequestTypeDef = TypedDict(
    "RetryWorkflowStepRequestRequestTypeDef",
    {
        "workflowId": str,
        "stepGroupId": str,
        "id": str,
    },
)

RetryWorkflowStepResponseTypeDef = TypedDict(
    "RetryWorkflowStepResponseTypeDef",
    {
        "stepGroupId": str,
        "workflowId": str,
        "id": str,
        "status": StepStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartMigrationWorkflowRequestRequestTypeDef = TypedDict(
    "StartMigrationWorkflowRequestRequestTypeDef",
    {
        "id": str,
    },
)

StartMigrationWorkflowResponseTypeDef = TypedDict(
    "StartMigrationWorkflowResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "status": MigrationWorkflowStatusEnumType,
        "statusMessage": str,
        "lastStartTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopMigrationWorkflowRequestRequestTypeDef = TypedDict(
    "StopMigrationWorkflowRequestRequestTypeDef",
    {
        "id": str,
    },
)

StopMigrationWorkflowResponseTypeDef = TypedDict(
    "StopMigrationWorkflowResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "status": MigrationWorkflowStatusEnumType,
        "statusMessage": str,
        "lastStopTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
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

_RequiredUpdateWorkflowStepGroupRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWorkflowStepGroupRequestRequestTypeDef",
    {
        "workflowId": str,
        "id": str,
    },
)
_OptionalUpdateWorkflowStepGroupRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWorkflowStepGroupRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
        "next": Sequence[str],
        "previous": Sequence[str],
    },
    total=False,
)

class UpdateWorkflowStepGroupRequestRequestTypeDef(
    _RequiredUpdateWorkflowStepGroupRequestRequestTypeDef,
    _OptionalUpdateWorkflowStepGroupRequestRequestTypeDef,
):
    pass

UpdateWorkflowStepResponseTypeDef = TypedDict(
    "UpdateWorkflowStepResponseTypeDef",
    {
        "id": str,
        "stepGroupId": str,
        "workflowId": str,
        "name": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

WorkflowStepOutputUnionTypeDef = TypedDict(
    "WorkflowStepOutputUnionTypeDef",
    {
        "integerValue": int,
        "stringValue": str,
        "listOfStringValue": Sequence[str],
    },
    total=False,
)

_RequiredCreateMigrationWorkflowRequestRequestTypeDef = TypedDict(
    "_RequiredCreateMigrationWorkflowRequestRequestTypeDef",
    {
        "name": str,
        "templateId": str,
        "applicationConfigurationId": str,
        "inputParameters": Mapping[str, StepInputTypeDef],
    },
)
_OptionalCreateMigrationWorkflowRequestRequestTypeDef = TypedDict(
    "_OptionalCreateMigrationWorkflowRequestRequestTypeDef",
    {
        "description": str,
        "stepTargets": Sequence[str],
        "tags": Mapping[str, str],
    },
    total=False,
)

class CreateMigrationWorkflowRequestRequestTypeDef(
    _RequiredCreateMigrationWorkflowRequestRequestTypeDef,
    _OptionalCreateMigrationWorkflowRequestRequestTypeDef,
):
    pass

CreateMigrationWorkflowResponseTypeDef = TypedDict(
    "CreateMigrationWorkflowResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "templateId": str,
        "adsApplicationConfigurationId": str,
        "workflowInputs": Dict[str, StepInputTypeDef],
        "stepTargets": List[str],
        "status": MigrationWorkflowStatusEnumType,
        "creationTime": datetime,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateMigrationWorkflowRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateMigrationWorkflowRequestRequestTypeDef",
    {
        "id": str,
    },
)
_OptionalUpdateMigrationWorkflowRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateMigrationWorkflowRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
        "inputParameters": Mapping[str, StepInputTypeDef],
        "stepTargets": Sequence[str],
    },
    total=False,
)

class UpdateMigrationWorkflowRequestRequestTypeDef(
    _RequiredUpdateMigrationWorkflowRequestRequestTypeDef,
    _OptionalUpdateMigrationWorkflowRequestRequestTypeDef,
):
    pass

UpdateMigrationWorkflowResponseTypeDef = TypedDict(
    "UpdateMigrationWorkflowResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "templateId": str,
        "adsApplicationConfigurationId": str,
        "workflowInputs": Dict[str, StepInputTypeDef],
        "stepTargets": List[str],
        "status": MigrationWorkflowStatusEnumType,
        "creationTime": datetime,
        "lastModifiedTime": datetime,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateWorkflowStepGroupResponseTypeDef = TypedDict(
    "CreateWorkflowStepGroupResponseTypeDef",
    {
        "workflowId": str,
        "name": str,
        "id": str,
        "description": str,
        "tools": List[ToolTypeDef],
        "next": List[str],
        "previous": List[str],
        "creationTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetMigrationWorkflowResponseTypeDef = TypedDict(
    "GetMigrationWorkflowResponseTypeDef",
    {
        "id": str,
        "arn": str,
        "name": str,
        "description": str,
        "templateId": str,
        "adsApplicationConfigurationId": str,
        "adsApplicationName": str,
        "status": MigrationWorkflowStatusEnumType,
        "statusMessage": str,
        "creationTime": datetime,
        "lastStartTime": datetime,
        "lastStopTime": datetime,
        "lastModifiedTime": datetime,
        "endTime": datetime,
        "tools": List[ToolTypeDef],
        "totalSteps": int,
        "completedSteps": int,
        "workflowInputs": Dict[str, StepInputTypeDef],
        "tags": Dict[str, str],
        "workflowBucket": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetTemplateStepGroupResponseTypeDef = TypedDict(
    "GetTemplateStepGroupResponseTypeDef",
    {
        "templateId": str,
        "id": str,
        "name": str,
        "description": str,
        "status": StepGroupStatusType,
        "creationTime": datetime,
        "lastModifiedTime": datetime,
        "tools": List[ToolTypeDef],
        "previous": List[str],
        "next": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetWorkflowStepGroupResponseTypeDef = TypedDict(
    "GetWorkflowStepGroupResponseTypeDef",
    {
        "id": str,
        "workflowId": str,
        "name": str,
        "description": str,
        "status": StepGroupStatusType,
        "owner": OwnerType,
        "creationTime": datetime,
        "lastModifiedTime": datetime,
        "endTime": datetime,
        "tools": List[ToolTypeDef],
        "previous": List[str],
        "next": List[str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateWorkflowStepGroupResponseTypeDef = TypedDict(
    "UpdateWorkflowStepGroupResponseTypeDef",
    {
        "workflowId": str,
        "name": str,
        "id": str,
        "description": str,
        "tools": List[ToolTypeDef],
        "next": List[str],
        "previous": List[str],
        "lastModifiedTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetMigrationWorkflowTemplateResponseTypeDef = TypedDict(
    "GetMigrationWorkflowTemplateResponseTypeDef",
    {
        "id": str,
        "name": str,
        "description": str,
        "inputs": List[TemplateInputTypeDef],
        "tools": List[ToolTypeDef],
        "status": Literal["CREATED"],
        "creationTime": datetime,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMigrationWorkflowTemplatesResponseTypeDef = TypedDict(
    "ListMigrationWorkflowTemplatesResponseTypeDef",
    {
        "nextToken": str,
        "templateSummary": List[TemplateSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListMigrationWorkflowsResponseTypeDef = TypedDict(
    "ListMigrationWorkflowsResponseTypeDef",
    {
        "nextToken": str,
        "migrationWorkflowSummary": List[MigrationWorkflowSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListPluginsResponseTypeDef = TypedDict(
    "ListPluginsResponseTypeDef",
    {
        "nextToken": str,
        "plugins": List[PluginSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTemplateStepGroupsResponseTypeDef = TypedDict(
    "ListTemplateStepGroupsResponseTypeDef",
    {
        "nextToken": str,
        "templateStepGroupSummary": List[TemplateStepGroupSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTemplateStepsResponseTypeDef = TypedDict(
    "ListTemplateStepsResponseTypeDef",
    {
        "nextToken": str,
        "templateStepSummaryList": List[TemplateStepSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListWorkflowStepGroupsResponseTypeDef = TypedDict(
    "ListWorkflowStepGroupsResponseTypeDef",
    {
        "nextToken": str,
        "workflowStepGroupsSummary": List[WorkflowStepGroupSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListWorkflowStepsResponseTypeDef = TypedDict(
    "ListWorkflowStepsResponseTypeDef",
    {
        "nextToken": str,
        "workflowStepsSummary": List[WorkflowStepSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StepAutomationConfigurationTypeDef = TypedDict(
    "StepAutomationConfigurationTypeDef",
    {
        "scriptLocationS3Bucket": str,
        "scriptLocationS3Key": PlatformScriptKeyTypeDef,
        "command": PlatformCommandTypeDef,
        "runEnvironment": RunEnvironmentType,
        "targetType": TargetTypeType,
    },
    total=False,
)

WorkflowStepAutomationConfigurationTypeDef = TypedDict(
    "WorkflowStepAutomationConfigurationTypeDef",
    {
        "scriptLocationS3Bucket": str,
        "scriptLocationS3Key": PlatformScriptKeyTypeDef,
        "command": PlatformCommandTypeDef,
        "runEnvironment": RunEnvironmentType,
        "targetType": TargetTypeType,
    },
    total=False,
)

WorkflowStepOutputTypeDef = TypedDict(
    "WorkflowStepOutputTypeDef",
    {
        "name": str,
        "dataType": DataTypeType,
        "required": bool,
        "value": WorkflowStepOutputUnionTypeDef,
    },
    total=False,
)

GetTemplateStepResponseTypeDef = TypedDict(
    "GetTemplateStepResponseTypeDef",
    {
        "id": str,
        "stepGroupId": str,
        "templateId": str,
        "name": str,
        "description": str,
        "stepActionType": StepActionTypeType,
        "creationTime": str,
        "previous": List[str],
        "next": List[str],
        "outputs": List[StepOutputTypeDef],
        "stepAutomationConfiguration": StepAutomationConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateWorkflowStepRequestRequestTypeDef = TypedDict(
    "_RequiredCreateWorkflowStepRequestRequestTypeDef",
    {
        "name": str,
        "stepGroupId": str,
        "workflowId": str,
        "stepActionType": StepActionTypeType,
    },
)
_OptionalCreateWorkflowStepRequestRequestTypeDef = TypedDict(
    "_OptionalCreateWorkflowStepRequestRequestTypeDef",
    {
        "description": str,
        "workflowStepAutomationConfiguration": WorkflowStepAutomationConfigurationTypeDef,
        "stepTarget": Sequence[str],
        "outputs": Sequence[WorkflowStepOutputTypeDef],
        "previous": Sequence[str],
        "next": Sequence[str],
    },
    total=False,
)

class CreateWorkflowStepRequestRequestTypeDef(
    _RequiredCreateWorkflowStepRequestRequestTypeDef,
    _OptionalCreateWorkflowStepRequestRequestTypeDef,
):
    pass

GetWorkflowStepResponseTypeDef = TypedDict(
    "GetWorkflowStepResponseTypeDef",
    {
        "name": str,
        "stepGroupId": str,
        "workflowId": str,
        "stepId": str,
        "description": str,
        "stepActionType": StepActionTypeType,
        "owner": OwnerType,
        "workflowStepAutomationConfiguration": WorkflowStepAutomationConfigurationTypeDef,
        "stepTarget": List[str],
        "outputs": List[WorkflowStepOutputTypeDef],
        "previous": List[str],
        "next": List[str],
        "status": StepStatusType,
        "statusMessage": str,
        "scriptOutputLocation": str,
        "creationTime": datetime,
        "lastStartTime": datetime,
        "endTime": datetime,
        "noOfSrvCompleted": int,
        "noOfSrvFailed": int,
        "totalNoOfSrv": int,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateWorkflowStepRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateWorkflowStepRequestRequestTypeDef",
    {
        "id": str,
        "stepGroupId": str,
        "workflowId": str,
    },
)
_OptionalUpdateWorkflowStepRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateWorkflowStepRequestRequestTypeDef",
    {
        "name": str,
        "description": str,
        "stepActionType": StepActionTypeType,
        "workflowStepAutomationConfiguration": WorkflowStepAutomationConfigurationTypeDef,
        "stepTarget": Sequence[str],
        "outputs": Sequence[WorkflowStepOutputTypeDef],
        "previous": Sequence[str],
        "next": Sequence[str],
        "status": StepStatusType,
    },
    total=False,
)

class UpdateWorkflowStepRequestRequestTypeDef(
    _RequiredUpdateWorkflowStepRequestRequestTypeDef,
    _OptionalUpdateWorkflowStepRequestRequestTypeDef,
):
    pass
