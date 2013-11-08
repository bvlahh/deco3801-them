<?php

class JsonRpcFault extends Exception {}

class JsonRpcClient {
    private $uri;

    /**
    * The JSON-RPC client which sends JSON-RPC requests, in the form of method calls,
    * to the Python JSON-RPC server. The response is either an array of error information
    * returned from the parser or an error message indicating that something has
    * gone wrong with the parser.
    *
    * @param string $uri The URI of the document we intend to parse.
    */
    public function __construct($uri) {
        $this->uri = $uri;
    }

    /**
    * Generates a random ID with a length of 16 characters from the ranges A-Z,
    * a-z and 0-9. Used as the ID for the JSON-RPC request.
    */
    private function generateId() {
        $chars = array_merge(range('A', 'Z'), range('a', 'z'), range(0, 9));
        $id = '';
        for($c = 0; $c < 16; ++$c)
            $id .= $chars[mt_rand(0, count($chars) - 1)];
        return $id;
    }

    /**
    * Attempts to create a valid JSON-RPC 2.0 request which calls a registered function on
    * the JSON-RPC server, returning the response from the server.
    *
    * @param   string    $name       The name of the remote function to call.  
    * @param   string[]  $arguments  An array of arguments to be passed to the function being called.
    * @return  string    A string representation of the JSON-RPC response that is returned
    * by the server. 
    */
    public function __call($name, $arguments) {
        $id = $this->generateId();

        $request = array(
            'jsonrpc' => '2.0',
            'method'  => $name,
            'params'  => $arguments,
            'id'      => $id
        );

        $jsonRequest = json_encode($request);

        $ctx = stream_context_create(array(
            'http' => array(
                'method'  => 'POST',
                'header'  => 'Content-Type: application/json\r\n',
                'content' => $jsonRequest
            )
        ));
        $jsonResponse = file_get_contents($this->uri, false, $ctx);

        if ($jsonResponse === false)
            throw new JsonRpcFault('file_get_contents failed', -32603);

        $response = json_decode($jsonResponse);

        if ($response === null)
            throw new JsonRpcFault('JSON cannot be decoded', -32603);

        if ($response->id != $id)
            throw new JsonRpcFault('Mismatched JSON-RPC IDs', -32603);

        if (property_exists($response, 'error'))
            throw new JsonRpcFault($response->error->message, $response->error->code);
        else if (property_exists($response, 'result'))
            return $response->result;
        else
            throw new JsonRpcFault('Invalid JSON-RPC response', -32603);
    }
}

?>
