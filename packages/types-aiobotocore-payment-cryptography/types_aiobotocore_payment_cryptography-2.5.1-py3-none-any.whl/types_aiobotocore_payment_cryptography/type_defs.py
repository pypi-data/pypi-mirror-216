"""
Type annotations for payment-cryptography service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_payment_cryptography/type_defs/)

Usage::

    ```python
    from types_aiobotocore_payment_cryptography.type_defs import AliasTypeDef

    data: AliasTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import Dict, List, Sequence

from .literals import (
    KeyAlgorithmType,
    KeyCheckValueAlgorithmType,
    KeyClassType,
    KeyMaterialTypeType,
    KeyOriginType,
    KeyStateType,
    KeyUsageType,
    WrappedKeyMaterialFormatType,
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
    "AliasTypeDef",
    "CreateAliasInputRequestTypeDef",
    "TagTypeDef",
    "DeleteAliasInputRequestTypeDef",
    "DeleteKeyInputRequestTypeDef",
    "ExportTr31KeyBlockTypeDef",
    "ExportTr34KeyBlockTypeDef",
    "WrappedKeyTypeDef",
    "GetAliasInputRequestTypeDef",
    "GetKeyInputRequestTypeDef",
    "GetParametersForExportInputRequestTypeDef",
    "GetParametersForExportOutputTypeDef",
    "GetParametersForImportInputRequestTypeDef",
    "GetParametersForImportOutputTypeDef",
    "GetPublicKeyCertificateInputRequestTypeDef",
    "GetPublicKeyCertificateOutputTypeDef",
    "ImportTr31KeyBlockTypeDef",
    "ImportTr34KeyBlockTypeDef",
    "KeyModesOfUseTypeDef",
    "ListAliasesInputListAliasesPaginateTypeDef",
    "ListAliasesInputRequestTypeDef",
    "ListKeysInputListKeysPaginateTypeDef",
    "ListKeysInputRequestTypeDef",
    "ListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "RestoreKeyInputRequestTypeDef",
    "StartKeyUsageInputRequestTypeDef",
    "StopKeyUsageInputRequestTypeDef",
    "UntagResourceInputRequestTypeDef",
    "UpdateAliasInputRequestTypeDef",
    "CreateAliasOutputTypeDef",
    "GetAliasOutputTypeDef",
    "ListAliasesOutputTypeDef",
    "UpdateAliasOutputTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "TagResourceInputRequestTypeDef",
    "ExportKeyMaterialTypeDef",
    "ExportKeyOutputTypeDef",
    "KeyAttributesTypeDef",
    "ExportKeyInputRequestTypeDef",
    "CreateKeyInputRequestTypeDef",
    "KeySummaryTypeDef",
    "KeyTypeDef",
    "RootCertificatePublicKeyTypeDef",
    "TrustedCertificatePublicKeyTypeDef",
    "ListKeysOutputTypeDef",
    "CreateKeyOutputTypeDef",
    "DeleteKeyOutputTypeDef",
    "GetKeyOutputTypeDef",
    "ImportKeyOutputTypeDef",
    "RestoreKeyOutputTypeDef",
    "StartKeyUsageOutputTypeDef",
    "StopKeyUsageOutputTypeDef",
    "ImportKeyMaterialTypeDef",
    "ImportKeyInputRequestTypeDef",
)

_RequiredAliasTypeDef = TypedDict(
    "_RequiredAliasTypeDef",
    {
        "AliasName": str,
    },
)
_OptionalAliasTypeDef = TypedDict(
    "_OptionalAliasTypeDef",
    {
        "KeyArn": str,
    },
    total=False,
)


class AliasTypeDef(_RequiredAliasTypeDef, _OptionalAliasTypeDef):
    pass


_RequiredCreateAliasInputRequestTypeDef = TypedDict(
    "_RequiredCreateAliasInputRequestTypeDef",
    {
        "AliasName": str,
    },
)
_OptionalCreateAliasInputRequestTypeDef = TypedDict(
    "_OptionalCreateAliasInputRequestTypeDef",
    {
        "KeyArn": str,
    },
    total=False,
)


class CreateAliasInputRequestTypeDef(
    _RequiredCreateAliasInputRequestTypeDef, _OptionalCreateAliasInputRequestTypeDef
):
    pass


_RequiredTagTypeDef = TypedDict(
    "_RequiredTagTypeDef",
    {
        "Key": str,
    },
)
_OptionalTagTypeDef = TypedDict(
    "_OptionalTagTypeDef",
    {
        "Value": str,
    },
    total=False,
)


class TagTypeDef(_RequiredTagTypeDef, _OptionalTagTypeDef):
    pass


DeleteAliasInputRequestTypeDef = TypedDict(
    "DeleteAliasInputRequestTypeDef",
    {
        "AliasName": str,
    },
)

_RequiredDeleteKeyInputRequestTypeDef = TypedDict(
    "_RequiredDeleteKeyInputRequestTypeDef",
    {
        "KeyIdentifier": str,
    },
)
_OptionalDeleteKeyInputRequestTypeDef = TypedDict(
    "_OptionalDeleteKeyInputRequestTypeDef",
    {
        "DeleteKeyInDays": int,
    },
    total=False,
)


class DeleteKeyInputRequestTypeDef(
    _RequiredDeleteKeyInputRequestTypeDef, _OptionalDeleteKeyInputRequestTypeDef
):
    pass


ExportTr31KeyBlockTypeDef = TypedDict(
    "ExportTr31KeyBlockTypeDef",
    {
        "WrappingKeyIdentifier": str,
    },
)

_RequiredExportTr34KeyBlockTypeDef = TypedDict(
    "_RequiredExportTr34KeyBlockTypeDef",
    {
        "CertificateAuthorityPublicKeyIdentifier": str,
        "ExportToken": str,
        "KeyBlockFormat": Literal["X9_TR34_2012"],
        "WrappingKeyCertificate": str,
    },
)
_OptionalExportTr34KeyBlockTypeDef = TypedDict(
    "_OptionalExportTr34KeyBlockTypeDef",
    {
        "RandomNonce": str,
    },
    total=False,
)


class ExportTr34KeyBlockTypeDef(
    _RequiredExportTr34KeyBlockTypeDef, _OptionalExportTr34KeyBlockTypeDef
):
    pass


WrappedKeyTypeDef = TypedDict(
    "WrappedKeyTypeDef",
    {
        "KeyMaterial": str,
        "WrappedKeyMaterialFormat": WrappedKeyMaterialFormatType,
        "WrappingKeyArn": str,
    },
)

GetAliasInputRequestTypeDef = TypedDict(
    "GetAliasInputRequestTypeDef",
    {
        "AliasName": str,
    },
)

GetKeyInputRequestTypeDef = TypedDict(
    "GetKeyInputRequestTypeDef",
    {
        "KeyIdentifier": str,
    },
)

GetParametersForExportInputRequestTypeDef = TypedDict(
    "GetParametersForExportInputRequestTypeDef",
    {
        "KeyMaterialType": KeyMaterialTypeType,
        "SigningKeyAlgorithm": KeyAlgorithmType,
    },
)

GetParametersForExportOutputTypeDef = TypedDict(
    "GetParametersForExportOutputTypeDef",
    {
        "ExportToken": str,
        "ParametersValidUntilTimestamp": datetime,
        "SigningKeyAlgorithm": KeyAlgorithmType,
        "SigningKeyCertificate": str,
        "SigningKeyCertificateChain": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetParametersForImportInputRequestTypeDef = TypedDict(
    "GetParametersForImportInputRequestTypeDef",
    {
        "KeyMaterialType": KeyMaterialTypeType,
        "WrappingKeyAlgorithm": KeyAlgorithmType,
    },
)

GetParametersForImportOutputTypeDef = TypedDict(
    "GetParametersForImportOutputTypeDef",
    {
        "ImportToken": str,
        "ParametersValidUntilTimestamp": datetime,
        "WrappingKeyAlgorithm": KeyAlgorithmType,
        "WrappingKeyCertificate": str,
        "WrappingKeyCertificateChain": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetPublicKeyCertificateInputRequestTypeDef = TypedDict(
    "GetPublicKeyCertificateInputRequestTypeDef",
    {
        "KeyIdentifier": str,
    },
)

GetPublicKeyCertificateOutputTypeDef = TypedDict(
    "GetPublicKeyCertificateOutputTypeDef",
    {
        "KeyCertificate": str,
        "KeyCertificateChain": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ImportTr31KeyBlockTypeDef = TypedDict(
    "ImportTr31KeyBlockTypeDef",
    {
        "WrappedKeyBlock": str,
        "WrappingKeyIdentifier": str,
    },
)

_RequiredImportTr34KeyBlockTypeDef = TypedDict(
    "_RequiredImportTr34KeyBlockTypeDef",
    {
        "CertificateAuthorityPublicKeyIdentifier": str,
        "ImportToken": str,
        "KeyBlockFormat": Literal["X9_TR34_2012"],
        "SigningKeyCertificate": str,
        "WrappedKeyBlock": str,
    },
)
_OptionalImportTr34KeyBlockTypeDef = TypedDict(
    "_OptionalImportTr34KeyBlockTypeDef",
    {
        "RandomNonce": str,
    },
    total=False,
)


class ImportTr34KeyBlockTypeDef(
    _RequiredImportTr34KeyBlockTypeDef, _OptionalImportTr34KeyBlockTypeDef
):
    pass


KeyModesOfUseTypeDef = TypedDict(
    "KeyModesOfUseTypeDef",
    {
        "Decrypt": bool,
        "DeriveKey": bool,
        "Encrypt": bool,
        "Generate": bool,
        "NoRestrictions": bool,
        "Sign": bool,
        "Unwrap": bool,
        "Verify": bool,
        "Wrap": bool,
    },
    total=False,
)

ListAliasesInputListAliasesPaginateTypeDef = TypedDict(
    "ListAliasesInputListAliasesPaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListAliasesInputRequestTypeDef = TypedDict(
    "ListAliasesInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

ListKeysInputListKeysPaginateTypeDef = TypedDict(
    "ListKeysInputListKeysPaginateTypeDef",
    {
        "KeyState": KeyStateType,
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)

ListKeysInputRequestTypeDef = TypedDict(
    "ListKeysInputRequestTypeDef",
    {
        "KeyState": KeyStateType,
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)

_RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef",
    {
        "PaginationConfig": "PaginatorConfigTypeDef",
    },
    total=False,
)


class ListTagsForResourceInputListTagsForResourcePaginateTypeDef(
    _RequiredListTagsForResourceInputListTagsForResourcePaginateTypeDef,
    _OptionalListTagsForResourceInputListTagsForResourcePaginateTypeDef,
):
    pass


_RequiredListTagsForResourceInputRequestTypeDef = TypedDict(
    "_RequiredListTagsForResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
    },
)
_OptionalListTagsForResourceInputRequestTypeDef = TypedDict(
    "_OptionalListTagsForResourceInputRequestTypeDef",
    {
        "MaxResults": int,
        "NextToken": str,
    },
    total=False,
)


class ListTagsForResourceInputRequestTypeDef(
    _RequiredListTagsForResourceInputRequestTypeDef, _OptionalListTagsForResourceInputRequestTypeDef
):
    pass


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

RestoreKeyInputRequestTypeDef = TypedDict(
    "RestoreKeyInputRequestTypeDef",
    {
        "KeyIdentifier": str,
    },
)

StartKeyUsageInputRequestTypeDef = TypedDict(
    "StartKeyUsageInputRequestTypeDef",
    {
        "KeyIdentifier": str,
    },
)

StopKeyUsageInputRequestTypeDef = TypedDict(
    "StopKeyUsageInputRequestTypeDef",
    {
        "KeyIdentifier": str,
    },
)

UntagResourceInputRequestTypeDef = TypedDict(
    "UntagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "TagKeys": Sequence[str],
    },
)

_RequiredUpdateAliasInputRequestTypeDef = TypedDict(
    "_RequiredUpdateAliasInputRequestTypeDef",
    {
        "AliasName": str,
    },
)
_OptionalUpdateAliasInputRequestTypeDef = TypedDict(
    "_OptionalUpdateAliasInputRequestTypeDef",
    {
        "KeyArn": str,
    },
    total=False,
)


class UpdateAliasInputRequestTypeDef(
    _RequiredUpdateAliasInputRequestTypeDef, _OptionalUpdateAliasInputRequestTypeDef
):
    pass


CreateAliasOutputTypeDef = TypedDict(
    "CreateAliasOutputTypeDef",
    {
        "Alias": AliasTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetAliasOutputTypeDef = TypedDict(
    "GetAliasOutputTypeDef",
    {
        "Alias": AliasTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListAliasesOutputTypeDef = TypedDict(
    "ListAliasesOutputTypeDef",
    {
        "Aliases": List[AliasTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

UpdateAliasOutputTypeDef = TypedDict(
    "UpdateAliasOutputTypeDef",
    {
        "Alias": AliasTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ListTagsForResourceOutputTypeDef = TypedDict(
    "ListTagsForResourceOutputTypeDef",
    {
        "NextToken": str,
        "Tags": List[TagTypeDef],
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

TagResourceInputRequestTypeDef = TypedDict(
    "TagResourceInputRequestTypeDef",
    {
        "ResourceArn": str,
        "Tags": Sequence[TagTypeDef],
    },
)

ExportKeyMaterialTypeDef = TypedDict(
    "ExportKeyMaterialTypeDef",
    {
        "Tr31KeyBlock": ExportTr31KeyBlockTypeDef,
        "Tr34KeyBlock": ExportTr34KeyBlockTypeDef,
    },
    total=False,
)

ExportKeyOutputTypeDef = TypedDict(
    "ExportKeyOutputTypeDef",
    {
        "WrappedKey": WrappedKeyTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

KeyAttributesTypeDef = TypedDict(
    "KeyAttributesTypeDef",
    {
        "KeyAlgorithm": KeyAlgorithmType,
        "KeyClass": KeyClassType,
        "KeyModesOfUse": KeyModesOfUseTypeDef,
        "KeyUsage": KeyUsageType,
    },
)

ExportKeyInputRequestTypeDef = TypedDict(
    "ExportKeyInputRequestTypeDef",
    {
        "ExportKeyIdentifier": str,
        "KeyMaterial": ExportKeyMaterialTypeDef,
    },
)

_RequiredCreateKeyInputRequestTypeDef = TypedDict(
    "_RequiredCreateKeyInputRequestTypeDef",
    {
        "Exportable": bool,
        "KeyAttributes": KeyAttributesTypeDef,
    },
)
_OptionalCreateKeyInputRequestTypeDef = TypedDict(
    "_OptionalCreateKeyInputRequestTypeDef",
    {
        "Enabled": bool,
        "KeyCheckValueAlgorithm": KeyCheckValueAlgorithmType,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class CreateKeyInputRequestTypeDef(
    _RequiredCreateKeyInputRequestTypeDef, _OptionalCreateKeyInputRequestTypeDef
):
    pass


KeySummaryTypeDef = TypedDict(
    "KeySummaryTypeDef",
    {
        "Enabled": bool,
        "Exportable": bool,
        "KeyArn": str,
        "KeyAttributes": KeyAttributesTypeDef,
        "KeyCheckValue": str,
        "KeyState": KeyStateType,
    },
)

_RequiredKeyTypeDef = TypedDict(
    "_RequiredKeyTypeDef",
    {
        "CreateTimestamp": datetime,
        "Enabled": bool,
        "Exportable": bool,
        "KeyArn": str,
        "KeyAttributes": KeyAttributesTypeDef,
        "KeyCheckValue": str,
        "KeyCheckValueAlgorithm": KeyCheckValueAlgorithmType,
        "KeyOrigin": KeyOriginType,
        "KeyState": KeyStateType,
    },
)
_OptionalKeyTypeDef = TypedDict(
    "_OptionalKeyTypeDef",
    {
        "DeletePendingTimestamp": datetime,
        "DeleteTimestamp": datetime,
        "UsageStartTimestamp": datetime,
        "UsageStopTimestamp": datetime,
    },
    total=False,
)


class KeyTypeDef(_RequiredKeyTypeDef, _OptionalKeyTypeDef):
    pass


RootCertificatePublicKeyTypeDef = TypedDict(
    "RootCertificatePublicKeyTypeDef",
    {
        "KeyAttributes": KeyAttributesTypeDef,
        "PublicKeyCertificate": str,
    },
)

TrustedCertificatePublicKeyTypeDef = TypedDict(
    "TrustedCertificatePublicKeyTypeDef",
    {
        "CertificateAuthorityPublicKeyIdentifier": str,
        "KeyAttributes": KeyAttributesTypeDef,
        "PublicKeyCertificate": str,
    },
)

ListKeysOutputTypeDef = TypedDict(
    "ListKeysOutputTypeDef",
    {
        "Keys": List[KeySummaryTypeDef],
        "NextToken": str,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

CreateKeyOutputTypeDef = TypedDict(
    "CreateKeyOutputTypeDef",
    {
        "Key": KeyTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

DeleteKeyOutputTypeDef = TypedDict(
    "DeleteKeyOutputTypeDef",
    {
        "Key": KeyTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

GetKeyOutputTypeDef = TypedDict(
    "GetKeyOutputTypeDef",
    {
        "Key": KeyTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ImportKeyOutputTypeDef = TypedDict(
    "ImportKeyOutputTypeDef",
    {
        "Key": KeyTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

RestoreKeyOutputTypeDef = TypedDict(
    "RestoreKeyOutputTypeDef",
    {
        "Key": KeyTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StartKeyUsageOutputTypeDef = TypedDict(
    "StartKeyUsageOutputTypeDef",
    {
        "Key": KeyTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

StopKeyUsageOutputTypeDef = TypedDict(
    "StopKeyUsageOutputTypeDef",
    {
        "Key": KeyTypeDef,
        "ResponseMetadata": "ResponseMetadataTypeDef",
    },
)

ImportKeyMaterialTypeDef = TypedDict(
    "ImportKeyMaterialTypeDef",
    {
        "RootCertificatePublicKey": RootCertificatePublicKeyTypeDef,
        "Tr31KeyBlock": ImportTr31KeyBlockTypeDef,
        "Tr34KeyBlock": ImportTr34KeyBlockTypeDef,
        "TrustedCertificatePublicKey": TrustedCertificatePublicKeyTypeDef,
    },
    total=False,
)

_RequiredImportKeyInputRequestTypeDef = TypedDict(
    "_RequiredImportKeyInputRequestTypeDef",
    {
        "KeyMaterial": ImportKeyMaterialTypeDef,
    },
)
_OptionalImportKeyInputRequestTypeDef = TypedDict(
    "_OptionalImportKeyInputRequestTypeDef",
    {
        "Enabled": bool,
        "KeyCheckValueAlgorithm": KeyCheckValueAlgorithmType,
        "Tags": Sequence[TagTypeDef],
    },
    total=False,
)


class ImportKeyInputRequestTypeDef(
    _RequiredImportKeyInputRequestTypeDef, _OptionalImportKeyInputRequestTypeDef
):
    pass
