import os
import subprocess
import yaml

def add_partner(base_directory, group, partner, access_type):
    group_file_path = os.path.join(base_directory, "groups", "TestOfAutomation.yml")
    repo_file_path = os.path.join(base_directory, "repos", "Example_Repo.yml")
    
    group_data = read_yaml(group_file_path)
    repo_data = read_repo_yaml(repo_file_path)
    
    full_group_name = f"{group}_{access_type}"

    # Update group file
    update_group_file(group_data, full_group_name, partner)

    # Remove from other access types in group file
    remove_from_other_access_types(group_data, group, partner, access_type)

    # Update repo file
    update_repo_file(repo_data, group, access_type)

    write_yaml(group_file_path, group_data)
    write_repo_yaml(repo_file_path, repo_data)
    print(f"Partner {partner} added to {full_group_name}")

def update_group_file(group_data, full_group_name, partner):
    if full_group_name not in group_data:
        group_data[full_group_name] = []
    if partner not in group_data[full_group_name]:
        group_data[full_group_name].append(partner)

def remove_from_other_access_types(group_data, group, partner, current_access_type):
    all_access_types = ["read", "triage", "write"]
    for access_type in all_access_types:
        if access_type != current_access_type:
            group_name = f"{group}_{access_type}"
            if group_name in group_data:
                group_data[group_name].remove(partner)
                if len(group_data[group_name]) == 0:
                    del group_data[group_name]

def update_repo_file(repo_data, group, access_type):
    full_group_name = f"{group}_{access_type}"
    if "Example_Repo" not in repo_data:
        repo_data["Example_Repo"] = {}
    
    repo_group = repo_data["Example_Repo"]
    repo_group[full_group_name] = {
        "type": "group",
        "permissions": access_type
    }

def remove_partner(base_directory, group, partner, access_type):
    group_file_path = os.path.join(base_directory, "groups", "TestOfAutomation.yml")
    repo_file_path = os.path.join(base_directory, "repos", "Example_Repo.yml")
    
    group_data = read_yaml(group_file_path)
    repo_data = read_repo_yaml(repo_file_path)
    
    full_group_name = f"{group}_{access_type}"

    if full_group_name in group_data:
        if partner in group_data[full_group_name]:
            group_data[full_group_name].remove(partner)
            if len(group_data[full_group_name]) == 0:
                del group_data[full_group_name]
                # Also remove from repo file if group is empty
                if "Example_Repo" in repo_data:
                    repo_data["Example_Repo"].pop(full_group_name, None)
            write_yaml(group_file_path, group_data)
            write_repo_yaml(repo_file_path, repo_data)
            print(f"Partner {partner} removed from {full_group_name}")
        else:
            print(f"Partner {partner} not found in {full_group_name}")
    else:
        print(f"Group {full_group_name} not found")

def read_yaml(file_path):
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, 'r') as file:
        return yaml.safe_load(file) or {}

def read_repo_yaml(file_path):
    if not os.path.exists(file_path):
        return {}
    
    with open(file_path, 'r') as file:
        return yaml.safe_load(file) or {}

def write_yaml(file_path, data):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def write_repo_yaml(file_path, data):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def run_git_command(base_directory, arguments):
    process = subprocess.Popen(
        ["git"] + arguments.split(),
        cwd=base_directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output, error = process.communicate()

    if process.returncode != 0:
        raise Exception(f"Git command failed with error: {error.decode()}")

def push_to_github(base_directory, commit_message):
    try:
        run_git_command(base_directory, "add .")
        run_git_command(base_directory, f"commit -m \"{commit_message}\"")
        run_git_command(base_directory, "push")
        print("Changes pushed to GitHub successfully.")
    except Exception as ex:
        print(f"An error occurred while pushing to GitHub: {ex}")

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]

    if len(args) != 5:
        print("Usage: script.py <Add|Remove> <group> <partner> <accessType> <commitMessage>")
        sys.exit(1)

    add_or_remove = args[0]
    group = args[1]
    partner = args[2]
    access_type = args[3]
    commit_message = args[4]

    base_directory = r"C:\Users\User\Documents\Automation_Test\AutomationTest"

    if add_or_remove == "Add":
        add_partner(base_directory, group, partner, access_type)
    elif add_or_remove == "Remove":
        remove_partner(base_directory, group, partner, access_type)
    else:
        print("Invalid command. Please use 'Add' or 'Remove'.")

    push_to_github(base_directory, commit_message)
