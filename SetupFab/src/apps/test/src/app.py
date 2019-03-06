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
            pip3 install tensorflow
            echo "import tensorflow" >> app.py
            echo "ses=tensorflow.Session()" >> app.py
            echo "ses.close()" >> app.py
            python3 app.py
            """
        ),
        'rm app.py'
    )
    if results['ok']:
        if 'Created TensorFlow device' in results['tensor_test']:
            return str(connection_tuple[1]) + ' ' + str(connection_tuple[2]) + ' ok'
        return str(connection_tuple[1]) + ' ' + str(connection_tuple[2]) + ' failed'
    return str(connection_tuple[1]) + ' ' + str(connection_tuple[2]) + ' script error on : ' + str(
        results['failed_command'])
