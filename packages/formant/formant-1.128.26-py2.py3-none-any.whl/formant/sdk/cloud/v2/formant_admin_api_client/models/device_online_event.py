import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.device_online_event_severity import DeviceOnlineEventSeverity
from ..models.device_online_event_stream_type import DeviceOnlineEventStreamType
from ..models.device_online_event_type import DeviceOnlineEventType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.device_online_event_tags import DeviceOnlineEventTags


T = TypeVar("T", bound="DeviceOnlineEvent")


@attr.s(auto_attribs=True)
class DeviceOnlineEvent:
    """
    Attributes:
        time (datetime.datetime):
        severity (DeviceOnlineEventSeverity):
        event_trigger_id (str):
        interval (int):
        type (Union[Unset, DeviceOnlineEventType]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        organization_id (Union[Unset, str]):
        end_time (Union[Unset, None, datetime.datetime]):
        message (Union[Unset, str]):
        viewed (Union[Unset, bool]):
        device_id (Union[Unset, None, str]):
        stream_name (Union[Unset, None, str]):
        stream_type (Union[Unset, None, DeviceOnlineEventStreamType]):
        tags (Union[Unset, None, DeviceOnlineEventTags]):
        notification_enabled (Union[Unset, bool]):
        interval_start (Union[Unset, datetime.datetime]):
    """

    time: datetime.datetime
    severity: DeviceOnlineEventSeverity
    event_trigger_id: str
    interval: int
    type: Union[Unset, DeviceOnlineEventType] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    organization_id: Union[Unset, str] = UNSET
    end_time: Union[Unset, None, datetime.datetime] = UNSET
    message: Union[Unset, str] = UNSET
    viewed: Union[Unset, bool] = UNSET
    device_id: Union[Unset, None, str] = UNSET
    stream_name: Union[Unset, None, str] = UNSET
    stream_type: Union[Unset, None, DeviceOnlineEventStreamType] = UNSET
    tags: Union[Unset, None, "DeviceOnlineEventTags"] = UNSET
    notification_enabled: Union[Unset, bool] = UNSET
    interval_start: Union[Unset, datetime.datetime] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        time = self.time.isoformat()

        severity = self.severity.value

        event_trigger_id = self.event_trigger_id
        interval = self.interval
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        organization_id = self.organization_id
        end_time: Union[Unset, None, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat() if self.end_time else None

        message = self.message
        viewed = self.viewed
        device_id = self.device_id
        stream_name = self.stream_name
        stream_type: Union[Unset, None, str] = UNSET
        if not isinstance(self.stream_type, Unset):
            stream_type = self.stream_type.value if self.stream_type else None

        tags: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.tags, Unset):
            tags = self.tags.to_dict() if self.tags else None

        notification_enabled = self.notification_enabled
        interval_start: Union[Unset, str] = UNSET
        if not isinstance(self.interval_start, Unset):
            interval_start = self.interval_start.isoformat()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "time": time,
                "severity": severity,
                "eventTriggerId": event_trigger_id,
                "interval": interval,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if message is not UNSET:
            field_dict["message"] = message
        if viewed is not UNSET:
            field_dict["viewed"] = viewed
        if device_id is not UNSET:
            field_dict["deviceId"] = device_id
        if stream_name is not UNSET:
            field_dict["streamName"] = stream_name
        if stream_type is not UNSET:
            field_dict["streamType"] = stream_type
        if tags is not UNSET:
            field_dict["tags"] = tags
        if notification_enabled is not UNSET:
            field_dict["notificationEnabled"] = notification_enabled
        if interval_start is not UNSET:
            field_dict["intervalStart"] = interval_start

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.device_online_event_tags import DeviceOnlineEventTags

        d = src_dict.copy()
        time = isoparse(d.pop("time"))

        severity = DeviceOnlineEventSeverity(d.pop("severity"))

        event_trigger_id = d.pop("eventTriggerId")

        interval = d.pop("interval")

        _type = d.pop("type", UNSET)
        type: Union[Unset, DeviceOnlineEventType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = DeviceOnlineEventType(_type)

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

        organization_id = d.pop("organizationId", UNSET)

        _end_time = d.pop("endTime", UNSET)
        end_time: Union[Unset, None, datetime.datetime]
        if _end_time is None:
            end_time = None
        elif isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = isoparse(_end_time)

        message = d.pop("message", UNSET)

        viewed = d.pop("viewed", UNSET)

        device_id = d.pop("deviceId", UNSET)

        stream_name = d.pop("streamName", UNSET)

        _stream_type = d.pop("streamType", UNSET)
        stream_type: Union[Unset, None, DeviceOnlineEventStreamType]
        if _stream_type is None:
            stream_type = None
        elif isinstance(_stream_type, Unset):
            stream_type = UNSET
        else:
            stream_type = DeviceOnlineEventStreamType(_stream_type)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, None, DeviceOnlineEventTags]
        if _tags is None:
            tags = None
        elif isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = DeviceOnlineEventTags.from_dict(_tags)

        notification_enabled = d.pop("notificationEnabled", UNSET)

        _interval_start = d.pop("intervalStart", UNSET)
        interval_start: Union[Unset, datetime.datetime]
        if isinstance(_interval_start, Unset):
            interval_start = UNSET
        else:
            interval_start = isoparse(_interval_start)

        device_online_event = cls(
            time=time,
            severity=severity,
            event_trigger_id=event_trigger_id,
            interval=interval,
            type=type,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            organization_id=organization_id,
            end_time=end_time,
            message=message,
            viewed=viewed,
            device_id=device_id,
            stream_name=stream_name,
            stream_type=stream_type,
            tags=tags,
            notification_enabled=notification_enabled,
            interval_start=interval_start,
        )

        device_online_event.additional_properties = d
        return device_online_event

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
