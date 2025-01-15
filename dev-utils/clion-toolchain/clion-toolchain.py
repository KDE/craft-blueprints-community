# SPDX-License-Identifier: GPL-2.0-only OR GPL-3.0-only OR LicenseRef-KDE-Accepted-GPL
# SPDX-FileCopyrightText: 2023 Hannah von Reth <vonreth@kde.org>

import shlex

import info
from Utils.CaseInsensitiveDict import CaseInsensitiveDict


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["latests"] = ""
        self.defaultTarget = "latests"


from Package.VirtualPackageBase import *


class Package(VirtualPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.shelveAble = False

    def install(self):
        if not self.cleanImage():
            return False
        environ = CaseInsensitiveDict(sorted(os.environ.items(), key=lambda t: t[0]))
        if self.supportsCCACHE:
            environ["CXX"] = CraftCore.standardDirs.craftRoot() / "dev-utils/ccache/bin" / Path(environ["CXX"]).name
            environ["CC"] = CraftCore.standardDirs.craftRoot() / "dev-utils/ccache/bin" / Path(environ["CC"]).name

        if CraftCore.compiler.isWindows:
            scriptPath = self.imageDir() / "etc/clion-craftenv.bat"
            if not utils.createDir(scriptPath.parent):
                return False
            with scriptPath.open("wt", encoding="UTF-8", newline="\r\n") as out:
                lines = [f"@echo off", "rem This file is auto generated, don't change it", "rem To update it run craft -i clion-toolchain"] + [
                    f"set {k}={v}" for k, v in environ.items()
                ]
                out.write("\n".join(lines))
            return True
        else:
            scriptPath = self.imageDir() / "etc/clion-craftenv.sh"
            if not utils.createDir(scriptPath.parent):
                return False
            with scriptPath.open("wt", encoding="UTF-8", newline="\n") as out:
                lines = ["# This file is auto generated, don't change it", "# To update it run craft -i clion-toolchain"] + [
                    f"export {shlex.quote(str(k))}={shlex.quote(str(v))}" for k, v in environ.items()
                ]
                out.write("\n".join(lines))
            return True
