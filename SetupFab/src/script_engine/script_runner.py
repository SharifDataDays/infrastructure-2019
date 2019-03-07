def run_script_list(connection_tuple: tuple, *command_sets, list_results=True) -> dict:
    """
    gets a conneciton_tuple -> (fabric Connection object, hostname, port_number, tunnel)
    and run (multi-line) commands and returns a list of results

    """
    results = {
        'ok': True
    }
    connection = connection_tuple[0]
    for index, command_set in enumerate(command_sets):
        try:
            name, commands = command_set
            commands = commands.split('\n')
        except Exception:
            name = index
            commands = command_set.split('\n')

        if list_results:
            results[name] = []

        # running command set
        res = ''
        for command in commands:
            command = command.strip()
            if not command:
                continue
            print('\033[34m*\033[0m ', command)
            res = str(connection.run(command))
            try:
                pass
            except Exception:
                results['ok'] = False
                results['failed_command'] = command
                return results

            if list_results:
                results[name].append(res)

        if not list_results:
            results[name] = res

    return results
