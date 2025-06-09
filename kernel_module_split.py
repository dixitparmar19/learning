# SPDX-License-Identifier: MIT

import os
from oeqa.selftest.case import OESelftestTestCase
from oeqa.utils.commands import bitbake, get_bb_var

class KernelSplitAutoloadTest(OESelftestTestCase):
    """
    Tests to verify the effect of KERNEL_SPLIT_MODULES on autoload config file creation
    """

    image = "core-image-minimal"
    autoload_file = "etc/modules-load.d/hello.conf"

    def setUp(self):
        """
        Apply shared configuration for kernel modules and autoload
        """
        super().setUp()
        shared_config = f'''
IMAGE_INSTALL:append = " kernel-module-hello"
KERNEL_MODULE_AUTOLOAD:append = " hello"
'''
        self.append_config(shared_config)

    def _run_test_with_split_modules(self, enable_split):
        """
        Common logic for both enable/disable tests
        """
        split_value = "1" if enable_split else "0"
        self.append_config(f'KERNEL_SPLIT_MODULES = "{split_value}"')

        # Build the image
        bitbake(self.image)

        # Get path to rootfs
        rootfs_path = get_bb_var("IMAGE_ROOTFS", self.image)
        autoload_path = os.path.join(rootfs_path, self.autoload_file)

        # Check for existence or absence of the autoload file
        self.assertTrue(
            os.path.exists(autoload_path),
            f"Autoload config file should exist at {autoload_path} incase of KERNEL_SPLIT_MODULES is enabled or disabled"
        )

    def test_split_modules_enabled(self):
        """
        Test with KERNEL_SPLIT_MODULES enabled — autoload file should exist
        """
        self._run_test_with_split_modules(enable_split=True)

    def test_split_modules_disabled(self):
        """
        Test with KERNEL_SPLIT_MODULES disabled — autoload file should not exist
        """
        self._run_test_with_split_modules(enable_split=False)

    def tearDown(self):
        """
        Clean up all config changes
        """
        super().tearDown()

