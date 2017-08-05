import os
import conans


class ConanFileInst(conans.ConanFile):
    name = "arm-none-eabi-gcc_installer"
    description = "creates arm-none-eabi-gcc binaries package"
    version = "0.1"
    license = "MIT"
    url = "https://github.com/omicronns/conan-arm-none-eabi-gcc-installer.git"
    settings = {"os": ["Windows", "Linux", "Macos"]}

    version_path_filename_map = {
        "6.3.1-20170620": ("6-2017q2", "gcc-arm-none-eabi-6-2017-q2-update-%s"),
        "6.3.1-20170215": ("6_1-2017q1", "gcc-arm-none-eabi-6-2017-q1-update-%s-zip"),
        "6.2.1-20161205": ("6-2016q4", "gcc-arm-none-eabi-6_2-2016q4-20161216-%s-zip"),
        "5.4.1-20160919": ("5_4-2016q3", "gcc-arm-none-eabi-5_4-2016q3-20160926-%s-zip"),
    }

    options = {"version": list(version_path_filename_map.keys())}
    default_options = "version=6.3.1-20170620"
    build_policy = "missing"
    short_paths = True


    def get_path_filename(self):
        (path, filename) = self.version_path_filename_map[str(self.options.version)]
        os_id = {"Macos": "mac", "Windows": "win32", "Linux": "linux"}.get(str(self.settings.os))
        filename = filename % os_id
        return path, filename

    def build(self):
        (path, filename) = self.get_path_filename()
        ext = "tar.bz2" if not self.settings.os == "Windows" else "zip"
        url = "https://developer.arm.com/-/media/Files/downloads/gnu-rm/%s/%s.%s" % (path, filename, ext)
        dest_file = "file.%s" % ext
        self.output.info("Downloading: %s" % url)
        conans.tools.download(url, dest_file, verify=False)
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

