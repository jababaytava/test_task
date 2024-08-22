import sys
import subprocess


def install_requirements():
    print("Installing requirements...")
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    )


def apply_migrations():
    print("Applying migrations...")
    subprocess.check_call([sys.executable, "manage.py", "migrate"])


def create_superuser():
    print("Creating superuser...")
    subprocess.check_call([sys.executable, "manage.py", "createsuperuser"])


def load_fixtures():
    print("Loading fixtures...")
    subprocess.check_call(
        [sys.executable, "manage.py", "loaddata", "initial_tests.json"]
    )


def main():
    install_requirements()
    apply_migrations()
    create_superuser()
    load_fixtures()
    print("Setup completed successfully!")


if __name__ == "__main__":
    main()
