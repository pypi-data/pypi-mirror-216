import argparse
from tools.init_task.scraper import main as init_task, show_help
from tools.checker.index import shell_main as checker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-init", nargs="?", const="", help="Run the init-task tool")
    parser.add_argument("-checker", nargs="+", help="Run the checker tool")
    args = parser.parse_args()

    if args.init is not None:
        init_task(args.init)
    elif args.checker:
        checker(*args.checker)


if __name__ == "__main__":
    main()
