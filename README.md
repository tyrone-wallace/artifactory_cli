# Artifactory CLI

## Overview
The **Artifactory CLI** is a command-line interface (CLI) tool designed to manage an Artifactory SaaS instance via its API. This application provides an interactive and user-friendly way to manage users, repositories, and system information in Artifactory.

---

## Features

- **Authentication**: Login using username and password to generate a token for secure API interaction.
- **System Information**:
  - Ping the system to check health status.
  - Retrieve Artifactory version and storage information.
- **User Management**:
  - List all users.
  - Create new users with optional admin privileges.
  - Delete users with confirmation prompts.
- **Repository Management**:
  - List all repositories, categorized by type.
  - Create repositories with configurable types and package types.
  - Update repository configurations.

---

## Installation

### Prerequisites
- Python 3.10 or higher
- An Artifactory SaaS instance

### Installation Steps
1. **Install via Artifactory**:
   ```bash
   pip install https://trials5ruji.jfrog.io/artifactory/tyrone-rt-cli-repo/artifactory_cli-0.0.1.tar.gz
   ```

2. **Verify Installation**:
   ```bash
   artifactory-cli --help
   ```

---

## Usage

### Login
To start using the CLI, login with your Artifactory credentials:
```bash
artifactory-cli
```
You will be prompted to enter your username and password. A token will be generated for subsequent API interactions.

### Main Menu
The main menu provides the following options:

1. **System Ping**: Check the health status of the Artifactory instance.
2. **Get System Version**: Retrieve the Artifactory version and revision details.
3. **Get Storage Info**: Retrieve all storage details of the Artifactory instance.
4. **List Users**: View all registered users.
5. **Create User**: Add a new user with a username, email, and password.
6. **Delete User**: Select a user to delete from a list, with confirmation prompts.
7. **List Repositories**: View all repositories with their types.
8. **Create Repository**: Add a new repository by selecting type and package.
9. **Update Repository**: Modify repository configurations interactively.
10. **Exit**: Close the CLI application. Alternative is "Ctrl+C".

### Example Workflow
1. **Login**:
   ```plaintext
   Enter your Artifactory username: test-user
   Enter your Artifactory password: ********
   ✅ Login successful! Token generated.
   ```

2. **Perform Actions**:
   Select options from the interactive menu to perform actions like creating a repository or listing users.

3. **Exit Application**:
   When done, select `Exit` to safely close application.

---

## Development

### Project Structure
```
artifactory_cli/
├── __init__.py         # Marks the folder as a Python package
├── main.py             # Entry point for the application
├── views.py            # Handles user interaction (CLI views)
├── controls.py         # Handles API interactions with Artifactory
├── utils_list.py       # Contains global constants (e.g., package types)
└── requirements.txt    # Python dependencies
```

### Setup for Local Development
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd artifactory_cli
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application locally:
   ```bash
   python -m artifactory_cli.main
   ```

---

## Configuration
The Artifactory base URL is stored in the controls.py file for now:

```
BASE_URL=https://trials5ruji.jfrog.io
```

To user for other another Artifactory instance, just change base url.

---

## Contributing
If you would like to contribute:
1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request with detailed descriptions of the changes.

---

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Support
If you encounter issues or have questions, please reach out to the project maintainer or submit an issue in the repository.

