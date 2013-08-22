import os
import signal
import sys 
import errno
import time
import base64
 
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
import html5lib
from html5lib import treewalkers
from html5lib import treebuilders
 
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

# Generates an array of errors found after parsing the given base64 input.
def parse_base64(input):
    parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))
    document = parser.parse(base64.b64decode(input["document"]))
    return parser.parseErrors()

def line_count(input):
    if ( type(input) == unicode ):
        time.sleep(10)
        return len(input.split('\n'))
    else:
        return None

# Basic line count test
def parse_html(s):
    return parse_base64(s)

# Registered function for parsing direct input.
def parse_direct_input(s):
    return parse_base64(s)
 
# Server processing
def main(name, *argv):
    global _PIDS
 
    # Create a new JSON-RPC server on localhost:8080
    s = SimpleJSONRPCServer(('localhost', 8080))
 
    # Register the functions to be called by the PHP client
    s.register_function(parse_html, 'parse_html')
 
    # Creates 5 child server processes
    for i in range(5):
        # Fork current process
        pid = os.fork()
 
        # Child fork:
        if 0 == pid:
            # Prevent interrupt messages
            for signum in ( signal.SIGINT, signal.SIGTERM, ):
                signal.signal(signum, _gogentle)
 
            # Start server
            s.serve_forever()
            os._exit(0)
 
        # Parent:
        else:
            _PIDS.append(pid)
 
    # Handle interrupt signals quietly
    for signum in ( signal.SIGINT, signal.SIGTERM, ):
        signal.signal(signum, _kronos)
 
    # Wait for child processes
    while len(_PIDS):
        pid, rc = os.waitpid(-1, 0)
        _PIDS.remove(pid)
 
    return 0
 
if __name__ == '__main__':
    sys.exit(main(*sys.argv))