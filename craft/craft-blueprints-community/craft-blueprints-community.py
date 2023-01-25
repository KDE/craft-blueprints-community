# SPDX-License-Identifier: GPL-2.0-only OR GPL-3.0-only OR LicenseRef-KDE-Accepted-GPL
# SPDX-FileCopyrightText: 2022 Hannah von Reth <vonreth@kde.org>

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["master"]:
            self.svnTargets[ver] = f"https://invent.kde.org/packaging/craft-blueprints-community.git|{ver}|"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.buildDependencies["craft/craft-core"] = None


from Package.SourceOnlyPackageBase import *


class Package(SourceOnlyPackageBase):
    def __init__(self):
        SourceOnlyPackageBase.__init__(self)
        self.subinfo.options.package.disableBinaryCache = True
        self.subinfo.options.dailyUpdate = True

    def unpack(self):
        return True

    def install(self):
        return True

    def qmerge(self):
        if not SourceOnlyPackageBase.qmerge(self):
            return False
        CraftCore.cache.clear()
        return True

    def createPackage(self):
        return True

    def checkoutDir(self, index=0):
        return os.path.join(CraftStandardDirs.blueprintRoot(), self.package.name)
