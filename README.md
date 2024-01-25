# `rflow` - Release Flow CLI Tool 🚀

`rflow` is a Command Line Interface (CLI) tool designed to facilitate the management of release branches in software development projects. Using the Release Flow branching strategy. It simplifies creating release, major release, and fix branches, as well as tagging releases in a Git repository.

---

## 📦 Installation
### 🍺 Install with Homebrew

You can also install `rflow` using [Homebrew](https://brew.sh/), a package manager for macOS (and Linux) without worrying about dependencies:

```bash
brew tap tonylook/rflow
brew install rflow
````
### Install Without Homebrew
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

---

## 🧪 Running Tests

To run the tests, use the following command:

```bash
pytest tests/
```
Ensure you have `pytest` and `pytest-mock` installed in your environment.

---

## 📘 User Manual

For detailed instructions on how to use `rflow`, please refer to the [MANUAL.md](MANUAL.md) file in this repository. It provides comprehensive guidance on utilizing all the features of `rflow`.

---

## 🛠️ DevOps Manual

For detailed instructions on how to automatize versioning with `rflow`, please refer to the [DEVOPS.md](DEVOPS.md) file in this repository. It explains how to prepare your project for a fully automated versioning experience.

---

## Known Issues 🐛

Here's a list of known issues we're currently working on in `rflow`. We appreciate your understanding and patience as we work towards resolving them.

### Issue with `rflow tag` on Main/Master Branch

- **Description**: Currently, the `rflow tag` command cannot be used on the main/master branch due to complications in managing automatic versioning for this type of action.
- **Impact**: This limitation affects the ability to tag releases directly from the main/master branch, which might be a part of some users' standard workflows.
- **Status**: I'm actively investigating ways to address this issue and hope to provide a solution in future updates. In the meantime, use the `rflow tag` command (as also compliant with Release Flow) on release branches for tagging releases.

I encourage users to report any other issues they encounter on our GitHub issues page to help me continue improving `rflow`.
