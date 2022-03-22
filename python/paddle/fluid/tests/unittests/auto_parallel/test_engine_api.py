# Copyright (c) 2022 PaddlePaddle Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import os
import sys
import shutil
import subprocess
from paddle.distributed.fleet.launch_utils import run_with_coverage


class TestEngineAPI(unittest.TestCase):
    def test_engine_api(self):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        launch_model_path = os.path.join(file_dir, "engine_api.py")

        if os.environ.get("WITH_COVERAGE", "OFF") == "ON":
            coverage_args = ["-m", "coverage", "run", "--branch", "-p"]
        else:
            coverage_args = []

        cmd = [sys.executable, "-u"] + coverage_args + [
            "-m", "launch", "--gpus", "0,1", launch_model_path
        ]

        process = subprocess.Popen(cmd)
        process.wait()
        self.assertEqual(process.returncode, 0)

        # Remove unnecessary files
        log_path = os.path.join(file_dir, "log")
        if os.path.exists(log_path):
            shutil.rmtree(log_path)


if __name__ == "__main__":
    unittest.main()
