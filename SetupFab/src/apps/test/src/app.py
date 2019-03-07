# project imports
from ....script_engine.script_runner import run_script_list


# app action
def action(connection_tuple: tuple):
    results = run_script_list(
        connection_tuple,
        """
        adduser --disabled-password --force-badname --gecos "" datadays
        su datadays
        pip3 install --ignore-installed tornado==4.5 --user
        pip3 install tensorflow --user
        screen -S jup
        jupyter notebook --ip=0.0.0.0 --port=8321 --NotebookApp.token= --NotebookApp.password=
        screen -d jup
        exit
        """
    )

    if results['ok']:
        return str(connection_tuple[1]) + ' ' + str(connection_tuple[2]) + ' ok'
        # return str(connection_tuple[1]) + ' ' + str(connection_tuple[2]) + ' failed'
    return str(connection_tuple[1]) + ' ' + str(connection_tuple[2]) + ' script error on : ' + str(
        results['failed_command'])
