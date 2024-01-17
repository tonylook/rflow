# DevOps Manual 🛠️

The `rflow` tool comes with a dedicated `scripts` folder and pipeline configurations for Azure DevOps and GitHub Actions, facilitating its integration into your DevOps pipelines.

### Setting Up the `scripts` Folder

The `scripts` folder, located within the `rflow` repository, is designed to be placed directly into the root of your project for automating versioning processes.

1. **Locate the `scripts` Folder**: Find the `scripts` folder in the `rflow` repository.
2. **Place the `scripts` Folder in Your Project**: Simply copy this folder into the root directory of your project where `rflow` is to be used.

### Using Pipeline Configurations

`rflow` provides ready-to-use pipeline files for Azure and GitHub Actions in the `pipelines` folder. These files are prepared for immediate implementation.

#### For Azure DevOps

- **Pipeline File**: `azure-rflow.yml`
- **Implementation**:
  - Place `azure-rflow.yml` in your Azure DevOps pipeline configuration to integrate `rflow` into your Azure pipelines.
  - In Azure DevOps, navigate to **Project Settings -> Repositories -> Security**.
  - Modify the **User Permissions** for the **Project Collection Build Service** account.
  - Set the **Contribute** permission to **Allow**. This step is crucial to ensure that the pipeline has the necessary permissions to operate within the repository.

#### For GitHub Actions

- **Pipeline File**: `github-rflow.yml`
- **Implementation**:
  - Add `github-rflow.yml` to the `.github/workflows` directory of your GitHub repository to integrate `rflow` with your GitHub Actions workflows.
  - Go to the **Settings** of your GitHub repository.
  - Navigate to **Actions -> General**.
  - Under **Workflow permissions**, set the permissions to **Read and write**. This adjustment allows the workflow to have the appropriate access for its operations.

### Integrating `rflow` into CI/CD

Integrate `rflow` into your Continuous Integration and Continuous Deployment (CI/CD) processes by using the provided scripts and pipeline files. This integration ensures a smooth and automated process for managing releases and version control in your development cycle.