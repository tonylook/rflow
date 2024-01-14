# `rflow` - Release Flow CLI Tool 🚀

`rflow` is a Command Line Interface (CLI) tool designed to facilitate the management of release branches in software development projects. Using the Release Flow branching strategy. It simplifies creating release, major release, and fix branches, as well as tagging releases in a Git repository.

## 📦 Installation

Before installing `rflow`, ensure you have Python and Git installed on your system. `rflow` is developed and tested primarily on Python 3.

### Clone the repository
```bash
git clone https://github.com/tonylook/rflow.git
cd rflow
```
### Setting Up a Virtual Environment (Optional)

It's recommended to use a virtual environment to manage the dependencies.

```bash
python -m venv venv
````
### Activate the virtual environment
#### On Windows:
```.\venv\Scripts\activate```
#### On macOS and Linux:
```bash
source venv/bin/activate
```
### Install dependencies
Clone the repository and install the required dependencies:
```bash
pip install -r requirements.txt
```

## 🧪 Running Tests

To run the tests, use the following command:

```bash
pytest tests/
```
Ensure you have `pytest` and `pytest-mock` installed in your environment.

## 📘 User Manual

For detailed instructions on how to use `rflow`, please refer to the [MANUAL.md](MANUAL.md) file in this repository. It provides comprehensive guidance on utilizing all the features of `rflow`.

## DevOps Settings 🛠️

The `rflow` tool comes with a dedicated `scripts` folder and pipeline configurations for Azure DevOps and GitHub Actions, facilitating its integration into your DevOps pipelines.

### Setting Up the `scripts` Folder

The `scripts` folder, located within the `rflow` repository, is designed to be placed directly into the root of your project for automating versioning processes.

1. **Locate the `scripts` Folder**: Find the `scripts` folder in the `rflow` repository.
2. **Place the `scripts` Folder in Your Project**: Simply copy this folder into the root directory of your project where `rflow` is to be used.

### Using Pipeline Configurations

`rflow` provides ready-to-use pipeline files for Azure and GitHub Actions in the `pipelines` folder. These files are prepared for immediate implementation.

#### For Azure DevOps

- **Pipeline File**: `azure-rflow.yml`
- **Implementation** :
    - Place `azure-rflow.yml` in your Azure DevOps pipeline configuration to integrate `rflow` into your Azure pipelines.

#### For GitHub Actions

- **Pipeline File**: `github-rflow.yml`
- **Implementation** :
    - Add `github-rflow.yml` to the `.github/workflows` directory of your GitHub repository to integrate `rflow` with your GitHub Actions workflows.

### Integrating `rflow` into CI/CD

Integrate `rflow` into your Continuous Integration and Continuous Deployment (CI/CD) processes by using the provided scripts and pipeline files. This integration ensures a smooth and automated process for managing releases and version control in your development cycle.

# 🗺️ Development Roadmap

The roadmap of the project is available in the [ROADMAP.md](ROADMAP.md) file within this repository.


