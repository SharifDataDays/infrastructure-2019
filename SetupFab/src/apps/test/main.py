# project imports
from ...main import set_file_paths
from ...main import run_for_all

# app imports
from .src import app as test_app


# CLI --help & invalid command message
def help_command():
    command_name = 'test'
    print(
        f"""\033[34m{command_name} available options:\033[0m
        \033[34m*\033[0m --all [ hosts_file= files/hosts.txt] [ output_file= output/report.txt ]
        \033[34m*\033[0m --single [ host_ip/url ] [ host_port ] [ user= None ] -> prints report in stdout

    \033[34musage :\033[0m {command_name} [ options ... ]"""
    )


# command interpreter
def command_interpreter(args: list):
    if len(args) < 1 or '--help' == args[0]:
        help_command()
    else:
        # checking subcommand options
        if '--all' in args:
            run_for_all(
                test_app.action,
                *set_file_paths(
                    args[args.index('--all') + 1:args.index('--all') + 3]
                ),
            )
        elif '--single' in args:
            pass
        else:
            help_command()

    exit(0)
