import os
import signal
import sys 
import errno
import time
 
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
 
# Child processes
_PIDS = []
 
def _kronos(signum, frame):
    # Handle child processes
    for pid in _PIDS:
        try:
            os.kill(pid, signum)
        except OSError, e:
            if e.errno == errno.ESRCH:
                _PIDS.remove(pid)
 
    # Wait on child processes
    while len(_PIDS):
        pid, rc = os.waitpid(-1, 0)
        _PIDS.remove(pid)
 
    # exit non-zero to signal abnormal termination
    sys.exit(1)
 
def _gogentle(signum, frame):
    # Prevent keyboard interrupt error
    os._exit(1)

def line_count(input):
    if ( type(input) == unicode ):
        time.sleep(10)
        return len(input.split('\n'))
    else:
        return None

# Parsing function
def parse_html(s):
    return line_count(s) 
 
# server
def main(name, *argv):
    global _PIDS
 
    # JSON-RPC over HTTP on INET socket localhost:8080
    # under the hood, this calls `socket.bind` then `socket.listen`
    s = SimpleJSONRPCServer(('localhost', 8080))
 
    # Register the functions to be called by the PHP client
    s.register_function(parse_html, 'parse_html')
 
    # simple pre-fork server, fork before accept
    for i in range(5):
        # fork our current process
        pid = os.fork()
 
        # if we are the child fork ... 
        if 0 == pid:
            # die without unhandled exception
            for signum in ( signal.SIGINT, signal.SIGTERM, ):
                signal.signal(signum, _gogentle)
 
            # Start server
            s.serve_forever()
            os._exit(0)
 
        # if we are the papa fork
        else:
            _PIDS.append(pid)
 
    # setup signal relaying for INT and TERM
    for signum in ( signal.SIGINT, signal.SIGTERM, ):
        signal.signal(signum, _kronos)
 
    # wait on the kids
    while len(_PIDS):
        pid, rc = os.waitpid(-1, 0)
        _PIDS.remove(pid)
 
    return 0
 
if __name__ == '__main__':
    sys.exit(main(*sys.argv))