# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from dataclasses import InitVar, dataclass, field
from typing import Dict, List, Optional

from dataclasses_json import dataclass_json
from marshmallow import validate

from lisa import schema
from lisa.environment import Environment
from lisa.node import Node
from lisa.util import LisaException, constants, field_metadata


@dataclass
class EnvironmentContext:
    key_pair_name: str = ""
    security_group_name: str = ""
    security_group_id: str = ""
    security_group_is_created: bool = False


@dataclass
class NodeContext:
    ip_address: str = ""
    username: str = ""
    password: str = ""
    private_key_file: str = ""


def get_node_context(node: Node) -> NodeContext:
    return node.get_context(NodeContext)


def get_environment_context(environment: Environment) -> EnvironmentContext:
    return environment.get_context(EnvironmentContext)
