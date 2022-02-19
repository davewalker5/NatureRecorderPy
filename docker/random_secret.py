import os
import sys


def get_project_path():
    """
    Return the path to the project root folder

    :return: The path to the project root folder
    """
    return os.path.dirname(os.path.dirname(__file__))


def set_web_app_secret():
    """
    Replace the secret key in the web application Python source file
    """
    file = os.path.join(get_project_path(), "data", ".env")
    with open(file, mode="wt", encoding="utf-8") as f:
        f.writelines([
            f"SECRET_KEY={os.urandom(32).hex()}\n"
        ])


if __name__ == "__main__":
    try:
        set_web_app_secret()
        sys.exit(0)

    except BaseException as e:
        print(f"Error: {e}")
        sys.exit(1)
