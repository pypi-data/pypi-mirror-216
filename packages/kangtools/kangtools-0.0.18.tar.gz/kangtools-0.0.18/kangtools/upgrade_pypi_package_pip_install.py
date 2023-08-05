import os
import shutil
import subprocess
import time
import argparse
import re

def update_setup_version():
    with open('setup.py', 'r') as f:
        content = f.read()

    version_match = re.search(r"version='(.*)'", content)
    if version_match is None:
        raise Exception("Could not find version in setup.py")

    version_parts = list(map(int, version_match.group(1).split('.')))
    version_parts[-1] += 1

    new_version = '.'.join(map(str, version_parts))
    content = re.sub(r"version='(.*)'", "version='{}'".format(new_version), content)

    with open('setup.py', 'w') as f:
        f.write(content)

    print(f'Updated setup.py to version {new_version}')
    return new_version

def remove_old_distributions():
    print("Removing old distributions...")
    if os.path.exists('./dist'):
        shutil.rmtree('./dist')

def build_new_distribution():
    print("Building new distribution...")
    subprocess.check_call(['python3', 'setup.py', 'sdist', 'bdist_wheel'])

def upload_new_distribution():
    print("Uploading new distribution to PyPI...")
    subprocess.check_call(['twine', 'upload', 'dist/*'])

def uninstall_old_version(package_name):
    print(f"Uninstalling old version of the {package_name}...")
    subprocess.check_call(['pip3', 'uninstall', '-y', package_name])

def clear_pip_cache():
    print("Clearing pip cache...")
    subprocess.check_call(['pip3', 'cache', 'purge'])

def install_new_version(package_name, new_version):
    print(f"Attempting to install new version: {new_version}")
    max_attempts = 3
    delay_between_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            subprocess.check_call(['pip3', 'install', '--no-cache-dir', f'{package_name}=={new_version}'])
            print("New version of the package successfully installed!")
            break
        except subprocess.CalledProcessError:
            if attempt == max_attempts:
                print("Attempt limit reached. Please check your command or network status.")
                break
            else:
                print(f"Installation failed, waiting {delay_between_attempts} seconds before attempt number {attempt}...")
                time.sleep(delay_between_attempts)

def main():
    parser = argparse.ArgumentParser(description="""
        This script performs several steps to update, build, upload and install a new version of a specified Python package. Here are the detailed steps:

        1. Updates the version number in the setup.py file.
        2. Removes the old distributions in the 'dist' directory.
        3. Builds a new distribution of the package.
        4. Uploads the new distribution to PyPI.
        5. Uninstalls the old version of the package.
        6. Waits for a while for the server to update to the latest version.
        7. Clears the pip cache.
        8. Tries to install the new version of the package.
    """)
    parser.add_argument('package_name', type=str, help='The name of the package to update, build, upload and install')
    args = parser.parse_args()

    if args.package_name is None:
        print("Please provide the name of the package as an argument. Example usage:")
        print("python ./clear_clean_go_upgrage/clean_prj_update_build_twine_pip_install_pipline.py your_package_name")
        return

    new_version = update_setup_version()
    remove_old_distributions()
    build_new_distribution()
    upload_new_distribution()
    uninstall_old_version(args.package_name)
    time.sleep(2)  # wait for the server to update to the latest version
    clear_pip_cache()
    install_new_version(args.package_name, new_version)
    print("All done!")

if __name__ == "__main__":
    main()
