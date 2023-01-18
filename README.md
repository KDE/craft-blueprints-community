<!--
    SPDX-License-Identifier: CC0-1.0
    SPDX-FileCopyrightText: none
-->

# Craft Community Blueprints

## About KDE Craft
KDE Craft is an open source meta build system and package manager. It manages dependencies and builds libraries and applications from source, on Windows, Mac, Linux, FreeBSD and Android.

## About blueprints
Build instructions for each library or application are stored in so called blueprints. These blueprints are collected in blueprint repositories like this. You can use one or multiple blueprint repositories.

## About this repository
There is a blueprint repository called [craft-blueprints-kde](https://invent.kde.org/packaging/craft-blueprints-kde) that is added to Craft by default. It contains blueprints for Qt, KDE Software and its dependencies.

In contrast to craft-blueprints-kde this repository is aimed for blueprints of other Software that is not directly related to KDE Software. However blueprints of this repository might depend on blueprints of craft-blueprints-kde like Qt.

## Getting started

First you need to [setup Craft](https://community.kde.org/Craft).

Now you can add this blueprints repository with the following command:

```craft --add-blueprint-repository https://invent.kde.org/packaging/craft-blueprints-community.git```

Use the same command to update the craft-blueprints-community repository in your Craft setup.
