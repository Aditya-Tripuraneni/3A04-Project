# GitHub Actions CI/CD

This project uses GitHub Actions for continuous integration and continuous deployment.

## Workflows

### 1. CI Workflow (`ci.yml`)

The CI workflow runs on every pull request to the `main` branch:

- **Test job**: Runs the test suite to ensure functionality
- **Lint job**: Performs type-checking to catch errors early

### 2. Tauri Build and Release Workflow (`tauri-build.yml`)

This workflow handles building and releasing the Tauri application:

- Triggered on:
  - Pushes to the `main` branch (builds only)
  - New tags starting with `v*` (builds and creates releases)
  - Manual execution via workflow_dispatch

- Features:
  - Cross-platform builds for macOS, Windows, and Linux
  - Artifact upload for each platform
  - Automated GitHub release creation for tags

## Setting Up Repository Secrets

The workflows may require these secrets to be set in your GitHub repository:

- `GITHUB_TOKEN`: Automatically provided by GitHub
- For code signing (optional):
  - Windows: `WINDOWS_CERTIFICATE` and `WINDOWS_CERTIFICATE_PASSWORD`
  - macOS: `APPLE_CERTIFICATE`, `APPLE_CERTIFICATE_PASSWORD`, `APPLE_SIGNING_IDENTITY`

## Creating a Release

To create a new release:

1. Update the version in `package.json` and `src-tauri/tauri.conf.json`
2. Commit the changes
3. Create and push a new tag:

```bash
git tag v1.0.0
git push origin v1.0.0
```

This will automatically trigger the release workflow, which will build and publish the application.