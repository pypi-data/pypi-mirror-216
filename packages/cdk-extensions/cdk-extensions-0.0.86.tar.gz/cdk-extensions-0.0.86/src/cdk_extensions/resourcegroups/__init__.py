import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_resourcegroups as _aws_cdk_aws_resourcegroups_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="cdk-extensions.resourcegroups.BoundGroupConfiguration",
    jsii_struct_bases=[],
    name_mapping={"configuration": "configuration", "query": "query"},
)
class BoundGroupConfiguration:
    def __init__(
        self,
        *,
        configuration: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_resourcegroups_ceddda9d.CfnGroup.ConfigurationItemProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        query: typing.Optional[typing.Union[_aws_cdk_aws_resourcegroups_ceddda9d.CfnGroup.ResourceQueryProperty, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param configuration: 
        :param query: 
        '''
        if isinstance(query, dict):
            query = _aws_cdk_aws_resourcegroups_ceddda9d.CfnGroup.ResourceQueryProperty(**query)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d78e0c9b073e26af2229294f065139cc61a985550545e80e6090b52d7a8b4815)
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument query", value=query, expected_type=type_hints["query"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if configuration is not None:
            self._values["configuration"] = configuration
        if query is not None:
            self._values["query"] = query

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_resourcegroups_ceddda9d.CfnGroup.ConfigurationItemProperty]]:
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_resourcegroups_ceddda9d.CfnGroup.ConfigurationItemProperty]], result)

    @builtins.property
    def query(
        self,
    ) -> typing.Optional[_aws_cdk_aws_resourcegroups_ceddda9d.CfnGroup.ResourceQueryProperty]:
        result = self._values.get("query")
        return typing.cast(typing.Optional[_aws_cdk_aws_resourcegroups_ceddda9d.CfnGroup.ResourceQueryProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BoundGroupConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.resourcegroups.CloudFormationStackProps",
    jsii_struct_bases=[],
    name_mapping={"resource_types": "resourceTypes"},
)
class CloudFormationStackProps:
    def __init__(
        self,
        *,
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param resource_types: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65facf546021877ff05946c7a7c8280e51d0dad25de0b0a020c3f77648dfe305)
            check_type(argname="argument resource_types", value=resource_types, expected_type=type_hints["resource_types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_types is not None:
            self._values["resource_types"] = resource_types

    @builtins.property
    def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("resource_types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CloudFormationStackProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.resourcegroups.GroupAttributes",
    jsii_struct_bases=[],
    name_mapping={"arn": "arn", "name": "name"},
)
class GroupAttributes:
    def __init__(
        self,
        *,
        arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param arn: 
        :param name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f880da69493115ef75f0b4b868b1128afd7424ef3187d6ac5a5f801216816d2)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if arn is not None:
            self._values["arn"] = arn
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def arn(self) -> typing.Optional[builtins.str]:
        result = self._values.get("arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GroupConfiguration(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.resourcegroups.GroupConfiguration",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="cloudFormationStack")
    @builtins.classmethod
    def cloud_formation_stack(
        cls,
        reference: "IStackReference",
        *,
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> "CloudFormationStack":
        '''
        :param reference: -
        :param resource_types: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__914a48dbccb8e839746ef64f3bc92afa7eb37998bac46f29cdced72ae5167695)
            check_type(argname="argument reference", value=reference, expected_type=type_hints["reference"])
        props = CloudFormationStackProps(resource_types=resource_types)

        return typing.cast("CloudFormationStack", jsii.sinvoke(cls, "cloudFormationStack", [reference, props]))

    @jsii.member(jsii_name="tagFilter")
    @builtins.classmethod
    def tag_filter(cls, props: typing.Optional["TagFilterProps"] = None) -> "TagFilter":
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0640e9b25e4e9929f13c24c3968210ed7c942b12efcf549a6e3d94a8ef3edf2a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast("TagFilter", jsii.sinvoke(cls, "tagFilter", [props]))


@jsii.data_type(
    jsii_type="cdk-extensions.resourcegroups.GroupProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "configuration": "configuration",
        "description": "description",
        "name": "name",
    },
)
class GroupProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        configuration: "IGroupConfiguration",
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param configuration: 
        :param description: 
        :param name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7d3c1b31024217edf3430298333ec71348a4649848c97a1a474e103db0a9eb9)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration": configuration,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if description is not None:
            self._values["description"] = description
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''The AWS account ID this resource belongs to.

        :default: - the resource is in the same account as the stack it belongs to
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_from_arn(self) -> typing.Optional[builtins.str]:
        '''ARN to deduce region and account from.

        The ARN is parsed and the account and region are taken from the ARN.
        This should be used for imported resources.

        Cannot be supplied together with either ``account`` or ``region``.

        :default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        '''
        result = self._values.get("environment_from_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def physical_name(self) -> typing.Optional[builtins.str]:
        '''The value passed in by users to the physical name prop of the resource.

        - ``undefined`` implies that a physical name will be allocated by
          CloudFormation during deployment.
        - a concrete value implies a specific physical name
        - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated
          by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation.

        :default: - The physical name will be allocated by CloudFormation at deployment time
        '''
        result = self._values.get("physical_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''The AWS region this resource belongs to.

        :default: - the resource is in the same region as the stack it belongs to
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def configuration(self) -> "IGroupConfiguration":
        result = self._values.get("configuration")
        assert result is not None, "Required property 'configuration' is missing"
        return typing.cast("IGroupConfiguration", result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="cdk-extensions.resourcegroups.IGroup")
class IGroup(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        ...


class _IGroupProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.resourcegroups.IGroup"

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupArn"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGroup).__jsii_proxy_class__ = lambda : _IGroupProxy


@jsii.interface(jsii_type="cdk-extensions.resourcegroups.IGroupConfiguration")
class IGroupConfiguration(typing_extensions.Protocol):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _constructs_77d1e7e8.IConstruct) -> BoundGroupConfiguration:
        '''
        :param scope: -
        '''
        ...


class _IGroupConfigurationProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.resourcegroups.IGroupConfiguration"

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _constructs_77d1e7e8.IConstruct) -> BoundGroupConfiguration:
        '''
        :param scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56b8a72441cc83c32e5f341c5b69b14ddc027c902f10cb313eed7f83776e4165)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(BoundGroupConfiguration, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGroupConfiguration).__jsii_proxy_class__ = lambda : _IGroupConfigurationProxy


@jsii.interface(jsii_type="cdk-extensions.resourcegroups.IStackReference")
class IStackReference(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="stackConstruct")
    def stack_construct(self) -> typing.Optional[_aws_cdk_ceddda9d.Stack]:
        ...


class _IStackReferenceProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.resourcegroups.IStackReference"

    @builtins.property
    @jsii.member(jsii_name="stackId")
    def stack_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "stackId"))

    @builtins.property
    @jsii.member(jsii_name="stackConstruct")
    def stack_construct(self) -> typing.Optional[_aws_cdk_ceddda9d.Stack]:
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Stack], jsii.get(self, "stackConstruct"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStackReference).__jsii_proxy_class__ = lambda : _IStackReferenceProxy


class StackReference(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.resourcegroups.StackReference",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromStack")
    @builtins.classmethod
    def from_stack(cls, stack: _aws_cdk_ceddda9d.Stack) -> IStackReference:
        '''
        :param stack: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c9b597509fd61a83fc0c7faed4435dfe31ea85b80437ed0ee33a4a8742fa3a7)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(IStackReference, jsii.sinvoke(cls, "fromStack", [stack]))

    @jsii.member(jsii_name="fromStackId")
    @builtins.classmethod
    def from_stack_id(cls, stack_id: builtins.str) -> IStackReference:
        '''
        :param stack_id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fe0b4b4c0fc4b1d4699714498d2bcd73041cfc1f75f0f83f62b81a8125a2caa)
            check_type(argname="argument stack_id", value=stack_id, expected_type=type_hints["stack_id"])
        return typing.cast(IStackReference, jsii.sinvoke(cls, "fromStackId", [stack_id]))


@jsii.implements(IGroupConfiguration)
class TagFilter(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.resourcegroups.TagFilter",
):
    def __init__(self, props: typing.Optional["TagFilterProps"] = None) -> None:
        '''Creates a new instance of the TagFilter class.

        :param props: Settings to use when applying the tag filter.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eca9d11c312f3365c2d88fc9b5cab689134f0aad15b05fe625b5d34cc8bf6aa4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addResourceType")
    def add_resource_type(self, type_id: builtins.str) -> "TagFilter":
        '''Add a resource type to the resource group.

        If no resource types are registered in the configuration then all resource
        types are allowed.

        :param type_id: The type that is to be added to the resource group.

        :return:

        The Resource Group configuration object to which the type was
        registered.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__693709c1c55f21ea386b712c6adeb95a3cbda51eda835b096830e57a596245c8)
            check_type(argname="argument type_id", value=type_id, expected_type=type_hints["type_id"])
        return typing.cast("TagFilter", jsii.invoke(self, "addResourceType", [type_id]))

    @jsii.member(jsii_name="addTagFilter")
    def add_tag_filter(self, key: builtins.str, *values: builtins.str) -> "TagFilter":
        '''Adds a new tag filter that should be used for controlling the resources in the Resource Group.

        :param key: The name of the tag to be filtered on.
        :param values: Values to match for the given tag.

        :return:

        The Resource Group configuration object to which the type was
        registered.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12ed5ed6842087154cf14fae494671aceddb862e5958eeee5ca7a890b8062596)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("TagFilter", jsii.invoke(self, "addTagFilter", [key, *values]))

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _constructs_77d1e7e8.IConstruct) -> BoundGroupConfiguration:
        '''Associates this configuration with a construct that is handling the creation of a resource group.

        :param _scope: The construct managing the creation of the Resource Group.

        :return: The configuration to be used for the Resource Group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32e3c7e2fd39ae1ea9d3a5680a3fb5c43d3f5b120df26da33a4559aca97ca8f)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(BoundGroupConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        '''Collection of resource types that are allowed to be in the Resource Group being configured.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))

    @builtins.property
    @jsii.member(jsii_name="tagFilters")
    def tag_filters(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        '''Collection of filters to be used to determine the resources that belong to the Resource Group.'''
        return typing.cast(typing.Mapping[builtins.str, typing.List[builtins.str]], jsii.get(self, "tagFilters"))


class TagFilterProps(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.resourcegroups.TagFilterProps",
):
    '''Configuration options for configuring a Resource Group containing resources based on a set of matching tags.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resource types that are allowed to be in the Resource Group being configured.'''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypes"))

    @builtins.property
    @jsii.member(jsii_name="tagFilters")
    def tag_filters(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]]:
        '''The filters that should be used to determine the resources that belong to the resource group.'''
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]], jsii.get(self, "tagFilters"))


@jsii.implements(IGroupConfiguration)
class CloudFormationStack(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.resourcegroups.CloudFormationStack",
):
    '''Configuration object for a Resource Group whose resources mirror those controlled by a CloudFormation stack.'''

    def __init__(
        self,
        reference: IStackReference,
        *,
        resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Creates a new instance of the CloudFormationStack class.

        :param reference: A reference to a CloudFormation stack that determines the resources to be contained in the Resource Group.
        :param resource_types: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d30c0ad3bf95964bcae166136bd457a620e3b0cc1fd636d7c19977d672cd2b63)
            check_type(argname="argument reference", value=reference, expected_type=type_hints["reference"])
        props = CloudFormationStackProps(resource_types=resource_types)

        jsii.create(self.__class__, self, [reference, props])

    @jsii.member(jsii_name="addResourceType")
    def add_resource_type(self, type_id: builtins.str) -> "CloudFormationStack":
        '''Add a resource type to the resource group.

        If no resource types are registered in the configuration then all resource
        types are allowed.

        :param type_id: The type that is to be added to the resource group.

        :return:

        The Resource Group configuration object to which the type was
        registered.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e437a702d98dce4388109e4a0d9173f59ec224abb44bef88254acee57c84b4ab)
            check_type(argname="argument type_id", value=type_id, expected_type=type_hints["type_id"])
        return typing.cast("CloudFormationStack", jsii.invoke(self, "addResourceType", [type_id]))

    @jsii.member(jsii_name="bind")
    def bind(self, _scope: _constructs_77d1e7e8.IConstruct) -> BoundGroupConfiguration:
        '''Associates this configuration with a construct that is handling the creation of a resource group.

        :param _scope: The construct managing the creation of the Resource Group.

        :return: The configuration to be used for the Resource Group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30885bb32b90e4446f19a5b98bab89fca8f927f92a0be48e4ae605d5c2b9267e)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(BoundGroupConfiguration, jsii.invoke(self, "bind", [_scope]))

    @builtins.property
    @jsii.member(jsii_name="reference")
    def reference(self) -> IStackReference:
        '''The details of the CloudFormation stack that is referenced to create the Resource Group.'''
        return typing.cast(IStackReference, jsii.get(self, "reference"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypes")
    def resource_types(self) -> typing.List[builtins.str]:
        '''Collection of resource types that are allowed to be in the Resource Group being configured.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypes"))


@jsii.implements(IGroup)
class Group(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.resourcegroups.Group",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        configuration: IGroupConfiguration,
        description: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param configuration: 
        :param description: 
        :param name: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99f37663338e9fa663257e532d540b01628dda470b440f5d40a056c51129a2b0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GroupProps(
            configuration=configuration,
            description=description,
            name=name,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromGroupArn")
    @builtins.classmethod
    def from_group_arn(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        arn: builtins.str,
    ) -> IGroup:
        '''
        :param scope: -
        :param id: -
        :param arn: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__546994e5fcd064abb53c20cc57c0eaf8b4353d6f733b70c3c4893a05d87336af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast(IGroup, jsii.sinvoke(cls, "fromGroupArn", [scope, id, arn]))

    @jsii.member(jsii_name="fromGroupAttributes")
    @builtins.classmethod
    def from_group_attributes(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> IGroup:
        '''
        :param scope: -
        :param id: -
        :param arn: 
        :param name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7081677d012441bdffae034a67eaf3da43693019a4495bb9fd81bcc32b154193)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = GroupAttributes(arn=arn, name=name)

        return typing.cast(IGroup, jsii.sinvoke(cls, "fromGroupAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromGroupName")
    @builtins.classmethod
    def from_group_name(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        name: builtins.str,
    ) -> IGroup:
        '''
        :param scope: -
        :param id: -
        :param name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed99a22adcbd5b3a37a238ac97ed1b6842c3fe72f9fd051fac61a8a1d41fbfef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(IGroup, jsii.sinvoke(cls, "fromGroupName", [scope, id, name]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="ARN_FORMAT")
    def ARN_FORMAT(cls) -> _aws_cdk_ceddda9d.ArnFormat:
        return typing.cast(_aws_cdk_ceddda9d.ArnFormat, jsii.sget(cls, "ARN_FORMAT"))

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupArn"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="resource")
    def resource(self) -> _aws_cdk_aws_resourcegroups_ceddda9d.CfnGroup:
        return typing.cast(_aws_cdk_aws_resourcegroups_ceddda9d.CfnGroup, jsii.get(self, "resource"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))


__all__ = [
    "BoundGroupConfiguration",
    "CloudFormationStack",
    "CloudFormationStackProps",
    "Group",
    "GroupAttributes",
    "GroupConfiguration",
    "GroupProps",
    "IGroup",
    "IGroupConfiguration",
    "IStackReference",
    "StackReference",
    "TagFilter",
    "TagFilterProps",
]

publication.publish()

def _typecheckingstub__d78e0c9b073e26af2229294f065139cc61a985550545e80e6090b52d7a8b4815(
    *,
    configuration: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_aws_resourcegroups_ceddda9d.CfnGroup.ConfigurationItemProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    query: typing.Optional[typing.Union[_aws_cdk_aws_resourcegroups_ceddda9d.CfnGroup.ResourceQueryProperty, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65facf546021877ff05946c7a7c8280e51d0dad25de0b0a020c3f77648dfe305(
    *,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f880da69493115ef75f0b4b868b1128afd7424ef3187d6ac5a5f801216816d2(
    *,
    arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914a48dbccb8e839746ef64f3bc92afa7eb37998bac46f29cdced72ae5167695(
    reference: IStackReference,
    *,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0640e9b25e4e9929f13c24c3968210ed7c942b12efcf549a6e3d94a8ef3edf2a(
    props: typing.Optional[TagFilterProps] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d3c1b31024217edf3430298333ec71348a4649848c97a1a474e103db0a9eb9(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    configuration: IGroupConfiguration,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b8a72441cc83c32e5f341c5b69b14ddc027c902f10cb313eed7f83776e4165(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c9b597509fd61a83fc0c7faed4435dfe31ea85b80437ed0ee33a4a8742fa3a7(
    stack: _aws_cdk_ceddda9d.Stack,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fe0b4b4c0fc4b1d4699714498d2bcd73041cfc1f75f0f83f62b81a8125a2caa(
    stack_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eca9d11c312f3365c2d88fc9b5cab689134f0aad15b05fe625b5d34cc8bf6aa4(
    props: typing.Optional[TagFilterProps] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__693709c1c55f21ea386b712c6adeb95a3cbda51eda835b096830e57a596245c8(
    type_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12ed5ed6842087154cf14fae494671aceddb862e5958eeee5ca7a890b8062596(
    key: builtins.str,
    *values: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32e3c7e2fd39ae1ea9d3a5680a3fb5c43d3f5b120df26da33a4559aca97ca8f(
    _scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d30c0ad3bf95964bcae166136bd457a620e3b0cc1fd636d7c19977d672cd2b63(
    reference: IStackReference,
    *,
    resource_types: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e437a702d98dce4388109e4a0d9173f59ec224abb44bef88254acee57c84b4ab(
    type_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30885bb32b90e4446f19a5b98bab89fca8f927f92a0be48e4ae605d5c2b9267e(
    _scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f37663338e9fa663257e532d540b01628dda470b440f5d40a056c51129a2b0(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    configuration: IGroupConfiguration,
    description: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__546994e5fcd064abb53c20cc57c0eaf8b4353d6f733b70c3c4893a05d87336af(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7081677d012441bdffae034a67eaf3da43693019a4495bb9fd81bcc32b154193(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed99a22adcbd5b3a37a238ac97ed1b6842c3fe72f9fd051fac61a8a1d41fbfef(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
