import sys
from cli.cli import Init

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'web':
        from web.app import app
        app.run(debug=True)
    else:
        app = Init()
        app.main_menu()