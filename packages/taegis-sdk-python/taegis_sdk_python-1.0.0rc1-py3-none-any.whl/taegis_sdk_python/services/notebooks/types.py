"""Notebooks Types and Enums."""
# pylint: disable=no-member, unused-argument, too-many-locals, duplicate-code

# Autogenerated
# DO NOT MODIFY

from typing import Optional, List, Dict, Union, Any, Tuple


from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config


@dataclass_json
@dataclass(order=True, eq=True, frozen=True)
class Notebook:
    """Notebook."""

    id: Optional[str] = field(default=None, metadata=config(field_name="id"))
    status: Optional[str] = field(default=None, metadata=config(field_name="status"))
    failure_reason: Optional[str] = field(
        default=None, metadata=config(field_name="failureReason")
    )
    instance_type: Optional[str] = field(
        default=None, metadata=config(field_name="instanceType")
    )
    url: Optional[str] = field(default=None, metadata=config(field_name="url"))
    created_at: Optional[str] = field(
        default=None, metadata=config(field_name="createdAt")
    )
    updated_at: Optional[str] = field(
        default=None, metadata=config(field_name="updatedAt")
    )
