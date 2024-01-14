# `rflow` CLI Tool User Manual 📘

Welcome to the `rflow` CLI Tool! This tool automates various tasks in your software version management process. Below are instructions for using the different features available in `rflow`.

## Table of Contents 📑
1. [Installation](#installation-)
2. [Initialize Repository](#initialize-repository-)
3. [Release Branch Creation](#release-branch-creation-)
4. [Major Release Branch Creation](#major-release-branch-creation-)
5. [Fix Branch Creation](#fix-branch-creation-)
6. [Snapshot Creation](#snapshot-creation-)
7. [Tagging a Release](#tagging-a-release-)
8. [Troubleshooting](#troubleshooting-)

## Installation 📥

Before using `rflow`, install it on your system by following these steps:

1. Ensure Python is installed on your system.
2. Clone the `rflow` repository from GitHub or download the source code.
3. Navigate to the `rflow` directory and run `pip install .` to install the tool.

## Initialize Repository 🌱

The `rflow init` command initializes a Git repository for use with `rflow`.

### When to Use

- When setting up `rflow` in a new repository.

### How to Use


   ```bash
   rflow init
   ```

## Release Branch Creation 🚀

Create a release branch after initializing your repository with `rflow init`.

```bash
rflow release
```

## Major Release Branch Creation 🌟

Create a major release branch, which automatically calculates the next major version.

```bash
rflow major
```

## Fix Branch Creation 🛠️

Create a fix branch from a specific tag version and bug description.

```bash
rflow fix [tag_version] [bug_description]
```

## Snapshot Creation 📸

The `rflow snap` command creates a snapshot tag, marking the current state of the project with a timestamp.

### When to Use

- To mark the current project state for quick rollbacks or references.
- To put in dev environment the software.

### How to Use

   ```bash
   rflow snap
   ```

## Tagging a Release 🏷️

Create a Git tag for the current release using the `rflow tag` command.

### When to Use

- When you're ready to tag a new release in your repository.

### How to Use

   ```bash
   rflow tag
   ```

## Troubleshooting 🔍

If you encounter issues:

1. Check that you're in the correct directory containing the Git repository.
2. Verify that you have the necessary permissions to perform the operations.
3. Look for error messages in the console for clues about what might be wrong.
4. For more support, refer to the `rflow` documentation or contact the development team.

Thank you for using `rflow`! 🎉