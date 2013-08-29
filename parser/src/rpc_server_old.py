from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

def line_count(input):
    if ( type(input) == unicode ):
        return len(input.split('\n'))
    else:
        return None

#def parse_html(s):
#    return line_count(s) 

def parse_html(s):
    return "%s\n" % s 

server = SimpleJSONRPCServer(('localhost', 8080))
server.register_function(parse_html, 'parse_html')
server.serve_forever()



