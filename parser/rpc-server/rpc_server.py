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
 
# Function for terminating all child processes before we exit
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

# Generates an array of errors found after parsing the given base64 input. This
# is our main entry into the heavily modified html5lib parser.
def parse_html(input):
    parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))

    text = base64.b64decode(input["document"])
    
    files = input.get("files")
    filename = input.get("filename")

    # If we weren't given any files, set to None (they come through by default as empty strings
    if files == []: 
        files = None
        filename = None

    try:
        document = parser.parse(text, files=files, filename=filename)
    except: 
        # We got here because of a fatal parseError, 
        # which we threw in specific cases to cease parsing immediately
        pass

    if not ascii_only(text):
        parser.parseError("html-contains-non-ascii-characters")

    return parser.parseErrors()

# Determines if file contains on ascii content
# returns true if ascii only, else false
def ascii_only(input):
    try:
        input.decode('ascii')
        return True
    except UnicodeDecodeError:
        return False

# Forks a number of RPC servers to list on port 8080 and handle
# RPC calls to the parser. The function parse_html is registered
# for RPC calls.
def main():
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
    sys.exit(main())
