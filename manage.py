#!/usr/bin/env python
import sys

if __name__ == "__main__":
    if '--settings' not in sys.argv:
        print("""
    Couldn't load settings. You must add --settings <settings_python_path> into command line.
    Example:
    \tpython manage.py --settings boxing_app.app_settings <args>
    \tpython manage.py --settings boxing_console.console_settings <args>
    """)
        exit(1)

    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 3.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
    except ImportError:
        pass
    execute_from_command_line(sys.argv)
