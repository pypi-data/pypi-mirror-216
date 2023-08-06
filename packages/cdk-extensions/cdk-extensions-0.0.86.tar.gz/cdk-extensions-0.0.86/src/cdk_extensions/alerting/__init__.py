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
import aws_cdk.aws_events as _aws_cdk_aws_events_ceddda9d
import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import aws_cdk.aws_secretsmanager as _aws_cdk_aws_secretsmanager_ceddda9d
import aws_cdk.aws_stepfunctions as _aws_cdk_aws_stepfunctions_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.AddReferenceProps",
    jsii_struct_bases=[],
    name_mapping={
        "value": "value",
        "delimiter": "delimiter",
        "label": "label",
        "required": "required",
    },
)
class AddReferenceProps:
    def __init__(
        self,
        *,
        value: builtins.str,
        delimiter: typing.Optional["AppendDelimiter"] = None,
        label: typing.Optional[builtins.str] = None,
        required: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param value: 
        :param delimiter: 
        :param label: 
        :param required: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04f904628bb25dde32dd6031cb272c404da266d7f01a88c1db9a10e0415f0bdd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if delimiter is not None:
            self._values["delimiter"] = delimiter
        if label is not None:
            self._values["label"] = label
        if required is not None:
            self._values["required"] = required

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delimiter(self) -> typing.Optional["AppendDelimiter"]:
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional["AppendDelimiter"], result)

    @builtins.property
    def label(self) -> typing.Optional[builtins.str]:
        result = self._values.get("label")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def required(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("required")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddReferenceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AppendDelimiter(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.AppendDelimiter",
):
    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, delimiter: builtins.str) -> "AppendDelimiter":
        '''
        :param delimiter: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25dff048782bd89514e2efe3c493308e5b027e5caea3fc67cb7edc636e45e2bd)
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
        return typing.cast("AppendDelimiter", jsii.sinvoke(cls, "of", [delimiter]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NEWLINE")
    def NEWLINE(cls) -> "AppendDelimiter":
        return typing.cast("AppendDelimiter", jsii.sget(cls, "NEWLINE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="PARAGRAPH")
    def PARAGRAPH(cls) -> "AppendDelimiter":
        return typing.cast("AppendDelimiter", jsii.sget(cls, "PARAGRAPH"))

    @builtins.property
    @jsii.member(jsii_name="delimiter")
    def delimiter(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delimiter"))


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.ConfigComplianceChangeRuleOptions",
    jsii_struct_bases=[],
    name_mapping={
        "include_security_hub": "includeSecurityHub",
        "overrides": "overrides",
        "severity": "severity",
    },
)
class ConfigComplianceChangeRuleOptions:
    def __init__(
        self,
        *,
        include_security_hub: typing.Optional[builtins.bool] = None,
        overrides: typing.Optional[typing.Sequence["IssueHandlerOverride"]] = None,
        severity: typing.Optional[typing.Sequence["InspectorSeverity"]] = None,
    ) -> None:
        '''
        :param include_security_hub: 
        :param overrides: 
        :param severity: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a7fbfd7623d1863957228909a2a94428f87e6aca695a5aad641186c1e0077e0)
            check_type(argname="argument include_security_hub", value=include_security_hub, expected_type=type_hints["include_security_hub"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if include_security_hub is not None:
            self._values["include_security_hub"] = include_security_hub
        if overrides is not None:
            self._values["overrides"] = overrides
        if severity is not None:
            self._values["severity"] = severity

    @builtins.property
    def include_security_hub(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("include_security_hub")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def overrides(self) -> typing.Optional[typing.List["IssueHandlerOverride"]]:
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.List["IssueHandlerOverride"]], result)

    @builtins.property
    def severity(self) -> typing.Optional[typing.List["InspectorSeverity"]]:
        result = self._values.get("severity")
        return typing.cast(typing.Optional[typing.List["InspectorSeverity"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfigComplianceChangeRuleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.DescriptionBuilderIteratorProps",
    jsii_struct_bases=[],
    name_mapping={
        "array_ref": "arrayRef",
        "result_path": "resultPath",
        "field_delimiter": "fieldDelimiter",
        "record_delimiter": "recordDelimiter",
        "section_delimiter": "sectionDelimiter",
        "title": "title",
    },
)
class DescriptionBuilderIteratorProps:
    def __init__(
        self,
        *,
        array_ref: builtins.str,
        result_path: builtins.str,
        field_delimiter: typing.Optional[AppendDelimiter] = None,
        record_delimiter: typing.Optional[AppendDelimiter] = None,
        section_delimiter: typing.Optional[AppendDelimiter] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param array_ref: 
        :param result_path: 
        :param field_delimiter: 
        :param record_delimiter: 
        :param section_delimiter: 
        :param title: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea6e1ba4f2a92d82b0b5b46bef759c993454be033d460bb87e09b078422da893)
            check_type(argname="argument array_ref", value=array_ref, expected_type=type_hints["array_ref"])
            check_type(argname="argument result_path", value=result_path, expected_type=type_hints["result_path"])
            check_type(argname="argument field_delimiter", value=field_delimiter, expected_type=type_hints["field_delimiter"])
            check_type(argname="argument record_delimiter", value=record_delimiter, expected_type=type_hints["record_delimiter"])
            check_type(argname="argument section_delimiter", value=section_delimiter, expected_type=type_hints["section_delimiter"])
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "array_ref": array_ref,
            "result_path": result_path,
        }
        if field_delimiter is not None:
            self._values["field_delimiter"] = field_delimiter
        if record_delimiter is not None:
            self._values["record_delimiter"] = record_delimiter
        if section_delimiter is not None:
            self._values["section_delimiter"] = section_delimiter
        if title is not None:
            self._values["title"] = title

    @builtins.property
    def array_ref(self) -> builtins.str:
        result = self._values.get("array_ref")
        assert result is not None, "Required property 'array_ref' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def result_path(self) -> builtins.str:
        result = self._values.get("result_path")
        assert result is not None, "Required property 'result_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def field_delimiter(self) -> typing.Optional[AppendDelimiter]:
        result = self._values.get("field_delimiter")
        return typing.cast(typing.Optional[AppendDelimiter], result)

    @builtins.property
    def record_delimiter(self) -> typing.Optional[AppendDelimiter]:
        result = self._values.get("record_delimiter")
        return typing.cast(typing.Optional[AppendDelimiter], result)

    @builtins.property
    def section_delimiter(self) -> typing.Optional[AppendDelimiter]:
        result = self._values.get("section_delimiter")
        return typing.cast(typing.Optional[AppendDelimiter], result)

    @builtins.property
    def title(self) -> typing.Optional[builtins.str]:
        result = self._values.get("title")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DescriptionBuilderIteratorProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.DescriptionBuilderProps",
    jsii_struct_bases=[],
    name_mapping={"initial_description": "initialDescription"},
)
class DescriptionBuilderProps:
    def __init__(
        self,
        *,
        initial_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param initial_description: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37fbcb76257f0d6b53c5673dd85b932667d4efe2c20a1d3cda088c388a4a2778)
            check_type(argname="argument initial_description", value=initial_description, expected_type=type_hints["initial_description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if initial_description is not None:
            self._values["initial_description"] = initial_description

    @builtins.property
    def initial_description(self) -> typing.Optional[builtins.str]:
        result = self._values.get("initial_description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DescriptionBuilderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.DescriptionBuilderSectionProps",
    jsii_struct_bases=[],
    name_mapping={"title": "title", "reference_checks": "referenceChecks"},
)
class DescriptionBuilderSectionProps:
    def __init__(
        self,
        *,
        title: builtins.str,
        reference_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param title: 
        :param reference_checks: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eda6817459c7b764f8c57dcbc8259687527b5aa22d72369f5db50a3aeb0ded7)
            check_type(argname="argument title", value=title, expected_type=type_hints["title"])
            check_type(argname="argument reference_checks", value=reference_checks, expected_type=type_hints["reference_checks"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "title": title,
        }
        if reference_checks is not None:
            self._values["reference_checks"] = reference_checks

    @builtins.property
    def title(self) -> builtins.str:
        result = self._values.get("title")
        assert result is not None, "Required property 'title' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def reference_checks(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("reference_checks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DescriptionBuilderSectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.DiscordOverrideOptions",
    jsii_struct_bases=[],
    name_mapping={"channel": "channel", "mentions": "mentions"},
)
class DiscordOverrideOptions:
    def __init__(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        mentions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param channel: 
        :param mentions: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__253bd589f4b779840486be7096aa59433e6c2634024583dedc1e45fa90aefc20)
            check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
            check_type(argname="argument mentions", value=mentions, expected_type=type_hints["mentions"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if channel is not None:
            self._values["channel"] = channel
        if mentions is not None:
            self._values["mentions"] = mentions

    @builtins.property
    def channel(self) -> typing.Optional[builtins.str]:
        result = self._values.get("channel")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mentions(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("mentions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscordOverrideOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class EcrImageScanSeverity(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.EcrImageScanSeverity",
):
    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        name: builtins.str,
        priority: jsii.Number,
        standardized: builtins.str,
    ) -> "EcrImageScanSeverity":
        '''
        :param name: -
        :param priority: -
        :param standardized: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d0339c6d2e7f75b5fad2a1cd75c3f1c5bb5fedaae0d185457222fa11329e56)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument standardized", value=standardized, expected_type=type_hints["standardized"])
        return typing.cast("EcrImageScanSeverity", jsii.sinvoke(cls, "of", [name, priority, standardized]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CRITICAL")
    def CRITICAL(cls) -> "EcrImageScanSeverity":
        return typing.cast("EcrImageScanSeverity", jsii.sget(cls, "CRITICAL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIGH")
    def HIGH(cls) -> "EcrImageScanSeverity":
        return typing.cast("EcrImageScanSeverity", jsii.sget(cls, "HIGH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LOW")
    def LOW(cls) -> "EcrImageScanSeverity":
        return typing.cast("EcrImageScanSeverity", jsii.sget(cls, "LOW"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MEDIUM")
    def MEDIUM(cls) -> "EcrImageScanSeverity":
        return typing.cast("EcrImageScanSeverity", jsii.sget(cls, "MEDIUM"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UNDEFINED")
    def UNDEFINED(cls) -> "EcrImageScanSeverity":
        return typing.cast("EcrImageScanSeverity", jsii.sget(cls, "UNDEFINED"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @builtins.property
    @jsii.member(jsii_name="standardized")
    def standardized(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "standardized"))


class EcrImageScanSeverityConfiguration(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.EcrImageScanSeverityConfiguration",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls) -> "IEcrImageScanSeverityConfiguration":
        return typing.cast("IEcrImageScanSeverityConfiguration", jsii.sinvoke(cls, "all", []))

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(
        cls,
        *levels: EcrImageScanSeverity,
    ) -> "IEcrImageScanSeverityConfiguration":
        '''
        :param levels: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f3c2db4ae04fddf5eaa2a312c7e148c014088162d41c292fe5cbc4bd633cf0c)
            check_type(argname="argument levels", value=levels, expected_type=typing.Tuple[type_hints["levels"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("IEcrImageScanSeverityConfiguration", jsii.sinvoke(cls, "custom", [*levels]))

    @jsii.member(jsii_name="threshold")
    @builtins.classmethod
    def threshold(
        cls,
        level: EcrImageScanSeverity,
    ) -> "IEcrImageScanSeverityConfiguration":
        '''
        :param level: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e3541bf824f9e2d2c143b2a3a38dfbd2199f9965389dea35d2ec38cea4a6e5e)
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
        return typing.cast("IEcrImageScanSeverityConfiguration", jsii.sinvoke(cls, "threshold", [level]))


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.EcrScanFindingEventOptions",
    jsii_struct_bases=[],
    name_mapping={"overrides": "overrides", "severity": "severity"},
)
class EcrScanFindingEventOptions:
    def __init__(
        self,
        *,
        overrides: typing.Optional[typing.Sequence["IssueHandlerOverride"]] = None,
        severity: typing.Optional["IEcrImageScanSeverityConfiguration"] = None,
    ) -> None:
        '''
        :param overrides: 
        :param severity: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f861d1625d2bf64d7799c9afaa9c4dbe8c48a75ba31a62300f13388932a11474)
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if overrides is not None:
            self._values["overrides"] = overrides
        if severity is not None:
            self._values["severity"] = severity

    @builtins.property
    def overrides(self) -> typing.Optional[typing.List["IssueHandlerOverride"]]:
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.List["IssueHandlerOverride"]], result)

    @builtins.property
    def severity(self) -> typing.Optional["IEcrImageScanSeverityConfiguration"]:
        result = self._values.get("severity")
        return typing.cast(typing.Optional["IEcrImageScanSeverityConfiguration"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcrScanFindingEventOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.GuardDutyFindingRuleOptions",
    jsii_struct_bases=[],
    name_mapping={"overrides": "overrides", "severity": "severity"},
)
class GuardDutyFindingRuleOptions:
    def __init__(
        self,
        *,
        overrides: typing.Optional[typing.Sequence["IssueHandlerOverride"]] = None,
        severity: typing.Optional[typing.Sequence["GuardDutySeverity"]] = None,
    ) -> None:
        '''
        :param overrides: 
        :param severity: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fd75bc62445d8ffbf385240f2d7f90d7bd38795e18ae196db64a84d1235295b)
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if overrides is not None:
            self._values["overrides"] = overrides
        if severity is not None:
            self._values["severity"] = severity

    @builtins.property
    def overrides(self) -> typing.Optional[typing.List["IssueHandlerOverride"]]:
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.List["IssueHandlerOverride"]], result)

    @builtins.property
    def severity(self) -> typing.Optional[typing.List["GuardDutySeverity"]]:
        result = self._values.get("severity")
        return typing.cast(typing.Optional[typing.List["GuardDutySeverity"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuardDutyFindingRuleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GuardDutySeverity(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.GuardDutySeverity",
):
    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls) -> typing.List["GuardDutySeverity"]:
        return typing.cast(typing.List["GuardDutySeverity"], jsii.sinvoke(cls, "all", []))

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, *levels: "GuardDutySeverity") -> typing.List["GuardDutySeverity"]:
        '''
        :param levels: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7054b205177878cf39892467f187d50136525d04d5d4a40cc90ab08257d3989b)
            check_type(argname="argument levels", value=levels, expected_type=typing.Tuple[type_hints["levels"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(typing.List["GuardDutySeverity"], jsii.sinvoke(cls, "custom", [*levels]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        standardized: builtins.str,
        lower_bound: typing.Optional[jsii.Number] = None,
        upper_bound: typing.Optional[jsii.Number] = None,
    ) -> "GuardDutySeverity":
        '''
        :param standardized: -
        :param lower_bound: -
        :param upper_bound: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__015817cc0484b8c3fd8aa7e8b3ce0698c463101fe83055b3e8ddba4d892eed1f)
            check_type(argname="argument standardized", value=standardized, expected_type=type_hints["standardized"])
            check_type(argname="argument lower_bound", value=lower_bound, expected_type=type_hints["lower_bound"])
            check_type(argname="argument upper_bound", value=upper_bound, expected_type=type_hints["upper_bound"])
        return typing.cast("GuardDutySeverity", jsii.sinvoke(cls, "of", [standardized, lower_bound, upper_bound]))

    @jsii.member(jsii_name="threshold")
    @builtins.classmethod
    def threshold(cls, level: "GuardDutySeverity") -> typing.List["GuardDutySeverity"]:
        '''
        :param level: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11e5ba579f1ca10ddac7ef691ff93b2112cf9c9eba602aa79738cddd50b4b8cb)
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
        return typing.cast(typing.List["GuardDutySeverity"], jsii.sinvoke(cls, "threshold", [level]))

    @jsii.member(jsii_name="buildCondition")
    def build_condition(
        self,
        path: builtins.str,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.Condition:
        '''
        :param path: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__914c5cc51dfbef689f3ddb96d90c1a844fd7c1ef367c71cee64ae4bda11d8456)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Condition, jsii.invoke(self, "buildCondition", [path]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CRITICAL")
    def CRITICAL(cls) -> "GuardDutySeverity":
        return typing.cast("GuardDutySeverity", jsii.sget(cls, "CRITICAL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIGH")
    def HIGH(cls) -> "GuardDutySeverity":
        return typing.cast("GuardDutySeverity", jsii.sget(cls, "HIGH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INFORMATIONAL")
    def INFORMATIONAL(cls) -> "GuardDutySeverity":
        return typing.cast("GuardDutySeverity", jsii.sget(cls, "INFORMATIONAL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LOW")
    def LOW(cls) -> "GuardDutySeverity":
        return typing.cast("GuardDutySeverity", jsii.sget(cls, "LOW"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MEDIUM")
    def MEDIUM(cls) -> "GuardDutySeverity":
        return typing.cast("GuardDutySeverity", jsii.sget(cls, "MEDIUM"))

    @builtins.property
    @jsii.member(jsii_name="standardized")
    def standardized(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "standardized"))

    @builtins.property
    @jsii.member(jsii_name="lowerBound")
    def lower_bound(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "lowerBound"))

    @builtins.property
    @jsii.member(jsii_name="upperBound")
    def upper_bound(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "upperBound"))


@jsii.interface(jsii_type="cdk-extensions.alerting.IDelayedChainable")
class IDelayedChainable(typing_extensions.Protocol):
    @jsii.member(jsii_name="render")
    def render(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        ...


class _IDelayedChainableProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.alerting.IDelayedChainable"

    @jsii.member(jsii_name="render")
    def render(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "render", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDelayedChainable).__jsii_proxy_class__ = lambda : _IDelayedChainableProxy


@jsii.interface(jsii_type="cdk-extensions.alerting.IDescriptionBuilderComponent")
class IDescriptionBuilderComponent(IDelayedChainable, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="classifier")
    def classifier(self) -> builtins.str:
        ...

    @jsii.member(jsii_name="addIterator")
    def add_iterator(
        self,
        id: builtins.str,
        *,
        array_ref: builtins.str,
        result_path: builtins.str,
        field_delimiter: typing.Optional[AppendDelimiter] = None,
        record_delimiter: typing.Optional[AppendDelimiter] = None,
        section_delimiter: typing.Optional[AppendDelimiter] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> "DescriptionBuilderIterator":
        '''
        :param id: -
        :param array_ref: 
        :param result_path: 
        :param field_delimiter: 
        :param record_delimiter: 
        :param section_delimiter: 
        :param title: 
        '''
        ...

    @jsii.member(jsii_name="addReference")
    def add_reference(
        self,
        id: builtins.str,
        *,
        value: builtins.str,
        delimiter: typing.Optional[AppendDelimiter] = None,
        label: typing.Optional[builtins.str] = None,
        required: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param value: 
        :param delimiter: 
        :param label: 
        :param required: 
        '''
        ...

    @jsii.member(jsii_name="setDelimiter")
    def set_delimiter(
        self,
        id: builtins.str,
        *,
        delimiter: AppendDelimiter,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param delimiter: 
        '''
        ...

    @jsii.member(jsii_name="write")
    def write(
        self,
        id: builtins.str,
        *,
        value: builtins.str,
        default_delimiter: typing.Optional[AppendDelimiter] = None,
        delimiter: typing.Optional[AppendDelimiter] = None,
        prefix: typing.Optional[builtins.str] = None,
        required: typing.Optional[builtins.bool] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param value: 
        :param default_delimiter: 
        :param delimiter: 
        :param prefix: 
        :param required: 
        :param suffix: 
        '''
        ...


class _IDescriptionBuilderComponentProxy(
    jsii.proxy_for(IDelayedChainable), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.alerting.IDescriptionBuilderComponent"

    @builtins.property
    @jsii.member(jsii_name="classifier")
    def classifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "classifier"))

    @jsii.member(jsii_name="addIterator")
    def add_iterator(
        self,
        id: builtins.str,
        *,
        array_ref: builtins.str,
        result_path: builtins.str,
        field_delimiter: typing.Optional[AppendDelimiter] = None,
        record_delimiter: typing.Optional[AppendDelimiter] = None,
        section_delimiter: typing.Optional[AppendDelimiter] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> "DescriptionBuilderIterator":
        '''
        :param id: -
        :param array_ref: 
        :param result_path: 
        :param field_delimiter: 
        :param record_delimiter: 
        :param section_delimiter: 
        :param title: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2811087530adfda34e0d5ca69f82bf4edfe4dd7dead821ae656750beaee108ad)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DescriptionBuilderIteratorProps(
            array_ref=array_ref,
            result_path=result_path,
            field_delimiter=field_delimiter,
            record_delimiter=record_delimiter,
            section_delimiter=section_delimiter,
            title=title,
        )

        return typing.cast("DescriptionBuilderIterator", jsii.invoke(self, "addIterator", [id, props]))

    @jsii.member(jsii_name="addReference")
    def add_reference(
        self,
        id: builtins.str,
        *,
        value: builtins.str,
        delimiter: typing.Optional[AppendDelimiter] = None,
        label: typing.Optional[builtins.str] = None,
        required: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param value: 
        :param delimiter: 
        :param label: 
        :param required: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__407e002cef1199f985cb7b8d4a606f3303e0b3adb37ec32da2b4e1c5bb60c9c8)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AddReferenceProps(
            value=value, delimiter=delimiter, label=label, required=required
        )

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "addReference", [id, props]))

    @jsii.member(jsii_name="setDelimiter")
    def set_delimiter(
        self,
        id: builtins.str,
        *,
        delimiter: AppendDelimiter,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param delimiter: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b703a54f51bfd91257570f2784d19f7a98fec6d940a794f7fa49d41fa63a6b6e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SetDelimiterProps(delimiter=delimiter)

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "setDelimiter", [id, props]))

    @jsii.member(jsii_name="write")
    def write(
        self,
        id: builtins.str,
        *,
        value: builtins.str,
        default_delimiter: typing.Optional[AppendDelimiter] = None,
        delimiter: typing.Optional[AppendDelimiter] = None,
        prefix: typing.Optional[builtins.str] = None,
        required: typing.Optional[builtins.bool] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param value: 
        :param default_delimiter: 
        :param delimiter: 
        :param prefix: 
        :param required: 
        :param suffix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ef53e69c71c047fdd6c569e1e0bc77987b471295de0a6231aff47a94acce4d4)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WriteProps(
            value=value,
            default_delimiter=default_delimiter,
            delimiter=delimiter,
            prefix=prefix,
            required=required,
            suffix=suffix,
        )

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "write", [id, props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IDescriptionBuilderComponent).__jsii_proxy_class__ = lambda : _IDescriptionBuilderComponentProxy


@jsii.interface(jsii_type="cdk-extensions.alerting.IEcrImageScanSeverityConfiguration")
class IEcrImageScanSeverityConfiguration(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="levels")
    def levels(self) -> typing.List[EcrImageScanSeverity]:
        ...


class _IEcrImageScanSeverityConfigurationProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.alerting.IEcrImageScanSeverityConfiguration"

    @builtins.property
    @jsii.member(jsii_name="levels")
    def levels(self) -> typing.List[EcrImageScanSeverity]:
        return typing.cast(typing.List[EcrImageScanSeverity], jsii.get(self, "levels"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IEcrImageScanSeverityConfiguration).__jsii_proxy_class__ = lambda : _IEcrImageScanSeverityConfigurationProxy


@jsii.interface(jsii_type="cdk-extensions.alerting.IIssueHandler")
class IIssueHandler(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine:
        ...

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        ...


class _IIssueHandlerProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.alerting.IIssueHandler"

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine, jsii.get(self, "handler"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIssueHandler).__jsii_proxy_class__ = lambda : _IIssueHandlerProxy


@jsii.interface(jsii_type="cdk-extensions.alerting.IIssueParser")
class IIssueParser(_aws_cdk_ceddda9d.IResource, typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine:
        ...

    @builtins.property
    @jsii.member(jsii_name="matchType")
    def match_type(self) -> builtins.str:
        ...

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        node: _constructs_77d1e7e8.IConstruct,
    ) -> typing.List["IssueTrigger"]:
        '''
        :param node: -
        '''
        ...


class _IIssueParserProxy(
    jsii.proxy_for(_aws_cdk_ceddda9d.IResource), # type: ignore[misc]
):
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.alerting.IIssueParser"

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine, jsii.get(self, "handler"))

    @builtins.property
    @jsii.member(jsii_name="matchType")
    def match_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchType"))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        node: _constructs_77d1e7e8.IConstruct,
    ) -> typing.List["IssueTrigger"]:
        '''
        :param node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca6411dafdb3a630d40eb02ceb6e0f9eac287717175f980c56ed3c9667dd6ebf)
            check_type(argname="argument node", value=node, expected_type=type_hints["node"])
        return typing.cast(typing.List["IssueTrigger"], jsii.invoke(self, "bind", [node]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIssueParser).__jsii_proxy_class__ = lambda : _IIssueParserProxy


@jsii.interface(jsii_type="cdk-extensions.alerting.ISecurityHubSeverityConfiguration")
class ISecurityHubSeverityConfiguration(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="levels")
    def levels(self) -> typing.List["SecurityHubSeverity"]:
        ...


class _ISecurityHubSeverityConfigurationProxy:
    __jsii_type__: typing.ClassVar[str] = "cdk-extensions.alerting.ISecurityHubSeverityConfiguration"

    @builtins.property
    @jsii.member(jsii_name="levels")
    def levels(self) -> typing.List["SecurityHubSeverity"]:
        return typing.cast(typing.List["SecurityHubSeverity"], jsii.get(self, "levels"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISecurityHubSeverityConfiguration).__jsii_proxy_class__ = lambda : _ISecurityHubSeverityConfigurationProxy


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.InspectorFindingEventOptions",
    jsii_struct_bases=[],
    name_mapping={"overrides": "overrides", "severity": "severity"},
)
class InspectorFindingEventOptions:
    def __init__(
        self,
        *,
        overrides: typing.Optional[typing.Sequence["IssueHandlerOverride"]] = None,
        severity: typing.Optional[typing.Sequence["InspectorSeverity"]] = None,
    ) -> None:
        '''
        :param overrides: 
        :param severity: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c503396c1371555347496adc9a21268c35b6a2316731a0e9e2fd48db7b3d993)
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if overrides is not None:
            self._values["overrides"] = overrides
        if severity is not None:
            self._values["severity"] = severity

    @builtins.property
    def overrides(self) -> typing.Optional[typing.List["IssueHandlerOverride"]]:
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.List["IssueHandlerOverride"]], result)

    @builtins.property
    def severity(self) -> typing.Optional[typing.List["InspectorSeverity"]]:
        result = self._values.get("severity")
        return typing.cast(typing.Optional[typing.List["InspectorSeverity"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InspectorFindingEventOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class InspectorSeverity(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.InspectorSeverity",
):
    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls) -> typing.List["InspectorSeverity"]:
        return typing.cast(typing.List["InspectorSeverity"], jsii.sinvoke(cls, "all", []))

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, *levels: "InspectorSeverity") -> typing.List["InspectorSeverity"]:
        '''
        :param levels: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7135596fcdd94bfa8874941eea15dbc9dcfad89a2df7658f0eebcede3d2bb7a6)
            check_type(argname="argument levels", value=levels, expected_type=typing.Tuple[type_hints["levels"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(typing.List["InspectorSeverity"], jsii.sinvoke(cls, "custom", [*levels]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        standardized: builtins.str,
        original: builtins.str,
        priority: jsii.Number,
    ) -> "InspectorSeverity":
        '''
        :param standardized: -
        :param original: -
        :param priority: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef21c3e44aabcc6d32cfa08ddf1fe98813ba40dfa40ebfcf5620718f80cdb911)
            check_type(argname="argument standardized", value=standardized, expected_type=type_hints["standardized"])
            check_type(argname="argument original", value=original, expected_type=type_hints["original"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        return typing.cast("InspectorSeverity", jsii.sinvoke(cls, "of", [standardized, original, priority]))

    @jsii.member(jsii_name="threshold")
    @builtins.classmethod
    def threshold(cls, level: "InspectorSeverity") -> typing.List["InspectorSeverity"]:
        '''
        :param level: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ff52cc5f981ba30046f04d62b2c8a6bdb7725b4e38d07d3a29ca5dec4ff7db2)
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
        return typing.cast(typing.List["InspectorSeverity"], jsii.sinvoke(cls, "threshold", [level]))

    @jsii.member(jsii_name="buildCondition")
    def build_condition(
        self,
        path: builtins.str,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.Condition:
        '''
        :param path: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__add09d93d064fe5f98082939df59303379ccf56d73870b39e6b320fedfe6964d)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Condition, jsii.invoke(self, "buildCondition", [path]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CRITICAL")
    def CRITICAL(cls) -> "InspectorSeverity":
        return typing.cast("InspectorSeverity", jsii.sget(cls, "CRITICAL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIGH")
    def HIGH(cls) -> "InspectorSeverity":
        return typing.cast("InspectorSeverity", jsii.sget(cls, "HIGH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INFORMATIONAL")
    def INFORMATIONAL(cls) -> "InspectorSeverity":
        return typing.cast("InspectorSeverity", jsii.sget(cls, "INFORMATIONAL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LOW")
    def LOW(cls) -> "InspectorSeverity":
        return typing.cast("InspectorSeverity", jsii.sget(cls, "LOW"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MEDIUM")
    def MEDIUM(cls) -> "InspectorSeverity":
        return typing.cast("InspectorSeverity", jsii.sget(cls, "MEDIUM"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UNTRIAGED")
    def UNTRIAGED(cls) -> "InspectorSeverity":
        return typing.cast("InspectorSeverity", jsii.sget(cls, "UNTRIAGED"))

    @builtins.property
    @jsii.member(jsii_name="original")
    def original(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "original"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @builtins.property
    @jsii.member(jsii_name="standardized")
    def standardized(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "standardized"))


class IssueHander(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.IssueHander",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="discord")
    @builtins.classmethod
    def discord(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        channel: builtins.str,
        token: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
        mentions: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union["StateMachineLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "Discord":
        '''
        :param scope: -
        :param id: -
        :param channel: 
        :param token: 
        :param event_bus: 
        :param mentions: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f869ab3c2616a04b67f30bb9166b3c542397e1994c482091441b40066447005e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DiscordProps(
            channel=channel,
            token=token,
            event_bus=event_bus,
            mentions=mentions,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast("Discord", jsii.sinvoke(cls, "discord", [scope, id, props]))

    @jsii.member(jsii_name="jiraTicket")
    @builtins.classmethod
    def jira_ticket(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        credentials: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        issue_type: builtins.str,
        jira_url: builtins.str,
        priority_map: typing.Union["JiraTicketPriorityMap", typing.Dict[builtins.str, typing.Any]],
        project: builtins.str,
        assignee: typing.Optional[builtins.str] = None,
        event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union["StateMachineLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "JiraTicket":
        '''
        :param scope: -
        :param id: -
        :param credentials: 
        :param issue_type: 
        :param jira_url: 
        :param priority_map: 
        :param project: 
        :param assignee: 
        :param event_bus: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc82eedaec69377fec470cfcf06b82e1b425e2a8c85b604da5b7375421112d61)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = JiraTicketProps(
            credentials=credentials,
            issue_type=issue_type,
            jira_url=jira_url,
            priority_map=priority_map,
            project=project,
            assignee=assignee,
            event_bus=event_bus,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast("JiraTicket", jsii.sinvoke(cls, "jiraTicket", [scope, id, props]))


class IssueHandlerOverride(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.IssueHandlerOverride",
):
    def __init__(
        self,
        handler: IIssueHandler,
        overrides: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''
        :param handler: -
        :param overrides: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71c067f96e657bdfe55287a28ac52f9563da10b89615bb14e3ba931322f16324)
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
        jsii.create(self.__class__, self, [handler, overrides])

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> IIssueHandler:
        return typing.cast(IIssueHandler, jsii.get(self, "handler"))

    @builtins.property
    @jsii.member(jsii_name="overrides")
    def overrides(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "overrides"))


class IssueManager(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.IssueManager",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        handlers: typing.Optional[typing.Sequence[IIssueHandler]] = None,
        name: typing.Optional[builtins.str] = None,
        parsers: typing.Optional[typing.Sequence[IIssueParser]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param handlers: 
        :param name: 
        :param parsers: 
        :param timeout: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17a0a3e999f7e38036ae2886cdec0fd7d970e598852259abe7f608ddf4ec7721)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IssueManagerProps(
            handlers=handlers,
            name=name,
            parsers=parsers,
            timeout=timeout,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addEventRules")
    def _add_event_rules(
        self,
        state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine,
    ) -> None:
        '''
        :param state_machine: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__006da00f8a75f6b92f98098984ff0af078263991e437146ac4127a85a112a3ca)
            check_type(argname="argument state_machine", value=state_machine, expected_type=type_hints["state_machine"])
        return typing.cast(None, jsii.invoke(self, "addEventRules", [state_machine]))

    @jsii.member(jsii_name="addHandler")
    def add_handler(self, handler: IIssueHandler) -> None:
        '''Adds a destination that handles issues that get passed to the issue manager.

        :param handler: The destination that will handle issues that have been raised.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__654b7156f2800145e438153ffe09c71e5081c98202b48f3edc5f002bf19055ab)
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
        return typing.cast(None, jsii.invoke(self, "addHandler", [handler]))

    @jsii.member(jsii_name="addIssueParser")
    def add_issue_parser(self, parser: IIssueParser) -> None:
        '''Adds a parser that is used to transform incoming issues into a known format that can be passed to the destinations where they will be consumed by users.

        :param parser: A parser that handles a specific type of event that should trigger an issue to be raised.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d7f6de6f0e05b39da7c8baab073824cfd3e82aa3c5e53c2970b4ddd3bca5778)
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
        return typing.cast(None, jsii.invoke(self, "addIssueParser", [parser]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "timeout"))


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.IssueManagerProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "handlers": "handlers",
        "name": "name",
        "parsers": "parsers",
        "timeout": "timeout",
    },
)
class IssueManagerProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        handlers: typing.Optional[typing.Sequence[IIssueHandler]] = None,
        name: typing.Optional[builtins.str] = None,
        parsers: typing.Optional[typing.Sequence[IIssueParser]] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param handlers: 
        :param name: 
        :param parsers: 
        :param timeout: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e29efc7fa79c705c84d2f4a658b848da2928c0ddd24221ea7888cdf35bbdf296)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument handlers", value=handlers, expected_type=type_hints["handlers"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument parsers", value=parsers, expected_type=type_hints["parsers"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if handlers is not None:
            self._values["handlers"] = handlers
        if name is not None:
            self._values["name"] = name
        if parsers is not None:
            self._values["parsers"] = parsers
        if timeout is not None:
            self._values["timeout"] = timeout

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
    def handlers(self) -> typing.Optional[typing.List[IIssueHandler]]:
        result = self._values.get("handlers")
        return typing.cast(typing.Optional[typing.List[IIssueHandler]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parsers(self) -> typing.Optional[typing.List[IIssueParser]]:
        result = self._values.get("parsers")
        return typing.cast(typing.Optional[typing.List[IIssueParser]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssueManagerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IssueParser(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.IssueParser",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="configComplianceChange")
    @builtins.classmethod
    def config_compliance_change(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union["StateMachineLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "ConfigComplianceChange":
        '''
        :param scope: -
        :param id: -
        :param match_type: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__648c3911944076b0bf1ca667d34ed7e3c3871836988c48ff5e5ae3854255d86d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ConfigComplianceChangeProps(
            match_type=match_type,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast("ConfigComplianceChange", jsii.sinvoke(cls, "configComplianceChange", [scope, id, props]))

    @jsii.member(jsii_name="ecrScanFinding")
    @builtins.classmethod
    def ecr_scan_finding(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union["StateMachineLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "EcrScanFinding":
        '''
        :param scope: -
        :param id: -
        :param match_type: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6abcb9f27bdf7ccef0c6a644d8abfbb4f13d78d8a1519ce50db75e4494d3bb7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EcrScanFindingProps(
            match_type=match_type,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast("EcrScanFinding", jsii.sinvoke(cls, "ecrScanFinding", [scope, id, props]))

    @jsii.member(jsii_name="guardDutyFinding")
    @builtins.classmethod
    def guard_duty_finding(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        logging: typing.Optional[typing.Union["StateMachineLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "GuardDutyFinding":
        '''
        :param scope: -
        :param id: -
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1aad78620c0e98f670fddddcf0a5dc72d486a34a04977e10426e875da960857e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GuardDutyFindingProps(
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast("GuardDutyFinding", jsii.sinvoke(cls, "guardDutyFinding", [scope, id, props]))

    @jsii.member(jsii_name="inspectorFinding")
    @builtins.classmethod
    def inspector_finding(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union["StateMachineLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "InspectorFinding":
        '''
        :param scope: -
        :param id: -
        :param match_type: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e8fcbf9702240630da05ae5ef9be7931f2f71960c1d6d3aaf5062ec365baa64)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InspectorFindingProps(
            match_type=match_type,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast("InspectorFinding", jsii.sinvoke(cls, "inspectorFinding", [scope, id, props]))

    @jsii.member(jsii_name="openSearchEvent")
    @builtins.classmethod
    def open_search_event(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union["StateMachineLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "OpenSearchEvent":
        '''
        :param scope: -
        :param id: -
        :param match_type: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b81ee6b7854b5fbce0b73e4ecaa7916dd5ce8ba3f9409a6de2f327dbd5b6890)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = OpenSearchEventProps(
            match_type=match_type,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast("OpenSearchEvent", jsii.sinvoke(cls, "openSearchEvent", [scope, id, props]))

    @jsii.member(jsii_name="securityHubFinding")
    @builtins.classmethod
    def security_hub_finding(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union["StateMachineLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> "SecurityHubFinding":
        '''
        :param scope: -
        :param id: -
        :param match_type: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4a4ad71f1d1a7c0341ca14f2d361fd2b7a761f8fbda6ce95328e5d5a136bf71)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecurityHubFindingProps(
            match_type=match_type,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        return typing.cast("SecurityHubFinding", jsii.sinvoke(cls, "securityHubFinding", [scope, id, props]))


class IssuePluginBase(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.alerting.IssuePluginBase",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        logging: typing.Optional[typing.Union["StateMachineLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__027fc616c754753d62015be334050a7b4e26be331d5e20391a42498402fa2455)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IssuePluginBaseProps(
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="buildLogging")
    def _build_logging(
        self,
    ) -> typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.LogOptions]:
        return typing.cast(typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.LogOptions], jsii.invoke(self, "buildLogging", []))

    @builtins.property
    @jsii.member(jsii_name="logging")
    def logging(self) -> "StateMachineLogging":
        return typing.cast("StateMachineLogging", jsii.get(self, "logging"))


class _IssuePluginBaseProxy(
    IssuePluginBase,
    jsii.proxy_for(_aws_cdk_ceddda9d.Resource), # type: ignore[misc]
):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, IssuePluginBase).__jsii_proxy_class__ = lambda : _IssuePluginBaseProxy


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.IssuePluginBaseProps",
    jsii_struct_bases=[_aws_cdk_ceddda9d.ResourceProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "logging": "logging",
    },
)
class IssuePluginBaseProps(_aws_cdk_ceddda9d.ResourceProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union["StateMachineLogging", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param logging: 
        '''
        if isinstance(logging, dict):
            logging = StateMachineLogging(**logging)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f634e82d7e189610321f5dd3c927a2dc1d40995c6f87f66ebe13118b5b877c8)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if logging is not None:
            self._values["logging"] = logging

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
    def logging(self) -> typing.Optional["StateMachineLogging"]:
        result = self._values.get("logging")
        return typing.cast(typing.Optional["StateMachineLogging"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssuePluginBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class IssueTrigger(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.IssueTrigger",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        event_pattern: typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]],
        parser: IIssueParser,
        overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param event_pattern: 
        :param parser: 
        :param overrides: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56df0d9f4491a32d9f6ba0466693d652b321500a63f290664ccd18f865f059fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IssueTriggerProps(
            event_pattern=event_pattern, parser=parser, overrides=overrides
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addOverride")
    def add_override(self, handler_overrides: IssueHandlerOverride) -> None:
        '''
        :param handler_overrides: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f18ea78c183fd470371a786755a599e139cd9b3f8f9d8654118c0a202e550f1)
            check_type(argname="argument handler_overrides", value=handler_overrides, expected_type=type_hints["handler_overrides"])
        return typing.cast(None, jsii.invoke(self, "addOverride", [handler_overrides]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine,
    ) -> _aws_cdk_aws_events_ceddda9d.Rule:
        '''
        :param state_machine: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64c8214e6d65268ffc7a640ba6f7c49c65a6e0d9788c3ca8448d90ddfe3272ab)
            check_type(argname="argument state_machine", value=state_machine, expected_type=type_hints["state_machine"])
        return typing.cast(_aws_cdk_aws_events_ceddda9d.Rule, jsii.invoke(self, "bind", [state_machine]))

    @builtins.property
    @jsii.member(jsii_name="eventPattern")
    def event_pattern(self) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, jsii.get(self, "eventPattern"))

    @builtins.property
    @jsii.member(jsii_name="overrides")
    def overrides(self) -> typing.List[IssueHandlerOverride]:
        return typing.cast(typing.List[IssueHandlerOverride], jsii.get(self, "overrides"))

    @builtins.property
    @jsii.member(jsii_name="parser")
    def parser(self) -> IIssueParser:
        return typing.cast(IIssueParser, jsii.get(self, "parser"))


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.IssueTriggerProps",
    jsii_struct_bases=[],
    name_mapping={
        "event_pattern": "eventPattern",
        "parser": "parser",
        "overrides": "overrides",
    },
)
class IssueTriggerProps:
    def __init__(
        self,
        *,
        event_pattern: typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]],
        parser: IIssueParser,
        overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
    ) -> None:
        '''
        :param event_pattern: 
        :param parser: 
        :param overrides: 
        '''
        if isinstance(event_pattern, dict):
            event_pattern = _aws_cdk_aws_events_ceddda9d.EventPattern(**event_pattern)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc891efbaae81aac0dc215f01b59a21abd6ef60e4aee7dda84e6a919e5d93ca8)
            check_type(argname="argument event_pattern", value=event_pattern, expected_type=type_hints["event_pattern"])
            check_type(argname="argument parser", value=parser, expected_type=type_hints["parser"])
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "event_pattern": event_pattern,
            "parser": parser,
        }
        if overrides is not None:
            self._values["overrides"] = overrides

    @builtins.property
    def event_pattern(self) -> _aws_cdk_aws_events_ceddda9d.EventPattern:
        result = self._values.get("event_pattern")
        assert result is not None, "Required property 'event_pattern' is missing"
        return typing.cast(_aws_cdk_aws_events_ceddda9d.EventPattern, result)

    @builtins.property
    def parser(self) -> IIssueParser:
        result = self._values.get("parser")
        assert result is not None, "Required property 'parser' is missing"
        return typing.cast(IIssueParser, result)

    @builtins.property
    def overrides(self) -> typing.Optional[typing.List[IssueHandlerOverride]]:
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.List[IssueHandlerOverride]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssueTriggerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IIssueHandler)
class JiraTicket(
    IssuePluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.JiraTicket",
):
    '''A standardized implementation that allows Jira tickets to be created in response to events detected in AWS.

    Intended for use with the ``IssueManager`` state machine which allows
    arbitrary types of events to be processed into standard values and then
    output or one of more issue tracking services.

    :see: `AWS-CreateJiraIssue <https://docs.aws.amazon.com/systems-manager-automation-runbooks/latest/userguide/automation-aws-createjiraissue.html>`_
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        credentials: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        issue_type: builtins.str,
        jira_url: builtins.str,
        priority_map: typing.Union["JiraTicketPriorityMap", typing.Dict[builtins.str, typing.Any]],
        project: builtins.str,
        assignee: typing.Optional[builtins.str] = None,
        event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union["StateMachineLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the JiraTicket class.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param credentials: 
        :param issue_type: 
        :param jira_url: 
        :param priority_map: 
        :param project: 
        :param assignee: 
        :param event_bus: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__faa3790c193df8caeefa2eb5592127364a27e0fb785386efce4e0e73c6c1272d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = JiraTicketProps(
            credentials=credentials,
            issue_type=issue_type,
            jira_url=jira_url,
            priority_map=priority_map,
            project=project,
            assignee=assignee,
            event_bus=event_bus,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="buildEventOverrides")
    def build_event_overrides(
        self,
        *,
        assignee: typing.Optional[builtins.str] = None,
        issue_priority: typing.Optional[builtins.str] = None,
        issue_type: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
    ) -> IssueHandlerOverride:
        '''
        :param assignee: 
        :param issue_priority: 
        :param issue_type: 
        :param project: 
        '''
        options = JiraTicketOverrideOptions(
            assignee=assignee,
            issue_priority=issue_priority,
            issue_type=issue_type,
            project=project,
        )

        return typing.cast(IssueHandlerOverride, jsii.invoke(self, "buildEventOverrides", [options]))

    @jsii.member(jsii_name="buildSeverityMap")
    def build_severity_map(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.Chain:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Chain, jsii.invoke(self, "buildSeverityMap", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_NAME")
    def DEFAULT_NAME(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "DEFAULT_NAME"))

    @builtins.property
    @jsii.member(jsii_name="apiDestination")
    def api_destination(self) -> _aws_cdk_aws_events_ceddda9d.ApiDestination:
        '''Destination pointing to a Jira instance where tickets are to be created.'''
        return typing.cast(_aws_cdk_aws_events_ceddda9d.ApiDestination, jsii.get(self, "apiDestination"))

    @builtins.property
    @jsii.member(jsii_name="connection")
    def connection(self) -> _aws_cdk_aws_events_ceddda9d.Connection:
        '''API connection providing details of how to communicate with the configured Jira instance.'''
        return typing.cast(_aws_cdk_aws_events_ceddda9d.Connection, jsii.get(self, "connection"))

    @builtins.property
    @jsii.member(jsii_name="credentials")
    def credentials(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The credentials to be used for connecting to Jira. The secret should be in JSON format and contain the key:.

        username: The name of the user issues should be created as.
        password: A password or API key for the user specified in ``username``.

        :group: Inputs
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "credentials"))

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine:
        '''The State Machine that handles creating a Jira ticket for a passed issue.

        Internally this state machine uses the AWS managed ``AWS-CreateJiraIssue``
        SSM Automation document.

        :group: Resources
        '''
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine, jsii.get(self, "handler"))

    @builtins.property
    @jsii.member(jsii_name="issueType")
    def issue_type(self) -> builtins.str:
        '''The default issue type that issues should be created as if no other type is specified by the event that triggered the issue creation.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "issueType"))

    @builtins.property
    @jsii.member(jsii_name="jiraUrl")
    def jira_url(self) -> builtins.str:
        '''The URL of the Jira instance where tickets should be created.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "jiraUrl"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The human friendly name that can be used to identify the plugin.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="priorityMap")
    def priority_map(self) -> "JiraTicketPriorityMap":
        '''A mapping of the standard severities supported by issue manager to priority levels supported by the destination Jira instance.

        :group: Inputs
        '''
        return typing.cast("JiraTicketPriorityMap", jsii.get(self, "priorityMap"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> builtins.str:
        '''The name of the default project to use for creating issues if no other project is specified by the event that triggered the issue creation.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="assignee")
    def assignee(self) -> typing.Optional[builtins.str]:
        '''The default assignee that issues should be created with if no other assignee is specified by the event that triggered the issue creation.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assignee"))

    @builtins.property
    @jsii.member(jsii_name="eventBus")
    def event_bus(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus]:
        '''The event bus to use to trigger writes to the Jira instance.

        This integration formats a Jira API response and then sends it to a Jira
        instance by means of an EventBridge Destination API and a specially
        crafted event pattern. This is the event bus where the rule to trigger the
        API will be added and the trigger event will be sent.
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus], jsii.get(self, "eventBus"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The length of time that the State Machine that handles creation of Jira tickets is allowed to run before timing out.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "timeout"))


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.JiraTicketOverrideOptions",
    jsii_struct_bases=[],
    name_mapping={
        "assignee": "assignee",
        "issue_priority": "issuePriority",
        "issue_type": "issueType",
        "project": "project",
    },
)
class JiraTicketOverrideOptions:
    def __init__(
        self,
        *,
        assignee: typing.Optional[builtins.str] = None,
        issue_priority: typing.Optional[builtins.str] = None,
        issue_type: typing.Optional[builtins.str] = None,
        project: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param assignee: 
        :param issue_priority: 
        :param issue_type: 
        :param project: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3597edffb011fcf9cb1f88b624d61e6a661249b81bae761d7607034e73a6b1c7)
            check_type(argname="argument assignee", value=assignee, expected_type=type_hints["assignee"])
            check_type(argname="argument issue_priority", value=issue_priority, expected_type=type_hints["issue_priority"])
            check_type(argname="argument issue_type", value=issue_type, expected_type=type_hints["issue_type"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assignee is not None:
            self._values["assignee"] = assignee
        if issue_priority is not None:
            self._values["issue_priority"] = issue_priority
        if issue_type is not None:
            self._values["issue_type"] = issue_type
        if project is not None:
            self._values["project"] = project

    @builtins.property
    def assignee(self) -> typing.Optional[builtins.str]:
        result = self._values.get("assignee")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issue_priority(self) -> typing.Optional[builtins.str]:
        result = self._values.get("issue_priority")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def issue_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("issue_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project(self) -> typing.Optional[builtins.str]:
        result = self._values.get("project")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JiraTicketOverrideOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.JiraTicketPriorityMap",
    jsii_struct_bases=[],
    name_mapping={
        "critical": "critical",
        "default": "default",
        "high": "high",
        "info": "info",
        "low": "low",
        "medium": "medium",
    },
)
class JiraTicketPriorityMap:
    def __init__(
        self,
        *,
        critical: typing.Optional[builtins.str] = None,
        default: typing.Optional[builtins.str] = None,
        high: typing.Optional[builtins.str] = None,
        info: typing.Optional[builtins.str] = None,
        low: typing.Optional[builtins.str] = None,
        medium: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param critical: 
        :param default: 
        :param high: 
        :param info: 
        :param low: 
        :param medium: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a08739fa088feae15f5aa82920113fc7790f876d4635fef42fe471aeffe31a4)
            check_type(argname="argument critical", value=critical, expected_type=type_hints["critical"])
            check_type(argname="argument default", value=default, expected_type=type_hints["default"])
            check_type(argname="argument high", value=high, expected_type=type_hints["high"])
            check_type(argname="argument info", value=info, expected_type=type_hints["info"])
            check_type(argname="argument low", value=low, expected_type=type_hints["low"])
            check_type(argname="argument medium", value=medium, expected_type=type_hints["medium"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if critical is not None:
            self._values["critical"] = critical
        if default is not None:
            self._values["default"] = default
        if high is not None:
            self._values["high"] = high
        if info is not None:
            self._values["info"] = info
        if low is not None:
            self._values["low"] = low
        if medium is not None:
            self._values["medium"] = medium

    @builtins.property
    def critical(self) -> typing.Optional[builtins.str]:
        result = self._values.get("critical")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def default(self) -> typing.Optional[builtins.str]:
        result = self._values.get("default")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def high(self) -> typing.Optional[builtins.str]:
        result = self._values.get("high")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def info(self) -> typing.Optional[builtins.str]:
        result = self._values.get("info")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def low(self) -> typing.Optional[builtins.str]:
        result = self._values.get("low")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def medium(self) -> typing.Optional[builtins.str]:
        result = self._values.get("medium")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JiraTicketPriorityMap(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.JiraTicketProps",
    jsii_struct_bases=[IssuePluginBaseProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "logging": "logging",
        "credentials": "credentials",
        "issue_type": "issueType",
        "jira_url": "jiraUrl",
        "priority_map": "priorityMap",
        "project": "project",
        "assignee": "assignee",
        "event_bus": "eventBus",
        "name": "name",
        "timeout": "timeout",
    },
)
class JiraTicketProps(IssuePluginBaseProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union["StateMachineLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        credentials: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        issue_type: builtins.str,
        jira_url: builtins.str,
        priority_map: typing.Union[JiraTicketPriorityMap, typing.Dict[builtins.str, typing.Any]],
        project: builtins.str,
        assignee: typing.Optional[builtins.str] = None,
        event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''Configuration controlling how Jira tickets should be created in response to events.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param logging: 
        :param credentials: 
        :param issue_type: 
        :param jira_url: 
        :param priority_map: 
        :param project: 
        :param assignee: 
        :param event_bus: 
        :param name: 
        :param timeout: 
        '''
        if isinstance(logging, dict):
            logging = StateMachineLogging(**logging)
        if isinstance(priority_map, dict):
            priority_map = JiraTicketPriorityMap(**priority_map)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed6d5eb60877b2a48722da609ac945a0a97beeb637b33690c8915560a61340f7)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument issue_type", value=issue_type, expected_type=type_hints["issue_type"])
            check_type(argname="argument jira_url", value=jira_url, expected_type=type_hints["jira_url"])
            check_type(argname="argument priority_map", value=priority_map, expected_type=type_hints["priority_map"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument assignee", value=assignee, expected_type=type_hints["assignee"])
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "credentials": credentials,
            "issue_type": issue_type,
            "jira_url": jira_url,
            "priority_map": priority_map,
            "project": project,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if logging is not None:
            self._values["logging"] = logging
        if assignee is not None:
            self._values["assignee"] = assignee
        if event_bus is not None:
            self._values["event_bus"] = event_bus
        if name is not None:
            self._values["name"] = name
        if timeout is not None:
            self._values["timeout"] = timeout

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
    def logging(self) -> typing.Optional["StateMachineLogging"]:
        result = self._values.get("logging")
        return typing.cast(typing.Optional["StateMachineLogging"], result)

    @builtins.property
    def credentials(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        result = self._values.get("credentials")
        assert result is not None, "Required property 'credentials' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def issue_type(self) -> builtins.str:
        result = self._values.get("issue_type")
        assert result is not None, "Required property 'issue_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def jira_url(self) -> builtins.str:
        result = self._values.get("jira_url")
        assert result is not None, "Required property 'jira_url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority_map(self) -> JiraTicketPriorityMap:
        result = self._values.get("priority_map")
        assert result is not None, "Required property 'priority_map' is missing"
        return typing.cast(JiraTicketPriorityMap, result)

    @builtins.property
    def project(self) -> builtins.str:
        result = self._values.get("project")
        assert result is not None, "Required property 'project' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assignee(self) -> typing.Optional[builtins.str]:
        result = self._values.get("assignee")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def event_bus(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus]:
        result = self._values.get("event_bus")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JiraTicketProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.OpenSearchEventRuleOptions",
    jsii_struct_bases=[],
    name_mapping={"overrides": "overrides", "severity": "severity", "types": "types"},
)
class OpenSearchEventRuleOptions:
    def __init__(
        self,
        *,
        overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
        severity: typing.Optional[typing.Sequence["OpenSearchEventSeverity"]] = None,
        types: typing.Optional[typing.Sequence["OpenSearchEventType"]] = None,
    ) -> None:
        '''
        :param overrides: 
        :param severity: 
        :param types: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__699d7a494eacfff85e5fb493304a3e6b77d53d626719ea9797143d77c98839e1)
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if overrides is not None:
            self._values["overrides"] = overrides
        if severity is not None:
            self._values["severity"] = severity
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def overrides(self) -> typing.Optional[typing.List[IssueHandlerOverride]]:
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.List[IssueHandlerOverride]], result)

    @builtins.property
    def severity(self) -> typing.Optional[typing.List["OpenSearchEventSeverity"]]:
        result = self._values.get("severity")
        return typing.cast(typing.Optional[typing.List["OpenSearchEventSeverity"]], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List["OpenSearchEventType"]]:
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List["OpenSearchEventType"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpenSearchEventRuleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OpenSearchEventSeverity(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.OpenSearchEventSeverity",
):
    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls) -> typing.List["OpenSearchEventSeverity"]:
        return typing.cast(typing.List["OpenSearchEventSeverity"], jsii.sinvoke(cls, "all", []))

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(
        cls,
        *levels: "OpenSearchEventSeverity",
    ) -> typing.List["OpenSearchEventSeverity"]:
        '''
        :param levels: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd6f8670ec2ad255eb3e1c1257163903e257229f51b40f226df3de18a7e9a374)
            check_type(argname="argument levels", value=levels, expected_type=typing.Tuple[type_hints["levels"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(typing.List["OpenSearchEventSeverity"], jsii.sinvoke(cls, "custom", [*levels]))

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        standardized: builtins.str,
        original: builtins.str,
        priority: jsii.Number,
    ) -> "OpenSearchEventSeverity":
        '''
        :param standardized: -
        :param original: -
        :param priority: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a107e60c49274129b060940d98a8008d6c5b027cf04f49b95c93be6931f88530)
            check_type(argname="argument standardized", value=standardized, expected_type=type_hints["standardized"])
            check_type(argname="argument original", value=original, expected_type=type_hints["original"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        return typing.cast("OpenSearchEventSeverity", jsii.sinvoke(cls, "of", [standardized, original, priority]))

    @jsii.member(jsii_name="threshold")
    @builtins.classmethod
    def threshold(
        cls,
        level: "OpenSearchEventSeverity",
    ) -> typing.List["OpenSearchEventSeverity"]:
        '''
        :param level: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54431185d7d2de065a2df9a2bba74641b715d32f1f97db3ee231d4f52a4f998c)
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
        return typing.cast(typing.List["OpenSearchEventSeverity"], jsii.sinvoke(cls, "threshold", [level]))

    @jsii.member(jsii_name="buildCondition")
    def build_condition(
        self,
        path: builtins.str,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.Condition:
        '''
        :param path: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113310a0c5e7559602f64863de5e62d33a52838536af822bf129089260b1c769)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Condition, jsii.invoke(self, "buildCondition", [path]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIGH")
    def HIGH(cls) -> "OpenSearchEventSeverity":
        return typing.cast("OpenSearchEventSeverity", jsii.sget(cls, "HIGH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INFORMATIONAL")
    def INFORMATIONAL(cls) -> "OpenSearchEventSeverity":
        return typing.cast("OpenSearchEventSeverity", jsii.sget(cls, "INFORMATIONAL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LOW")
    def LOW(cls) -> "OpenSearchEventSeverity":
        return typing.cast("OpenSearchEventSeverity", jsii.sget(cls, "LOW"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MEDIUM")
    def MEDIUM(cls) -> "OpenSearchEventSeverity":
        return typing.cast("OpenSearchEventSeverity", jsii.sget(cls, "MEDIUM"))

    @builtins.property
    @jsii.member(jsii_name="original")
    def original(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "original"))

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @builtins.property
    @jsii.member(jsii_name="standardized")
    def standardized(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "standardized"))


class OpenSearchEventType(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.OpenSearchEventType",
):
    '''Represents a type of event that can be generated in response to circumstances happening on an AWS OpenSearch service cluster.

    :see: `Monitoring OpenSearch Service events with Amazon EventBridge <https://docs.aws.amazon.com/opensearch-service/latest/developerguide/monitoring-events.html>`_
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        *,
        detail_type: builtins.str,
        event_name: builtins.str,
    ) -> "OpenSearchEventType":
        '''
        :param detail_type: 
        :param event_name: 
        '''
        props = OpenSearchEventTypeProps(
            detail_type=detail_type, event_name=event_name
        )

        return typing.cast("OpenSearchEventType", jsii.sinvoke(cls, "of", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="all")
    def all(cls) -> typing.List["OpenSearchEventType"]:
        return typing.cast(typing.List["OpenSearchEventType"], jsii.sget(cls, "all"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="AUTO_TUNE")
    def AUTO_TUNE(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "AUTO_TUNE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CLUSTER_RECOVERY")
    def CLUSTER_RECOVERY(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "CLUSTER_RECOVERY"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CUSTOM_INDEX_ROUTING")
    def CUSTOM_INDEX_ROUTING(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "CUSTOM_INDEX_ROUTING"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DISK_THROUGHPUT_THROTTLE")
    def DISK_THROUGHPUT_THROTTLE(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "DISK_THROUGHPUT_THROTTLE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DOMAIN_UPDATE")
    def DOMAIN_UPDATE(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "DOMAIN_UPDATE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="EBS_BURST_BALANCE")
    def EBS_BURST_BALANCE(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "EBS_BURST_BALANCE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="FAILED_SHARD_LOCK")
    def FAILED_SHARD_LOCK(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "FAILED_SHARD_LOCK"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIGH_JVM_USAGE")
    def HIGH_JVM_USAGE(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "HIGH_JVM_USAGE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIGH_SHARED_COUNT")
    def HIGH_SHARED_COUNT(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "HIGH_SHARED_COUNT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INSUFFICIENT_GARBAGE_COLLECTION")
    def INSUFFICIENT_GARBAGE_COLLECTION(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "INSUFFICIENT_GARBAGE_COLLECTION"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="KMS_KEY_INACCESSIBLE")
    def KMS_KEY_INACCESSIBLE(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "KMS_KEY_INACCESSIBLE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LARGE_SHARD_SIZE")
    def LARGE_SHARD_SIZE(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "LARGE_SHARD_SIZE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LOW_DISK_SPACE")
    def LOW_DISK_SPACE(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "LOW_DISK_SPACE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LOW_DISK_WATERMARK_BREACH")
    def LOW_DISK_WATERMARK_BREACH(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "LOW_DISK_WATERMARK_BREACH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="NODE_RETIREMENT")
    def NODE_RETIREMENT(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "NODE_RETIREMENT"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SERVICE_SOFTWARE_UPDATE")
    def SERVICE_SOFTWARE_UPDATE(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "SERVICE_SOFTWARE_UPDATE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VPC_ENDPOINT_CREATE")
    def VPC_ENDPOINT_CREATE(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "VPC_ENDPOINT_CREATE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VPC_ENDPOINT_DELETE")
    def VPC_ENDPOINT_DELETE(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "VPC_ENDPOINT_DELETE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="VPC_ENDPOINT_UPDATE")
    def VPC_ENDPOINT_UPDATE(cls) -> "OpenSearchEventType":
        return typing.cast("OpenSearchEventType", jsii.sget(cls, "VPC_ENDPOINT_UPDATE"))

    @builtins.property
    @jsii.member(jsii_name="detailType")
    def detail_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "detailType"))

    @builtins.property
    @jsii.member(jsii_name="eventName")
    def event_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventName"))


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.OpenSearchEventTypeProps",
    jsii_struct_bases=[],
    name_mapping={"detail_type": "detailType", "event_name": "eventName"},
)
class OpenSearchEventTypeProps:
    def __init__(self, *, detail_type: builtins.str, event_name: builtins.str) -> None:
        '''
        :param detail_type: 
        :param event_name: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__297acd47d2c33794c0ea7437ed6bd3b867ad3c2219f60ec2cde0e221d39f5d2e)
            check_type(argname="argument detail_type", value=detail_type, expected_type=type_hints["detail_type"])
            check_type(argname="argument event_name", value=event_name, expected_type=type_hints["event_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "detail_type": detail_type,
            "event_name": event_name,
        }

    @builtins.property
    def detail_type(self) -> builtins.str:
        result = self._values.get("detail_type")
        assert result is not None, "Required property 'detail_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_name(self) -> builtins.str:
        result = self._values.get("event_name")
        assert result is not None, "Required property 'event_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpenSearchEventTypeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IIssueParser)
class SecurityHubFinding(
    IssuePluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.SecurityHubFinding",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union["StateMachineLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param match_type: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__380b1636b1f967bc917f9f72a3debc0caf5126cc6e8e510d4066b83f85eaaa1e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SecurityHubFindingProps(
            match_type=match_type,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.IConstruct,
    ) -> typing.List[IssueTrigger]:
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__258010b44491929bcf69c6f3260753afbe509aca50a192e5bf7c93a6f3c77843)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(typing.List[IssueTrigger], jsii.invoke(self, "bind", [_scope]))

    @jsii.member(jsii_name="buildDescription")
    def _build_description(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.Chain:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Chain, jsii.invoke(self, "buildDescription", []))

    @jsii.member(jsii_name="buildRemediation")
    def _build_remediation(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.Chain:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Chain, jsii.invoke(self, "buildRemediation", []))

    @jsii.member(jsii_name="buildResources")
    def _build_resources(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.Chain:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Chain, jsii.invoke(self, "buildResources", []))

    @jsii.member(jsii_name="buildSeverityMap")
    def _build_severity_map(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.Chain:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Chain, jsii.invoke(self, "buildSeverityMap", []))

    @jsii.member(jsii_name="buildUrl")
    def _build_url(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.Chain:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Chain, jsii.invoke(self, "buildUrl", []))

    @jsii.member(jsii_name="registerIssueTrigger")
    def register_issue_trigger(
        self,
        id: builtins.str,
        *,
        overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
        severity: typing.Optional[ISecurityHubSeverityConfiguration] = None,
    ) -> IssueTrigger:
        '''
        :param id: -
        :param overrides: 
        :param severity: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21fd3ae4500b241033b6cef515920861faab44979faf975e1d542b4f8316e3bc)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = SecurityHubFindingEventOptions(
            overrides=overrides, severity=severity
        )

        return typing.cast(IssueTrigger, jsii.invoke(self, "registerIssueTrigger", [id, options]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MATCH_TYPE")
    def MATCH_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "MATCH_TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SEVERITIES")
    def SEVERITIES(cls) -> typing.List["SecurityHubSeverity"]:
        return typing.cast(typing.List["SecurityHubSeverity"], jsii.sget(cls, "SEVERITIES"))

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine, jsii.get(self, "handler"))

    @builtins.property
    @jsii.member(jsii_name="matchType")
    def match_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchType"))

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> typing.List[IssueTrigger]:
        return typing.cast(typing.List[IssueTrigger], jsii.get(self, "triggers"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "timeout"))


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.SecurityHubFindingEventOptions",
    jsii_struct_bases=[],
    name_mapping={"overrides": "overrides", "severity": "severity"},
)
class SecurityHubFindingEventOptions:
    def __init__(
        self,
        *,
        overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
        severity: typing.Optional[ISecurityHubSeverityConfiguration] = None,
    ) -> None:
        '''
        :param overrides: 
        :param severity: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8655a09b8f54d0a3b830e464a308025fe70e639a13291f48bff63e0b6bd5901f)
            check_type(argname="argument overrides", value=overrides, expected_type=type_hints["overrides"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if overrides is not None:
            self._values["overrides"] = overrides
        if severity is not None:
            self._values["severity"] = severity

    @builtins.property
    def overrides(self) -> typing.Optional[typing.List[IssueHandlerOverride]]:
        result = self._values.get("overrides")
        return typing.cast(typing.Optional[typing.List[IssueHandlerOverride]], result)

    @builtins.property
    def severity(self) -> typing.Optional[ISecurityHubSeverityConfiguration]:
        result = self._values.get("severity")
        return typing.cast(typing.Optional[ISecurityHubSeverityConfiguration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityHubFindingEventOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.SecurityHubFindingProps",
    jsii_struct_bases=[IssuePluginBaseProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "logging": "logging",
        "match_type": "matchType",
        "name": "name",
        "timeout": "timeout",
    },
)
class SecurityHubFindingProps(IssuePluginBaseProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union["StateMachineLogging", typing.Dict[builtins.str, typing.Any]]] = None,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param logging: 
        :param match_type: 
        :param name: 
        :param timeout: 
        '''
        if isinstance(logging, dict):
            logging = StateMachineLogging(**logging)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca783ee46a82565d9b2cd4907f5ad9c03223b85389f280a5b41cc4f4a2190277)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument match_type", value=match_type, expected_type=type_hints["match_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if logging is not None:
            self._values["logging"] = logging
        if match_type is not None:
            self._values["match_type"] = match_type
        if name is not None:
            self._values["name"] = name
        if timeout is not None:
            self._values["timeout"] = timeout

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
    def logging(self) -> typing.Optional["StateMachineLogging"]:
        result = self._values.get("logging")
        return typing.cast(typing.Optional["StateMachineLogging"], result)

    @builtins.property
    def match_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("match_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityHubFindingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SecurityHubSeverity(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.SecurityHubSeverity",
):
    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(
        cls,
        name: builtins.str,
        lower_bound: jsii.Number,
        upper_bound: jsii.Number,
        standardized: builtins.str,
    ) -> "SecurityHubSeverity":
        '''
        :param name: -
        :param lower_bound: -
        :param upper_bound: -
        :param standardized: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__880d3c74d98dfff1d219a68a56d35589351dbd43f2a35cc9a8b1856266ad301d)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument lower_bound", value=lower_bound, expected_type=type_hints["lower_bound"])
            check_type(argname="argument upper_bound", value=upper_bound, expected_type=type_hints["upper_bound"])
            check_type(argname="argument standardized", value=standardized, expected_type=type_hints["standardized"])
        return typing.cast("SecurityHubSeverity", jsii.sinvoke(cls, "of", [name, lower_bound, upper_bound, standardized]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CRITICAL")
    def CRITICAL(cls) -> "SecurityHubSeverity":
        return typing.cast("SecurityHubSeverity", jsii.sget(cls, "CRITICAL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="HIGH")
    def HIGH(cls) -> "SecurityHubSeverity":
        return typing.cast("SecurityHubSeverity", jsii.sget(cls, "HIGH"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="INFORMATIONAL")
    def INFORMATIONAL(cls) -> "SecurityHubSeverity":
        return typing.cast("SecurityHubSeverity", jsii.sget(cls, "INFORMATIONAL"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="LOW")
    def LOW(cls) -> "SecurityHubSeverity":
        return typing.cast("SecurityHubSeverity", jsii.sget(cls, "LOW"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MEDIUM")
    def MEDIUM(cls) -> "SecurityHubSeverity":
        return typing.cast("SecurityHubSeverity", jsii.sget(cls, "MEDIUM"))

    @builtins.property
    @jsii.member(jsii_name="lowerBound")
    def lower_bound(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "lowerBound"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="standardized")
    def standardized(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "standardized"))

    @builtins.property
    @jsii.member(jsii_name="upperBound")
    def upper_bound(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "upperBound"))


class SecurityHubSeverityConfiguration(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.SecurityHubSeverityConfiguration",
):
    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="all")
    @builtins.classmethod
    def all(cls) -> ISecurityHubSeverityConfiguration:
        return typing.cast(ISecurityHubSeverityConfiguration, jsii.sinvoke(cls, "all", []))

    @jsii.member(jsii_name="custom")
    @builtins.classmethod
    def custom(cls, *levels: SecurityHubSeverity) -> ISecurityHubSeverityConfiguration:
        '''
        :param levels: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28583288e953240e63f8bdb060d4261683c5e292e21929f74b5ef677cbb834c6)
            check_type(argname="argument levels", value=levels, expected_type=typing.Tuple[type_hints["levels"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(ISecurityHubSeverityConfiguration, jsii.sinvoke(cls, "custom", [*levels]))

    @jsii.member(jsii_name="threshold")
    @builtins.classmethod
    def threshold(cls, level: SecurityHubSeverity) -> ISecurityHubSeverityConfiguration:
        '''
        :param level: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__863f802289de2b198caedda8eb31a9bef07b59b1ef6be2257b5bff4414b73401)
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
        return typing.cast(ISecurityHubSeverityConfiguration, jsii.sinvoke(cls, "threshold", [level]))


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.SetDelimiterProps",
    jsii_struct_bases=[],
    name_mapping={"delimiter": "delimiter"},
)
class SetDelimiterProps:
    def __init__(self, *, delimiter: AppendDelimiter) -> None:
        '''
        :param delimiter: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d52efedb526beaf6890c8ab6bdf08af1d2c01494c0fbad4d2238af151424af2)
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "delimiter": delimiter,
        }

    @builtins.property
    def delimiter(self) -> AppendDelimiter:
        result = self._values.get("delimiter")
        assert result is not None, "Required property 'delimiter' is missing"
        return typing.cast(AppendDelimiter, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SetDelimiterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.StateMachineLogging",
    jsii_struct_bases=[],
    name_mapping={
        "destination": "destination",
        "enabled": "enabled",
        "include_execution_data": "includeExecutionData",
        "level": "level",
    },
)
class StateMachineLogging:
    def __init__(
        self,
        *,
        destination: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
        enabled: typing.Optional[builtins.bool] = None,
        include_execution_data: typing.Optional[builtins.bool] = None,
        level: typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.LogLevel] = None,
    ) -> None:
        '''
        :param destination: 
        :param enabled: 
        :param include_execution_data: 
        :param level: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fbb086a355e5841e0230f4aa4854b365e4400b834a6df4d009a7884a526168f)
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument include_execution_data", value=include_execution_data, expected_type=type_hints["include_execution_data"])
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination is not None:
            self._values["destination"] = destination
        if enabled is not None:
            self._values["enabled"] = enabled
        if include_execution_data is not None:
            self._values["include_execution_data"] = include_execution_data
        if level is not None:
            self._values["level"] = level

    @builtins.property
    def destination(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup]:
        result = self._values.get("destination")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def include_execution_data(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("include_execution_data")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def level(self) -> typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.LogLevel]:
        result = self._values.get("level")
        return typing.cast(typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.LogLevel], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StateMachineLogging(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.WriteProps",
    jsii_struct_bases=[],
    name_mapping={
        "value": "value",
        "default_delimiter": "defaultDelimiter",
        "delimiter": "delimiter",
        "prefix": "prefix",
        "required": "required",
        "suffix": "suffix",
    },
)
class WriteProps:
    def __init__(
        self,
        *,
        value: builtins.str,
        default_delimiter: typing.Optional[AppendDelimiter] = None,
        delimiter: typing.Optional[AppendDelimiter] = None,
        prefix: typing.Optional[builtins.str] = None,
        required: typing.Optional[builtins.bool] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param value: 
        :param default_delimiter: 
        :param delimiter: 
        :param prefix: 
        :param required: 
        :param suffix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce897381a7a6ad487b1bbbd631e32ac3942ca9709805ecf1caf3c11704b87231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            check_type(argname="argument default_delimiter", value=default_delimiter, expected_type=type_hints["default_delimiter"])
            check_type(argname="argument delimiter", value=delimiter, expected_type=type_hints["delimiter"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument required", value=required, expected_type=type_hints["required"])
            check_type(argname="argument suffix", value=suffix, expected_type=type_hints["suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "value": value,
        }
        if default_delimiter is not None:
            self._values["default_delimiter"] = default_delimiter
        if delimiter is not None:
            self._values["delimiter"] = delimiter
        if prefix is not None:
            self._values["prefix"] = prefix
        if required is not None:
            self._values["required"] = required
        if suffix is not None:
            self._values["suffix"] = suffix

    @builtins.property
    def value(self) -> builtins.str:
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_delimiter(self) -> typing.Optional[AppendDelimiter]:
        result = self._values.get("default_delimiter")
        return typing.cast(typing.Optional[AppendDelimiter], result)

    @builtins.property
    def delimiter(self) -> typing.Optional[AppendDelimiter]:
        result = self._values.get("delimiter")
        return typing.cast(typing.Optional[AppendDelimiter], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def required(self) -> typing.Optional[builtins.bool]:
        result = self._values.get("required")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def suffix(self) -> typing.Optional[builtins.str]:
        result = self._values.get("suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WriteProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IDescriptionBuilderComponent, IDelayedChainable)
class DescriptionBuilder(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.DescriptionBuilder",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        *,
        initial_description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param initial_description: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76ae5316c6c731592af25328b99f469342a02f8b2b96f2f6056575e7cca257b4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        props = DescriptionBuilderProps(initial_description=initial_description)

        jsii.create(self.__class__, self, [scope, props])

    @jsii.member(jsii_name="addIterator")
    def add_iterator(
        self,
        id: builtins.str,
        *,
        array_ref: builtins.str,
        result_path: builtins.str,
        field_delimiter: typing.Optional[AppendDelimiter] = None,
        record_delimiter: typing.Optional[AppendDelimiter] = None,
        section_delimiter: typing.Optional[AppendDelimiter] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> "DescriptionBuilderIterator":
        '''
        :param id: -
        :param array_ref: 
        :param result_path: 
        :param field_delimiter: 
        :param record_delimiter: 
        :param section_delimiter: 
        :param title: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac15be8a7b4087186efaff33859d15adc2c5950f524034601e8e0841597e540b)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DescriptionBuilderIteratorProps(
            array_ref=array_ref,
            result_path=result_path,
            field_delimiter=field_delimiter,
            record_delimiter=record_delimiter,
            section_delimiter=section_delimiter,
            title=title,
        )

        return typing.cast("DescriptionBuilderIterator", jsii.invoke(self, "addIterator", [id, props]))

    @jsii.member(jsii_name="addReference")
    def add_reference(
        self,
        id: builtins.str,
        *,
        value: builtins.str,
        delimiter: typing.Optional[AppendDelimiter] = None,
        label: typing.Optional[builtins.str] = None,
        required: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param value: 
        :param delimiter: 
        :param label: 
        :param required: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96dbc2c00e9108a2a7d85034168a4bb6f29d993ac63d7041b7996da10d2b8006)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AddReferenceProps(
            value=value, delimiter=delimiter, label=label, required=required
        )

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "addReference", [id, props]))

    @jsii.member(jsii_name="addSection")
    def add_section(
        self,
        id: builtins.str,
        *,
        title: builtins.str,
        reference_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> "DescriptionBuilderSection":
        '''
        :param id: -
        :param title: 
        :param reference_checks: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a474a63d42135823453c5f22f0283f6b31e3ea7f4def19dea97a75d71e5a1f0f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DescriptionBuilderSectionProps(
            title=title, reference_checks=reference_checks
        )

        return typing.cast("DescriptionBuilderSection", jsii.invoke(self, "addSection", [id, props]))

    @jsii.member(jsii_name="buildId")
    def _build_id(
        self,
        prefix: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''
        :param prefix: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e0b6eb6e81a5e45f8253f9c0933a8a6ee17eb67f446a9ccb39aaca710dade7f)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(builtins.str, jsii.invoke(self, "buildId", [prefix, id]))

    @jsii.member(jsii_name="initialize")
    def _initialize(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "initialize", []))

    @jsii.member(jsii_name="registerBuilder")
    def _register_builder(
        self,
        builder: IDescriptionBuilderComponent,
    ) -> IDescriptionBuilderComponent:
        '''
        :param builder: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad3b238746c06b75e41661d9ff9d65526821be37672ae9d67bb5f391b46efd55)
            check_type(argname="argument builder", value=builder, expected_type=type_hints["builder"])
        return typing.cast(IDescriptionBuilderComponent, jsii.invoke(self, "registerBuilder", [builder]))

    @jsii.member(jsii_name="registerChainable")
    def _register_chainable(
        self,
        chainable: _aws_cdk_aws_stepfunctions_ceddda9d.IChainable,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param chainable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39effaee482adb498d97c478f42007a087994ee3deef74af511c9075cba6e3a2)
            check_type(argname="argument chainable", value=chainable, expected_type=type_hints["chainable"])
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "registerChainable", [chainable]))

    @jsii.member(jsii_name="render")
    def render(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "render", []))

    @jsii.member(jsii_name="setDelimiter")
    def set_delimiter(
        self,
        id: builtins.str,
        *,
        delimiter: AppendDelimiter,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param delimiter: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16c79b956a8c1987e777f724971101bae6be1ead3ccc2958bd5b927096079e9d)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SetDelimiterProps(delimiter=delimiter)

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "setDelimiter", [id, props]))

    @jsii.member(jsii_name="write")
    def write(
        self,
        id: builtins.str,
        *,
        value: builtins.str,
        default_delimiter: typing.Optional[AppendDelimiter] = None,
        delimiter: typing.Optional[AppendDelimiter] = None,
        prefix: typing.Optional[builtins.str] = None,
        required: typing.Optional[builtins.bool] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param value: 
        :param default_delimiter: 
        :param delimiter: 
        :param prefix: 
        :param required: 
        :param suffix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__059282f45164bce07a6b303d31c55c48873e9f90df2695104f68eacbb46fe688)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WriteProps(
            value=value,
            default_delimiter=default_delimiter,
            delimiter=delimiter,
            prefix=prefix,
            required=required,
            suffix=suffix,
        )

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "write", [id, props]))

    @builtins.property
    @jsii.member(jsii_name="classifier")
    def classifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "classifier"))

    @builtins.property
    @jsii.member(jsii_name="initialDescription")
    def initial_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "initialDescription"))

    @builtins.property
    @jsii.member(jsii_name="initializeNode")
    def initialize_node(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.get(self, "initializeNode"))


@jsii.implements(IDescriptionBuilderComponent, IDelayedChainable)
class DescriptionBuilderIterator(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.DescriptionBuilderIterator",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        array_ref: builtins.str,
        result_path: builtins.str,
        field_delimiter: typing.Optional[AppendDelimiter] = None,
        record_delimiter: typing.Optional[AppendDelimiter] = None,
        section_delimiter: typing.Optional[AppendDelimiter] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param array_ref: 
        :param result_path: 
        :param field_delimiter: 
        :param record_delimiter: 
        :param section_delimiter: 
        :param title: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcfd81f6847b2855e5867b4b0669d62b9afef539fb734f8c70567c3a4e13868e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DescriptionBuilderIteratorProps(
            array_ref=array_ref,
            result_path=result_path,
            field_delimiter=field_delimiter,
            record_delimiter=record_delimiter,
            section_delimiter=section_delimiter,
            title=title,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addIterator")
    def add_iterator(
        self,
        id: builtins.str,
        *,
        array_ref: builtins.str,
        result_path: builtins.str,
        field_delimiter: typing.Optional[AppendDelimiter] = None,
        record_delimiter: typing.Optional[AppendDelimiter] = None,
        section_delimiter: typing.Optional[AppendDelimiter] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> "DescriptionBuilderIterator":
        '''
        :param id: -
        :param array_ref: 
        :param result_path: 
        :param field_delimiter: 
        :param record_delimiter: 
        :param section_delimiter: 
        :param title: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__462d03a128fd156179f1090938db59ffea06783917bf5d57dce17ae2d2d1e8ef)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DescriptionBuilderIteratorProps(
            array_ref=array_ref,
            result_path=result_path,
            field_delimiter=field_delimiter,
            record_delimiter=record_delimiter,
            section_delimiter=section_delimiter,
            title=title,
        )

        return typing.cast("DescriptionBuilderIterator", jsii.invoke(self, "addIterator", [id, props]))

    @jsii.member(jsii_name="addReference")
    def add_reference(
        self,
        id: builtins.str,
        *,
        value: builtins.str,
        delimiter: typing.Optional[AppendDelimiter] = None,
        label: typing.Optional[builtins.str] = None,
        required: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param value: 
        :param delimiter: 
        :param label: 
        :param required: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d35545a175b2e2cbbe3b5bb9e6f4e6ebfc39fb8650579529524d6745b86769d)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AddReferenceProps(
            value=value, delimiter=delimiter, label=label, required=required
        )

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "addReference", [id, props]))

    @jsii.member(jsii_name="buildId")
    def _build_id(
        self,
        prefix: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''
        :param prefix: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e5c13c7e5ceea2af4cf13dd7371fe24516d78f84853f831b739ddd7a809de5e)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(builtins.str, jsii.invoke(self, "buildId", [prefix, id]))

    @jsii.member(jsii_name="registerBuilder")
    def _register_builder(
        self,
        builder: IDescriptionBuilderComponent,
    ) -> IDescriptionBuilderComponent:
        '''
        :param builder: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6081e98e12fadf65028d6623ba15661a7ff62cc47f4f0ed12189f0deb0174030)
            check_type(argname="argument builder", value=builder, expected_type=type_hints["builder"])
        return typing.cast(IDescriptionBuilderComponent, jsii.invoke(self, "registerBuilder", [builder]))

    @jsii.member(jsii_name="registerChainable")
    def _register_chainable(
        self,
        chainable: _aws_cdk_aws_stepfunctions_ceddda9d.IChainable,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param chainable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b28b734bb363d31e78f0073c5827b7971ac74566393ad096fd55ca8c90f6f915)
            check_type(argname="argument chainable", value=chainable, expected_type=type_hints["chainable"])
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "registerChainable", [chainable]))

    @jsii.member(jsii_name="render")
    def render(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "render", []))

    @jsii.member(jsii_name="setDelimiter")
    def set_delimiter(
        self,
        id: builtins.str,
        *,
        delimiter: AppendDelimiter,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param delimiter: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff99364db406f0dd2ebf79d6226811c7c7abc87dee88aa122e988ae002f16930)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SetDelimiterProps(delimiter=delimiter)

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "setDelimiter", [id, props]))

    @jsii.member(jsii_name="write")
    def write(
        self,
        id: builtins.str,
        *,
        value: builtins.str,
        default_delimiter: typing.Optional[AppendDelimiter] = None,
        delimiter: typing.Optional[AppendDelimiter] = None,
        prefix: typing.Optional[builtins.str] = None,
        required: typing.Optional[builtins.bool] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param value: 
        :param default_delimiter: 
        :param delimiter: 
        :param prefix: 
        :param required: 
        :param suffix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e9211877b3b1f3cea27e971c80b93245acf989efd6df4ced306f426a73c9343)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WriteProps(
            value=value,
            default_delimiter=default_delimiter,
            delimiter=delimiter,
            prefix=prefix,
            required=required,
            suffix=suffix,
        )

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "write", [id, props]))

    @builtins.property
    @jsii.member(jsii_name="arrayRef")
    def array_ref(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arrayRef"))

    @builtins.property
    @jsii.member(jsii_name="classifier")
    def classifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "classifier"))

    @builtins.property
    @jsii.member(jsii_name="fieldDelimiter")
    def field_delimiter(self) -> AppendDelimiter:
        return typing.cast(AppendDelimiter, jsii.get(self, "fieldDelimiter"))

    @builtins.property
    @jsii.member(jsii_name="recordDelimiter")
    def record_delimiter(self) -> AppendDelimiter:
        return typing.cast(AppendDelimiter, jsii.get(self, "recordDelimiter"))

    @builtins.property
    @jsii.member(jsii_name="resultPath")
    def result_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resultPath"))

    @builtins.property
    @jsii.member(jsii_name="sectionDelimiter")
    def section_delimiter(self) -> AppendDelimiter:
        return typing.cast(AppendDelimiter, jsii.get(self, "sectionDelimiter"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "title"))


@jsii.implements(IDescriptionBuilderComponent, IDelayedChainable)
class DescriptionBuilderSection(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.DescriptionBuilderSection",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        title: builtins.str,
        reference_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param title: 
        :param reference_checks: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87ca90a46892ec0e335ac0242b06d52781533b02652dd31251b67c510bb4bdc3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DescriptionBuilderSectionProps(
            title=title, reference_checks=reference_checks
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addIterator")
    def add_iterator(
        self,
        id: builtins.str,
        *,
        array_ref: builtins.str,
        result_path: builtins.str,
        field_delimiter: typing.Optional[AppendDelimiter] = None,
        record_delimiter: typing.Optional[AppendDelimiter] = None,
        section_delimiter: typing.Optional[AppendDelimiter] = None,
        title: typing.Optional[builtins.str] = None,
    ) -> DescriptionBuilderIterator:
        '''
        :param id: -
        :param array_ref: 
        :param result_path: 
        :param field_delimiter: 
        :param record_delimiter: 
        :param section_delimiter: 
        :param title: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dff71b352d679fe0ac944cde79f865ab23cbcd664c124d055bd22b5fe542875)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DescriptionBuilderIteratorProps(
            array_ref=array_ref,
            result_path=result_path,
            field_delimiter=field_delimiter,
            record_delimiter=record_delimiter,
            section_delimiter=section_delimiter,
            title=title,
        )

        return typing.cast(DescriptionBuilderIterator, jsii.invoke(self, "addIterator", [id, props]))

    @jsii.member(jsii_name="addReference")
    def add_reference(
        self,
        id: builtins.str,
        *,
        value: builtins.str,
        delimiter: typing.Optional[AppendDelimiter] = None,
        label: typing.Optional[builtins.str] = None,
        required: typing.Optional[builtins.bool] = None,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param value: 
        :param delimiter: 
        :param label: 
        :param required: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a5ee28fcd7d15d7059ea9114158d9c5943430b79ea2c7e2223cc4dcf2380bb)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AddReferenceProps(
            value=value, delimiter=delimiter, label=label, required=required
        )

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "addReference", [id, props]))

    @jsii.member(jsii_name="addReferenceCheck")
    def add_reference_check(self, ref: builtins.str) -> None:
        '''
        :param ref: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16f28a78161f21f99820434b97d98105c60109dd5a7c6db86dd89f683d9fdb35)
            check_type(argname="argument ref", value=ref, expected_type=type_hints["ref"])
        return typing.cast(None, jsii.invoke(self, "addReferenceCheck", [ref]))

    @jsii.member(jsii_name="buildId")
    def _build_id(
        self,
        prefix: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> builtins.str:
        '''
        :param prefix: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00d70736c81dd0c1242aa8e8d04845df7d4c12252dbdd364c7b68b0150c5314a)
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(builtins.str, jsii.invoke(self, "buildId", [prefix, id]))

    @jsii.member(jsii_name="registerBuilder")
    def _register_builder(
        self,
        builder: IDescriptionBuilderComponent,
    ) -> IDescriptionBuilderComponent:
        '''
        :param builder: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86cdb432065e5e722bf28646340f08e7804f7b4b66ff3da7f75b23079e80c89f)
            check_type(argname="argument builder", value=builder, expected_type=type_hints["builder"])
        return typing.cast(IDescriptionBuilderComponent, jsii.invoke(self, "registerBuilder", [builder]))

    @jsii.member(jsii_name="registerChainable")
    def _register_chainable(
        self,
        chainable: _aws_cdk_aws_stepfunctions_ceddda9d.IChainable,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param chainable: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22f61284bc611f89bf448a53dc8c1d8acce3782300a7c9f634106042c531be9b)
            check_type(argname="argument chainable", value=chainable, expected_type=type_hints["chainable"])
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "registerChainable", [chainable]))

    @jsii.member(jsii_name="render")
    def render(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "render", []))

    @jsii.member(jsii_name="setDelimiter")
    def set_delimiter(
        self,
        id: builtins.str,
        *,
        delimiter: AppendDelimiter,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param delimiter: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__baacaecef78bbec42c4f14777fdbc34e5475b3119c475238f8df79a42bb03b2c)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SetDelimiterProps(delimiter=delimiter)

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "setDelimiter", [id, props]))

    @jsii.member(jsii_name="write")
    def write(
        self,
        id: builtins.str,
        *,
        value: builtins.str,
        default_delimiter: typing.Optional[AppendDelimiter] = None,
        delimiter: typing.Optional[AppendDelimiter] = None,
        prefix: typing.Optional[builtins.str] = None,
        required: typing.Optional[builtins.bool] = None,
        suffix: typing.Optional[builtins.str] = None,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.IChainable:
        '''
        :param id: -
        :param value: 
        :param default_delimiter: 
        :param delimiter: 
        :param prefix: 
        :param required: 
        :param suffix: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1633db301d7f7a5473af75803e66b5765abf81ab8e8458ac352530045ff0b43c)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WriteProps(
            value=value,
            default_delimiter=default_delimiter,
            delimiter=delimiter,
            prefix=prefix,
            required=required,
            suffix=suffix,
        )

        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IChainable, jsii.invoke(self, "write", [id, props]))

    @builtins.property
    @jsii.member(jsii_name="classifier")
    def classifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "classifier"))

    @builtins.property
    @jsii.member(jsii_name="refs")
    def refs(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "refs"))

    @builtins.property
    @jsii.member(jsii_name="title")
    def title(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "title"))


@jsii.implements(IIssueHandler)
class Discord(
    IssuePluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.Discord",
):
    '''A standardized implementation that allows Discord messages to be sent in response to events detected in AWS.

    Intended for use with the ``IssueManager`` state machine which allows
    arbitrary types of events to be processed into standard values and then
    output or one of more issue tracking services.
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        channel: builtins.str,
        token: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
        mentions: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a new instance of the JiraTicket class.

        :param scope: A CDK Construct that will serve as this resource's parent in the construct tree.
        :param id: A name to be associated with the stack and used in resource naming. Must be unique within the context of 'scope'.
        :param channel: 
        :param token: 
        :param event_bus: 
        :param mentions: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb4e198a320ebbe55fb811ad6494b480b2e2697eeedb57f725f878668c229625)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DiscordProps(
            channel=channel,
            token=token,
            event_bus=event_bus,
            mentions=mentions,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="buildEventOverrides")
    def build_event_overrides(
        self,
        *,
        channel: typing.Optional[builtins.str] = None,
        mentions: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> IssueHandlerOverride:
        '''
        :param channel: 
        :param mentions: 
        '''
        options = DiscordOverrideOptions(channel=channel, mentions=mentions)

        return typing.cast(IssueHandlerOverride, jsii.invoke(self, "buildEventOverrides", [options]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="DEFAULT_NAME")
    def DEFAULT_NAME(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "DEFAULT_NAME"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MESSAGES_ENDPOINT")
    def MESSAGES_ENDPOINT(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "MESSAGES_ENDPOINT"))

    @builtins.property
    @jsii.member(jsii_name="apiDestination")
    def api_destination(self) -> _aws_cdk_aws_events_ceddda9d.ApiDestination:
        '''Destination pointing to a Jira instance where tickets are to be created.'''
        return typing.cast(_aws_cdk_aws_events_ceddda9d.ApiDestination, jsii.get(self, "apiDestination"))

    @builtins.property
    @jsii.member(jsii_name="channel")
    def channel(self) -> builtins.str:
        '''The default Discord channel where messages processed by the handler should be sent if no override is given.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "channel"))

    @builtins.property
    @jsii.member(jsii_name="connection")
    def connection(self) -> _aws_cdk_aws_events_ceddda9d.Connection:
        '''API connection providing details of how to communicate with the configured Jira instance.'''
        return typing.cast(_aws_cdk_aws_events_ceddda9d.Connection, jsii.get(self, "connection"))

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine:
        '''The State Machine that handles creating a Jira ticket for a passed issue.

        Internally this state machine uses the AWS managed ``AWS-CreateJiraIssue``
        SSM Automation document.

        :group: Resources
        '''
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine, jsii.get(self, "handler"))

    @builtins.property
    @jsii.member(jsii_name="mentions")
    def mentions(self) -> typing.List[builtins.str]:
        '''Collection of users or roles who should be mentioned by default when sending a message to Discord.'''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "mentions"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The human friendly name that can be used to identify the plugin.

        :group: Inputs
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="token")
    def token(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        '''The token for a Discord bot that has permissions to post in the destination channels.

        The secret should be in JSON format and contain the
        key:

        token: The token for the bot that has permissions to post in the
        destination Discord channels.

        :group: Inputs
        '''
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, jsii.get(self, "token"))

    @builtins.property
    @jsii.member(jsii_name="eventBus")
    def event_bus(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus]:
        '''The event bus to use to trigger writes to the Jira instance.

        This integration formats a Jira API response and then sends it to a Jira
        instance by means of an EventBridge Destination API and a specially
        crafted event pattern. This is the event bus where the rule to trigger the
        API will be added and the trigger event will be sent.
        '''
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus], jsii.get(self, "eventBus"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        '''The length of time that the State Machine that handles creation of Jira tickets is allowed to run before timing out.

        :group: Inputs
        '''
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "timeout"))


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.DiscordProps",
    jsii_struct_bases=[IssuePluginBaseProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "logging": "logging",
        "channel": "channel",
        "token": "token",
        "event_bus": "eventBus",
        "mentions": "mentions",
        "name": "name",
        "timeout": "timeout",
    },
)
class DiscordProps(IssuePluginBaseProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        channel: builtins.str,
        token: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
        event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
        mentions: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''Configuration controlling how Discord messages should be sent in response to events.

        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param logging: 
        :param channel: 
        :param token: 
        :param event_bus: 
        :param mentions: 
        :param name: 
        :param timeout: 
        '''
        if isinstance(logging, dict):
            logging = StateMachineLogging(**logging)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29753140d336d671dafb38ed6d56c41ca40aba29a1c30d7d247039c3e7a19497)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
            check_type(argname="argument token", value=token, expected_type=type_hints["token"])
            check_type(argname="argument event_bus", value=event_bus, expected_type=type_hints["event_bus"])
            check_type(argname="argument mentions", value=mentions, expected_type=type_hints["mentions"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel": channel,
            "token": token,
        }
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if logging is not None:
            self._values["logging"] = logging
        if event_bus is not None:
            self._values["event_bus"] = event_bus
        if mentions is not None:
            self._values["mentions"] = mentions
        if name is not None:
            self._values["name"] = name
        if timeout is not None:
            self._values["timeout"] = timeout

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
    def logging(self) -> typing.Optional[StateMachineLogging]:
        result = self._values.get("logging")
        return typing.cast(typing.Optional[StateMachineLogging], result)

    @builtins.property
    def channel(self) -> builtins.str:
        result = self._values.get("channel")
        assert result is not None, "Required property 'channel' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def token(self) -> _aws_cdk_aws_secretsmanager_ceddda9d.ISecret:
        result = self._values.get("token")
        assert result is not None, "Required property 'token' is missing"
        return typing.cast(_aws_cdk_aws_secretsmanager_ceddda9d.ISecret, result)

    @builtins.property
    def event_bus(self) -> typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus]:
        result = self._values.get("event_bus")
        return typing.cast(typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus], result)

    @builtins.property
    def mentions(self) -> typing.Optional[typing.List[builtins.str]]:
        result = self._values.get("mentions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DiscordProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IIssueParser)
class EcrScanFinding(
    IssuePluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.EcrScanFinding",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param match_type: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73bcbf64ab813f7e2495560494a57d70b4d06ec8af196d2201175402c96def41)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EcrScanFindingProps(
            match_type=match_type,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.IConstruct,
    ) -> typing.List[IssueTrigger]:
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8985ff0250d37f3f3bb35edc1e8c6b7b5536bce1eb8cac6d4200806ca9ff5ad9)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(typing.List[IssueTrigger], jsii.invoke(self, "bind", [_scope]))

    @jsii.member(jsii_name="buildDescription")
    def _build_description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "buildDescription", []))

    @jsii.member(jsii_name="buildSummary")
    def _build_summary(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.invoke(self, "buildSummary", []))

    @jsii.member(jsii_name="registerIssueTrigger")
    def register_issue_trigger(
        self,
        id: builtins.str,
        *,
        overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
        severity: typing.Optional[IEcrImageScanSeverityConfiguration] = None,
    ) -> IssueTrigger:
        '''
        :param id: -
        :param overrides: 
        :param severity: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__489c123b0055bedbfd9248bb93bd3d47474a17c6776b2f4b12c0e6ad0df4b20d)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = EcrScanFindingEventOptions(overrides=overrides, severity=severity)

        return typing.cast(IssueTrigger, jsii.invoke(self, "registerIssueTrigger", [id, options]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MATCH_TYPE")
    def MATCH_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "MATCH_TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SEVERITIES")
    def SEVERITIES(cls) -> typing.List[EcrImageScanSeverity]:
        return typing.cast(typing.List[EcrImageScanSeverity], jsii.sget(cls, "SEVERITIES"))

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine, jsii.get(self, "handler"))

    @builtins.property
    @jsii.member(jsii_name="matchType")
    def match_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchType"))

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> typing.List[IssueTrigger]:
        return typing.cast(typing.List[IssueTrigger], jsii.get(self, "triggers"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "timeout"))


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.EcrScanFindingProps",
    jsii_struct_bases=[IssuePluginBaseProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "logging": "logging",
        "match_type": "matchType",
        "name": "name",
        "timeout": "timeout",
    },
)
class EcrScanFindingProps(IssuePluginBaseProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param logging: 
        :param match_type: 
        :param name: 
        :param timeout: 
        '''
        if isinstance(logging, dict):
            logging = StateMachineLogging(**logging)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e82595dd3c35b39845d75b90d1e29c23a1e20c15b47ab93498b4357e3f1cac3e)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument match_type", value=match_type, expected_type=type_hints["match_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if logging is not None:
            self._values["logging"] = logging
        if match_type is not None:
            self._values["match_type"] = match_type
        if name is not None:
            self._values["name"] = name
        if timeout is not None:
            self._values["timeout"] = timeout

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
    def logging(self) -> typing.Optional[StateMachineLogging]:
        result = self._values.get("logging")
        return typing.cast(typing.Optional[StateMachineLogging], result)

    @builtins.property
    def match_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("match_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcrScanFindingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.GuardDutyFindingProps",
    jsii_struct_bases=[IssuePluginBaseProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "logging": "logging",
    },
)
class GuardDutyFindingProps(IssuePluginBaseProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param logging: 
        '''
        if isinstance(logging, dict):
            logging = StateMachineLogging(**logging)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e6e55a7b929c92d8053bca94a0c31912b92cf30a1a9a3fc1db1e473e5fd8a0c)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if logging is not None:
            self._values["logging"] = logging

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
    def logging(self) -> typing.Optional[StateMachineLogging]:
        result = self._values.get("logging")
        return typing.cast(typing.Optional[StateMachineLogging], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GuardDutyFindingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IIssueParser)
class IssueParserPluginBase(
    IssuePluginBase,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-extensions.alerting.IssueParserPluginBase",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param match_type: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__098f4284c9e06c1e3293de00b0756ebf6635c18259a0b2a1759b76c43d648717)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = IssueParserPluginBaseProps(
            match_type=match_type,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDefaultTrigger")
    @abc.abstractmethod
    def _add_default_trigger(self) -> IssueTrigger:
        ...

    @jsii.member(jsii_name="bind")
    def bind(self, _node: _constructs_77d1e7e8.IConstruct) -> typing.List[IssueTrigger]:
        '''
        :param _node: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21924158e796009491fe19ef69565c16346a59d3fccee6034d692ee83b9fff34)
            check_type(argname="argument _node", value=_node, expected_type=type_hints["_node"])
        return typing.cast(typing.List[IssueTrigger], jsii.invoke(self, "bind", [_node]))

    @builtins.property
    @jsii.member(jsii_name="handler")
    @abc.abstractmethod
    def handler(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine:
        ...

    @builtins.property
    @jsii.member(jsii_name="matchType")
    def match_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "matchType"))

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> typing.List[IssueTrigger]:
        return typing.cast(typing.List[IssueTrigger], jsii.get(self, "triggers"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "timeout"))


class _IssueParserPluginBaseProxy(
    IssueParserPluginBase,
    jsii.proxy_for(IssuePluginBase), # type: ignore[misc]
):
    @jsii.member(jsii_name="addDefaultTrigger")
    def _add_default_trigger(self) -> IssueTrigger:
        return typing.cast(IssueTrigger, jsii.invoke(self, "addDefaultTrigger", []))

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine, jsii.get(self, "handler"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, IssueParserPluginBase).__jsii_proxy_class__ = lambda : _IssueParserPluginBaseProxy


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.IssueParserPluginBaseProps",
    jsii_struct_bases=[IssuePluginBaseProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "logging": "logging",
        "match_type": "matchType",
        "name": "name",
        "timeout": "timeout",
    },
)
class IssueParserPluginBaseProps(IssuePluginBaseProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param logging: 
        :param match_type: 
        :param name: 
        :param timeout: 
        '''
        if isinstance(logging, dict):
            logging = StateMachineLogging(**logging)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a653d12e009407e19b4ddbffb5515a0879508b341b41eebb4da215911faf5a)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument match_type", value=match_type, expected_type=type_hints["match_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if logging is not None:
            self._values["logging"] = logging
        if match_type is not None:
            self._values["match_type"] = match_type
        if name is not None:
            self._values["name"] = name
        if timeout is not None:
            self._values["timeout"] = timeout

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
    def logging(self) -> typing.Optional[StateMachineLogging]:
        result = self._values.get("logging")
        return typing.cast(typing.Optional[StateMachineLogging], result)

    @builtins.property
    def match_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("match_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssueParserPluginBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IIssueParser)
class OpenSearchEvent(
    IssueParserPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.OpenSearchEvent",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param match_type: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52949d2720a4b949a4717cfdc50240485b8d1e41c556c4fa8b0d0f71dd5a034b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = OpenSearchEventProps(
            match_type=match_type,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDefaultTrigger")
    def _add_default_trigger(self) -> IssueTrigger:
        return typing.cast(IssueTrigger, jsii.invoke(self, "addDefaultTrigger", []))

    @jsii.member(jsii_name="buildDescription")
    def _build_description(self) -> DescriptionBuilder:
        return typing.cast(DescriptionBuilder, jsii.invoke(self, "buildDescription", []))

    @jsii.member(jsii_name="registerIssueTrigger")
    def register_issue_trigger(
        self,
        id: builtins.str,
        *,
        overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
        severity: typing.Optional[typing.Sequence[OpenSearchEventSeverity]] = None,
        types: typing.Optional[typing.Sequence[OpenSearchEventType]] = None,
    ) -> IssueTrigger:
        '''
        :param id: -
        :param overrides: 
        :param severity: 
        :param types: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__528c8f017248cc4de2a746c2b39f9784eb824979d28584d4c6eba3b40ae962bf)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = OpenSearchEventRuleOptions(
            overrides=overrides, severity=severity, types=types
        )

        return typing.cast(IssueTrigger, jsii.invoke(self, "registerIssueTrigger", [id, options]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MATCH_TYPE")
    def MATCH_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "MATCH_TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SEVERITIES")
    def SEVERITIES(cls) -> typing.List[OpenSearchEventSeverity]:
        return typing.cast(typing.List[OpenSearchEventSeverity], jsii.sget(cls, "SEVERITIES"))

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine, jsii.get(self, "handler"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "timeout"))


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.OpenSearchEventProps",
    jsii_struct_bases=[IssueParserPluginBaseProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "logging": "logging",
        "match_type": "matchType",
        "name": "name",
        "timeout": "timeout",
    },
)
class OpenSearchEventProps(IssueParserPluginBaseProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param logging: 
        :param match_type: 
        :param name: 
        :param timeout: 
        '''
        if isinstance(logging, dict):
            logging = StateMachineLogging(**logging)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae40a32488fbfdbf39a11db5e8fabeb99440eb84e909317292d73d23d5c52254)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument match_type", value=match_type, expected_type=type_hints["match_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if logging is not None:
            self._values["logging"] = logging
        if match_type is not None:
            self._values["match_type"] = match_type
        if name is not None:
            self._values["name"] = name
        if timeout is not None:
            self._values["timeout"] = timeout

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
    def logging(self) -> typing.Optional[StateMachineLogging]:
        result = self._values.get("logging")
        return typing.cast(typing.Optional[StateMachineLogging], result)

    @builtins.property
    def match_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("match_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpenSearchEventProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IIssueParser)
class ConfigComplianceChange(
    IssueParserPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.ConfigComplianceChange",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param match_type: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f0ca51d313cf87797035d101ae40927fb9b2cc859649a09f9468b8a005ed32d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ConfigComplianceChangeProps(
            match_type=match_type,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDefaultTrigger")
    def _add_default_trigger(self) -> IssueTrigger:
        return typing.cast(IssueTrigger, jsii.invoke(self, "addDefaultTrigger", []))

    @jsii.member(jsii_name="buildDescription")
    def _build_description(self) -> DescriptionBuilder:
        return typing.cast(DescriptionBuilder, jsii.invoke(self, "buildDescription", []))

    @jsii.member(jsii_name="buildResourceUrl")
    def _build_resource_url(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.Chain:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Chain, jsii.invoke(self, "buildResourceUrl", []))

    @jsii.member(jsii_name="registerIssueTrigger")
    def register_issue_trigger(
        self,
        id: builtins.str,
        *,
        include_security_hub: typing.Optional[builtins.bool] = None,
        overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
        severity: typing.Optional[typing.Sequence[InspectorSeverity]] = None,
    ) -> IssueTrigger:
        '''
        :param id: -
        :param include_security_hub: 
        :param overrides: 
        :param severity: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d057fe9ac6c510dc502950cd49d8223be9823d80453df9058c4caa6ee70aa4)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = ConfigComplianceChangeRuleOptions(
            include_security_hub=include_security_hub,
            overrides=overrides,
            severity=severity,
        )

        return typing.cast(IssueTrigger, jsii.invoke(self, "registerIssueTrigger", [id, options]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MATCH_TYPE")
    def MATCH_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "MATCH_TYPE"))

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine, jsii.get(self, "handler"))

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> typing.List[IssueTrigger]:
        return typing.cast(typing.List[IssueTrigger], jsii.get(self, "triggers"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "timeout"))


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.ConfigComplianceChangeProps",
    jsii_struct_bases=[IssueParserPluginBaseProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "logging": "logging",
        "match_type": "matchType",
        "name": "name",
        "timeout": "timeout",
    },
)
class ConfigComplianceChangeProps(IssueParserPluginBaseProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param logging: 
        :param match_type: 
        :param name: 
        :param timeout: 
        '''
        if isinstance(logging, dict):
            logging = StateMachineLogging(**logging)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101661ed7f114b2db2fef50e85a8366c5587a47ca9daaa52954c8f4529c5edde)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument match_type", value=match_type, expected_type=type_hints["match_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if logging is not None:
            self._values["logging"] = logging
        if match_type is not None:
            self._values["match_type"] = match_type
        if name is not None:
            self._values["name"] = name
        if timeout is not None:
            self._values["timeout"] = timeout

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
    def logging(self) -> typing.Optional[StateMachineLogging]:
        result = self._values.get("logging")
        return typing.cast(typing.Optional[StateMachineLogging], result)

    @builtins.property
    def match_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("match_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConfigComplianceChangeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GuardDutyFinding(
    IssueParserPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.GuardDutyFinding",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4dec916a40d82e4fe4c479f7016f0b32693677212cdfb097b6bc59cacc2df9d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GuardDutyFindingProps(
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDefaultTrigger")
    def _add_default_trigger(self) -> IssueTrigger:
        return typing.cast(IssueTrigger, jsii.invoke(self, "addDefaultTrigger", []))

    @jsii.member(jsii_name="addSectionField")
    def add_section_field(
        self,
        id: builtins.str,
        key: builtins.str,
        path: builtins.str,
    ) -> _aws_cdk_aws_stepfunctions_ceddda9d.Chain:
        '''
        :param id: -
        :param key: -
        :param path: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__188e0d53744dfde0d390bddf2c56068094307650522fe820b92884e25ca49018)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Chain, jsii.invoke(self, "addSectionField", [id, key, path]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        _scope: _constructs_77d1e7e8.IConstruct,
    ) -> typing.List[IssueTrigger]:
        '''
        :param _scope: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e44c4b56ea3bb6f28f6ac0ed446d8c6a855c3b85f96dfc591fe5374d8df01b1b)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(typing.List[IssueTrigger], jsii.invoke(self, "bind", [_scope]))

    @jsii.member(jsii_name="buildSeverityMap")
    def _build_severity_map(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.Chain:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.Chain, jsii.invoke(self, "buildSeverityMap", []))

    @jsii.member(jsii_name="registerIssueTrigger")
    def register_issue_trigger(
        self,
        id: builtins.str,
        *,
        overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
        severity: typing.Optional[typing.Sequence[GuardDutySeverity]] = None,
    ) -> IssueTrigger:
        '''
        :param id: -
        :param overrides: 
        :param severity: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce6b93596110d320b6a75478b55171b882dbec52aa31661f28596ed0ebc85352)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = GuardDutyFindingRuleOptions(overrides=overrides, severity=severity)

        return typing.cast(IssueTrigger, jsii.invoke(self, "registerIssueTrigger", [id, options]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MATCH_TYPE")
    def MATCH_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "MATCH_TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SEVERITIES")
    def SEVERITIES(cls) -> typing.List[GuardDutySeverity]:
        return typing.cast(typing.List[GuardDutySeverity], jsii.sget(cls, "SEVERITIES"))

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine, jsii.get(self, "handler"))

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> typing.List[IssueTrigger]:
        return typing.cast(typing.List[IssueTrigger], jsii.get(self, "triggers"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "timeout"))


@jsii.implements(IIssueParser)
class InspectorFinding(
    IssueParserPluginBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-extensions.alerting.InspectorFinding",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
        logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param match_type: 
        :param name: 
        :param timeout: 
        :param logging: 
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9224638f3a4743e696fb351670045b9d5d0ae8cd2300e1602025e87e3a13f96d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = InspectorFindingProps(
            match_type=match_type,
            name=name,
            timeout=timeout,
            logging=logging,
            account=account,
            environment_from_arn=environment_from_arn,
            physical_name=physical_name,
            region=region,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addDefaultTrigger")
    def _add_default_trigger(self) -> IssueTrigger:
        return typing.cast(IssueTrigger, jsii.invoke(self, "addDefaultTrigger", []))

    @jsii.member(jsii_name="buildDescription")
    def _build_description(self) -> DescriptionBuilder:
        return typing.cast(DescriptionBuilder, jsii.invoke(self, "buildDescription", []))

    @jsii.member(jsii_name="registerIssueTrigger")
    def register_issue_trigger(
        self,
        id: builtins.str,
        *,
        overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
        severity: typing.Optional[typing.Sequence[InspectorSeverity]] = None,
    ) -> IssueTrigger:
        '''
        :param id: -
        :param overrides: 
        :param severity: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__157e671b4ccf574f7c866559c6373ed6cd98917bf041a2d0d8dede3ed033a584)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = InspectorFindingEventOptions(overrides=overrides, severity=severity)

        return typing.cast(IssueTrigger, jsii.invoke(self, "registerIssueTrigger", [id, options]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MATCH_TYPE")
    def MATCH_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "MATCH_TYPE"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="SEVERITIES")
    def SEVERITIES(cls) -> typing.List[InspectorSeverity]:
        return typing.cast(typing.List[InspectorSeverity], jsii.sget(cls, "SEVERITIES"))

    @builtins.property
    @jsii.member(jsii_name="handler")
    def handler(self) -> _aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine:
        return typing.cast(_aws_cdk_aws_stepfunctions_ceddda9d.IStateMachine, jsii.get(self, "handler"))

    @builtins.property
    @jsii.member(jsii_name="triggers")
    def triggers(self) -> typing.List[IssueTrigger]:
        return typing.cast(typing.List[IssueTrigger], jsii.get(self, "triggers"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], jsii.get(self, "timeout"))


@jsii.data_type(
    jsii_type="cdk-extensions.alerting.InspectorFindingProps",
    jsii_struct_bases=[IssueParserPluginBaseProps],
    name_mapping={
        "account": "account",
        "environment_from_arn": "environmentFromArn",
        "physical_name": "physicalName",
        "region": "region",
        "logging": "logging",
        "match_type": "matchType",
        "name": "name",
        "timeout": "timeout",
    },
)
class InspectorFindingProps(IssueParserPluginBaseProps):
    def __init__(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        environment_from_arn: typing.Optional[builtins.str] = None,
        physical_name: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
        match_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    ) -> None:
        '''
        :param account: The AWS account ID this resource belongs to. Default: - the resource is in the same account as the stack it belongs to
        :param environment_from_arn: ARN to deduce region and account from. The ARN is parsed and the account and region are taken from the ARN. This should be used for imported resources. Cannot be supplied together with either ``account`` or ``region``. Default: - take environment from ``account``, ``region`` parameters, or use Stack environment.
        :param physical_name: The value passed in by users to the physical name prop of the resource. - ``undefined`` implies that a physical name will be allocated by CloudFormation during deployment. - a concrete value implies a specific physical name - ``PhysicalName.GENERATE_IF_NEEDED`` is a marker that indicates that a physical will only be generated by the CDK if it is needed for cross-environment references. Otherwise, it will be allocated by CloudFormation. Default: - The physical name will be allocated by CloudFormation at deployment time
        :param region: The AWS region this resource belongs to. Default: - the resource is in the same region as the stack it belongs to
        :param logging: 
        :param match_type: 
        :param name: 
        :param timeout: 
        '''
        if isinstance(logging, dict):
            logging = StateMachineLogging(**logging)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__641a11b0c1c3ff293eb9fa770d49410787e6f0e12c99ce5f277a96ab600afa6c)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument environment_from_arn", value=environment_from_arn, expected_type=type_hints["environment_from_arn"])
            check_type(argname="argument physical_name", value=physical_name, expected_type=type_hints["physical_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument logging", value=logging, expected_type=type_hints["logging"])
            check_type(argname="argument match_type", value=match_type, expected_type=type_hints["match_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if account is not None:
            self._values["account"] = account
        if environment_from_arn is not None:
            self._values["environment_from_arn"] = environment_from_arn
        if physical_name is not None:
            self._values["physical_name"] = physical_name
        if region is not None:
            self._values["region"] = region
        if logging is not None:
            self._values["logging"] = logging
        if match_type is not None:
            self._values["match_type"] = match_type
        if name is not None:
            self._values["name"] = name
        if timeout is not None:
            self._values["timeout"] = timeout

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
    def logging(self) -> typing.Optional[StateMachineLogging]:
        result = self._values.get("logging")
        return typing.cast(typing.Optional[StateMachineLogging], result)

    @builtins.property
    def match_type(self) -> typing.Optional[builtins.str]:
        result = self._values.get("match_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_aws_cdk_ceddda9d.Duration]:
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_aws_cdk_ceddda9d.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "InspectorFindingProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddReferenceProps",
    "AppendDelimiter",
    "ConfigComplianceChange",
    "ConfigComplianceChangeProps",
    "ConfigComplianceChangeRuleOptions",
    "DescriptionBuilder",
    "DescriptionBuilderIterator",
    "DescriptionBuilderIteratorProps",
    "DescriptionBuilderProps",
    "DescriptionBuilderSection",
    "DescriptionBuilderSectionProps",
    "Discord",
    "DiscordOverrideOptions",
    "DiscordProps",
    "EcrImageScanSeverity",
    "EcrImageScanSeverityConfiguration",
    "EcrScanFinding",
    "EcrScanFindingEventOptions",
    "EcrScanFindingProps",
    "GuardDutyFinding",
    "GuardDutyFindingProps",
    "GuardDutyFindingRuleOptions",
    "GuardDutySeverity",
    "IDelayedChainable",
    "IDescriptionBuilderComponent",
    "IEcrImageScanSeverityConfiguration",
    "IIssueHandler",
    "IIssueParser",
    "ISecurityHubSeverityConfiguration",
    "InspectorFinding",
    "InspectorFindingEventOptions",
    "InspectorFindingProps",
    "InspectorSeverity",
    "IssueHander",
    "IssueHandlerOverride",
    "IssueManager",
    "IssueManagerProps",
    "IssueParser",
    "IssueParserPluginBase",
    "IssueParserPluginBaseProps",
    "IssuePluginBase",
    "IssuePluginBaseProps",
    "IssueTrigger",
    "IssueTriggerProps",
    "JiraTicket",
    "JiraTicketOverrideOptions",
    "JiraTicketPriorityMap",
    "JiraTicketProps",
    "OpenSearchEvent",
    "OpenSearchEventProps",
    "OpenSearchEventRuleOptions",
    "OpenSearchEventSeverity",
    "OpenSearchEventType",
    "OpenSearchEventTypeProps",
    "SecurityHubFinding",
    "SecurityHubFindingEventOptions",
    "SecurityHubFindingProps",
    "SecurityHubSeverity",
    "SecurityHubSeverityConfiguration",
    "SetDelimiterProps",
    "StateMachineLogging",
    "WriteProps",
]

publication.publish()

def _typecheckingstub__04f904628bb25dde32dd6031cb272c404da266d7f01a88c1db9a10e0415f0bdd(
    *,
    value: builtins.str,
    delimiter: typing.Optional[AppendDelimiter] = None,
    label: typing.Optional[builtins.str] = None,
    required: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25dff048782bd89514e2efe3c493308e5b027e5caea3fc67cb7edc636e45e2bd(
    delimiter: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a7fbfd7623d1863957228909a2a94428f87e6aca695a5aad641186c1e0077e0(
    *,
    include_security_hub: typing.Optional[builtins.bool] = None,
    overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
    severity: typing.Optional[typing.Sequence[InspectorSeverity]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea6e1ba4f2a92d82b0b5b46bef759c993454be033d460bb87e09b078422da893(
    *,
    array_ref: builtins.str,
    result_path: builtins.str,
    field_delimiter: typing.Optional[AppendDelimiter] = None,
    record_delimiter: typing.Optional[AppendDelimiter] = None,
    section_delimiter: typing.Optional[AppendDelimiter] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fbcb76257f0d6b53c5673dd85b932667d4efe2c20a1d3cda088c388a4a2778(
    *,
    initial_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eda6817459c7b764f8c57dcbc8259687527b5aa22d72369f5db50a3aeb0ded7(
    *,
    title: builtins.str,
    reference_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__253bd589f4b779840486be7096aa59433e6c2634024583dedc1e45fa90aefc20(
    *,
    channel: typing.Optional[builtins.str] = None,
    mentions: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d0339c6d2e7f75b5fad2a1cd75c3f1c5bb5fedaae0d185457222fa11329e56(
    name: builtins.str,
    priority: jsii.Number,
    standardized: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3c2db4ae04fddf5eaa2a312c7e148c014088162d41c292fe5cbc4bd633cf0c(
    *levels: EcrImageScanSeverity,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e3541bf824f9e2d2c143b2a3a38dfbd2199f9965389dea35d2ec38cea4a6e5e(
    level: EcrImageScanSeverity,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f861d1625d2bf64d7799c9afaa9c4dbe8c48a75ba31a62300f13388932a11474(
    *,
    overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
    severity: typing.Optional[IEcrImageScanSeverityConfiguration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fd75bc62445d8ffbf385240f2d7f90d7bd38795e18ae196db64a84d1235295b(
    *,
    overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
    severity: typing.Optional[typing.Sequence[GuardDutySeverity]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7054b205177878cf39892467f187d50136525d04d5d4a40cc90ab08257d3989b(
    *levels: GuardDutySeverity,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__015817cc0484b8c3fd8aa7e8b3ce0698c463101fe83055b3e8ddba4d892eed1f(
    standardized: builtins.str,
    lower_bound: typing.Optional[jsii.Number] = None,
    upper_bound: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11e5ba579f1ca10ddac7ef691ff93b2112cf9c9eba602aa79738cddd50b4b8cb(
    level: GuardDutySeverity,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__914c5cc51dfbef689f3ddb96d90c1a844fd7c1ef367c71cee64ae4bda11d8456(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2811087530adfda34e0d5ca69f82bf4edfe4dd7dead821ae656750beaee108ad(
    id: builtins.str,
    *,
    array_ref: builtins.str,
    result_path: builtins.str,
    field_delimiter: typing.Optional[AppendDelimiter] = None,
    record_delimiter: typing.Optional[AppendDelimiter] = None,
    section_delimiter: typing.Optional[AppendDelimiter] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__407e002cef1199f985cb7b8d4a606f3303e0b3adb37ec32da2b4e1c5bb60c9c8(
    id: builtins.str,
    *,
    value: builtins.str,
    delimiter: typing.Optional[AppendDelimiter] = None,
    label: typing.Optional[builtins.str] = None,
    required: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b703a54f51bfd91257570f2784d19f7a98fec6d940a794f7fa49d41fa63a6b6e(
    id: builtins.str,
    *,
    delimiter: AppendDelimiter,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ef53e69c71c047fdd6c569e1e0bc77987b471295de0a6231aff47a94acce4d4(
    id: builtins.str,
    *,
    value: builtins.str,
    default_delimiter: typing.Optional[AppendDelimiter] = None,
    delimiter: typing.Optional[AppendDelimiter] = None,
    prefix: typing.Optional[builtins.str] = None,
    required: typing.Optional[builtins.bool] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6411dafdb3a630d40eb02ceb6e0f9eac287717175f980c56ed3c9667dd6ebf(
    node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c503396c1371555347496adc9a21268c35b6a2316731a0e9e2fd48db7b3d993(
    *,
    overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
    severity: typing.Optional[typing.Sequence[InspectorSeverity]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7135596fcdd94bfa8874941eea15dbc9dcfad89a2df7658f0eebcede3d2bb7a6(
    *levels: InspectorSeverity,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef21c3e44aabcc6d32cfa08ddf1fe98813ba40dfa40ebfcf5620718f80cdb911(
    standardized: builtins.str,
    original: builtins.str,
    priority: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff52cc5f981ba30046f04d62b2c8a6bdb7725b4e38d07d3a29ca5dec4ff7db2(
    level: InspectorSeverity,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add09d93d064fe5f98082939df59303379ccf56d73870b39e6b320fedfe6964d(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f869ab3c2616a04b67f30bb9166b3c542397e1994c482091441b40066447005e(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    channel: builtins.str,
    token: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
    mentions: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc82eedaec69377fec470cfcf06b82e1b425e2a8c85b604da5b7375421112d61(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    credentials: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    issue_type: builtins.str,
    jira_url: builtins.str,
    priority_map: typing.Union[JiraTicketPriorityMap, typing.Dict[builtins.str, typing.Any]],
    project: builtins.str,
    assignee: typing.Optional[builtins.str] = None,
    event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71c067f96e657bdfe55287a28ac52f9563da10b89615bb14e3ba931322f16324(
    handler: IIssueHandler,
    overrides: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17a0a3e999f7e38036ae2886cdec0fd7d970e598852259abe7f608ddf4ec7721(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    handlers: typing.Optional[typing.Sequence[IIssueHandler]] = None,
    name: typing.Optional[builtins.str] = None,
    parsers: typing.Optional[typing.Sequence[IIssueParser]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__006da00f8a75f6b92f98098984ff0af078263991e437146ac4127a85a112a3ca(
    state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__654b7156f2800145e438153ffe09c71e5081c98202b48f3edc5f002bf19055ab(
    handler: IIssueHandler,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d7f6de6f0e05b39da7c8baab073824cfd3e82aa3c5e53c2970b4ddd3bca5778(
    parser: IIssueParser,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e29efc7fa79c705c84d2f4a658b848da2928c0ddd24221ea7888cdf35bbdf296(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    handlers: typing.Optional[typing.Sequence[IIssueHandler]] = None,
    name: typing.Optional[builtins.str] = None,
    parsers: typing.Optional[typing.Sequence[IIssueParser]] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__648c3911944076b0bf1ca667d34ed7e3c3871836988c48ff5e5ae3854255d86d(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6abcb9f27bdf7ccef0c6a644d8abfbb4f13d78d8a1519ce50db75e4494d3bb7(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1aad78620c0e98f670fddddcf0a5dc72d486a34a04977e10426e875da960857e(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8fcbf9702240630da05ae5ef9be7931f2f71960c1d6d3aaf5062ec365baa64(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b81ee6b7854b5fbce0b73e4ecaa7916dd5ce8ba3f9409a6de2f327dbd5b6890(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4a4ad71f1d1a7c0341ca14f2d361fd2b7a761f8fbda6ce95328e5d5a136bf71(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__027fc616c754753d62015be334050a7b4e26be331d5e20391a42498402fa2455(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f634e82d7e189610321f5dd3c927a2dc1d40995c6f87f66ebe13118b5b877c8(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56df0d9f4491a32d9f6ba0466693d652b321500a63f290664ccd18f865f059fd(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    event_pattern: typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]],
    parser: IIssueParser,
    overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f18ea78c183fd470371a786755a599e139cd9b3f8f9d8654118c0a202e550f1(
    handler_overrides: IssueHandlerOverride,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c8214e6d65268ffc7a640ba6f7c49c65a6e0d9788c3ca8448d90ddfe3272ab(
    state_machine: _aws_cdk_aws_stepfunctions_ceddda9d.StateMachine,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc891efbaae81aac0dc215f01b59a21abd6ef60e4aee7dda84e6a919e5d93ca8(
    *,
    event_pattern: typing.Union[_aws_cdk_aws_events_ceddda9d.EventPattern, typing.Dict[builtins.str, typing.Any]],
    parser: IIssueParser,
    overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__faa3790c193df8caeefa2eb5592127364a27e0fb785386efce4e0e73c6c1272d(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    credentials: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    issue_type: builtins.str,
    jira_url: builtins.str,
    priority_map: typing.Union[JiraTicketPriorityMap, typing.Dict[builtins.str, typing.Any]],
    project: builtins.str,
    assignee: typing.Optional[builtins.str] = None,
    event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3597edffb011fcf9cb1f88b624d61e6a661249b81bae761d7607034e73a6b1c7(
    *,
    assignee: typing.Optional[builtins.str] = None,
    issue_priority: typing.Optional[builtins.str] = None,
    issue_type: typing.Optional[builtins.str] = None,
    project: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a08739fa088feae15f5aa82920113fc7790f876d4635fef42fe471aeffe31a4(
    *,
    critical: typing.Optional[builtins.str] = None,
    default: typing.Optional[builtins.str] = None,
    high: typing.Optional[builtins.str] = None,
    info: typing.Optional[builtins.str] = None,
    low: typing.Optional[builtins.str] = None,
    medium: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed6d5eb60877b2a48722da609ac945a0a97beeb637b33690c8915560a61340f7(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    credentials: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    issue_type: builtins.str,
    jira_url: builtins.str,
    priority_map: typing.Union[JiraTicketPriorityMap, typing.Dict[builtins.str, typing.Any]],
    project: builtins.str,
    assignee: typing.Optional[builtins.str] = None,
    event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__699d7a494eacfff85e5fb493304a3e6b77d53d626719ea9797143d77c98839e1(
    *,
    overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
    severity: typing.Optional[typing.Sequence[OpenSearchEventSeverity]] = None,
    types: typing.Optional[typing.Sequence[OpenSearchEventType]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd6f8670ec2ad255eb3e1c1257163903e257229f51b40f226df3de18a7e9a374(
    *levels: OpenSearchEventSeverity,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a107e60c49274129b060940d98a8008d6c5b027cf04f49b95c93be6931f88530(
    standardized: builtins.str,
    original: builtins.str,
    priority: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54431185d7d2de065a2df9a2bba74641b715d32f1f97db3ee231d4f52a4f998c(
    level: OpenSearchEventSeverity,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113310a0c5e7559602f64863de5e62d33a52838536af822bf129089260b1c769(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297acd47d2c33794c0ea7437ed6bd3b867ad3c2219f60ec2cde0e221d39f5d2e(
    *,
    detail_type: builtins.str,
    event_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380b1636b1f967bc917f9f72a3debc0caf5126cc6e8e510d4066b83f85eaaa1e(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__258010b44491929bcf69c6f3260753afbe509aca50a192e5bf7c93a6f3c77843(
    _scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21fd3ae4500b241033b6cef515920861faab44979faf975e1d542b4f8316e3bc(
    id: builtins.str,
    *,
    overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
    severity: typing.Optional[ISecurityHubSeverityConfiguration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8655a09b8f54d0a3b830e464a308025fe70e639a13291f48bff63e0b6bd5901f(
    *,
    overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
    severity: typing.Optional[ISecurityHubSeverityConfiguration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca783ee46a82565d9b2cd4907f5ad9c03223b85389f280a5b41cc4f4a2190277(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__880d3c74d98dfff1d219a68a56d35589351dbd43f2a35cc9a8b1856266ad301d(
    name: builtins.str,
    lower_bound: jsii.Number,
    upper_bound: jsii.Number,
    standardized: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28583288e953240e63f8bdb060d4261683c5e292e21929f74b5ef677cbb834c6(
    *levels: SecurityHubSeverity,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__863f802289de2b198caedda8eb31a9bef07b59b1ef6be2257b5bff4414b73401(
    level: SecurityHubSeverity,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d52efedb526beaf6890c8ab6bdf08af1d2c01494c0fbad4d2238af151424af2(
    *,
    delimiter: AppendDelimiter,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fbb086a355e5841e0230f4aa4854b365e4400b834a6df4d009a7884a526168f(
    *,
    destination: typing.Optional[_aws_cdk_aws_logs_ceddda9d.ILogGroup] = None,
    enabled: typing.Optional[builtins.bool] = None,
    include_execution_data: typing.Optional[builtins.bool] = None,
    level: typing.Optional[_aws_cdk_aws_stepfunctions_ceddda9d.LogLevel] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce897381a7a6ad487b1bbbd631e32ac3942ca9709805ecf1caf3c11704b87231(
    *,
    value: builtins.str,
    default_delimiter: typing.Optional[AppendDelimiter] = None,
    delimiter: typing.Optional[AppendDelimiter] = None,
    prefix: typing.Optional[builtins.str] = None,
    required: typing.Optional[builtins.bool] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76ae5316c6c731592af25328b99f469342a02f8b2b96f2f6056575e7cca257b4(
    scope: _constructs_77d1e7e8.IConstruct,
    *,
    initial_description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac15be8a7b4087186efaff33859d15adc2c5950f524034601e8e0841597e540b(
    id: builtins.str,
    *,
    array_ref: builtins.str,
    result_path: builtins.str,
    field_delimiter: typing.Optional[AppendDelimiter] = None,
    record_delimiter: typing.Optional[AppendDelimiter] = None,
    section_delimiter: typing.Optional[AppendDelimiter] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96dbc2c00e9108a2a7d85034168a4bb6f29d993ac63d7041b7996da10d2b8006(
    id: builtins.str,
    *,
    value: builtins.str,
    delimiter: typing.Optional[AppendDelimiter] = None,
    label: typing.Optional[builtins.str] = None,
    required: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a474a63d42135823453c5f22f0283f6b31e3ea7f4def19dea97a75d71e5a1f0f(
    id: builtins.str,
    *,
    title: builtins.str,
    reference_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e0b6eb6e81a5e45f8253f9c0933a8a6ee17eb67f446a9ccb39aaca710dade7f(
    prefix: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad3b238746c06b75e41661d9ff9d65526821be37672ae9d67bb5f391b46efd55(
    builder: IDescriptionBuilderComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39effaee482adb498d97c478f42007a087994ee3deef74af511c9075cba6e3a2(
    chainable: _aws_cdk_aws_stepfunctions_ceddda9d.IChainable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16c79b956a8c1987e777f724971101bae6be1ead3ccc2958bd5b927096079e9d(
    id: builtins.str,
    *,
    delimiter: AppendDelimiter,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__059282f45164bce07a6b303d31c55c48873e9f90df2695104f68eacbb46fe688(
    id: builtins.str,
    *,
    value: builtins.str,
    default_delimiter: typing.Optional[AppendDelimiter] = None,
    delimiter: typing.Optional[AppendDelimiter] = None,
    prefix: typing.Optional[builtins.str] = None,
    required: typing.Optional[builtins.bool] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcfd81f6847b2855e5867b4b0669d62b9afef539fb734f8c70567c3a4e13868e(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    array_ref: builtins.str,
    result_path: builtins.str,
    field_delimiter: typing.Optional[AppendDelimiter] = None,
    record_delimiter: typing.Optional[AppendDelimiter] = None,
    section_delimiter: typing.Optional[AppendDelimiter] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__462d03a128fd156179f1090938db59ffea06783917bf5d57dce17ae2d2d1e8ef(
    id: builtins.str,
    *,
    array_ref: builtins.str,
    result_path: builtins.str,
    field_delimiter: typing.Optional[AppendDelimiter] = None,
    record_delimiter: typing.Optional[AppendDelimiter] = None,
    section_delimiter: typing.Optional[AppendDelimiter] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d35545a175b2e2cbbe3b5bb9e6f4e6ebfc39fb8650579529524d6745b86769d(
    id: builtins.str,
    *,
    value: builtins.str,
    delimiter: typing.Optional[AppendDelimiter] = None,
    label: typing.Optional[builtins.str] = None,
    required: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e5c13c7e5ceea2af4cf13dd7371fe24516d78f84853f831b739ddd7a809de5e(
    prefix: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6081e98e12fadf65028d6623ba15661a7ff62cc47f4f0ed12189f0deb0174030(
    builder: IDescriptionBuilderComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b28b734bb363d31e78f0073c5827b7971ac74566393ad096fd55ca8c90f6f915(
    chainable: _aws_cdk_aws_stepfunctions_ceddda9d.IChainable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff99364db406f0dd2ebf79d6226811c7c7abc87dee88aa122e988ae002f16930(
    id: builtins.str,
    *,
    delimiter: AppendDelimiter,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9211877b3b1f3cea27e971c80b93245acf989efd6df4ced306f426a73c9343(
    id: builtins.str,
    *,
    value: builtins.str,
    default_delimiter: typing.Optional[AppendDelimiter] = None,
    delimiter: typing.Optional[AppendDelimiter] = None,
    prefix: typing.Optional[builtins.str] = None,
    required: typing.Optional[builtins.bool] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87ca90a46892ec0e335ac0242b06d52781533b02652dd31251b67c510bb4bdc3(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    title: builtins.str,
    reference_checks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dff71b352d679fe0ac944cde79f865ab23cbcd664c124d055bd22b5fe542875(
    id: builtins.str,
    *,
    array_ref: builtins.str,
    result_path: builtins.str,
    field_delimiter: typing.Optional[AppendDelimiter] = None,
    record_delimiter: typing.Optional[AppendDelimiter] = None,
    section_delimiter: typing.Optional[AppendDelimiter] = None,
    title: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a5ee28fcd7d15d7059ea9114158d9c5943430b79ea2c7e2223cc4dcf2380bb(
    id: builtins.str,
    *,
    value: builtins.str,
    delimiter: typing.Optional[AppendDelimiter] = None,
    label: typing.Optional[builtins.str] = None,
    required: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16f28a78161f21f99820434b97d98105c60109dd5a7c6db86dd89f683d9fdb35(
    ref: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00d70736c81dd0c1242aa8e8d04845df7d4c12252dbdd364c7b68b0150c5314a(
    prefix: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86cdb432065e5e722bf28646340f08e7804f7b4b66ff3da7f75b23079e80c89f(
    builder: IDescriptionBuilderComponent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22f61284bc611f89bf448a53dc8c1d8acce3782300a7c9f634106042c531be9b(
    chainable: _aws_cdk_aws_stepfunctions_ceddda9d.IChainable,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__baacaecef78bbec42c4f14777fdbc34e5475b3119c475238f8df79a42bb03b2c(
    id: builtins.str,
    *,
    delimiter: AppendDelimiter,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1633db301d7f7a5473af75803e66b5765abf81ab8e8458ac352530045ff0b43c(
    id: builtins.str,
    *,
    value: builtins.str,
    default_delimiter: typing.Optional[AppendDelimiter] = None,
    delimiter: typing.Optional[AppendDelimiter] = None,
    prefix: typing.Optional[builtins.str] = None,
    required: typing.Optional[builtins.bool] = None,
    suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb4e198a320ebbe55fb811ad6494b480b2e2697eeedb57f725f878668c229625(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    channel: builtins.str,
    token: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
    mentions: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29753140d336d671dafb38ed6d56c41ca40aba29a1c30d7d247039c3e7a19497(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    channel: builtins.str,
    token: _aws_cdk_aws_secretsmanager_ceddda9d.ISecret,
    event_bus: typing.Optional[_aws_cdk_aws_events_ceddda9d.IEventBus] = None,
    mentions: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73bcbf64ab813f7e2495560494a57d70b4d06ec8af196d2201175402c96def41(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8985ff0250d37f3f3bb35edc1e8c6b7b5536bce1eb8cac6d4200806ca9ff5ad9(
    _scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__489c123b0055bedbfd9248bb93bd3d47474a17c6776b2f4b12c0e6ad0df4b20d(
    id: builtins.str,
    *,
    overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
    severity: typing.Optional[IEcrImageScanSeverityConfiguration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e82595dd3c35b39845d75b90d1e29c23a1e20c15b47ab93498b4357e3f1cac3e(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6e55a7b929c92d8053bca94a0c31912b92cf30a1a9a3fc1db1e473e5fd8a0c(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__098f4284c9e06c1e3293de00b0756ebf6635c18259a0b2a1759b76c43d648717(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21924158e796009491fe19ef69565c16346a59d3fccee6034d692ee83b9fff34(
    _node: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a653d12e009407e19b4ddbffb5515a0879508b341b41eebb4da215911faf5a(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52949d2720a4b949a4717cfdc50240485b8d1e41c556c4fa8b0d0f71dd5a034b(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__528c8f017248cc4de2a746c2b39f9784eb824979d28584d4c6eba3b40ae962bf(
    id: builtins.str,
    *,
    overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
    severity: typing.Optional[typing.Sequence[OpenSearchEventSeverity]] = None,
    types: typing.Optional[typing.Sequence[OpenSearchEventType]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae40a32488fbfdbf39a11db5e8fabeb99440eb84e909317292d73d23d5c52254(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f0ca51d313cf87797035d101ae40927fb9b2cc859649a09f9468b8a005ed32d(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d057fe9ac6c510dc502950cd49d8223be9823d80453df9058c4caa6ee70aa4(
    id: builtins.str,
    *,
    include_security_hub: typing.Optional[builtins.bool] = None,
    overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
    severity: typing.Optional[typing.Sequence[InspectorSeverity]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101661ed7f114b2db2fef50e85a8366c5587a47ca9daaa52954c8f4529c5edde(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4dec916a40d82e4fe4c479f7016f0b32693677212cdfb097b6bc59cacc2df9d(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__188e0d53744dfde0d390bddf2c56068094307650522fe820b92884e25ca49018(
    id: builtins.str,
    key: builtins.str,
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44c4b56ea3bb6f28f6ac0ed446d8c6a855c3b85f96dfc591fe5374d8df01b1b(
    _scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce6b93596110d320b6a75478b55171b882dbec52aa31661f28596ed0ebc85352(
    id: builtins.str,
    *,
    overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
    severity: typing.Optional[typing.Sequence[GuardDutySeverity]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9224638f3a4743e696fb351670045b9d5d0ae8cd2300e1602025e87e3a13f96d(
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157e671b4ccf574f7c866559c6373ed6cd98917bf041a2d0d8dede3ed033a584(
    id: builtins.str,
    *,
    overrides: typing.Optional[typing.Sequence[IssueHandlerOverride]] = None,
    severity: typing.Optional[typing.Sequence[InspectorSeverity]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__641a11b0c1c3ff293eb9fa770d49410787e6f0e12c99ce5f277a96ab600afa6c(
    *,
    account: typing.Optional[builtins.str] = None,
    environment_from_arn: typing.Optional[builtins.str] = None,
    physical_name: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    logging: typing.Optional[typing.Union[StateMachineLogging, typing.Dict[builtins.str, typing.Any]]] = None,
    match_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    timeout: typing.Optional[_aws_cdk_ceddda9d.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass
