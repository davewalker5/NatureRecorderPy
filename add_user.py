"""
Add a user to the database
"""

from src.naturerec_model.logic import create_user


if __name__ == "__main__":
    username = input("Username: ").strip()
    if username:
        password = input("Password: ").strip()
        if password:
            user = create_user(username, password)
            print(f"Created user '{user.username}'")
