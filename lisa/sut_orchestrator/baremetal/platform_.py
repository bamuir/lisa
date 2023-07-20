# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from dataclasses import dataclass, field
from typing import Any, List, Optional
import re
from dataclasses_json import dataclass_json

from lisa import RemoteNode, schema
from lisa.environment import Environment
from lisa.platform_ import Platform
from lisa.schema import Node
from lisa.sut_orchestrator.baremetal.build.source import Source, SourceSchema
from lisa.sut_orchestrator.baremetal.cluster.cluster import Cluster, ClusterSchema
from lisa.util import fields_to_dict
from lisa.util.shell import try_connect
from lisa.util.subclasses import Factory

from .. import BAREMETAL
from .common import get_environment_context, get_node_context
import os
import glob


@dataclass_json()
@dataclass
class SourceBuildSchema:
    source: Optional[SourceSchema] = None


@dataclass_json()
@dataclass
class BareMetalPlatformSchema:
    build: Optional[SourceBuildSchema] = field(default=None)
    cluster: Optional[List[ClusterSchema]] = field(default=None)


class BareMetalPlatform(Platform):
    def __init__(
        self,
        runbook: schema.Platform,
    ) -> None:
        super().__init__(runbook=runbook)

    @classmethod
    def type_name(cls) -> str:
        return BAREMETAL

    def _initialize(self, *args: Any, **kwargs: Any) -> None:
        # set needed environment variables for authentication
        baremetal_runbook: BareMetalPlatformSchema = self.runbook.get_extended_runbook(
            BareMetalPlatformSchema
        )
        assert baremetal_runbook, "platform runbook cannot be empty"
        self._baremetal_runbook = baremetal_runbook

        if baremetal_runbook.build and baremetal_runbook.build.source:
            source_factory = Factory[Source](Source)
            source = source_factory.create_by_runbook(baremetal_runbook.build.source)
            self._log.debug(f"found build '{source.type_name()}', to expand runbook.")
            source.initialize()

        cluster_factory = Factory[Cluster](Cluster)
        for cluster in baremetal_runbook.cluster:
            cluster_runbook = cluster_factory.create_by_runbook(cluster)
            cluster_runbook.initialize(source_path=source.source_path)

        # import spur
        # import spur.ssh

        # try:
        #     shell = spur.SshShell(
        #         hostname="",
        #         port=22,
        #         username="",
        #         password="",
        #         shell_type=spur.ssh.ShellTypes.minimal,
        #         missing_host_key=spur.ssh.MissingHostKey.accept,
        #     )
        #     with shell:
        #         result = shell.run(["sh", "help"])
        #         print(result)
        # except spur.ssh.ConnectionError as error:
        #     print(error.original_traceback)
        #     raise
        connection_info = schema.ConnectionInfo(
            address="",
            port=22,
            username="",
            password="",
        )

        nested_vm = RemoteNode(Node(name="name"), 0, "name")
        nested_vm.set_connection_info(
            public_port=22,
            **fields_to_dict(
                connection_info, ["address", "port", "username", "password"]
            ),
        )

        # wait for nested vm ssh connection to be ready
        try_connect(connection_info)
        nested_vm.execute("ls")
        # import paramiko

        # ssh = paramiko.SSHClient()
        # ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # ssh.connect(
        #     hostname="",
        #     username="",
        #     password="",
        #     port=22,
        #     # look_for_keys=False,
        #     # allow_agent=False,
        #     banner_timeout=200,
        #     auth_timeout=200,
        #     timeout=200,
        # )

        # stdin, stdout, stderr = ssh.exec_command("help")

        # print(stdout.read().decode())

    # def deploy_environment(self, environment: Environment, log: Logger) -> None:
    #     environment_context = get_environment_context(environment=environment)
