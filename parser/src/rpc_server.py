from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

def line_count(input):
    return len(input.split('\n'))

def parse_html(s):
    return '\n'+line_count(s) 

server = SimpleJSONRPCServer(('localhost', 8080))
server.register_function(parse_html, 'parse_html')
server.serve_forever()



