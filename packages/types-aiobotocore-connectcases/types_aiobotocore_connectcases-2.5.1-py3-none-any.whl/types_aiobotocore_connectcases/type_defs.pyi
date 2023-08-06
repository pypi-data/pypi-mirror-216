"""
Type annotations for connectcases service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_connectcases/type_defs/)

Usage::

    ```python
    from types_aiobotocore_connectcases.type_defs import FieldIdentifierTypeDef

    data: FieldIdentifierTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Any, Dict, List, Mapping, Sequence

from .literals import (
    DomainStatusType,
    FieldNamespaceType,
    FieldTypeType,
    OrderType,
    RelatedItemTypeType,
    TemplateStatusType,
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
    "FieldIdentifierTypeDef",
    "FieldErrorTypeDef",
    "GetFieldResponseTypeDef",
    "FieldOptionTypeDef",
    "FieldOptionErrorTypeDef",
    "CaseSummaryTypeDef",
    "CommentContentTypeDef",
    "ContactContentTypeDef",
    "ContactFilterTypeDef",
    "ContactTypeDef",
    "CreateCaseResponseTypeDef",
    "CreateDomainRequestRequestTypeDef",
    "CreateDomainResponseTypeDef",
    "CreateFieldRequestRequestTypeDef",
    "CreateFieldResponseTypeDef",
    "CreateLayoutResponseTypeDef",
    "CreateRelatedItemResponseTypeDef",
    "LayoutConfigurationTypeDef",
    "RequiredFieldTypeDef",
    "CreateTemplateResponseTypeDef",
    "DeleteDomainRequestRequestTypeDef",
    "DomainSummaryTypeDef",
    "EmptyResponseMetadataTypeDef",
    "RelatedItemEventIncludedDataTypeDef",
    "FieldItemTypeDef",
    "FieldSummaryTypeDef",
    "FieldValueUnionTypeDef",
    "GetCaseEventConfigurationRequestRequestTypeDef",
    "GetDomainRequestRequestTypeDef",
    "GetDomainResponseTypeDef",
    "GetLayoutRequestRequestTypeDef",
    "GetTemplateRequestRequestTypeDef",
    "LayoutSummaryTypeDef",
    "ListCasesForContactRequestRequestTypeDef",
    "ListDomainsRequestRequestTypeDef",
    "ListFieldOptionsRequestRequestTypeDef",
    "ListFieldsRequestRequestTypeDef",
    "ListLayoutsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListTemplatesRequestRequestTypeDef",
    "TemplateSummaryTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SortTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateFieldRequestRequestTypeDef",
    "BatchGetFieldRequestRequestTypeDef",
    "CaseEventIncludedDataTypeDef",
    "GetCaseRequestRequestTypeDef",
    "BatchGetFieldResponseTypeDef",
    "BatchPutFieldOptionsRequestRequestTypeDef",
    "ListFieldOptionsResponseTypeDef",
    "BatchPutFieldOptionsResponseTypeDef",
    "ListCasesForContactResponseTypeDef",
    "RelatedItemContentTypeDef",
    "RelatedItemTypeFilterTypeDef",
    "RelatedItemInputContentTypeDef",
    "CreateTemplateRequestRequestTypeDef",
    "GetTemplateResponseTypeDef",
    "UpdateTemplateRequestRequestTypeDef",
    "ListDomainsResponseTypeDef",
    "FieldGroupTypeDef",
    "ListFieldsResponseTypeDef",
    "FieldValueTypeDef",
    "ListLayoutsResponseTypeDef",
    "ListTemplatesResponseTypeDef",
    "SearchCasesRequestRequestTypeDef",
    "SearchCasesRequestSearchCasesPaginateTypeDef",
    "EventIncludedDataTypeDef",
    "SearchRelatedItemsResponseItemTypeDef",
    "SearchRelatedItemsRequestRequestTypeDef",
    "SearchRelatedItemsRequestSearchRelatedItemsPaginateTypeDef",
    "CreateRelatedItemRequestRequestTypeDef",
    "SectionTypeDef",
    "CreateCaseRequestRequestTypeDef",
    "FieldFilterTypeDef",
    "GetCaseResponseTypeDef",
    "SearchCasesResponseItemTypeDef",
    "UpdateCaseRequestRequestTypeDef",
    "EventBridgeConfigurationTypeDef",
    "SearchRelatedItemsResponseTypeDef",
    "LayoutSectionsTypeDef",
    "CaseFilterTypeDef",
    "SearchCasesResponseTypeDef",
    "GetCaseEventConfigurationResponseTypeDef",
    "PutCaseEventConfigurationRequestRequestTypeDef",
    "BasicLayoutTypeDef",
    "LayoutContentTypeDef",
    "CreateLayoutRequestRequestTypeDef",
    "GetLayoutResponseTypeDef",
    "UpdateLayoutRequestRequestTypeDef",
)

FieldIdentifierTypeDef = TypedDict(
    "FieldIdentifierTypeDef",
    {
        "id": str,
    },
)

_RequiredFieldErrorTypeDef = TypedDict(
    "_RequiredFieldErrorTypeDef",
    {
        "errorCode": str,
        "id": str,
    },
)
_OptionalFieldErrorTypeDef = TypedDict(
    "_OptionalFieldErrorTypeDef",
    {
        "message": str,
    },
    total=False,
)

class FieldErrorTypeDef(_RequiredFieldErrorTypeDef, _OptionalFieldErrorTypeDef):
    pass

_RequiredGetFieldResponseTypeDef = TypedDict(
    "_RequiredGetFieldResponseTypeDef",
    {
        "fieldArn": str,
        "fieldId": str,
        "name": str,
        "namespace": FieldNamespaceType,
        "type": FieldTypeType,
    },
)
_OptionalGetFieldResponseTypeDef = TypedDict(
    "_OptionalGetFieldResponseTypeDef",
    {
        "description": str,
        "tags": Dict[str, str],
    },
    total=False,
)

class GetFieldResponseTypeDef(_RequiredGetFieldResponseTypeDef, _OptionalGetFieldResponseTypeDef):
    pass

FieldOptionTypeDef = TypedDict(
    "FieldOptionTypeDef",
    {
        "active": bool,
        "name": str,
        "value": str,
    },
)

FieldOptionErrorTypeDef = TypedDict(
    "FieldOptionErrorTypeDef",
    {
        "errorCode": str,
        "message": str,
        "value": str,
    },
)

CaseSummaryTypeDef = TypedDict(
    "CaseSummaryTypeDef",
    {
        "caseId": str,
        "templateId": str,
    },
)

CommentContentTypeDef = TypedDict(
    "CommentContentTypeDef",
    {
        "body": str,
        "contentType": Literal["Text/Plain"],
    },
)

ContactContentTypeDef = TypedDict(
    "ContactContentTypeDef",
    {
        "channel": str,
        "connectedToSystemTime": datetime,
        "contactArn": str,
    },
)

ContactFilterTypeDef = TypedDict(
    "ContactFilterTypeDef",
    {
        "channel": Sequence[str],
        "contactArn": str,
    },
    total=False,
)

ContactTypeDef = TypedDict(
    "ContactTypeDef",
    {
        "contactArn": str,
    },
)

CreateCaseResponseTypeDef = TypedDict(
    "CreateCaseResponseTypeDef",
    {
        "caseArn": str,
        "caseId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateDomainRequestRequestTypeDef = TypedDict(
    "CreateDomainRequestRequestTypeDef",
    {
        "name": str,
    },
)

CreateDomainResponseTypeDef = TypedDict(
    "CreateDomainResponseTypeDef",
    {
        "domainArn": str,
        "domainId": str,
        "domainStatus": DomainStatusType,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredCreateFieldRequestRequestTypeDef = TypedDict(
    "_RequiredCreateFieldRequestRequestTypeDef",
    {
        "domainId": str,
        "name": str,
        "type": FieldTypeType,
    },
)
_OptionalCreateFieldRequestRequestTypeDef = TypedDict(
    "_OptionalCreateFieldRequestRequestTypeDef",
    {
        "description": str,
    },
    total=False,
)

class CreateFieldRequestRequestTypeDef(
    _RequiredCreateFieldRequestRequestTypeDef, _OptionalCreateFieldRequestRequestTypeDef
):
    pass

CreateFieldResponseTypeDef = TypedDict(
    "CreateFieldResponseTypeDef",
    {
        "fieldArn": str,
        "fieldId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateLayoutResponseTypeDef = TypedDict(
    "CreateLayoutResponseTypeDef",
    {
        "layoutArn": str,
        "layoutId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateRelatedItemResponseTypeDef = TypedDict(
    "CreateRelatedItemResponseTypeDef",
    {
        "relatedItemArn": str,
        "relatedItemId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LayoutConfigurationTypeDef = TypedDict(
    "LayoutConfigurationTypeDef",
    {
        "defaultLayout": str,
    },
    total=False,
)

RequiredFieldTypeDef = TypedDict(
    "RequiredFieldTypeDef",
    {
        "fieldId": str,
    },
)

CreateTemplateResponseTypeDef = TypedDict(
    "CreateTemplateResponseTypeDef",
    {
        "templateArn": str,
        "templateId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteDomainRequestRequestTypeDef = TypedDict(
    "DeleteDomainRequestRequestTypeDef",
    {
        "domainId": str,
    },
)

DomainSummaryTypeDef = TypedDict(
    "DomainSummaryTypeDef",
    {
        "domainArn": str,
        "domainId": str,
        "name": str,
    },
)

EmptyResponseMetadataTypeDef = TypedDict(
    "EmptyResponseMetadataTypeDef",
    {
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RelatedItemEventIncludedDataTypeDef = TypedDict(
    "RelatedItemEventIncludedDataTypeDef",
    {
        "includeContent": bool,
    },
)

FieldItemTypeDef = TypedDict(
    "FieldItemTypeDef",
    {
        "id": str,
    },
)

FieldSummaryTypeDef = TypedDict(
    "FieldSummaryTypeDef",
    {
        "fieldArn": str,
        "fieldId": str,
        "name": str,
        "namespace": FieldNamespaceType,
        "type": FieldTypeType,
    },
)

FieldValueUnionTypeDef = TypedDict(
    "FieldValueUnionTypeDef",
    {
        "booleanValue": bool,
        "doubleValue": float,
        "stringValue": str,
    },
    total=False,
)

GetCaseEventConfigurationRequestRequestTypeDef = TypedDict(
    "GetCaseEventConfigurationRequestRequestTypeDef",
    {
        "domainId": str,
    },
)

GetDomainRequestRequestTypeDef = TypedDict(
    "GetDomainRequestRequestTypeDef",
    {
        "domainId": str,
    },
)

GetDomainResponseTypeDef = TypedDict(
    "GetDomainResponseTypeDef",
    {
        "createdTime": datetime,
        "domainArn": str,
        "domainId": str,
        "domainStatus": DomainStatusType,
        "name": str,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetLayoutRequestRequestTypeDef = TypedDict(
    "GetLayoutRequestRequestTypeDef",
    {
        "domainId": str,
        "layoutId": str,
    },
)

GetTemplateRequestRequestTypeDef = TypedDict(
    "GetTemplateRequestRequestTypeDef",
    {
        "domainId": str,
        "templateId": str,
    },
)

LayoutSummaryTypeDef = TypedDict(
    "LayoutSummaryTypeDef",
    {
        "layoutArn": str,
        "layoutId": str,
        "name": str,
    },
)

_RequiredListCasesForContactRequestRequestTypeDef = TypedDict(
    "_RequiredListCasesForContactRequestRequestTypeDef",
    {
        "contactArn": str,
        "domainId": str,
    },
)
_OptionalListCasesForContactRequestRequestTypeDef = TypedDict(
    "_OptionalListCasesForContactRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListCasesForContactRequestRequestTypeDef(
    _RequiredListCasesForContactRequestRequestTypeDef,
    _OptionalListCasesForContactRequestRequestTypeDef,
):
    pass

ListDomainsRequestRequestTypeDef = TypedDict(
    "ListDomainsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

_RequiredListFieldOptionsRequestRequestTypeDef = TypedDict(
    "_RequiredListFieldOptionsRequestRequestTypeDef",
    {
        "domainId": str,
        "fieldId": str,
    },
)
_OptionalListFieldOptionsRequestRequestTypeDef = TypedDict(
    "_OptionalListFieldOptionsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "values": Sequence[str],
    },
    total=False,
)

class ListFieldOptionsRequestRequestTypeDef(
    _RequiredListFieldOptionsRequestRequestTypeDef, _OptionalListFieldOptionsRequestRequestTypeDef
):
    pass

_RequiredListFieldsRequestRequestTypeDef = TypedDict(
    "_RequiredListFieldsRequestRequestTypeDef",
    {
        "domainId": str,
    },
)
_OptionalListFieldsRequestRequestTypeDef = TypedDict(
    "_OptionalListFieldsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListFieldsRequestRequestTypeDef(
    _RequiredListFieldsRequestRequestTypeDef, _OptionalListFieldsRequestRequestTypeDef
):
    pass

_RequiredListLayoutsRequestRequestTypeDef = TypedDict(
    "_RequiredListLayoutsRequestRequestTypeDef",
    {
        "domainId": str,
    },
)
_OptionalListLayoutsRequestRequestTypeDef = TypedDict(
    "_OptionalListLayoutsRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class ListLayoutsRequestRequestTypeDef(
    _RequiredListLayoutsRequestRequestTypeDef, _OptionalListLayoutsRequestRequestTypeDef
):
    pass

ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "arn": str,
    },
)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredListTemplatesRequestRequestTypeDef = TypedDict(
    "_RequiredListTemplatesRequestRequestTypeDef",
    {
        "domainId": str,
    },
)
_OptionalListTemplatesRequestRequestTypeDef = TypedDict(
    "_OptionalListTemplatesRequestRequestTypeDef",
    {
        "maxResults": int,
        "nextToken": str,
        "status": Sequence[TemplateStatusType],
    },
    total=False,
)

class ListTemplatesRequestRequestTypeDef(
    _RequiredListTemplatesRequestRequestTypeDef, _OptionalListTemplatesRequestRequestTypeDef
):
    pass

TemplateSummaryTypeDef = TypedDict(
    "TemplateSummaryTypeDef",
    {
        "name": str,
        "status": TemplateStatusType,
        "templateArn": str,
        "templateId": str,
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

SortTypeDef = TypedDict(
    "SortTypeDef",
    {
        "fieldId": str,
        "sortOrder": OrderType,
    },
)

TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "arn": str,
        "tags": Mapping[str, str],
    },
)

UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "arn": str,
        "tagKeys": Sequence[str],
    },
)

_RequiredUpdateFieldRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateFieldRequestRequestTypeDef",
    {
        "domainId": str,
        "fieldId": str,
    },
)
_OptionalUpdateFieldRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateFieldRequestRequestTypeDef",
    {
        "description": str,
        "name": str,
    },
    total=False,
)

class UpdateFieldRequestRequestTypeDef(
    _RequiredUpdateFieldRequestRequestTypeDef, _OptionalUpdateFieldRequestRequestTypeDef
):
    pass

BatchGetFieldRequestRequestTypeDef = TypedDict(
    "BatchGetFieldRequestRequestTypeDef",
    {
        "domainId": str,
        "fields": Sequence[FieldIdentifierTypeDef],
    },
)

CaseEventIncludedDataTypeDef = TypedDict(
    "CaseEventIncludedDataTypeDef",
    {
        "fields": List[FieldIdentifierTypeDef],
    },
)

_RequiredGetCaseRequestRequestTypeDef = TypedDict(
    "_RequiredGetCaseRequestRequestTypeDef",
    {
        "caseId": str,
        "domainId": str,
        "fields": Sequence[FieldIdentifierTypeDef],
    },
)
_OptionalGetCaseRequestRequestTypeDef = TypedDict(
    "_OptionalGetCaseRequestRequestTypeDef",
    {
        "nextToken": str,
    },
    total=False,
)

class GetCaseRequestRequestTypeDef(
    _RequiredGetCaseRequestRequestTypeDef, _OptionalGetCaseRequestRequestTypeDef
):
    pass

BatchGetFieldResponseTypeDef = TypedDict(
    "BatchGetFieldResponseTypeDef",
    {
        "errors": List[FieldErrorTypeDef],
        "fields": List[GetFieldResponseTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchPutFieldOptionsRequestRequestTypeDef = TypedDict(
    "BatchPutFieldOptionsRequestRequestTypeDef",
    {
        "domainId": str,
        "fieldId": str,
        "options": Sequence[FieldOptionTypeDef],
    },
)

ListFieldOptionsResponseTypeDef = TypedDict(
    "ListFieldOptionsResponseTypeDef",
    {
        "nextToken": str,
        "options": List[FieldOptionTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

BatchPutFieldOptionsResponseTypeDef = TypedDict(
    "BatchPutFieldOptionsResponseTypeDef",
    {
        "errors": List[FieldOptionErrorTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListCasesForContactResponseTypeDef = TypedDict(
    "ListCasesForContactResponseTypeDef",
    {
        "cases": List[CaseSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RelatedItemContentTypeDef = TypedDict(
    "RelatedItemContentTypeDef",
    {
        "comment": CommentContentTypeDef,
        "contact": ContactContentTypeDef,
    },
    total=False,
)

RelatedItemTypeFilterTypeDef = TypedDict(
    "RelatedItemTypeFilterTypeDef",
    {
        "comment": Mapping[str, Any],
        "contact": ContactFilterTypeDef,
    },
    total=False,
)

RelatedItemInputContentTypeDef = TypedDict(
    "RelatedItemInputContentTypeDef",
    {
        "comment": CommentContentTypeDef,
        "contact": ContactTypeDef,
    },
    total=False,
)

_RequiredCreateTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredCreateTemplateRequestRequestTypeDef",
    {
        "domainId": str,
        "name": str,
    },
)
_OptionalCreateTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalCreateTemplateRequestRequestTypeDef",
    {
        "description": str,
        "layoutConfiguration": LayoutConfigurationTypeDef,
        "requiredFields": Sequence[RequiredFieldTypeDef],
        "status": TemplateStatusType,
    },
    total=False,
)

class CreateTemplateRequestRequestTypeDef(
    _RequiredCreateTemplateRequestRequestTypeDef, _OptionalCreateTemplateRequestRequestTypeDef
):
    pass

GetTemplateResponseTypeDef = TypedDict(
    "GetTemplateResponseTypeDef",
    {
        "description": str,
        "layoutConfiguration": LayoutConfigurationTypeDef,
        "name": str,
        "requiredFields": List[RequiredFieldTypeDef],
        "status": TemplateStatusType,
        "tags": Dict[str, str],
        "templateArn": str,
        "templateId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateTemplateRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateTemplateRequestRequestTypeDef",
    {
        "domainId": str,
        "templateId": str,
    },
)
_OptionalUpdateTemplateRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateTemplateRequestRequestTypeDef",
    {
        "description": str,
        "layoutConfiguration": LayoutConfigurationTypeDef,
        "name": str,
        "requiredFields": Sequence[RequiredFieldTypeDef],
        "status": TemplateStatusType,
    },
    total=False,
)

class UpdateTemplateRequestRequestTypeDef(
    _RequiredUpdateTemplateRequestRequestTypeDef, _OptionalUpdateTemplateRequestRequestTypeDef
):
    pass

ListDomainsResponseTypeDef = TypedDict(
    "ListDomainsResponseTypeDef",
    {
        "domains": List[DomainSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredFieldGroupTypeDef = TypedDict(
    "_RequiredFieldGroupTypeDef",
    {
        "fields": Sequence[FieldItemTypeDef],
    },
)
_OptionalFieldGroupTypeDef = TypedDict(
    "_OptionalFieldGroupTypeDef",
    {
        "name": str,
    },
    total=False,
)

class FieldGroupTypeDef(_RequiredFieldGroupTypeDef, _OptionalFieldGroupTypeDef):
    pass

ListFieldsResponseTypeDef = TypedDict(
    "ListFieldsResponseTypeDef",
    {
        "fields": List[FieldSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

FieldValueTypeDef = TypedDict(
    "FieldValueTypeDef",
    {
        "id": str,
        "value": FieldValueUnionTypeDef,
    },
)

ListLayoutsResponseTypeDef = TypedDict(
    "ListLayoutsResponseTypeDef",
    {
        "layouts": List[LayoutSummaryTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTemplatesResponseTypeDef = TypedDict(
    "ListTemplatesResponseTypeDef",
    {
        "nextToken": str,
        "templates": List[TemplateSummaryTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredSearchCasesRequestRequestTypeDef = TypedDict(
    "_RequiredSearchCasesRequestRequestTypeDef",
    {
        "domainId": str,
    },
)
_OptionalSearchCasesRequestRequestTypeDef = TypedDict(
    "_OptionalSearchCasesRequestRequestTypeDef",
    {
        "fields": Sequence[FieldIdentifierTypeDef],
        "filter": "CaseFilterTypeDef",
        "maxResults": int,
        "nextToken": str,
        "searchTerm": str,
        "sorts": Sequence[SortTypeDef],
    },
    total=False,
)

class SearchCasesRequestRequestTypeDef(
    _RequiredSearchCasesRequestRequestTypeDef, _OptionalSearchCasesRequestRequestTypeDef
):
    pass

_RequiredSearchCasesRequestSearchCasesPaginateTypeDef = TypedDict(
    "_RequiredSearchCasesRequestSearchCasesPaginateTypeDef",
    {
        "domainId": str,
    },
)
_OptionalSearchCasesRequestSearchCasesPaginateTypeDef = TypedDict(
    "_OptionalSearchCasesRequestSearchCasesPaginateTypeDef",
    {
        "fields": Sequence[FieldIdentifierTypeDef],
        "filter": "CaseFilterTypeDef",
        "searchTerm": str,
        "sorts": Sequence[SortTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class SearchCasesRequestSearchCasesPaginateTypeDef(
    _RequiredSearchCasesRequestSearchCasesPaginateTypeDef,
    _OptionalSearchCasesRequestSearchCasesPaginateTypeDef,
):
    pass

EventIncludedDataTypeDef = TypedDict(
    "EventIncludedDataTypeDef",
    {
        "caseData": CaseEventIncludedDataTypeDef,
        "relatedItemData": RelatedItemEventIncludedDataTypeDef,
    },
    total=False,
)

_RequiredSearchRelatedItemsResponseItemTypeDef = TypedDict(
    "_RequiredSearchRelatedItemsResponseItemTypeDef",
    {
        "associationTime": datetime,
        "content": RelatedItemContentTypeDef,
        "relatedItemId": str,
        "type": RelatedItemTypeType,
    },
)
_OptionalSearchRelatedItemsResponseItemTypeDef = TypedDict(
    "_OptionalSearchRelatedItemsResponseItemTypeDef",
    {
        "tags": Dict[str, str],
    },
    total=False,
)

class SearchRelatedItemsResponseItemTypeDef(
    _RequiredSearchRelatedItemsResponseItemTypeDef, _OptionalSearchRelatedItemsResponseItemTypeDef
):
    pass

_RequiredSearchRelatedItemsRequestRequestTypeDef = TypedDict(
    "_RequiredSearchRelatedItemsRequestRequestTypeDef",
    {
        "caseId": str,
        "domainId": str,
    },
)
_OptionalSearchRelatedItemsRequestRequestTypeDef = TypedDict(
    "_OptionalSearchRelatedItemsRequestRequestTypeDef",
    {
        "filters": Sequence[RelatedItemTypeFilterTypeDef],
        "maxResults": int,
        "nextToken": str,
    },
    total=False,
)

class SearchRelatedItemsRequestRequestTypeDef(
    _RequiredSearchRelatedItemsRequestRequestTypeDef,
    _OptionalSearchRelatedItemsRequestRequestTypeDef,
):
    pass

_RequiredSearchRelatedItemsRequestSearchRelatedItemsPaginateTypeDef = TypedDict(
    "_RequiredSearchRelatedItemsRequestSearchRelatedItemsPaginateTypeDef",
    {
        "caseId": str,
        "domainId": str,
    },
)
_OptionalSearchRelatedItemsRequestSearchRelatedItemsPaginateTypeDef = TypedDict(
    "_OptionalSearchRelatedItemsRequestSearchRelatedItemsPaginateTypeDef",
    {
        "filters": Sequence[RelatedItemTypeFilterTypeDef],
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

class SearchRelatedItemsRequestSearchRelatedItemsPaginateTypeDef(
    _RequiredSearchRelatedItemsRequestSearchRelatedItemsPaginateTypeDef,
    _OptionalSearchRelatedItemsRequestSearchRelatedItemsPaginateTypeDef,
):
    pass

CreateRelatedItemRequestRequestTypeDef = TypedDict(
    "CreateRelatedItemRequestRequestTypeDef",
    {
        "caseId": str,
        "content": RelatedItemInputContentTypeDef,
        "domainId": str,
        "type": RelatedItemTypeType,
    },
)

SectionTypeDef = TypedDict(
    "SectionTypeDef",
    {
        "fieldGroup": FieldGroupTypeDef,
    },
    total=False,
)

_RequiredCreateCaseRequestRequestTypeDef = TypedDict(
    "_RequiredCreateCaseRequestRequestTypeDef",
    {
        "domainId": str,
        "fields": Sequence[FieldValueTypeDef],
        "templateId": str,
    },
)
_OptionalCreateCaseRequestRequestTypeDef = TypedDict(
    "_OptionalCreateCaseRequestRequestTypeDef",
    {
        "clientToken": str,
    },
    total=False,
)

class CreateCaseRequestRequestTypeDef(
    _RequiredCreateCaseRequestRequestTypeDef, _OptionalCreateCaseRequestRequestTypeDef
):
    pass

FieldFilterTypeDef = TypedDict(
    "FieldFilterTypeDef",
    {
        "contains": FieldValueTypeDef,
        "equalTo": FieldValueTypeDef,
        "greaterThan": FieldValueTypeDef,
        "greaterThanOrEqualTo": FieldValueTypeDef,
        "lessThan": FieldValueTypeDef,
        "lessThanOrEqualTo": FieldValueTypeDef,
    },
    total=False,
)

GetCaseResponseTypeDef = TypedDict(
    "GetCaseResponseTypeDef",
    {
        "fields": List[FieldValueTypeDef],
        "nextToken": str,
        "tags": Dict[str, str],
        "templateId": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredSearchCasesResponseItemTypeDef = TypedDict(
    "_RequiredSearchCasesResponseItemTypeDef",
    {
        "caseId": str,
        "fields": List[FieldValueTypeDef],
        "templateId": str,
    },
)
_OptionalSearchCasesResponseItemTypeDef = TypedDict(
    "_OptionalSearchCasesResponseItemTypeDef",
    {
        "tags": Dict[str, str],
    },
    total=False,
)

class SearchCasesResponseItemTypeDef(
    _RequiredSearchCasesResponseItemTypeDef, _OptionalSearchCasesResponseItemTypeDef
):
    pass

UpdateCaseRequestRequestTypeDef = TypedDict(
    "UpdateCaseRequestRequestTypeDef",
    {
        "caseId": str,
        "domainId": str,
        "fields": Sequence[FieldValueTypeDef],
    },
)

_RequiredEventBridgeConfigurationTypeDef = TypedDict(
    "_RequiredEventBridgeConfigurationTypeDef",
    {
        "enabled": bool,
    },
)
_OptionalEventBridgeConfigurationTypeDef = TypedDict(
    "_OptionalEventBridgeConfigurationTypeDef",
    {
        "includedData": EventIncludedDataTypeDef,
    },
    total=False,
)

class EventBridgeConfigurationTypeDef(
    _RequiredEventBridgeConfigurationTypeDef, _OptionalEventBridgeConfigurationTypeDef
):
    pass

SearchRelatedItemsResponseTypeDef = TypedDict(
    "SearchRelatedItemsResponseTypeDef",
    {
        "nextToken": str,
        "relatedItems": List[SearchRelatedItemsResponseItemTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

LayoutSectionsTypeDef = TypedDict(
    "LayoutSectionsTypeDef",
    {
        "sections": Sequence[SectionTypeDef],
    },
    total=False,
)

CaseFilterTypeDef = TypedDict(
    "CaseFilterTypeDef",
    {
        "andAll": Sequence[Dict[str, Any]],
        "field": FieldFilterTypeDef,
        "not": Dict[str, Any],
    },
    total=False,
)

SearchCasesResponseTypeDef = TypedDict(
    "SearchCasesResponseTypeDef",
    {
        "cases": List[SearchCasesResponseItemTypeDef],
        "nextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetCaseEventConfigurationResponseTypeDef = TypedDict(
    "GetCaseEventConfigurationResponseTypeDef",
    {
        "eventBridge": EventBridgeConfigurationTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

PutCaseEventConfigurationRequestRequestTypeDef = TypedDict(
    "PutCaseEventConfigurationRequestRequestTypeDef",
    {
        "domainId": str,
        "eventBridge": EventBridgeConfigurationTypeDef,
    },
)

BasicLayoutTypeDef = TypedDict(
    "BasicLayoutTypeDef",
    {
        "moreInfo": LayoutSectionsTypeDef,
        "topPanel": LayoutSectionsTypeDef,
    },
    total=False,
)

LayoutContentTypeDef = TypedDict(
    "LayoutContentTypeDef",
    {
        "basic": BasicLayoutTypeDef,
    },
    total=False,
)

CreateLayoutRequestRequestTypeDef = TypedDict(
    "CreateLayoutRequestRequestTypeDef",
    {
        "content": LayoutContentTypeDef,
        "domainId": str,
        "name": str,
    },
)

GetLayoutResponseTypeDef = TypedDict(
    "GetLayoutResponseTypeDef",
    {
        "content": LayoutContentTypeDef,
        "layoutArn": str,
        "layoutId": str,
        "name": str,
        "tags": Dict[str, str],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

_RequiredUpdateLayoutRequestRequestTypeDef = TypedDict(
    "_RequiredUpdateLayoutRequestRequestTypeDef",
    {
        "domainId": str,
        "layoutId": str,
    },
)
_OptionalUpdateLayoutRequestRequestTypeDef = TypedDict(
    "_OptionalUpdateLayoutRequestRequestTypeDef",
    {
        "content": LayoutContentTypeDef,
        "name": str,
    },
    total=False,
)

class UpdateLayoutRequestRequestTypeDef(
    _RequiredUpdateLayoutRequestRequestTypeDef, _OptionalUpdateLayoutRequestRequestTypeDef
):
    pass
