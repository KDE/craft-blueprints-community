# SPDX-License-Identifier: BSD-2-Clause
# SPDX-FileCopyrightText: 2023 Julius Künzel <jk.kdedev@smartlab.uber.space>

import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Potrace"
        self.description = "Transforming bitmaps into vector graphics"
        self.webpage = "http://potrace.sourceforge.net/"

        for ver in ['1.16']:
            self.targets[ ver ] = f"http://potrace.sourceforge.net/download/{ver}/potrace-{ver}.tar.gz"
            self.targetInstSrc[ ver ] = "potrace-" + ver

        self.defaultTarget = '1.16'


    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


from Package.AutoToolsPackageBase import *

class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += " --with-libpotrace "
