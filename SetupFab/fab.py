#!/usr/bin/python
import json
import random
import string
import sys

from fabric import Connection


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def _startConnection(host, user, port, password=None):
    c = Connection(host=host, user=user, port=port)
    return c


def _initialize(c):
    c.run('pip install tensorflow --user')
    c.run('echo "import tensorflow\nses=tensorflow.Session()\nimport time\ntime.sleep(1)\nses.close()" > test.py')
    test_result = c.run('python3 test.py')
    print(test_result.exited)
    print(test_result.ok)
    c.run('pip install jupyter notebook')
    c.run('apt install screen htop vim net-tools -y')
    c.run('apt install cmake libncurses5-dev libncursesw5-dev git -y;'
          'rm -rf nvtop;'
          'git clone https://github.com/Syllo/nvtop.git;'
          'mkdir -p nvtop/build;'
          'cd nvtop/build;'
          'cmake .. -DNVML_RETRIEVE_HEADER_ONLINE=True;'
          'make;'
          'make install')


def _create_user(c):
    username: str = id_generator(10)
    password = id_generator()
    users.append(User(username, password))
    c.run('adduser --disabled-password --force-badname --gecos "" ' + username)
    c.run('echo "{username}:{password}" | chpasswd'.format(
        username=username,
        password=password))
    return (username, password)
    # c.run('adduser ' + username + ' sudo')


def _ssh_config(c):
    c.run('echo -e "PasswordAuthentication yes\n$(cat /etc/ssh/sshd_config)" > "/etc/ssh/sshd_config"')
    c.run('service ssh reload')


def _run_jupyter(c, username, password, host, port):
    c = Connection(username + '@' + host + ':' + str(port),
                   connect_kwargs={"password": password})
    jup_port = random.randint(10000, 60000)
    c.run('nohup jupyter notebook --ip=0.0.0.0 --port='
          + str(jup_port)
          + ' --NotebookApp.token=\'\' '
            '--NotebookApp.password=\'\' '
            '0<&- &> '
            'my.admin.log.file &')
    return jup_port


users = []
server_info = {}
servers = []


def main(server_info_path):
    f = open(server_info_path, 'w+')
    server_file = open("server.json")
    # servers = json.load(server_file)
    count = 0
    for host, port in servers:
        user = 'root'
        # for host, user, port in [('ssh4.vast.ai', 'root', 16172), ('ssh4.vast.ai', 'root', 16174), ]:
        # for key in servers:
        #     item = servers[key]
        #     host = item['host']
        #     user = item['user']
        #     port = item['port']
        count += 1
        server_name = 'server' + str(count)
        server_info[server_name] = {}

        c = _startConnection(host=host, user=user, port=port)
        _initialize(c)
        server_info[server_name]['port'] = port
        server_info[server_name]['root_user'] = user
        server_info[server_name]['host'] = host
        server_info[server_name]['users'] = []
        for i in range(0, 2):
            user_username, user_password = _create_user(c)
            _ssh_config(c)
            jup_port = _run_jupyter(c, user_username, user_password, host, port)
            server_info[server_name]['users'].append(
                {'username': user_username, 'password': user_password, 'port': jup_port})
        c.close()

    json_data = json.dumps(server_info)
    f.write(json_data)
    f.close()


if __name__ == '__main__':
    args = sys.argv
    if '-all' in args:
        f = open(args[2], 'r')
        server_info_path = args[3]
        line = f.readline()
        while line:
            pars = line.split()
            servers.append((pars[3].split('@')[1], pars[2],))
            line = f.readline()
    elif len(args) == 3:
        key = 1
        while key < len(args) - 1:
            servers.append((args[key], args[key + 1]))
            key += 2
        server_info_path = args[len(args) - 1]
    else:                                                                    
        print('''
        -help
        -all [remote_host_file] [added_users_file]
        [remote_host remote_port ...] [added_users_file]
        ''')
        exit(0)
    main(server_info_path)
