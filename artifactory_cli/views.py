from controls import *
from InquirerPy import prompt
from utils_list import PACKAGE_TYPES, REPO_TYPE

def system_ping_view():
    try:
        response = ping_system_control()
        print("\n✅ System Ping Successful!")
        print(f"Response: {response}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")


def get_system_version_view():
    try:
        response = get_system_version_control()
        print("\n✅ System Version Retrieved Successfully!\n")
        
        # Extract and format the version details
        version = response.get("version", "Unknown")
        revision = response.get("revision", "Unknown")
        addons = response.get("addons", "Unknown")

        # Ensure addons is a list
        if isinstance(addons, str):
            addons = addons.split(",")  # Split if it's a comma-separated string
        elif not isinstance(addons, list):
            addons = []  # If it's not a list or string, set it to an empty list

        # Display the details in a clean format
        print("🔹 Artifactory System Version Information:")
        print("  ----------------------------------------")
        print(f"  📦 Version:          {version}")
        print(f"  🔄 Revision:         {revision}")
        print("  ----------------------------------------")
        print(f"  🛠  Add-ons Installed:")
        if addons:
            for addon in addons:
                print(f"     - {addon.strip()}")
        else:
            print("    - None")

        print("\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")


def list_repositories_view():
    try:
        response = list_repositories_control()
        print("\n✅ Repositories Retrieved Successfully!")
        for repo in response:
            print(f"- {repo['key']} ({repo['type']})")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")


def get_storage_info_view():
    try:
        response = get_storage_info_control()
        print("\n✅ Storage Info Retrieved Successfully!\n")

        # Extract relevant storage details
        binaries_summary = response.get("binariesSummary", {})
        repositories_summary_list = response.get("repositoriesSummaryList", [])
        file_store_summary = response.get("fileStoreSummary", {})

        # Display Binary Storage Info
        print("🔹 Binaries Summary:")
        print("  --------------------")
        print(f"  - Total Binaries Count:    {binaries_summary.get('binariesCount', 'Unknown')}")
        print(f"  - Total Binaries Size:     {binaries_summary.get('binariesSize', 'Unknown')}")
        print(f"  - Total Artifacts Size:    {binaries_summary.get('artifactsSize', 'Unknown')}")
        print(f"  - Optimization:            {binaries_summary.get('optimization', 'Unknown')}")
        print(f"  - Items Count:             {binaries_summary.get('itemsCount', 'Unknown')}")
        print(f"  - Artifacts Count:         {binaries_summary.get('artifactsCount', 'Unknown')}")
        print()

        # Display Repositories Summary
        print("🔹 Repositories Summary:")
        print("  ------------------------")
        if repositories_summary_list:
            for repo in repositories_summary_list:
                print(f"  - Repo Key: {repo.get('repoKey', 'Unknown')}")
                print(f"    - Type:          {repo.get('repoType', 'Unknown')}")
                print(f"    - Folders Count: {repo.get('foldersCount', 'Unknown')}")
                print(f"    - Files Count:   {repo.get('filesCount', 'Unknown')}")
                print(f"    - Used Space:    {repo.get('usedSpace', 'Unknown')}")
                print(f"    - Percentage:    {repo.get('percentage', 'Unknown')}")
                print()

        else:
            print("    - No repositories found.\n")

        # Display File Store Summary
        print("🔹 File Store Summary:")
        print("  ----------------------")
        print(f"  - Storage Type:     {file_store_summary.get('storageType', 'Unknown')}")
        print(f"  - Storage Directory:{file_store_summary.get('storageDirectory', 'Unknown')}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")


def list_users_view():
    """
    Retrieves and displays a list of users from Artifactory in a presentable format.
    """
    try:
        print("\n📋 List of Users in Artifactory\n")

        # Step 1: Fetch the list of users
        try:
            users = list_users_control()
        except Exception as e:
            print(f"\n❌ Error fetching users: {e}\n")
            return

        # Step 2: Display the users in a presentable format
        if users:
            print("🔹 Artifactory Users:")
            print("  ----------------------------------------")
            for user in users:
                username = user.get("name", "Unknown")
                email = user.get("email", "Unknown")
                admin = user.get("admin", False)

                print(f"  - Username: {username}")
                print(f"    Email:    {email}")
                print(f"    Admin:    {'Yes' if admin else 'No'}")
                print("  ----------------------------------------")
        else:
            print("No users found.")

    except Exception as e:
        print(f"\n❌ Application Error: {e}\n")


def create_user_view():
    """
    Handles the user input and logic for creating a new user in Artifactory.
    """
    try:
        print("\n🛠 Create a New User\n")

        # Step 1: Prompt for user details
        username = input("Enter the username: ").strip()
        email = input("Enter the email address: ").strip()
        password = input("Enter the password: ").strip()

        # Step 2: Use InquirerPy for admin selection
        questions = [
            {
                "type": "list",
                "name": "is_admin",
                "message": "Should the user be an admin?",
                "choices": ["No", "Yes"],  # Options for admin status
            }
        ]
        answers = prompt(questions)
        is_admin = answers["is_admin"] == "Yes"  # Convert response to a boolean

        # Validate inputs
        if not username or not email or not password:
            print("\n❌ All fields are required to create a user.\n")
            return

        # Step 3: Call the API control function
        response = create_user_control(username, email, password, is_admin)

        # Step 4: Handle API response
        if response == 201: 
            print(f"\n✅ User '{username}' created successfully as {'Admin' if is_admin else 'Regular User'}!\n")
        else:
            print(f"\n❌ Error: {response['error']}\n")

    except Exception as e:
        print(f"\n❌ Application Error: {e}\n")


from InquirerPy import prompt

def delete_user_view():
    """
    Handles the user interface for deleting a user from Artifactory.
    Excludes the usernames 'tyrone', 'anonymous', and 'test-user' from the selection.
    """
    try:
        print("\n🛠 Delete a User\n")

        # Step 1: Fetch the list of users
        try:
            users = list_users_control()
        except Exception as e:
            print(f"\n❌ Error fetching users: {e}\n")
            return

        if not users:
            print("❌ No users found.")
            return

        # Exclude specific usernames
        excluded_users = {"tyrone", "anonymous", "test-user"}
        user_choices = [user["name"] for user in users if user["name"] not in excluded_users]

        if not user_choices:
            print("\n❌ No users available for deletion.\n")
            return

        # Step 2: Use InquirerPy to select a user from the filtered list
        questions = [
            {
                "type": "list",
                "name": "selected_user",
                "message": "Select the user to delete:",
                "choices": user_choices,
            }
        ]
        answers = prompt(questions)
        username = answers.get("selected_user")

        if not username:
            print("\n❌ No user selected.\n")
            return

        # Step 3: Confirm the deletion using InquirerPy
        confirm_questions = [
            {
                "type": "confirm",
                "name": "confirm_delete",
                "message": f"Are you sure you want to delete the user '{username}'?",
                "default": False,  # Default to 'No' for safety
            }
        ]
        confirm_answers = prompt(confirm_questions)
        if not confirm_answers["confirm_delete"]:
            print("\n❌ Deletion canceled.\n")
            return

        # Step 4: Call the API control function to delete the user
        response = delete_user_control(username)

        # Step 5: Handle the API response
        if "error" in response:
            print(f"\n❌ Error: {response['error']}\n")
        else:
            print(f"\n✅ {response['message']}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")



def create_repository_view():
    """
    Handles the user interface for creating a new repository in Artifactory.
    Uses InquirerPy to select repository type and package type.
    """
    try:
        print("\n🛠 Create a New Repository\n")

        # Step 1: Prompt for repository key (name)
        repo_key = input("Enter the repository key (name): ").strip()
        if not repo_key:
            print("\n❌ Repository key is required.\n")
            return

        # Step 2: Use InquirerPy to select repository type
        repo_type_question = [
            {
                "type": "list",
                "name": "repo_type",
                "message": "Select the repository type:",
                "choices": REPO_TYPE,
            }
        ]
        repo_type_answer = prompt(repo_type_question)
        repo_type = repo_type_answer.get("repo_type")

        # Step 3: Use InquirerPy to select package type
        package_type_question = [
            {
                "type": "list",
                "name": "package_type",
                "message": "Select the package type:",
                "choices": PACKAGE_TYPES,
            }
        ]
        package_type_answer = prompt(package_type_question)
        package_type = package_type_answer.get("package_type")

        # Step 4: Handle additional input for remote repositories
        remote_url = None
        if repo_type == "remote":
            remote_url = input("Enter the remote repository URL: ").strip()
            if not remote_url:
                print("\n❌ Remote URL is required for remote repositories.\n")
                return

        # Step 5: Call API to create repository
        response = create_repository_control(repo_key, repo_type, package_type, remote_url)

        # Step 6: Handle API response
        if "error" in response:
            print(f"\n❌ Error: {response['error']}\n")
        else:
            print(f"\n✅ {response['message']}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")



def update_repository_view():
    """
    Handles the process of updating an existing repository by:
    - Fetching a list of repositories from Artifactory.
    - Allowing the user to select a repository.
    - Prompting the user to provide updated values for specific properties.
    - Sending the update request to the Artifactory API.

    Returns:
        None
    """
    try:
        print("\n🔄 Update an Existing Repository\n")

        # Step 1: Fetch the list of repositories
        try:
            repositories = list_repositories_control()
        except Exception as e:
            print(f"\n❌ Error fetching repositories: {e}\n")
            return

        if not repositories:
            print("\n❌ No repositories found.\n")
            return

        # Step 2: Prepare repository options for the menu
        repo_choices = [
            f"{repo['key']} ({repo['type']})" for repo in repositories
        ]

        # Step 3: Display the menu to select a repository
        questions = [
            {
                "type": "list",
                "name": "selected_repo",
                "message": "Select the repository to update:",
                "choices": repo_choices,
            }
        ]
        answers = prompt(questions)

        # Get the selected repository key
        repo_key = answers.get("selected_repo").split(" ")[0]
        
        if not repo_key:
            print("\n❌ No repository selected.\n")
            return

        # Step 4: Prompt for new repository properties
        print("\nProvide values for the properties you want to update (leave blank to skip):\n")

        description = input("Enter the new description for the repository: ").strip()
        notes = input("Enter custom notes for the repository: ").strip()
        includes_pattern = input("Enter the includes pattern (e.g., '**/*'): ").strip()
        excludes_pattern = input("Enter the excludes pattern (e.g., '*.tmp'): ").strip()

        # Construct updates payload
        updates = {}
        if description:
            updates["description"] = description
        if notes:
            updates["notes"] = notes
        if includes_pattern:
            updates["includesPattern"] = includes_pattern
        if excludes_pattern:
            updates["excludesPattern"] = excludes_pattern

        if not updates:
            print("\n❌ No updates provided. Please enter at least one property to update.\n")
            return

        # Step 5: Call API to update repository
        response = update_repository_control(repo_key, updates)

        if "error" in response:
            print(f"\n❌ Error: {response['error']}\n")
        else:
            print(f"\n✅ {response['message']}\n")

    except Exception as e:
        print(f"\n❌ Error: {e}\n")



def login_view():
    """
    Handles CLI-based login to generate a token.

    Returns:
        str: The generated token or None if login fails.
    """
    try:
        print("\n🔑------------------------------🔑\n🔐     Login to Artifactory     🔐\n")

        # Step 1: Prompt for username and password
        questions = [
            {
                "type": "input",
                "name": "username",
                "message": "Enter your username:",
            },
            {
                "type": "password",
                "name": "password",
                "message": "Enter your password:",
            }
        ]
        answers = prompt(questions)
        username = answers["username"]
        password = answers["password"]

        if not username or not password:
            print("\n❌ Username and password are required for login.\n")
            return None

        response = login_control(username, password)

        if "token" in response:
            token = response["token"]
            print("\n✅ Login successful! Token generated.\n")
            return token
        else:
            print(f"\n❌ Login failed: {response['error']}\n")
            return None

    except Exception as e:
        print(f"\n❌ Application Error: {e}\n")
        return None