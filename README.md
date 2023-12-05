# `rflow` - Release Flow CLI Tool 🚀

`rflow` is a Command Line Interface (CLI) tool designed to facilitate the management of release branches in software development projects. Using the Release Flow branching strategy. It simplifies creating release, major release, and fix branches, as well as tagging releases in a Git repository.

## 📦 Installation

Before installing `rflow`, ensure you have Python and Git installed on your system. `rflow` is developed and tested primarily on Python 3.

### Setting Up a Virtual Environment (Optional)

It's recommended to use a virtual environment to manage the dependencies.

```bash
# Create a virtual environment
python -m venv venv
````
### Activate the virtual environment
#### On Windows:
```.\venv\Scripts\activate```
#### On macOS and Linux:
```bash
source venv/bin/activate
```
### Install `rflow`
Clone the repository and install the required dependencies:
```bash
# Clone the repository
git clone https://github.com/tonylook/rflow.git
cd rflow

# Install dependencies
pip install -r requirements.txt
```

## 🧪 Running Tests

To run the tests, use the following command:

```bash
pytest tests/
```
Ensure you have `pytest` and `pytest-mock` installed in your environment.

# 🗺️ Development Roadmap

The roadmap of the project is available in the [ROADMAP.md](ROADMAP.md) file within this repository.

