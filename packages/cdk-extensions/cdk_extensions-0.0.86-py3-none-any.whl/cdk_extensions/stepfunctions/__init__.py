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

import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d
import constructs as _constructs_77d1e7e8


class SfnFn(metaclass=jsii.JSIIMeta, jsii_type="cdk-extensions.stepfunctions.SfnFn"):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="array")
    @builtins.classmethod
    def array(cls, *values: typing.Any) -> builtins.str:
        '''
        :param values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa3bb3498c34712cc86cbb0ae66681c3c347acf59909bb9fb336d11a00d440fb)
            check_type(argname="argument values", value=values, expected_type=typing.Tuple[type_hints["values"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(builtins.str, jsii.sinvoke(cls, "array", [*values]))

    @jsii.member(jsii_name="arrayContains")
    @builtins.classmethod
    def array_contains(
        cls,
        array: builtins.str,
        looking_for: typing.Any,
    ) -> builtins.str:
        '''
        :param array: -
        :param looking_for: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a6b0cb485dac38980c26b61a35bd0e347b07808083018d5e96f784fca1484a47)
            check_type(argname="argument array", value=array, expected_type=type_hints["array"])
            check_type(argname="argument looking_for", value=looking_for, expected_type=type_hints["looking_for"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arrayContains", [array, looking_for]))

    @jsii.member(jsii_name="arrayGetItem")
    @builtins.classmethod
    def array_get_item(cls, array: builtins.str, index: typing.Any) -> builtins.str:
        '''
        :param array: -
        :param index: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20201fdf3ed68f1dde0bdb53c493b17ae7590ff39b78553bc213a8a81c959d13)
            check_type(argname="argument array", value=array, expected_type=type_hints["array"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arrayGetItem", [array, index]))

    @jsii.member(jsii_name="arrayLength")
    @builtins.classmethod
    def array_length(cls, array: builtins.str) -> builtins.str:
        '''
        :param array: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f4cbf0c3e6ae20aee3451208ad815e381b44f8155d46bd19190fcf0abfd98ac)
            check_type(argname="argument array", value=array, expected_type=type_hints["array"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arrayLength", [array]))

    @jsii.member(jsii_name="arrayPartition")
    @builtins.classmethod
    def array_partition(cls, array: builtins.str, size: typing.Any) -> builtins.str:
        '''
        :param array: -
        :param size: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcf9a5c483755466147b63db7a3eadc47d12ddd31ea0529681d9187b26649fcf)
            check_type(argname="argument array", value=array, expected_type=type_hints["array"])
            check_type(argname="argument size", value=size, expected_type=type_hints["size"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arrayPartition", [array, size]))

    @jsii.member(jsii_name="arrayRange")
    @builtins.classmethod
    def array_range(
        cls,
        start: typing.Any,
        stop: typing.Any,
        step: typing.Any,
    ) -> builtins.str:
        '''
        :param start: -
        :param stop: -
        :param step: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ced3184ad9264793367b45885c6698e79b5e109abc6e2fb139ab6c9f6e61fdbd)
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            check_type(argname="argument stop", value=stop, expected_type=type_hints["stop"])
            check_type(argname="argument step", value=step, expected_type=type_hints["step"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arrayRange", [start, stop, step]))

    @jsii.member(jsii_name="arrayUnique")
    @builtins.classmethod
    def array_unique(cls, array: builtins.str) -> builtins.str:
        '''
        :param array: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72b5db4cef8674b8ef1c22eb72d8836d605edfdc5c73aaf11ebbd4c3603d467b)
            check_type(argname="argument array", value=array, expected_type=type_hints["array"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "arrayUnique", [array]))

    @jsii.member(jsii_name="base64Decode")
    @builtins.classmethod
    def base64_decode(cls, value: builtins.str) -> builtins.str:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcb18f3203f0bf8ab2df0ce5ae905fd039c266ec29bed518e33d40db9c48d541)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "base64Decode", [value]))

    @jsii.member(jsii_name="base64Encode")
    @builtins.classmethod
    def base64_encode(cls, value: builtins.str) -> builtins.str:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e44ccf7762c15822234b94a7735ef11bd6b9e9c93a34e40cef2139e5f26f32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "base64Encode", [value]))

    @jsii.member(jsii_name="format")
    @builtins.classmethod
    def format(
        cls,
        template: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> builtins.str:
        '''
        :param template: -
        :param values: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76aa9f122748902a1fbce9f0d6b160ffa2b27f7c19b4f5ad2c0f7575f043ca07)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "format", [template, values]))

    @jsii.member(jsii_name="hash")
    @builtins.classmethod
    def hash(cls, data: builtins.str, algorithm: builtins.str) -> builtins.str:
        '''
        :param data: -
        :param algorithm: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a70beba04618382f09b948214701d12e71ae54fea38915b81d6b3946b5b1feb9)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "hash", [data, algorithm]))

    @jsii.member(jsii_name="jsonMerge")
    @builtins.classmethod
    def json_merge(cls, json1: builtins.str, json2: builtins.str) -> builtins.str:
        '''
        :param json1: -
        :param json2: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96b3989905926f55739330b05190760f01ee3a432702a9b0f8d4d304a73cccec)
            check_type(argname="argument json1", value=json1, expected_type=type_hints["json1"])
            check_type(argname="argument json2", value=json2, expected_type=type_hints["json2"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "jsonMerge", [json1, json2]))

    @jsii.member(jsii_name="jsonToString")
    @builtins.classmethod
    def json_to_string(cls, data: builtins.str) -> builtins.str:
        '''
        :param data: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f30335488144c59c680fd5b5dfa8ea3008fd55afa75939d053660b32fce2e887)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "jsonToString", [data]))

    @jsii.member(jsii_name="mathAdd")
    @builtins.classmethod
    def math_add(cls, value: builtins.str, step: typing.Any) -> builtins.str:
        '''
        :param value: -
        :param step: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dae420a5696d775dc67f4e651c00e04970d2bf2645bcd3da806714454aa0999)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument step", value=step, expected_type=type_hints["step"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "mathAdd", [value, step]))

    @jsii.member(jsii_name="mathRandom")
    @builtins.classmethod
    def math_random(cls, start: typing.Any, end: typing.Any) -> builtins.str:
        '''
        :param start: -
        :param end: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4463efb8019e6a1294e2544086537a4da434bd3ad1f423897ce03808d4db337a)
            check_type(argname="argument start", value=start, expected_type=type_hints["start"])
            check_type(argname="argument end", value=end, expected_type=type_hints["end"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "mathRandom", [start, end]))

    @jsii.member(jsii_name="stringSplit")
    @builtins.classmethod
    def string_split(cls, data: builtins.str, splitter: builtins.str) -> builtins.str:
        '''
        :param data: -
        :param splitter: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b70515fcc546ea9de37f014147f8c5d346d2e335ef087275cdf34906155458d)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument splitter", value=splitter, expected_type=type_hints["splitter"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "stringSplit", [data, splitter]))

    @jsii.member(jsii_name="stringToJson")
    @builtins.classmethod
    def string_to_json(cls, data: builtins.str) -> builtins.str:
        '''
        :param data: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9199a87ae8b21ea26373067a205cde7621b4fd9c58ab03b693f40333326680bd)
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "stringToJson", [data]))

    @jsii.member(jsii_name="uuid")
    @builtins.classmethod
    def uuid(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sinvoke(cls, "uuid", []))


class StepFunctionValidation(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.stepfunctions.StepFunctionValidation",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="isIntrinsic")
    @builtins.classmethod
    def is_intrinsic(cls, value: builtins.str) -> builtins.bool:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b14b8ebf388e0dc56974d29cf9555813b77d67f3d654fb2e2d41d7e1916116ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isIntrinsic", [value]))

    @jsii.member(jsii_name="isJsonPath")
    @builtins.classmethod
    def is_json_path(cls, value: builtins.str) -> builtins.bool:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8882cadc4b6842d3ac560f356e77aa89c72cbf019af9d85690205c5b290452fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isJsonPath", [value]))

    @jsii.member(jsii_name="isStatesExpression")
    @builtins.classmethod
    def is_states_expression(cls, value: builtins.str) -> builtins.bool:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdd21264bfa537cd7f04803f0f766ee2c3b53ca4fd8a4329f09a22428782a0a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isStatesExpression", [value]))


@jsii.implements(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, _aws_cdk_aws_stepfunctions_ceddda9d.INextable)
class StringReplace(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.stepfunctions.StringReplace",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        input_string: builtins.str,
        output_key: builtins.str,
        replace: builtins.str,
        search: builtins.str,
    ) -> None:
        '''
        :param scope: -
        :param id: Descriptive identifier for this chainable.
        :param input_string: 
        :param output_key: 
        :param replace: 
        :param search: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05ecf9c2bb8bbe3ed43a3db9415abb3c8bae20c472a7b57fbda881cad071f80c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StringReplaceProps(
            input_string=input_string,
            output_key=output_key,
            replace=replace,
            search=search,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="next")
    def next(
        self,
        state: _aws_cdk_aws_stepfunctions_ceddda9d.IChainable,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.Chain:
        '''Go to the indicated state after this state.

        :param state: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bd3411196c7744e61bac183e83ccbe06a854140b91d4b9305fa68dfbd2f6bd1)
            check_type(argname="argument state", value=state, expected_type=type_hints["state"])
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Chain, jsii.invoke(self, "next", [state]))

    @builtins.property
    @jsii.member(jsii_name="endStates")
    def end_states(self) -> typing.List[_aws_cdk_aws_stepfunctions_ceddda9d.INextable]:
        '''The chainable end state(s) of this chainable.'''
        return typing.cast(typing.List[_aws_cdk_aws_stepfunctions_ceddda9d.INextable], jsii.get(self, "endStates"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''Descriptive identifier for this chainable.'''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="startState")
    def start_state(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.State:
        '''The start state of this chainable.'''
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.State, jsii.get(self, "startState"))


@jsii.data_type(
    jsii_type="cdk-extensions.stepfunctions.StringReplaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "input_string": "inputString",
        "output_key": "outputKey",
        "replace": "replace",
        "search": "search",
    },
)
class StringReplaceProps:
    def __init__(
        self,
        *,
        input_string: builtins.str,
        output_key: builtins.str,
        replace: builtins.str,
        search: builtins.str,
    ) -> None:
        '''
        :param input_string: 
        :param output_key: 
        :param replace: 
        :param search: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5b9fc3796a85df354205104c8ab214537f99cc6b728d0773feb646b380815a1)
            check_type(argname="argument input_string", value=input_string, expected_type=type_hints["input_string"])
            check_type(argname="argument output_key", value=output_key, expected_type=type_hints["output_key"])
            check_type(argname="argument replace", value=replace, expected_type=type_hints["replace"])
            check_type(argname="argument search", value=search, expected_type=type_hints["search"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "input_string": input_string,
            "output_key": output_key,
            "replace": replace,
            "search": search,
        }

    @builtins.property
    def input_string(self) -> builtins.str:
        result = self._values.get("input_string")
        assert result is not None, "Required property 'input_string' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def output_key(self) -> builtins.str:
        result = self._values.get("output_key")
        assert result is not None, "Required property 'output_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replace(self) -> builtins.str:
        result = self._values.get("replace")
        assert result is not None, "Required property 'replace' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def search(self) -> builtins.str:
        result = self._values.get("search")
        assert result is not None, "Required property 'search' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StringReplaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SfnFn",
    "StepFunctionValidation",
    "StringReplace",
    "StringReplaceProps",
]

publication.publish()

def _typecheckingstub__fa3bb3498c34712cc86cbb0ae66681c3c347acf59909bb9fb336d11a00d440fb(
    *values: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6b0cb485dac38980c26b61a35bd0e347b07808083018d5e96f784fca1484a47(
    array: builtins.str,
    looking_for: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20201fdf3ed68f1dde0bdb53c493b17ae7590ff39b78553bc213a8a81c959d13(
    array: builtins.str,
    index: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f4cbf0c3e6ae20aee3451208ad815e381b44f8155d46bd19190fcf0abfd98ac(
    array: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcf9a5c483755466147b63db7a3eadc47d12ddd31ea0529681d9187b26649fcf(
    array: builtins.str,
    size: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ced3184ad9264793367b45885c6698e79b5e109abc6e2fb139ab6c9f6e61fdbd(
    start: typing.Any,
    stop: typing.Any,
    step: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72b5db4cef8674b8ef1c22eb72d8836d605edfdc5c73aaf11ebbd4c3603d467b(
    array: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcb18f3203f0bf8ab2df0ce5ae905fd039c266ec29bed518e33d40db9c48d541(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e44ccf7762c15822234b94a7735ef11bd6b9e9c93a34e40cef2139e5f26f32(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76aa9f122748902a1fbce9f0d6b160ffa2b27f7c19b4f5ad2c0f7575f043ca07(
    template: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a70beba04618382f09b948214701d12e71ae54fea38915b81d6b3946b5b1feb9(
    data: builtins.str,
    algorithm: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96b3989905926f55739330b05190760f01ee3a432702a9b0f8d4d304a73cccec(
    json1: builtins.str,
    json2: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f30335488144c59c680fd5b5dfa8ea3008fd55afa75939d053660b32fce2e887(
    data: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dae420a5696d775dc67f4e651c00e04970d2bf2645bcd3da806714454aa0999(
    value: builtins.str,
    step: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4463efb8019e6a1294e2544086537a4da434bd3ad1f423897ce03808d4db337a(
    start: typing.Any,
    end: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b70515fcc546ea9de37f014147f8c5d346d2e335ef087275cdf34906155458d(
    data: builtins.str,
    splitter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9199a87ae8b21ea26373067a205cde7621b4fd9c58ab03b693f40333326680bd(
    data: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b14b8ebf388e0dc56974d29cf9555813b77d67f3d654fb2e2d41d7e1916116ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8882cadc4b6842d3ac560f356e77aa89c72cbf019af9d85690205c5b290452fe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd21264bfa537cd7f04803f0f766ee2c3b53ca4fd8a4329f09a22428782a0a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05ecf9c2bb8bbe3ed43a3db9415abb3c8bae20c472a7b57fbda881cad071f80c(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    input_string: builtins.str,
    output_key: builtins.str,
    replace: builtins.str,
    search: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bd3411196c7744e61bac183e83ccbe06a854140b91d4b9305fa68dfbd2f6bd1(
    state: _aws_cdk_aws_stepfunctions_ceddda9d.IChainable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5b9fc3796a85df354205104c8ab214537f99cc6b728d0773feb646b380815a1(
    *,
    input_string: builtins.str,
    output_key: builtins.str,
    replace: builtins.str,
    search: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
