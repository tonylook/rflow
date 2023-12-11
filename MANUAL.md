# `rflow` CLI Tool User Manual 📘

Welcome to the `rflow` CLI Tool! This tool helps automate various tasks in your software version management process. Below you will find instructions on how to use the different features currently available in `rflow`.

## Table of Contents 📑
1. [Installation](#installation-)
2. [Release Branch Creation](#release-branch-creation-)
3. [Major Release Branch Creation](#major-release-branch-creation-)
4. [Fix Branch Creation](#fix-branch-creation-)
5. [Troubleshooting](#troubleshooting-)

## Installation 📥

Before using `rflow`, you need to install it on your system. Follow these steps:

1. Ensure you have Python installed on your system.
2. Clone the `rflow` repository from GitHub or download the source code.
3. Navigate to the `rflow` directory and run `pip install .` to install the tool.

## Release Branch Creation 🚀

To create a release branch:

```bash
rflow release --version <version_number>
```
Replace `<version_number>` with the desired version number for the release branch. For example, to create a release branch for version `1.2.0`, run:

```bash
rflow release --version 1.2.0
```
## Major Release Branch Creation 🌟

To create a major release branch:

```bash
rflow major
```
This command automatically calculates the next major version and creates a corresponding release branch.

## Fix Branch Creation 🛠️

To create a fix branch from the current release branch:

```bash
rflow fix
```
Ensure you're on a release branch when executing this command. The tool will create a new fix branch based on your current release branch.

## Troubleshooting 🔍

If you encounter any issues while using `rflow`, please check the following:

1. Ensure you're in the correct directory containing the Git repository.
2. Verify that you have the necessary permissions to perform the operations.
3. Check for any error messages in the console for clues on what went wrong.
4. For more support, refer to the rflow documentation or contact the development team.

Thank you for using rflow! 🎉
