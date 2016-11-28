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


"""Module containing CUDA toolkit 8 installation and cleanup functions."""


# CUDA_TOOLKIT_UBUNTU = 'cuda-repo-ubuntu1604_8.0.44-1_amd64.deb'
# CUDA_TOOLKIT_UBUNTU_URL = 'http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/%s' % CUDA_TOOLKIT_UBUNTU
CUDA_TOOLKIT_UBUNTU = 'cuda-repo-ubuntu1604-8-0-local_8.0.44-1_amd64.deb'
CUDA_TOOLKIT_UBUNTU_URL = 'https://storage.googleapis.com/p3rf-gpu-benchmark-dependencies/%s' % CUDA_TOOLKIT_UBUNTU
CUDA_TOOLKIT_INSTALL_DIR = '/usr/local/cuda'


def _MaximizeGPUClockSpeed(vm):
  vm.RemoteCommand('sudo nvidia-smi -pm 1')
  vm.RemoteCommand('sudo nvidia-smi -ac 2505,875')  # TODO: Currently specific to K80 GPUs


def _Install(vm):
  """Installs CUDA toolkit 8 on the VM."""
  vm.Install('build_tools')
  vm.Install('wget')
  wget_command = 'wget %s'
  vm.RemoteCommand(wget_command % CUDA_TOOLKIT_UBUNTU_URL)
  install_command = ('sudo dpkg -i %s')
  vm.RemoteCommand(install_command % (CUDA_TOOLKIT_UBUNTU))
  vm.RemoteCommand('sudo apt-get update')
  vm.RobustRemoteCommand('sudo apt-get install -y cuda')
  vm.RemoteCommand('sudo reboot', ignore_failure=True)
  vm.WaitForBootCompletion()
  _MaximizeGPUClockSpeed(vm)


def AptInstall(vm):
  """Installs the CUDA toolkit 8 on the VM."""
  _Install(vm)


def YumInstall(vm):
  """Installs the CUDA toolkit 8 on the VM."""
  raise NotImplemented()


def CheckPrerequisites():
  """Verifies that the required resources are present.

  Raises:
    perfkitbenchmarker.data.ResourceNotFound: On missing resource.
  """
  pass


def Uninstall(vm):
  """Removes the CUDA toolkit.
     Note that reinstallation does not work correctly, i.e. you cannot reinstall 
     CUDA by calling _Install() again.
  """
  vm.RemoteCommand('rm %s' % CUDA_TOOLKIT_UBUNTU)
  vm.RemoteCommand('sudo rm -rf %s' % CUDA_TOOLKIT_INSTALL_DIR)
