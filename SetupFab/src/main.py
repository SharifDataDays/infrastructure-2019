# General imports
import fabric


# is executed once to initialize fabric state settings
def init_fabric():
    pass


# load hosts from a file
def read_hosts_file(file_path: str) -> list:
    """
    reads a txt file containing ssh commands formatted like:
        ssh -p <port_number> hostname -L <tunnel>
    and returns a list of tuples of ( hostname, port_number, tunnel )
    """

    try:
        f = open(file_path, 'r')
    except:
        print('\033[32munable to load hosts list : \033[0m', file_path)
        return []

    hosts = []
    line = f.readline()
    while line:
        # replacing returns
        line = line.replace('\n', '')

        pars = line.split(' ')

        port_number = 22
        tunnel = None

        # format: ssh -p <port_number> hostname -L <tunnel>
        del pars[pars.index('ssh')]
        try:
            port_number = pars[pars.index('-p') + 1]
            del pars[pars.index('-p'):pars.index('-p') + 2]

            tunnel = pars[pars.index('-L') + 1]
            del pars[pars.index('-L'):pars.index('-L') + 2]
        except:
            pass
        hostname = pars[0]

        hosts.append((hostname, port_number, tunnel))
        line = f.readline()

    return hosts


def write_report_file(file_path: str, report_list: list):
    try:
        file = open(file_path, 'w+')
        file.writelines(report_list)
        file.close()
    except Exception:
        print('\033[31munable to open reports file : \033[0m', file_path)
        print('\033[32m\n\nreport : \033[0m\n', end='')
        print(*report_list, sep='\n')


# start connection
def start_connection(host_name: str, port_number: str, username: str = 'root', password=None) -> tuple:
    """
    Trys to start a new ssh connection and on success returns
    tuple containing ( fabric.Connection object, host_name, port_name, username)
    else returns None
    """
    hostname = username + '@' + host_name

    try:
        connection_object = fabric.Connection(host=hostname, port=int(port_number))
    except Exception:
        return None

    return connection_object, host_name, port_number, username


# sets file paths and their default values
def set_file_paths(args: list) -> tuple:
    hosts_file_path = './files/hosts.txt'
    report_file_path = './files/output/report.txt'

    try:
        hosts_file_path = args[0]
        report_file_path = args[1]
    except Exception:
        pass

    return hosts_file_path, report_file_path


# run for all
def run_for_all(action: callable, hosts_file_path: str, reports_path: str, multi_processed=False):
    hosts = read_hosts_file(hosts_file_path)
    connection_list = []
    reports = []

    # creating ssh connections
    for host in hosts:
        connection_tuple = start_connection(host[0], host[1])
        if connection_tuple:
            connection_list.append(connection_tuple)
        else:
            print('\033[31munable to connect to :  host \033[0m', host[0], '\033[31m port  \033[0m', host[1])
            reports.append((host[0], host[1], '-> test : connection creation error'))

    for connection in connection_list:
        reports.append(action(connection))

    write_report_file(reports_path, reports)
