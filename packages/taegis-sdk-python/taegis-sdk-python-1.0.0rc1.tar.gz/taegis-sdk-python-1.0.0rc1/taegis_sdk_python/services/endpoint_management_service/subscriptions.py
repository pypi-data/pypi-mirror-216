"""EndpointManagementService Subscription."""
# pylint: disable=no-member, unused-argument, too-many-locals, duplicate-code, wildcard-import, unused-wildcard-import, cyclic-import


# Autogenerated
# DO NOT MODIFY

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

from taegis_sdk_python import GraphQLNoRowsInResultSetError
from taegis_sdk_python.utils import (
    build_output_string,
    parse_union_result,
    prepare_input,
)
from taegis_sdk_python.services.endpoint_management_service.types import *

if TYPE_CHECKING:  # pragma: no cover
    from taegis_sdk_python.services.endpoint_management_service import (
        EndpointManagementServiceService,
    )

log = logging.getLogger(__name__)


class TaegisSDKEndpointManagementServiceSubscription:
    """Teagis Endpoint_management_service Subscription operations."""

    def __init__(self, service: EndpointManagementServiceService):
        self.service = service
