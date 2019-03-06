

# CLI --help & invalid command message
def help_command():
    command_name = 'setup'
    print(
        f'''\033[34m{command_name} available options:\033[0m
        \033[34m*\033[0m --all [ hosts_file= files/hosts.txt] [ output_file= output/report.txt ]
        \033[34m*\033[0m --single [ host_ip/url ] [ host_port ] [ user= None ] -> prints report in stdout

    \033[34musage :\033[0m {command_name} [ options ... ]'''
    )


# command interpreter
def command_interpreter(args: list):
    if len(args) < 1 or '--help' == args[0]:
        help_command()
    else:
        # checking subcommand options
        if '--all' in args:
            pass
        elif '--single' in args:
            pass
        else:
            help_command()

    exit(0)

