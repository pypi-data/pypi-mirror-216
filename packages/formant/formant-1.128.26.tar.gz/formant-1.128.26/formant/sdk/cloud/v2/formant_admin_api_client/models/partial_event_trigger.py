import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.partial_event_trigger_event_type import PartialEventTriggerEventType
from ..models.partial_event_trigger_severity import PartialEventTriggerSeverity
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.battery_event_trigger_condition import BatteryEventTriggerCondition
    from ..models.bitset_event_trigger_condition import BitsetEventTriggerCondition
    from ..models.event_trigger_command import EventTriggerCommand
    from ..models.forwarding_configuration import ForwardingConfiguration
    from ..models.numeric_set_event_trigger_condition import NumericSetEventTriggerCondition
    from ..models.partial_event_trigger_sms_tags import PartialEventTriggerSmsTags
    from ..models.partial_event_trigger_tags import PartialEventTriggerTags
    from ..models.presence_event_trigger_condition import PresenceEventTriggerCondition
    from ..models.regex_event_trigger_condition import RegexEventTriggerCondition
    from ..models.stateful_trigger_configuration import StatefulTriggerConfiguration
    from ..models.threshold_event_trigger_condition import ThresholdEventTriggerCondition
    from ..models.triggered_configuration import TriggeredConfiguration


T = TypeVar("T", bound="PartialEventTrigger")


@attr.s(auto_attribs=True)
class PartialEventTrigger:
    """
    Attributes:
        organization_id (Union[Unset, str]):
        event_type (Union[Unset, PartialEventTriggerEventType]):
        message (Union[Unset, str]):
        condition (Union['BatteryEventTriggerCondition', 'BitsetEventTriggerCondition',
            'NumericSetEventTriggerCondition', 'PresenceEventTriggerCondition', 'RegexEventTriggerCondition',
            'ThresholdEventTriggerCondition', None, Unset]):
        interval (Union[Unset, int]):
        severity (Union[Unset, PartialEventTriggerSeverity]):
        enabled (Union[Unset, bool]):
        format_ (Union[Unset, str]):
        triggered_configuration (Union[Unset, None, TriggeredConfiguration]):
        tags (Union[Unset, PartialEventTriggerTags]):
        sms_tags (Union[Unset, PartialEventTriggerSmsTags]):
        commands (Union[Unset, List['EventTriggerCommand']]):
        notification_enabled (Union[Unset, bool]):
        last_triggered_time (Union[Unset, None, datetime.datetime]):
        stateful_trigger_configuration (Union[Unset, None, StatefulTriggerConfiguration]):
        forwarding_configuration (Union[Unset, None, ForwardingConfiguration]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    organization_id: Union[Unset, str] = UNSET
    event_type: Union[Unset, PartialEventTriggerEventType] = UNSET
    message: Union[Unset, str] = UNSET
    condition: Union[
        "BatteryEventTriggerCondition",
        "BitsetEventTriggerCondition",
        "NumericSetEventTriggerCondition",
        "PresenceEventTriggerCondition",
        "RegexEventTriggerCondition",
        "ThresholdEventTriggerCondition",
        None,
        Unset,
    ] = UNSET
    interval: Union[Unset, int] = UNSET
    severity: Union[Unset, PartialEventTriggerSeverity] = UNSET
    enabled: Union[Unset, bool] = UNSET
    format_: Union[Unset, str] = UNSET
    triggered_configuration: Union[Unset, None, "TriggeredConfiguration"] = UNSET
    tags: Union[Unset, "PartialEventTriggerTags"] = UNSET
    sms_tags: Union[Unset, "PartialEventTriggerSmsTags"] = UNSET
    commands: Union[Unset, List["EventTriggerCommand"]] = UNSET
    notification_enabled: Union[Unset, bool] = UNSET
    last_triggered_time: Union[Unset, None, datetime.datetime] = UNSET
    stateful_trigger_configuration: Union[Unset, None, "StatefulTriggerConfiguration"] = UNSET
    forwarding_configuration: Union[Unset, None, "ForwardingConfiguration"] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        from ..models.battery_event_trigger_condition import BatteryEventTriggerCondition
        from ..models.bitset_event_trigger_condition import BitsetEventTriggerCondition
        from ..models.presence_event_trigger_condition import PresenceEventTriggerCondition
        from ..models.regex_event_trigger_condition import RegexEventTriggerCondition
        from ..models.threshold_event_trigger_condition import ThresholdEventTriggerCondition

        organization_id = self.organization_id
        event_type: Union[Unset, str] = UNSET
        if not isinstance(self.event_type, Unset):
            event_type = self.event_type.value

        message = self.message
        condition: Union[Dict[str, Any], None, Unset]
        if isinstance(self.condition, Unset):
            condition = UNSET
        elif self.condition is None:
            condition = None

        elif isinstance(self.condition, PresenceEventTriggerCondition):
            condition = UNSET
            if not isinstance(self.condition, Unset):
                condition = self.condition.to_dict()

        elif isinstance(self.condition, ThresholdEventTriggerCondition):
            condition = UNSET
            if not isinstance(self.condition, Unset):
                condition = self.condition.to_dict()

        elif isinstance(self.condition, RegexEventTriggerCondition):
            condition = UNSET
            if not isinstance(self.condition, Unset):
                condition = self.condition.to_dict()

        elif isinstance(self.condition, BitsetEventTriggerCondition):
            condition = UNSET
            if not isinstance(self.condition, Unset):
                condition = self.condition.to_dict()

        elif isinstance(self.condition, BatteryEventTriggerCondition):
            condition = UNSET
            if not isinstance(self.condition, Unset):
                condition = self.condition.to_dict()

        else:
            condition = UNSET
            if not isinstance(self.condition, Unset):
                condition = self.condition.to_dict()

        interval = self.interval
        severity: Union[Unset, str] = UNSET
        if not isinstance(self.severity, Unset):
            severity = self.severity.value

        enabled = self.enabled
        format_ = self.format_
        triggered_configuration: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.triggered_configuration, Unset):
            triggered_configuration = self.triggered_configuration.to_dict() if self.triggered_configuration else None

        tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict()

        sms_tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.sms_tags, Unset):
            sms_tags = self.sms_tags.to_dict()

        commands: Union[Unset, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.commands, Unset):
            commands = []
            for commands_item_data in self.commands:
                commands_item = commands_item_data.to_dict()

                commands.append(commands_item)

        notification_enabled = self.notification_enabled
        last_triggered_time: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_triggered_time, Unset):
            last_triggered_time = self.last_triggered_time.isoformat() if self.last_triggered_time else None

        stateful_trigger_configuration: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.stateful_trigger_configuration, Unset):
            stateful_trigger_configuration = (
                self.stateful_trigger_configuration.to_dict() if self.stateful_trigger_configuration else None
            )

        forwarding_configuration: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.forwarding_configuration, Unset):
            forwarding_configuration = (
                self.forwarding_configuration.to_dict() if self.forwarding_configuration else None
            )

        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if event_type is not UNSET:
            field_dict["eventType"] = event_type
        if message is not UNSET:
            field_dict["message"] = message
        if condition is not UNSET:
            field_dict["condition"] = condition
        if interval is not UNSET:
            field_dict["interval"] = interval
        if severity is not UNSET:
            field_dict["severity"] = severity
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if format_ is not UNSET:
            field_dict["format"] = format_
        if triggered_configuration is not UNSET:
            field_dict["triggeredConfiguration"] = triggered_configuration
        if tags is not UNSET:
            field_dict["tags"] = tags
        if sms_tags is not UNSET:
            field_dict["smsTags"] = sms_tags
        if commands is not UNSET:
            field_dict["commands"] = commands
        if notification_enabled is not UNSET:
            field_dict["notificationEnabled"] = notification_enabled
        if last_triggered_time is not UNSET:
            field_dict["lastTriggeredTime"] = last_triggered_time
        if stateful_trigger_configuration is not UNSET:
            field_dict["statefulTriggerConfiguration"] = stateful_trigger_configuration
        if forwarding_configuration is not UNSET:
            field_dict["forwardingConfiguration"] = forwarding_configuration
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.battery_event_trigger_condition import BatteryEventTriggerCondition
        from ..models.bitset_event_trigger_condition import BitsetEventTriggerCondition
        from ..models.event_trigger_command import EventTriggerCommand
        from ..models.forwarding_configuration import ForwardingConfiguration
        from ..models.numeric_set_event_trigger_condition import NumericSetEventTriggerCondition
        from ..models.partial_event_trigger_sms_tags import PartialEventTriggerSmsTags
        from ..models.partial_event_trigger_tags import PartialEventTriggerTags
        from ..models.presence_event_trigger_condition import PresenceEventTriggerCondition
        from ..models.regex_event_trigger_condition import RegexEventTriggerCondition
        from ..models.stateful_trigger_configuration import StatefulTriggerConfiguration
        from ..models.threshold_event_trigger_condition import ThresholdEventTriggerCondition
        from ..models.triggered_configuration import TriggeredConfiguration

        d = src_dict.copy()
        organization_id = d.pop("organizationId", UNSET)

        _event_type = d.pop("eventType", UNSET)
        event_type: Union[Unset, PartialEventTriggerEventType]
        if isinstance(_event_type, Unset):
            event_type = UNSET
        else:
            event_type = PartialEventTriggerEventType(_event_type)

        message = d.pop("message", UNSET)

        def _parse_condition(
            data: object,
        ) -> Union[
            "BatteryEventTriggerCondition",
            "BitsetEventTriggerCondition",
            "NumericSetEventTriggerCondition",
            "PresenceEventTriggerCondition",
            "RegexEventTriggerCondition",
            "ThresholdEventTriggerCondition",
            None,
            Unset,
        ]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _condition_type_0 = data
                condition_type_0: Union[Unset, PresenceEventTriggerCondition]
                if isinstance(_condition_type_0, Unset):
                    condition_type_0 = UNSET
                else:
                    condition_type_0 = PresenceEventTriggerCondition.from_dict(_condition_type_0)

                return condition_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _condition_type_1 = data
                condition_type_1: Union[Unset, ThresholdEventTriggerCondition]
                if isinstance(_condition_type_1, Unset):
                    condition_type_1 = UNSET
                else:
                    condition_type_1 = ThresholdEventTriggerCondition.from_dict(_condition_type_1)

                return condition_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _condition_type_2 = data
                condition_type_2: Union[Unset, RegexEventTriggerCondition]
                if isinstance(_condition_type_2, Unset):
                    condition_type_2 = UNSET
                else:
                    condition_type_2 = RegexEventTriggerCondition.from_dict(_condition_type_2)

                return condition_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _condition_type_3 = data
                condition_type_3: Union[Unset, BitsetEventTriggerCondition]
                if isinstance(_condition_type_3, Unset):
                    condition_type_3 = UNSET
                else:
                    condition_type_3 = BitsetEventTriggerCondition.from_dict(_condition_type_3)

                return condition_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                _condition_type_4 = data
                condition_type_4: Union[Unset, BatteryEventTriggerCondition]
                if isinstance(_condition_type_4, Unset):
                    condition_type_4 = UNSET
                else:
                    condition_type_4 = BatteryEventTriggerCondition.from_dict(_condition_type_4)

                return condition_type_4
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            _condition_type_5 = data
            condition_type_5: Union[Unset, NumericSetEventTriggerCondition]
            if isinstance(_condition_type_5, Unset):
                condition_type_5 = UNSET
            else:
                condition_type_5 = NumericSetEventTriggerCondition.from_dict(_condition_type_5)

            return condition_type_5

        condition = _parse_condition(d.pop("condition", UNSET))

        interval = d.pop("interval", UNSET)

        _severity = d.pop("severity", UNSET)
        severity: Union[Unset, PartialEventTriggerSeverity]
        if isinstance(_severity, Unset):
            severity = UNSET
        else:
            severity = PartialEventTriggerSeverity(_severity)

        enabled = d.pop("enabled", UNSET)

        format_ = d.pop("format", UNSET)

        _triggered_configuration = d.pop("triggeredConfiguration", UNSET)
        triggered_configuration: Union[Unset, None, TriggeredConfiguration]
        if _triggered_configuration is None:
            triggered_configuration = None
        elif isinstance(_triggered_configuration, Unset):
            triggered_configuration = UNSET
        else:
            triggered_configuration = TriggeredConfiguration.from_dict(_triggered_configuration)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, PartialEventTriggerTags]
        if isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = PartialEventTriggerTags.from_dict(_tags)

        _sms_tags = d.pop("smsTags", UNSET)
        sms_tags: Union[Unset, PartialEventTriggerSmsTags]
        if isinstance(_sms_tags, Unset):
            sms_tags = UNSET
        else:
            sms_tags = PartialEventTriggerSmsTags.from_dict(_sms_tags)

        commands = []
        _commands = d.pop("commands", UNSET)
        for commands_item_data in _commands or []:
            commands_item = EventTriggerCommand.from_dict(commands_item_data)

            commands.append(commands_item)

        notification_enabled = d.pop("notificationEnabled", UNSET)

        _last_triggered_time = d.pop("lastTriggeredTime", UNSET)
        last_triggered_time: Union[Unset, None, datetime.datetime]
        if _last_triggered_time is None:
            last_triggered_time = None
        elif isinstance(_last_triggered_time, Unset):
            last_triggered_time = UNSET
        else:
            last_triggered_time = isoparse(_last_triggered_time)

        _stateful_trigger_configuration = d.pop("statefulTriggerConfiguration", UNSET)
        stateful_trigger_configuration: Union[Unset, None, StatefulTriggerConfiguration]
        if _stateful_trigger_configuration is None:
            stateful_trigger_configuration = None
        elif isinstance(_stateful_trigger_configuration, Unset):
            stateful_trigger_configuration = UNSET
        else:
            stateful_trigger_configuration = StatefulTriggerConfiguration.from_dict(_stateful_trigger_configuration)

        _forwarding_configuration = d.pop("forwardingConfiguration", UNSET)
        forwarding_configuration: Union[Unset, None, ForwardingConfiguration]
        if _forwarding_configuration is None:
            forwarding_configuration = None
        elif isinstance(_forwarding_configuration, Unset):
            forwarding_configuration = UNSET
        else:
            forwarding_configuration = ForwardingConfiguration.from_dict(_forwarding_configuration)

        id = d.pop("id", UNSET)

        _created_at = d.pop("createdAt", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _updated_at = d.pop("updatedAt", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        partial_event_trigger = cls(
            organization_id=organization_id,
            event_type=event_type,
            message=message,
            condition=condition,
            interval=interval,
            severity=severity,
            enabled=enabled,
            format_=format_,
            triggered_configuration=triggered_configuration,
            tags=tags,
            sms_tags=sms_tags,
            commands=commands,
            notification_enabled=notification_enabled,
            last_triggered_time=last_triggered_time,
            stateful_trigger_configuration=stateful_trigger_configuration,
            forwarding_configuration=forwarding_configuration,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
        )

        partial_event_trigger.additional_properties = d
        return partial_event_trigger

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
