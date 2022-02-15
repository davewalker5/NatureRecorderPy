import os
import shutil
import sys


def get_project_path():
    """
    Return the path to the project root folder

    :return: The path to the project root folder
    """
    return os.path.dirname(os.path.dirname(__file__))


def get_docker_path():
    """
    Get the path to the project's Docker build folder

    :return: The path to the docker folder
    """
    return os.path.join(get_project_path(), "docker")


def get_web_app_source_path():
    """
    Return the path to the folder containing the source for the web app

    :return: The path to the web app source folder
    """
    return os.path.join(get_project_path(), "src", "naturerec_web")


def replace_secret(file_content):
    """
    Replace the secret key placeholder in the specified text with a new, random, secret key

    :param file_content: File content as a string
    :return: Updated file content
    """
    secret_key = os.urandom(32).hex()
    return file_content.replace("some secret key", secret_key)


def set_web_app_secret():
    """
    Replace the secret key in the web application Python source file
    """
    # Get the source and backup file
    file = os.path.join(get_web_app_source_path(), "naturerecorder.py")
    backup = os.path.join(get_docker_path(), "naturerecorder.py")

    # Check the backup file doesn't already exist
    if os.path.exists(backup):
        raise FileExistsError(f"{backup} already exists")

    # Backup the original file and make sure it's backed up OK
    shutil.copy(file, backup, follow_symlinks=False)
    if not os.path.exists(backup):
        raise FileNotFoundError(f"{backup} not found")

    # Read the content of the original file
    with open(file, mode="rt", encoding="utf-8") as f:
        file_content = f.read()

    # Replace the secret key with a new random key and rewrite the file
    updated_content = replace_secret(file_content)
    with open(file, mode="wt", encoding="utf-8") as f:
        f.write(updated_content)


if __name__ == "__main__":
    try:
        set_web_app_secret()
        sys.exit(0)

    except (FileExistsError, FileNotFoundError) as e:
        print(f"Error: {e}")
        sys.exit(1)
