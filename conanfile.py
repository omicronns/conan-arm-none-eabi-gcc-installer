import os
import conans


class ConanFileInst(conans.ConanFile):
    name = "arm-none-eabi-gcc_installer"
    description = "creates arm-none-eabi-gcc binaries package"
    version = "0.1"
    license = "MIT"
    url = "https://github.com/omicronns/conan-arm-none-eabi-gcc-installer.git"
    settings = {"os": ["Windows", "Linux", "Macos"]}

    year_quarter = {
        "6.3": ("2017", "q2")
    }

    options = {"version": list(year_quarter.keys())}
    default_options = "version=6.3"
    build_policy = "missing"
    short_paths = True
    
    
    def configure(self):
        if self.settings.os == "Macos" and self.settings.arch == "x86":
            raise Exception("Not supported x86 for OSx")

    def get_filename(self):
        major = str(self.options.version)[0]
        (year, quarter) = self.year_quarter[str(self.options.version)]
        if quarter == "q4":
            release = "major"
        else:
            release = "update"
        os_id = {"Macos": "mac", "Windows": "win32"}.get(str(self.settings.os))
        return "gcc-arm-none-eabi-%s-%s-%s-%s-%s" % (major, year, quarter, release, os_id)
    
    def build(self):
        major = str(self.options.version)[0]
        (year, quarter) = self.year_quarter[str(self.options.version)]
        ext = "tar.bz2" if not self.settings.os == "Windows" else "zip"
        url = "https://developer.arm.com/-/media/Files/downloads/gnu-rm/%s-%s%s/%s.%s" % (major, year, quarter, self.get_filename(), ext)

        # https://developer.arm.com/-/media/Files/downloads/gnu-rm/6-2017q2/gcc-arm-none-eabi-6-2017-q2-update-win32.exe

        dest_file = "file.%s" % ext
        self.output.info("Downloading: %s" % url)
        conans.tools.download(url, dest_file, verify=False)
        conans.tools.unzip(dest_file, destination=self.get_filename())

    def package(self):
        self.copy("*", dst="", src=self.get_filename())

    def package_info(self):
        if not self.package_folder is None:
            self.env_info.path.append(os.path.join(self.package_folder, "bin"))
