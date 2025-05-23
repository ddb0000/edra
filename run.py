import os
import subprocess
import sys

# Configuration: List of projects/directories to scan for scripts.
# Each entry is a dictionary:
#   "name": A display name for this group of scripts (e.g., "Eldoria Game").
#   "project_root_subdir": The subdirectory relative to this runner script 
#                          where the project root is located (e.g., "eldoria-pygame").
#                          The CWD for running scripts from this group will be this directory.
#   "scripts_subdir": The subdirectory within 'project_root_subdir' that 
#                     contains the Python scripts (e.g., "scripts").
CONFIGURED_TARGETS = [
    {
        "name": "Eldoria Pygame",
        "project_root_subdir": "eldoria-pygame",
        "scripts_subdir": "scripts"
    },
    {
        "name": "gg",
        "project_root_subdir": "gg",
        "scripts_subdir": "scripts"
    },
]

def main():
    runner_dir = os.path.abspath(os.path.dirname(__file__))
    
    all_runnable_scripts = [] 

    for target_config in CONFIGURED_TARGETS:
        project_root_subdir = target_config["project_root_subdir"]
        scripts_subdir_in_project = target_config["scripts_subdir"]
        
        project_root_abs_path = os.path.join(runner_dir, project_root_subdir)
        scripts_dir_abs_path = os.path.join(project_root_abs_path, scripts_subdir_in_project)

        target_display_name_prefix = target_config.get("name", project_root_subdir)

        if not os.path.isdir(project_root_abs_path):
            print(f"Warning: Project root directory not found for '{target_display_name_prefix}': {project_root_abs_path}")
            continue
        if not os.path.isdir(scripts_dir_abs_path):
            print(f"Warning: Scripts directory not found for '{target_display_name_prefix}': {scripts_dir_abs_path}")
            continue

        for item in os.listdir(scripts_dir_abs_path):
            if item.endswith(".py") and os.path.isfile(os.path.join(scripts_dir_abs_path, item)):
                script_path_in_project = os.path.join(scripts_subdir_in_project, item)
                
                display_name = f"[{target_display_name_prefix}] {item}"
                all_runnable_scripts.append({
                    "display_name": display_name,
                    "script_to_execute": script_path_in_project, 
                    "cwd": project_root_abs_path                 
                })
    
    if not all_runnable_scripts:
        print("No runnable Python scripts found in the configured locations.")
        print("Please check the CONFIGURED_TARGETS in the runner script (run.py) and ensure the directories exist.")
        return

    print("Available scripts to run:")
    all_runnable_scripts.sort(key=lambda x: x["display_name"])

    for i, script_info in enumerate(all_runnable_scripts):
        print(f"  {i + 1}. {script_info['display_name']}")
    print("  0. Exit")

    while True:
        try:
            choice_str = input(f"Enter the number of the script to run (1-{len(all_runnable_scripts)}, or 0 to exit): ")
            choice_num = int(choice_str)

            if choice_num == 0:
                print("Exiting.")
                break
            
            if 1 <= choice_num <= len(all_runnable_scripts):
                selected_script_info = all_runnable_scripts[choice_num - 1]
                
                script_to_execute = selected_script_info["script_to_execute"]
                cwd_for_script = selected_script_info["cwd"]
                display_name = selected_script_info["display_name"]
                
                print(f"\nRunning {display_name}...")
                print(f"  Command: {sys.executable} {script_to_execute}")
                print(f"  Working Directory: {cwd_for_script}\n")
                
                process = subprocess.run(
                    [sys.executable, script_to_execute],
                    cwd=cwd_for_script,
                    check=False 
                )
                
                print(f"\n'{display_name}' finished with exit code {process.returncode}.")
                break 
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(all_runnable_scripts)}, or 0.")
        except ValueError:
            print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user. Exiting.")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            break

if __name__ == "__main__":
    main()