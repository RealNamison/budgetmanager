# Contributing to BudgetManager

Thank you for your interest in contributing to **BudgetManager**! We welcome contributions from the community to improve the project. By following these guidelines, you’ll help ensure a smooth development workflow and maintain a high-quality codebase.

---

## Table of Contents

1. [Code of Conduct](#code-of-conduct)  
2. [Getting Started](#getting-started)  
   - [Prerequisites](#prerequisites)  
   - [Development Environment Setup](#development-environment-setup)  
3. [Branching and Workflow](#branching-and-workflow)  
4. [Coding Standards](#coding-standards)  
   - [Python Version](#python-version)  
   - [Project Structure](#project-structure)  
   - [Type Hints](#type-hints)  
   - [Formatting and Linting](#formatting-and-linting)  
   - [Documentation](#documentation)  
   - [Testing Requirements](#testing-requirements)  
5. [Submitting Changes](#submitting-changes)  
   - [Issues](#issues)  
   - [Pull Requests](#pull-requests)  
   - [Review Process](#review-process)  
6. [Release Process](#release-process)  
7. [Acknowledgments](#acknowledgments)

---

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold these guidelines at all times. Please report any unacceptable behavior to the project maintainers.

---

## Getting Started

### Prerequisites

Before contributing, ensure you have the following installed on your machine:

- **Python 3.10+**  
- **pip** (latest version)  
- **git**  

### Development Environment Setup

1. **Fork the Repository**  
   On GitHub, click the “Fork” button to create your own copy of the repository.

2. **Clone Your Fork**  
   ```bash
   git clone https://github.com/<your-username>/budgetmanager.git
   cd budgetmanager
   ```

3. **Create a Virtual Environment** (Recommended)  
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   ```

4. **Install Dependencies**  
   ```bash
   pip install --upgrade pip
   pip install .
   ```

5. **Verify Setup**  
   ```bash
   budgetmgr --help
   ```

---

## Branching and Workflow

1. **Main Branch**  
   The `main` branch always holds the latest stable release. Do **not** commit directly to `main`.

2. **Create Feature Branches**  
   Each new feature, bugfix, or improvement should have its own branch. Branch names should follow this convention:

   ```
   <type>/<short-description>
   ```

   - **type**: One of `feature`, `bugfix`, `docs`, `refactor`, or `test`.  
   - **short-description**: A concise summary in kebab-case (hyphens).  

   **Examples**:  
   - `feature/add-transaction-validation`  
   - `bugfix/fix-summary-calculation`  
   - `docs/update-readme`  

3. **Fetch and Rebase Regularly**  
   To keep your branch up to date:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

---

## Coding Standards

### Python Version

- Use **Python 3.10 or higher**. BudgetManager leverages modern language features such as the pipe (`|`) syntax for type hints.

### Project Structure

- Source code resides under:  
  ```
  src/budgetmanager/
  ```
- Tests are organized under:  
  ```
  tests/unit/
  tests/integration/
  ```

### Type Hints

- Use **PEP 484** type hints for all functions and methods.
- Prefer the pipe (`|`) syntax over `Optional[T]` or `Union[X, Y]`.  
  ```python
  def get_user(id: int) -> User | None:
      ...
  ```

### Formatting and Linting

- Follow **PEP 8** guidelines with a maximum of **79 characters per line** (72 characters for docstrings and comments).
- Indentation: **4 spaces**.
- Import order:
  1. Standard library modules  
  2. Third-party libraries  
  3. Local application imports  
- Use **Black** for automatic formatting (configured with `line-length = 79`).
- Use **Flake8** to catch style issues. The configuration is in `.flake8`.
- Use **Mypy** for type checking, as configured in `pyproject.toml`.

### Documentation

- All docstrings and inline comments must be written **in English**.
- Use **Google-style** docstrings with sections:  
  - **Short description**  
  - `Args:`  
  - `Returns:`  
  - `Raises:`  
  - `Examples:`  
- Update relevant documentation files (e.g., `README.md`, `usage.md`, `reports.md`, `docs/`) when adding or modifying features.

### Testing Requirements

- Write **pytest** unit tests for all new functionality.
- Tests should cover edge cases and error handling.
- Place unit tests under `tests/unit/` and integration tests under `tests/integration/`.
- Ensure tests pass before submitting a pull request:
  ```bash
  pytest --cov=budgetmanager
  ```

---

## Submitting Changes

### Issues

- Search existing issues before creating a new one to avoid duplicates.
- When opening a new issue, provide a clear and descriptive title, a detailed description of the problem or feature request, and relevant context (error messages, logs, screenshots).

### Pull Requests

1. **Fork & Branch**  
   - Fork the repository and create a feature branch as described above.

2. **Implement Changes**  
   - Commit atomic, focused changes with descriptive commit messages (imperative mood).  
   - Include tests for new behavior or bug fixes.  
   - Update documentation as needed.

3. **Rebase onto Latest `main`**  
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

4. **Push to Your Fork**  
   ```bash
   git push origin <type>/<short-description>
   ```

5. **Create Pull Request**  
   - Go to the original repository on GitHub.  
   - Click “New Pull Request” and select your branch.  
   - Use the following template for the PR description:
     ```
     ## Summary
     Short description of changes.

     ## Related Issues
     - Closes #[issue_number]

     ## Changes
     - Bullet points of what changed
     - Any backward-incompatible changes?

     ## Testing
     - How was this tested? (e.g., “Ran pytest tests”)

     ```

6. **Await Review**  
   - Team members will review your code, suggest improvements, or request changes.  
   - Engage constructively, address feedback, and update the PR accordingly.

### Review Process

- Code is reviewed based on correctness, readability, style, and test coverage.
- Once approved, a maintainer will merge the PR into `main`.
- After merging, the author should delete the feature branch from the remote.

---

## Release Process

Releases are managed by maintainers. Key steps include:

1. **Update Version**  
   - Modify the version number in `pyproject.toml` under `[tool.poetry]`.

2. **Changelog**  
   - Update `CHANGELOG.md` with changes in the new version. If `CHANGELOG.md` does not exist, create it.

3. **Tagging**  
   ```bash
   git checkout main
   git pull upstream main
   git tag -a vX.Y.Z -m "Release version X.Y.Z"
   git push upstream main --tags
   ```

4. **Build and Publish**  
   ```bash
   poetry build
   poetry publish
   ```
   - Ensure you have proper credentials for PyPI.

---

## Acknowledgments

Thank you to all contributors and community members who help make BudgetManager better. Your support and feedback are greatly appreciated!

