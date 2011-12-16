import ConfigParser, re
from fabric.api import run
from fabric.tasks import execute

config = ConfigParser.ConfigParser()
config.readfp(open('examples/hosts.txt'))

groups = dict((k, v.split(',')) for k, v in config.items('groups'))

def list_workers():
    try:
        r = run('ps -A | grep worker')
    except:
        return []
    processes = []
    for line in r.splitlines():
        m = re.match('^\s*(\d+)[^a-z]+(\w+)', line)
        if m:
            pid, nm = m.groups()
            processes.append((nm, pid))
    return processes

def kill_workers_on_host():
    processes = list_workers()
    for nm, pid in processes:
        run('kill ' + pid)

def kill_workers():
    for group in ['v500']:
        print "KILLING WORKERS ON %s" % (group,)
        for host in groups[group]:
            execute(kill_workers_on_host, host=host)
            
kill_workers()
