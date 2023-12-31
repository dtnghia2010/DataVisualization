#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

# Name: 1
# Duong Trong Nghia ITITIU21256
# Ngo Thi Thuong ITCSIU21160
# Nguyen Pham Ky Phuong ITITIU21287
# Nguyen Anh Thang ITCSIU21233
# Purpose: Help to run the django project.
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'datavisual.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
