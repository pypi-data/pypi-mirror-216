import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.event_trigger_event_type import EventTriggerEventType
from ..models.event_trigger_severity import EventTriggerSeverity
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.battery_event_trigger_condition import BatteryEventTriggerCondition
    from ..models.bitset_event_trigger_condition import BitsetEventTriggerCondition
    from ..models.event_trigger_command import EventTriggerCommand
    from ..models.event_trigger_sms_tags import EventTriggerSmsTags
    from ..models.event_trigger_tags import EventTriggerTags
    from ..models.forwarding_configuration import ForwardingConfiguration
    from ..models.numeric_set_event_trigger_condition import NumericSetEventTriggerCondition
    from ..models.presence_event_trigger_condition import PresenceEventTriggerCondition
    from ..models.regex_event_trigger_condition import RegexEventTriggerCondition
    from ..models.stateful_trigger_configuration import StatefulTriggerConfiguration
    from ..models.threshold_event_trigger_condition import ThresholdEventTriggerCondition
    from ..models.triggered_configuration import TriggeredConfiguration


T = TypeVar("T", bound="EventTrigger")


@attr.s(auto_attribs=True)
class EventTrigger:
    """
    Attributes:
        event_type (EventTriggerEventType):
        message (str):
        interval (int):
        severity (EventTriggerSeverity):
        tags (EventTriggerTags):
        commands (List['EventTriggerCommand']):
        notification_enabled (bool):
        organization_id (Union[Unset, str]):
        condition (Union['BatteryEventTriggerCondition', 'BitsetEventTriggerCondition',
            'NumericSetEventTriggerCondition', 'PresenceEventTriggerCondition', 'RegexEventTriggerCondition',
            'ThresholdEventTriggerCondition', None]):
        enabled (Union[Unset, bool]):
        format_ (Union[Unset, str]):
        triggered_configuration (Optional[TriggeredConfiguration]):
        sms_tags (Union[Unset, EventTriggerSmsTags]):
        last_triggered_time (Union[Unset, None, datetime.datetime]):
        stateful_trigger_configuration (Optional[StatefulTriggerConfiguration]):
        forwarding_configuration (Optional[ForwardingConfiguration]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
    """

    event_type: EventTriggerEventType
    message: str
    interval: int
    severity: EventTriggerSeverity
    tags: "EventTriggerTags"
    commands: List["EventTriggerCommand"]
    notification_enabled: bool
    condition: Union[
        "BatteryEventTriggerCondition",
        "BitsetEventTriggerCondition",
        "NumericSetEventTriggerCondition",
        "PresenceEventTriggerCondition",
        "RegexEventTriggerCondition",
        "ThresholdEventTriggerCondition",
        None,
    ]
    triggered_configuration: Optional["TriggeredConfiguration"]
    stateful_trigger_configuration: Optional["StatefulTriggerConfiguration"]
    forwarding_configuration: Optional["ForwardingConfiguration"]
    organization_id: Union[Unset, str] = UNSET
    enabled: Union[Unset, bool] = UNSET
    format_: Union[Unset, str] = UNSET
    sms_tags: Union[Unset, "EventTriggerSmsTags"] = UNSET
    last_triggered_time: Union[Unset, None, datetime.datetime] = UNSET
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

        event_type = self.event_type.value

        message = self.message
        interval = self.interval
        severity = self.severity.value

        tags = self.tags.to_dict()

        commands = []
        for commands_item_data in self.commands:
            commands_item = commands_item_data.to_dict()

            commands.append(commands_item)

        notification_enabled = self.notification_enabled
        organization_id = self.organization_id
        condition: Union[Dict[str, Any], None]
        if self.condition is None:
            condition = None

        elif isinstance(self.condition, PresenceEventTriggerCondition):
            condition = self.condition.to_dict()

        elif isinstance(self.condition, ThresholdEventTriggerCondition):
            condition = self.condition.to_dict()

        elif isinstance(self.condition, RegexEventTriggerCondition):
            condition = self.condition.to_dict()

        elif isinstance(self.condition, BitsetEventTriggerCondition):
            condition = self.condition.to_dict()

        elif isinstance(self.condition, BatteryEventTriggerCondition):
            condition = self.condition.to_dict()

        else:
            condition = self.condition.to_dict()

        enabled = self.enabled
        format_ = self.format_
        triggered_configuration = self.triggered_configuration.to_dict() if self.triggered_configuration else None

        sms_tags: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.sms_tags, Unset):
            sms_tags = self.sms_tags.to_dict()

        last_triggered_time: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_triggered_time, Unset):
            last_triggered_time = self.last_triggered_time.isoformat() if self.last_triggered_time else None

        stateful_trigger_configuration = (
            self.stateful_trigger_configuration.to_dict() if self.stateful_trigger_configuration else None
        )

        forwarding_configuration = self.forwarding_configuration.to_dict() if self.forwarding_configuration else None

        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "eventType": event_type,
                "message": message,
                "interval": interval,
                "severity": severity,
                "tags": tags,
                "commands": commands,
                "notificationEnabled": notification_enabled,
                "condition": condition,
                "triggeredConfiguration": triggered_configuration,
                "statefulTriggerConfiguration": stateful_trigger_configuration,
                "forwardingConfiguration": forwarding_configuration,
            }
        )
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if format_ is not UNSET:
            field_dict["format"] = format_
        if sms_tags is not UNSET:
            field_dict["smsTags"] = sms_tags
        if last_triggered_time is not UNSET:
            field_dict["lastTriggeredTime"] = last_triggered_time
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
        from ..models.event_trigger_sms_tags import EventTriggerSmsTags
        from ..models.event_trigger_tags import EventTriggerTags
        from ..models.forwarding_configuration import ForwardingConfiguration
        from ..models.numeric_set_event_trigger_condition import NumericSetEventTriggerCondition
        from ..models.presence_event_trigger_condition import PresenceEventTriggerCondition
        from ..models.regex_event_trigger_condition import RegexEventTriggerCondition
        from ..models.stateful_trigger_configuration import StatefulTriggerConfiguration
        from ..models.threshold_event_trigger_condition import ThresholdEventTriggerCondition
        from ..models.triggered_configuration import TriggeredConfiguration

        d = src_dict.copy()
        event_type = EventTriggerEventType(d.pop("eventType"))

        message = d.pop("message")

        interval = d.pop("interval")

        severity = EventTriggerSeverity(d.pop("severity"))

        tags = EventTriggerTags.from_dict(d.pop("tags"))

        commands = []
        _commands = d.pop("commands")
        for commands_item_data in _commands:
            commands_item = EventTriggerCommand.from_dict(commands_item_data)

            commands.append(commands_item)

        notification_enabled = d.pop("notificationEnabled")

        organization_id = d.pop("organizationId", UNSET)

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
        ]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                condition_type_0 = PresenceEventTriggerCondition.from_dict(data)

                return condition_type_0
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                condition_type_1 = ThresholdEventTriggerCondition.from_dict(data)

                return condition_type_1
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                condition_type_2 = RegexEventTriggerCondition.from_dict(data)

                return condition_type_2
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                condition_type_3 = BitsetEventTriggerCondition.from_dict(data)

                return condition_type_3
            except:  # noqa: E722
                pass
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                condition_type_4 = BatteryEventTriggerCondition.from_dict(data)

                return condition_type_4
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            condition_type_5 = NumericSetEventTriggerCondition.from_dict(data)

            return condition_type_5

        condition = _parse_condition(d.pop("condition"))

        enabled = d.pop("enabled", UNSET)

        format_ = d.pop("format", UNSET)

        _triggered_configuration = d.pop("triggeredConfiguration")
        triggered_configuration: Optional[TriggeredConfiguration]
        if _triggered_configuration is None:
            triggered_configuration = None
        else:
            triggered_configuration = TriggeredConfiguration.from_dict(_triggered_configuration)

        _sms_tags = d.pop("smsTags", UNSET)
        sms_tags: Union[Unset, EventTriggerSmsTags]
        if isinstance(_sms_tags, Unset):
            sms_tags = UNSET
        else:
            sms_tags = EventTriggerSmsTags.from_dict(_sms_tags)

        _last_triggered_time = d.pop("lastTriggeredTime", UNSET)
        last_triggered_time: Union[Unset, None, datetime.datetime]
        if _last_triggered_time is None:
            last_triggered_time = None
        elif isinstance(_last_triggered_time, Unset):
            last_triggered_time = UNSET
        else:
            last_triggered_time = isoparse(_last_triggered_time)

        _stateful_trigger_configuration = d.pop("statefulTriggerConfiguration")
        stateful_trigger_configuration: Optional[StatefulTriggerConfiguration]
        if _stateful_trigger_configuration is None:
            stateful_trigger_configuration = None
        else:
            stateful_trigger_configuration = StatefulTriggerConfiguration.from_dict(_stateful_trigger_configuration)

        _forwarding_configuration = d.pop("forwardingConfiguration")
        forwarding_configuration: Optional[ForwardingConfiguration]
        if _forwarding_configuration is None:
            forwarding_configuration = None
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

        event_trigger = cls(
            event_type=event_type,
            message=message,
            interval=interval,
            severity=severity,
            tags=tags,
            commands=commands,
            notification_enabled=notification_enabled,
            organization_id=organization_id,
            condition=condition,
            enabled=enabled,
            format_=format_,
            triggered_configuration=triggered_configuration,
            sms_tags=sms_tags,
            last_triggered_time=last_triggered_time,
            stateful_trigger_configuration=stateful_trigger_configuration,
            forwarding_configuration=forwarding_configuration,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
        )

        event_trigger.additional_properties = d
        return event_trigger

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
