import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.task_summary_stream_type import TaskSummaryStreamType
from ..models.task_summary_type import TaskSummaryType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.task_summary_tags import TaskSummaryTags


T = TypeVar("T", bound="TaskSummary")


@attr.s(auto_attribs=True)
class TaskSummary:
    """
    Attributes:
        task_summary_format_id (str):
        report (Any):
        task_id (str):
        generated_at (datetime.datetime):
        time (datetime.datetime):
        type (Union[Unset, TaskSummaryType]):
        end_time (Union[Unset, None, datetime.datetime]):
        deleted_at (Union[Unset, None, datetime.datetime]):
        id (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        updated_at (Union[Unset, datetime.datetime]):
        organization_id (Union[Unset, str]):
        message (Union[Unset, str]):
        viewed (Union[Unset, bool]):
        device_id (Union[Unset, None, str]):
        stream_name (Union[Unset, None, str]):
        stream_type (Union[Unset, None, TaskSummaryStreamType]):
        tags (Union[Unset, None, TaskSummaryTags]):
        notification_enabled (Union[Unset, bool]):
    """

    task_summary_format_id: str
    report: Any
    task_id: str
    generated_at: datetime.datetime
    time: datetime.datetime
    type: Union[Unset, TaskSummaryType] = UNSET
    end_time: Union[Unset, None, datetime.datetime] = UNSET
    deleted_at: Union[Unset, None, datetime.datetime] = UNSET
    id: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    organization_id: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    viewed: Union[Unset, bool] = UNSET
    device_id: Union[Unset, None, str] = UNSET
    stream_name: Union[Unset, None, str] = UNSET
    stream_type: Union[Unset, None, TaskSummaryStreamType] = UNSET
    tags: Union[Unset, None, "TaskSummaryTags"] = UNSET
    notification_enabled: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        task_summary_format_id = self.task_summary_format_id
        report = self.report
        task_id = self.task_id
        generated_at = self.generated_at.isoformat()

        time = self.time.isoformat()

        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        end_time: Union[Unset, None, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat() if self.end_time else None

        deleted_at: Union[Unset, None, str] = UNSET
        if not isinstance(self.deleted_at, Unset):
            deleted_at = self.deleted_at.isoformat() if self.deleted_at else None

        id = self.id
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        organization_id = self.organization_id
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

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "taskSummaryFormatId": task_summary_format_id,
                "report": report,
                "taskId": task_id,
                "generatedAt": generated_at,
                "time": time,
            }
        )
        if type is not UNSET:
            field_dict["type"] = type
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if deleted_at is not UNSET:
            field_dict["deletedAt"] = deleted_at
        if id is not UNSET:
            field_dict["id"] = id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if updated_at is not UNSET:
            field_dict["updatedAt"] = updated_at
        if organization_id is not UNSET:
            field_dict["organizationId"] = organization_id
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

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.task_summary_tags import TaskSummaryTags

        d = src_dict.copy()
        task_summary_format_id = d.pop("taskSummaryFormatId")

        report = d.pop("report")

        task_id = d.pop("taskId")

        generated_at = isoparse(d.pop("generatedAt"))

        time = isoparse(d.pop("time"))

        _type = d.pop("type", UNSET)
        type: Union[Unset, TaskSummaryType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = TaskSummaryType(_type)

        _end_time = d.pop("endTime", UNSET)
        end_time: Union[Unset, None, datetime.datetime]
        if _end_time is None:
            end_time = None
        elif isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = isoparse(_end_time)

        _deleted_at = d.pop("deletedAt", UNSET)
        deleted_at: Union[Unset, None, datetime.datetime]
        if _deleted_at is None:
            deleted_at = None
        elif isinstance(_deleted_at, Unset):
            deleted_at = UNSET
        else:
            deleted_at = isoparse(_deleted_at)

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

        message = d.pop("message", UNSET)

        viewed = d.pop("viewed", UNSET)

        device_id = d.pop("deviceId", UNSET)

        stream_name = d.pop("streamName", UNSET)

        _stream_type = d.pop("streamType", UNSET)
        stream_type: Union[Unset, None, TaskSummaryStreamType]
        if _stream_type is None:
            stream_type = None
        elif isinstance(_stream_type, Unset):
            stream_type = UNSET
        else:
            stream_type = TaskSummaryStreamType(_stream_type)

        _tags = d.pop("tags", UNSET)
        tags: Union[Unset, None, TaskSummaryTags]
        if _tags is None:
            tags = None
        elif isinstance(_tags, Unset):
            tags = UNSET
        else:
            tags = TaskSummaryTags.from_dict(_tags)

        notification_enabled = d.pop("notificationEnabled", UNSET)

        task_summary = cls(
            task_summary_format_id=task_summary_format_id,
            report=report,
            task_id=task_id,
            generated_at=generated_at,
            time=time,
            type=type,
            end_time=end_time,
            deleted_at=deleted_at,
            id=id,
            created_at=created_at,
            updated_at=updated_at,
            organization_id=organization_id,
            message=message,
            viewed=viewed,
            device_id=device_id,
            stream_name=stream_name,
            stream_type=stream_type,
            tags=tags,
            notification_enabled=notification_enabled,
        )

        task_summary.additional_properties = d
        return task_summary

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
