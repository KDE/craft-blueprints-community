# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>

import info
from Packager.AppImagePackager import AppImagePackager


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Cross-platform (Qt), open-source (GPLv3) video editor"
        self.webpage = "https://www.shotcut.org/"
        for ver in ['22.12.21']:
            self.targets[ ver ] = f"https://github.com/mltframework/shotcut/archive/v{ver}.tar.gz"
            self.targetInstSrc[ ver ] = "shotcut-" + ver
        self.svnTargets['master'] = "https://github.com/mltframework/shotcut.git"

        self.defaultTarget = '22.12.21'


    def setDependencies(self):
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt5/qtspeech"] = None
        self.runtimeDependencies["libs/qt5/qtimageformats"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtwebsockets"] = None
        #self.runtimeDependencies["libs/qt5/qtquickcontrols"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["libs/qt5/qtnetworkauth"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/mlt"] = None
        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/frei0r-bigsh0t"] = None
        if CraftCore.compiler.isWindows:
            self.runtimeDependencies["libs/drmingw"] = None

from Package.CMakePackageBase import *
from Utils import GetFiles

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-DWINDOWS_DEPLOY=OFF"]

    def setDefaults(self, defines: {str:str}) -> {str:str}:
        defines = super().setDefaults(defines)
        if OsUtils.isLinux() and isinstance(self, AppImagePackager):
            defines["runenv"] += [
                'LD_LIBRARY_PATH=$this_dir/usr/lib/:$LD_LIBRARY_PATH',
                'MLT_REPOSITORY=$this_dir/usr/lib/mlt-7/',
                'MLT_DATA=$this_dir/usr/share/mlt-7/',
                'MLT_ROOT_DIR=$this_dir/usr/',
                'LADSPA_PATH=$this_dir/usr/lib/ladspa',
                'FREI0R_PATH=$this_dir/usr/lib/frei0r-1',
                'MLT_PROFILES_PATH=$this_dir/usr/share/mlt-7/profiles/',
                'MLT_PRESETS_PATH=$this_dir/usr/share/mlt-7/presets/',
                'SDL_AUDIODRIVER=pulseaudio']
        return defines

    def createPackage(self):
        self.addExecutableFilter(r"bin/(?!(ff|shotcut|melt|update-mime-database|drmingw|data/shotcut)).*")
        self.ignoredPackages.append("libs/llvm")
        self.ignoredPackages.append("data/hunspell-dictionaries")
        self.ignoredPackages.append("binary/mysql")

        self.defines["appname"] = "org.shotcut.Shotcut"
        self.defines["icon"] = os.path.join(self.sourceDir(), "packaging", "windows", "shotcut-logo-64.ico")
        self.defines["icon_png"] = os.path.join(self.sourceDir(), "icons", "shotcut-logo-64.png")
        self.defines["shortcuts"] = [{"name" : "Shotcut", "target":"bin/shotcut.exe", "description" : self.subinfo.description}]
        self.defines["mimetypes"] = ["application/vnd.mlt+xml"]
        self.defines["file_types"] = [".mlt"]
        return super().createPackage()

