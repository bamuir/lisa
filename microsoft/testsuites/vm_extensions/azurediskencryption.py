# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import string
import os
from datetime import datetime, timezone
from typing import Any

from assertpy import assert_that

from lisa import (
    Logger,
    Node,
    TestCaseMetadata,
    TestSuite,
    TestSuiteMetadata,
    simple_requirement,
)
from lisa.operating_system import (
    SLES,
    BSD,
    CBLMariner,
    CentOs,
    Oracle,
    Posix,
    Redhat,
    Suse,
    Ubuntu,
)
from lisa.sut_orchestrator import AZURE
from lisa.sut_orchestrator.azure.common import (
    AzureNodeSchema,
    check_or_create_storage_account,
    get_node_context,
    get_or_create_storage_container,
    get_storage_credential,
)
from lisa.sut_orchestrator.azure.features import AzureExtension
from lisa.sut_orchestrator.azure.platform_ import AzurePlatform
from lisa.testsuite import TestResult
from lisa.util import SkippedException, generate_random_chars
@TestSuiteMetadata(
    area="vm_extension",
    category="functional",
    description="Test for the Azure Disk Encryption (ADE) extension",
    requirement=simple_requirement(
        supported_features=[AzureExtension],
        supported_platform_type=[AZURE],
        supported_os=[Ubuntu, CBLMariner, CentOs, Oracle, Redhat, SLES, Suse]
    ),
)
class AzureDiskEncryption(TestSuite):
    @TestCaseMetadata(
        description="""
        Runs the ADE extension and verifies it executed on the
        remote machine.
        """,
        priority=1,
        requirement=simple_requirement(supported_features=[AzureExtension]),
    )
    def verify_azure_disk_encryption(
        self, log: Logger, node: Node, result: TestResult
    ) -> None:
      
        log.debug("Environment setup")
        environment = result.environment
        assert environment, "fail to get environment from testresult"
        platform = environment.platform
        assert isinstance(platform, AzurePlatform)

        # VM attributes
        node_context = get_node_context(node)
        resource_group_name = node_context.resource_group_name
        node_capability = node.capability.get_extended_runbook(AzureNodeSchema, AZURE)
        location = node_capability.location

        # get user tenant id for KV creation
        user_tenant_id = os.environ.get("tenant_id")
        if user_tenant_id is None:
            raise ValueError("Environment variable 'tenant_id' is not set.")
        
        log.debug(f"User tenant ID: {user_tenant_id}")

        