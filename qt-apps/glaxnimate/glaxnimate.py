# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>

import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Glaxnimate"
        self.description = "Simple vector animation program"
        self.webpage = "https://glaxnimate.mattbas.org/"

        for ver in ['0.4.6', '0.5.0', '0.5.2']:
            self.targets[ ver ] = f"https://gitlab.com/mattbas/glaxnimate/-/archive/{ver}/glaxnimate-{ver}.tar.gz"
            self.targetInstSrc[ ver ] = "glaxnimate-" + ver

        self.patchToApply['master'] = [("0001_fix_android_build.patch", 1)]
        self.patchLevel['master'] = 1

        self.svnTargets['master'] = 'https://gitlab.com/mattbas/glaxnimate.git'
        self.defaultTarget = '0.5.2'


    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtsvg"] = None
        self.runtimeDependencies["libs/qt5/qttools"] = None
        if CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/qt5/qtandroidextras"] = None
        self.runtimeDependencies["libs/potrace"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/libarchive"] = None
        self.runtimeDependencies["libs/zlib"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        # enable submodule checkout
        self.subinfo.options.fetch.checkoutSubmodules = True

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isLinux:
            utils.copyFile(os.path.join(self.buildDir(), "external", "Qt-Color-Widgets", f"libQtColorWidgets.so.2.2.0"), os.path.join(self.installDir(), "lib", f"libQtColorWidgets.so.2.2.0"))
            utils.copyFile(os.path.join(self.buildDir(), "external", "Qt-Color-Widgets", f"libQtColorWidgets.so.2"), os.path.join(self.installDir(), "lib", f"libQtColorWidgets.so.2"))
            utils.copyFile(os.path.join(self.buildDir(), "external", "Qt-Color-Widgets", f"libQtColorWidgets.so"), os.path.join(self.installDir(), "lib", f"libQtColorWidgets.so"))
        if CraftCore.compiler.isWindows:
            utils.copyFile(os.path.join(self.buildDir(), "external", "Qt-Color-Widgets", f"libQtColorWidgets.dll"), os.path.join(self.installDir(), "bin", f"libQtColorWidgets.dll"))
        return True


    def createPackage(self):
        self.defines["executable"] = r"bin\glaxnimate.exe"
        #self.addExecutableFilter(r"(bin|libexec)/(?!(glaxnimate|update-mime-database)).*")
        self.ignoredPackages.append("binary/mysql")
        if not CraftCore.compiler.isLinux:
            self.ignoredPackages.append("libs/dbus")


        self.defines["appname"] = "Glaxnimate"
        #self.defines["icon"] = os.path.join(self.sourceDir(), "data", "icons", "kdenlive.ico")
        #self.defines["icon_png"] = os.path.join(self.sourceDir(), "logo.png")
        return super().createPackage()
