#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
<<<<<<< HEAD
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_project.settings")
=======
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "whateatver.settings")
>>>>>>> e67697016f5eccf4dfc41275c086a7a2f7c2ed10

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
