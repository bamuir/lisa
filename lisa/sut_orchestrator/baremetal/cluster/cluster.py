# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from dataclasses import dataclass, field
from functools import partial
from typing import Any, List, Type, Optional

from dataclasses_json import dataclass_json
from lisa.parameter_parser.runbook import RunbookBuilder

from lisa.util.subclasses import Factory
from lisa import schema
from lisa.util import InitializableMixin, field_metadata, subclasses
from lisa.util.logger import get_logger
from lisa.sut_orchestrator.baremetal.build.build import (
    BuildSchema,
)
from lisa.sut_orchestrator.baremetal.build.build import Build


@dataclass_json()
@dataclass
class ClusterSchema(schema.TypedSchema, schema.ExtendableSchemaMixin):
    type: str = field(default="rackmanager", metadata=field_metadata(required=True))
    build: Optional[BuildSchema] = None


class Cluster(subclasses.BaseClassWithRunbookMixin, InitializableMixin):
    def __init__(
        self,
        runbook: ClusterSchema,
    ) -> None:
        super().__init__(runbook=runbook)
        self.cluster_runbook: ClusterSchema = self.runbook
        self._log = get_logger("cluster", self.__class__.__name__)

    def initialize(self, *args: Any, **kwargs: Any) -> None:
        source_path = kwargs.pop("source_path")
        build_factory = Factory[Build](Build)
        build = build_factory.create_by_runbook(self.cluster_runbook.build)
        build.initialize(
            source_path=source_path, files=self.cluster_runbook.build.files
        )

    @classmethod
    def type_name(cls) -> str:
        return "cluster"

    @classmethod
    def type_schema(cls) -> Type[schema.TypedSchema]:
        return ClusterSchema
