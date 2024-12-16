import os
import time
from InquirerPy import inquirer
from views import *
import argparse


def show_help():
    """
    Displays the menu options and descriptions for the CLI.
    """
    help_text = """
    Artifactory CLI - Manage your JFrog Artifactory instance via its API.

    Usage:
      artifactory-cli [--help]

    Options:
      --help                     Show this help menu.

    Menu Options:
      1. System Ping             Check the health status of the Artifactory system.
      2. Get System Version      Retrieve the current version of the Artifactory system.
      3. List Users              List all users in the Artifactory instance.
      4. Create User             Create a new user in the Artifactory instance.
      5. Delete User             Delete an existing user from the Artifactory instance.
      6. List Repositories       List all repositories in the Artifactory instance.
      7. Create Repository       Create a new repository (local, remote, or virtual).
      8. Update Repository       Update an existing repository's properties.
      9. Get Storage Info        Retrieve storage information for Artifactory.
    """
    print(help_text)

def login():
    while True:
        token = login_view()
        if token:
            print("Token stored in memory for session.")
            break

def main_menu():
    while True:
        # Display menu options
        choice = inquirer.select(
            message="""📺📺         ⚙️         📺📺
            \n  ✨✨  Artifactory CLI  ✨✨ 
            \n  📇📇     Main Menu     📇📇 
            \n Select Option:""",
            choices=[
                "System Ping",
                "System Version",
                "Get Storage Info",
                "List Users",
                "Create User",
                "Delete User",
                "List Repositories",
                "Create Repository",
                "Update Repository",
                "Exit",
            ],
            default="System Ping",
        ).execute()
        
        if choice == "System Ping":
            system_ping_view()
            os.system('pause') 
            os.system('cls') 
            
        elif choice == "System Version":
            get_system_version_view()
            os.system('pause')
            os.system('cls')
            
        elif choice == "Get Storage Info":
            get_storage_info_view()
            os.system('pause') 
            os.system('cls')
        
        elif choice == "List Users":
            list_users_view()
            os.system('pause')
            os.system('cls')
                    
        elif choice == "Create User":
            create_user_view()
            os.system('pause')
            os.system('cls')
            
        elif choice == "Delete User":
            delete_user_view()
            os.system('pause') 
            os.system('cls')
            
        elif choice == "List Repositories":
            list_repositories_view()
            os.system('pause') 
            os.system('cls')
            
        elif choice == "Create Repository":
            create_repository_view()
            os.system('pause') 
            os.system('cls')
            
        elif choice == "Update Repository":
            update_repository_view()
            os.system('pause') 
            os.system('cls')
            
        elif choice == "Exit":
            print("Exiting... Goodbye!")
            time.sleep(1.5)
            break


def main():
    """
    Main entry point for the CLI application.
    Handles command-line arguments and displays the menu.
    """
    parser = argparse.ArgumentParser(add_help=False)  # Disable default help
    parser.add_argument("--help", action="store_true", help="Show help menu")
    args = parser.parse_args()

    if args.help:
        show_help()
        return
    
    try:
        login()
        main_menu()
        
    except KeyboardInterrupt:
        print("\n\n👋 Application terminated by user (Ctrl+C). Goodbye!")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}\n")

if __name__ == "__main__":
    main()
