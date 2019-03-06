# project imports
from ....script_engine.script_runner import run_script_list


# app action
def action(connection_tuple: tuple):
    results = run_script_list(
        connection_tuple,
        (
            'tensor_test',
            """
            rm -f app.py
            pip install tensorflow --user
            echo "import tensorflow" >> app.py
            echo "ses=tensorflow.Session()" >> app.py
            echo "ses.close()" >> app.py
            python3 app.py
            """

        ),
    )
    return 'ok'
