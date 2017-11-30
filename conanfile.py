import os
import subprocess
import conans
import conans.errors as ce


class ConanFileInst(conans.ConanFile):
    name = "arm-none-eabi-gcc_installer"
    description = "creates arm-none-eabi-gcc binaries package"
    version = "0.2"
    license = "MIT"
    url = "https://github.com/omicronns/conan-arm-none-eabi-gcc-installer.git"
    settings = {"os": ["Windows", "Linux", "Macos"]}

    arm_common_path = "https://developer.arm.com/-/media/Files/downloads/gnu-rm"
    bleeding_edge_common_path = "http://www.freddiechopin.info/phocadownload/bleeding-edge-toolchain"
    
    version_path_filename_map = {
        "bleeding-edge-toolchain-170901" : (bleeding_edge_common_path, "arm-none-eabi-gcc-7.2.0-170901-win64"),
        "bleeding-edge-toolchain-170503" : (bleeding_edge_common_path, "arm-none-eabi-gcc-7.1.0-170503-win64"),
        "6.3.1-20170620": (arm_common_path + "/6-2017q2", "gcc-arm-none-eabi-6-2017-q2-update-%s"),
        "6.3.1-20170215": (arm_common_path + "/6_1-2017q1", "gcc-arm-none-eabi-6-2017-q1-update-%s-zip"),
        "6.2.1-20161205": (arm_common_path + "/6-2016q4", "gcc-arm-none-eabi-6_2-2016q4-20161216-%s-zip"),
        "5.4.1-20160919": (arm_common_path + "/5_4-2016q3", "gcc-arm-none-eabi-5_4-2016q3-20160926-%s-zip"),
    }

    options = {"version": list(version_path_filename_map.keys())}
    default_options = "version=bleeding-edge-toolchain-170901"
    build_policy = "missing"
    short_paths = True
    exports = "7z.exe"


    def configure(self):
        if "bleeding-edge-toolchain" in str(self.options.version):
            if str(self.settings.os) in ("Linux", "Macos"):
                raise ce.ConanException("bleeding-edge-toolchain unavailible for %s" % self.settings.os)

    def get_path_filename(self):
        (path, filename) = self.version_path_filename_map[str(self.options.version)]
        if "bleeding-edge-toolchain" not in str(self.options.version):
            os_id = {"Macos": "mac", "Windows": "win32", "Linux": "linux"}.get(str(self.settings.os))
            filename = filename % os_id
        return path, filename

    def build(self):
        (path, filename) = self.get_path_filename()
        if "bleeding-edge-toolchain" in str(self.options.version):
            ext = "7z"
        else:
            ext = "tar.bz2" if not self.settings.os == "Windows" else "zip"
        url = "%s/%s.%s" % (path, filename, ext)
        dest_file = "file.%s" % ext
        self.output.info("Downloading: %s" % url)
        conans.tools.download(url, dest_file, verify=False)
        if "bleeding-edge-toolchain" in str(self.options.version):
            cmd_7z = "7z.exe x file.%s -o%s" % (ext, filename)
            subprocess.check_call(cmd_7z.split())
        else:
            conans.tools.unzip(dest_file, destination=filename)

    def package(self):
        (_, filename) = self.get_path_filename()
        extracted_dirs = os.listdir(filename)
        if len(extracted_dirs) == 1:
            files_path = os.path.join(filename, extracted_dirs[0])
        else:
            files_path = filename
        self.copy("*", dst="", src=files_path)

    def package_info(self):
        if not self.package_folder is None:
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))

