import re
import subprocess
import sys

def read_requirements(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()

def write_requirements(file_path, requirements):
    with open(file_path, 'w') as file:
        file.writelines(requirements)

def uninstall_package(package_name):
    subprocess.run([sys.executable, '-m', 'pip', 'uninstall', package_name, '-y'], check=True)

def install_package(package_name):
    subprocess.run([sys.executable, '-m', 'pip', 'install', package_name], check=True)

def get_package_name(requirement):
    # Extract the package name from the requirement string
    return requirement.split('@')[0].strip()

def is_local_path(requirement):
    return re.search(r'\s@ file://', requirement) is not None

def main():
    requirements_file = 'requirements.txt'
    requirements = read_requirements(requirements_file)
    cleaned_requirements = []

    for requirement in requirements:
        if is_local_path(requirement):
            package_name = get_package_name(requirement)
            print(f'Found local path for package {package_name}. Reinstalling from PyPI...')
            try:
                uninstall_package(package_name)
                install_package(package_name)
                # Get the correct version from pip freeze and add it to the cleaned requirements
                result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], capture_output=True, text=True, check=True)
                updated_requirements = result.stdout.splitlines()
                for updated_req in updated_requirements:
                    if updated_req.startswith(package_name + '=='):
                        cleaned_requirements.append(updated_req + '\n')
                        break
            except subprocess.CalledProcessError as e:
                print(f"Error reinstalling package {package_name}: {e}")
        else:
            cleaned_requirements.append(requirement)

    # Write the cleaned requirements back to the file
    write_requirements(requirements_file, cleaned_requirements)
    print("Updated requirements.txt")

if __name__ == '__main__':
    main()

