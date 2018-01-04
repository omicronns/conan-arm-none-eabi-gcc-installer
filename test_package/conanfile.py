import subprocess
import conans

class ConanFileInst(conans.ConanFile):
    name = "arm-none-eabi-gcc_installer_test"
    requires = "arm-none-eabi-gcc_installer/0.3@demo/test_package"

    def build(self):
        pass

    def test(self):
        try:
            subprocess.check_output("arm-none-eabi-gcc --version".split())
        except FileNotFoundError as e:
            self.output.error("%s package test failed" % self.name)
        else:
            self.output.success("%s package test passed" % self.name)
