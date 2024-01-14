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

## 🛠️ DevOps Manual

For detailed instructions on how to automatize versioning with `rflow`, please refer to the [DEVOPS.md](DEVOPS.md) file in this repository. It explains how to prepare your project for a fully automated versioning experience.

# 🗺️ Development Roadmap

The roadmap of the project is available in the [ROADMAP.md](ROADMAP.md) file within this repository.


