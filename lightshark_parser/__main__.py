try:
    from main import main
except (NameError, FileNotFoundError, ModuleNotFoundError):
    from lightshark_parser.main import main

main()
