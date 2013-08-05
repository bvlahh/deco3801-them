from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

def parse_html(s):
    return s[:10]

server = SimpleJSONRPCServer(('localhost', 8080))
server.register_function(parse_html, 'parse_html')
server.serve_forever()



