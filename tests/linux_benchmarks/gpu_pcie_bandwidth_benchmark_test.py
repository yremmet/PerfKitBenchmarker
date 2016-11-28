# Copyright 2016 PerfKitBenchmarker Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests for GPU PCIe bandwidth benchmark."""
import os
import unittest

import mock

from perfkitbenchmarker.linux_benchmarks import gpu_pcie_bandwidth_benchmark


class GpuBandwidthTestCase(unittest.TestCase):

  def setUp(self):
    p = mock.patch(gpu_pcie_bandwidth_benchmark.__name__ + '.FLAGS')
    p.start()
    self.addCleanup(p.stop)

    path = os.path.join(os.path.dirname(__file__), '../data',
                        'cuda_bandwidth_test_results.txt')
    with open(path) as fp:
      self.contents = fp.read()

  def testParseHpcc(self):
    result = gpu_pcie_bandwidth_benchmark.ParseOutput(self.contents)
    self.assertEqual(3, len(result))
    results = {i[0]: i[1] for i in result}

    self.assertAlmostEqual(9254.7, results['Host to device bandwidth'])
    self.assertAlmostEqual(9686.1, results['Device to host bandwidth'])
    self.assertAlmostEqual(155985.8, results['Device to device bandwidth'])

if __name__ == '__main__':
  unittest.main()
