# SPDX-License-Identifier: GPL-2.0-only OR GPL-3.0-only OR LicenseRef-KDE-Accepted-GPL
# SPDX-FileCopyrightText: 2023 Hannah von Reth <vonreth@kde.org>

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.0.12"]:
            if CraftCore.compiler.platform == CraftCore.compiler.Platforms.Windows:
                self.targets[ver] = f"https://github.com/zyedidia/micro/releases/download/v{ver}/micro-{ver}-win64.zip"
            elif CraftCore.compiler.platform == CraftCore.compiler.Platforms.MacOS:
                if CraftCore.compiler.architecture & CraftCore.compiler.Architecture.arm64:
                    self.targets[ver] = f"https://github.com/zyedidia/micro/releases/download/v{ver}/micro-{ver}-macos-arm64.tar.gz"
                else:
                    self.targets[ver] = f"https://github.com/zyedidia/micro/releases/download/v{ver}/micro-{ver}-osx.tar.gz"
            elif CraftCore.compiler.platform == CraftCore.compiler.Platforms.Linux:
                if CraftCore.compiler.architecture & CraftCore.compiler.Architecture.arm64:
                    self.targets[ver] = f"https://github.com/zyedidia/micro/releases/download/v{ver}/micro-{ver}-linux-arm64.tar.gz"
                else:
                    self.targets[ver] = f"https://github.com/zyedidia/micro/releases/download/v{ver}/micro-{ver}-linux64.tar.gz"
            elif CraftCore.compiler.platform == CraftCore.compiler.Platforms.FreeBSD:
                self.targets[ver] = f"https://github.com/zyedidia/micro/releases/download/v{ver}/micro-{ver}-freebsd64.tar.gz"
            self.targetInstallPath[ver] = "dev-utils/micro"
            self.targetInstSrc[ver] = f"micro-{ver}"

        self.defaultTarget = "2.0.12"

    def setDependencies(self):
        self.buildDependencies["dev-utils/7zip"] = None
        self.buildDependencies["core/cacert"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.shelveAble = False

    def postInstall(self):
        return utils.createShim(
            self.imageDir() / f"dev-utils/bin/micro{CraftCore.compiler.executableSuffix}",
            self.imageDir() / f"dev-utils/micro/micro{CraftCore.compiler.executableSuffix}",
        )

    def postQmerge(self):
        CraftCore.cache.clear()
        return True
