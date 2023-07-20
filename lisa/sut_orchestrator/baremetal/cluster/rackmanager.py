# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from dataclasses import dataclass
from typing import Any, Type

from dataclasses_json import dataclass_json

from lisa import schema
from lisa.sut_orchestrator.baremetal.cluster.cluster import Cluster, ClusterSchema


@dataclass_json()
@dataclass
class RackManagerSchema(ClusterSchema):
    address: str = ""
    username: str = ""
    password: str = ""


class RackManager(Cluster):
    def __init__(self, runbook: ClusterSchema) -> None:
        super().__init__(runbook)
        self.rm_runbook: ClusterSchema = self.runbook

    @classmethod
    def type_name(cls) -> str:
        return "rackmanager"

    @classmethod
    def type_schema(cls) -> Type[schema.TypedSchema]:
        return RackManagerSchema

    def _initialize(self, *args: Any, **kwargs: Any) -> None:
        print("rackmanager")

    def initialize(self, *args: Any, **kwargs: Any) -> None:
        super().initialize(*args, **kwargs)
        print("cluster")
