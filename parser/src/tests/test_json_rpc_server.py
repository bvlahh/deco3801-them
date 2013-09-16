from __future__ import absolute_import, division, unicode_literals

#from . import support
import unittest
import time
import jsonrpclib
from multiprocessing import Pool
from jsonrpclib import Server
import httplib
import simplejson as json
import base64

"""
Calls the test_concurrency method on the server. Required to be external from the
TestJsonServer class as it was causing a "pickling" error when used as a method.
"""
def getTime(time):
        return Server("http://localhost:8080").test_concurrency(time)

class TestJsonServer(unittest.TestCase):
    """
    Provides a number of test cases related to the functionality of the json 
    rpc server.

    These tests require that the server is currently running. The first
    test checks that the server is running.
    """

    def setUp(self):
        self.startTime = time.time()

    def resetCurrentTime(self):
        self.startTime = time.time()

    def getExecutionTimes(self, numProcesses):
        """
        Attempts to call the getTime function with startTime as the 
        only argument in a concurrent manner using numProcesses as the
        number of concurrent calls to make. The resulting times returned
        by the remote function, test_concurrency, are added to a list
        and returned.

        The timeout for each call attempt is currently set to 5 seconds.
        This will only allow for numProcesses to go up to 10. After that
        the processing times at the server side will trigger the timeout
        and result in an exception being thrown.
        """

        results = []
        times = []

        pool = Pool(processes=numProcesses)
        for i in range(numProcesses):
            results.append(pool.apply_async(getTime, (self.startTime,)))

        for result in results:
            times.append(result.get(timeout=5))

        return times

    def test_client(self):
        """
        Test that the server is currently running. Required for the
        remaining server tests to run.

        Input: Attempt to execute a known function on the server.

        Expected Result: No exception being raised, implying that the server
        is currently running.
        """

        exceptionRaised = False;
        try:
            getTime(self.startTime)
        except:
            exceptionRaised = True

        self.assertFalse(exceptionRaised, "The server isn't running.")

    def test_concurrent_connections(self):
        """
        Test that the server can handle the maxmimum number of concurrent
        connections while receiving a response in a similar time frame
        for all requests.

        Input: 5 concurrent function calls to the server. 

        Expected Result: The remote function, test_concurrency, contains a 2 
        second sleep call. The sum of the times taken to complete each of 
        the function calls, relative to self.startTime should be between the 
        range 11 > totalTime >= 10.
        """

        self.resetCurrentTime()

        totalTime = 0

        for time in self.getExecutionTimes(5):
            totalTime += time

        self.assertTrue(totalTime >= 10 and totalTime < 11, "Failed to " +
            "execute all 5 concurrent function calls within the expected " +
            "time frame.")

    def test_max_concurrent_connections(self):
        """
        Tests that the server processes excess function calls after the
        initial batch of calls.

        Input: 6 concurrent function calls to the server. 

        Expected Result: The remote function, test_concurrency, contains a 2 
        second sleep call. The server has a maximum number of concurrent 
        connections of 5, so the 6th call will take slightly over 4 seconds 
        to complete. The sum of the times for all 6 calls should be within 
        the range 15 > totalTime >= 14.
        """

        self.resetCurrentTime()

        totalTime = 0

        for time in self.getExecutionTimes(6):
            totalTime += time

        self.assertTrue(totalTime >= 14 and totalTime < 15, "Failed to " +
            "execute all 6 concurrent function calls within the expected " +
            "time frame.")

    def test_json_rpc_correct_response(self):
        """
        Tests that the server responds as expected to a correctly
        formed JSON-RPC 2.0 request.

        Input: A correctly formed JSON-RPC 2.0 request containing
        an empty array of file names, an empty file name (direct 
        input method) and a HTML fragment consisting of '<html></html>'.

        Expected Result: The returned JSON-RPC 2.0 response string
        should match the string expectedResponse, which contains
        the expected array of errors.
        """
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        fragment = base64.b64encode(b'<html></html>')
        params = [{"files": [], "document": fragment, "filename": ""}]
        request = json.JSONEncoder().encode({"jsonrpc": "2.0", "method": "parse_html",
            "params": params, "id": "A3s23"})
        header = {"Content-type": "application/json"}

        conn.request("POST", "", request, header)
        response = conn.getresponse()
        conn.close()

        expectedResponse = '{"jsonrpc": "2.0", "result": [[1, 0, 5, {"name": "html"}], [25, 6, 12, {"name": "html"}]], "id": "A3s23"}'

        self.assertEqual(response.read(), expectedResponse, "Wrong response.")

    def test_json_rpc_malformed_parameters(self):
        """
        Tests that the server responds with an error when 
        a request contains incorrect parameters.

        Input: A JSON-RPC 2.0 request containing incorrectly
        formatted parameters to be passed on to the requested
        function.

        Expected Result: The returned JSON-RPC 2.0 response string
        should match the string expectedResponse, which contains
        a response representing an invalid parameters error.
        """
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        fragment = base64.b64encode(b'<html></html>')
        params = []
        request = json.JSONEncoder().encode({"jsonrpc": "2.0", "method": "parse_html",
            "params": params, "id": "A3s23"})
        header = {"Content-type": "application/json"}

        conn.request("POST", "", request, header)
        response = conn.getresponse()
        conn.close()

        expectedResponse = '{"error": {"message": "Invalid parameters.", "code": -32602}, "jsonrpc": "2.0", "id": "A3s23"}'

        self.assertEqual(response.read(), expectedResponse, "Wrong response.")

    def test_json_rpc_unsupported_method(self):
        """
        Tests that the server responds with an error when
        a client attempts to make a function call for a function
        which hasn't been registered to the server.

        Input: A JSON-RPC 2.0 request containing a function name
        which hasn't been registered on the server.

        Expected Result: The returned JSON-RPC 2.0 response 
        string should match the string expectedResponse, which
        contains a response representing an unsupported method
        error.
        """
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        fragment = base64.b64encode(b'<html></html>')
        params = [{"files": [], "document": fragment, "filename": ""}]
        request = json.JSONEncoder().encode({"jsonrpc": "2.0", "method": "not_registered",
            "params": params, "id": "A3s23"})
        header = {"Content-type": "application/json"}

        conn.request("POST", "", request, header)
        response = conn.getresponse()
        conn.close()

        expectedResponse = '{"error": {"message": "Method not_registered not supported.", "code": -32601}, "jsonrpc": "2.0", "id": "A3s23"}'

        self.assertEqual(response.read(), expectedResponse, "Wrong response.")

    def test_invalid_filepath(self):
        """
        Tests that the server responds with an error when
        a client attempts to make a function call for a function
        which hasn't been registered to the server.

        Input: A JSON-RPC 2.0 request containing a function name
        which hasn't been registered on the server.

        Expected Result: The returned JSON-RPC 2.0 response 
        string should match the string expectedResponse, which
        contains a response representing an unsupported method
        error.
        """
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        fragment = base64.b64encode(b'<img src=../image.jpg><img src=directory2/image2.jpg>')
        params = [{"files": ["image.jpg", "directory/", "directory/current.html"], "document": fragment, "filename": "directory/current.html"}]
        request = json.JSONEncoder().encode({"jsonrpc": "2.0", "method": "not_registered",
            "params": params, "id": "A3s23"})
        header = {"Content-type": "application/json"}

        conn.request("POST", "", request, header)
        response = conn.getresponse()
        conn.close()

        expectedResponse = '{"error": {"message": "Method not_registered not supported.", "code": -32601}, "jsonrpc": "2.0", "id": "A3s23"}'

        self.assertEqual(response.read(), expectedResponse, "Wrong response.")

    def test_invalid_filepath(self):
        """
        Tests that the server responds with an error when
        a client attempts to make a function call for a function
        which hasn't been registered to the server.

        Input: A JSON-RPC 2.0 request containing a function name
        which hasn't been registered on the server.

        Expected Result: The returned JSON-RPC 2.0 response 
        string should match the string expectedResponse, which
        contains a response representing an unsupported method
        error.
        """
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        fragment = base64.b64encode(b'<img src=../image.jpg><img src=directory2/image2.jpg>')
        params = [{"files": ["image.jpg", "directory/", "directory/current.html"], "document": fragment, "filename": "directory/current.html"}]
        request = json.JSONEncoder().encode({"jsonrpc": "2.0", "method": "not_registered",
            "params": params, "id": "A3s23"})
        header = {"Content-type": "application/json"}

        conn.request("POST", "", request, header)
        response = conn.getresponse()
        conn.close()

        expectedResponse = '{"error": {"message": "Method not_registered not supported.", "code": -32601}, "jsonrpc": "2.0", "id": "A3s23"}'

        self.assertEqual(response.read(), expectedResponse, "Wrong response.")

    def test_invalid_filepath(self):
        """
        Tests that the server responds with an error when
        a client attempts to make a function call for a function
        which hasn't been registered to the server.

        Input: A JSON-RPC 2.0 request containing a function name
        which hasn't been registered on the server.

        Expected Result: The returned JSON-RPC 2.0 response 
        string should match the string expectedResponse, which
        contains a response representing an unsupported method
        error.
        """
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        fragment = base64.b64encode(b'<img src=../image.jpg><img src=directory2/image2.jpg>')
        params = [{"files": ["image.jpg", "directory/", "directory/current.html"], "document": fragment, "filename": "directory/current.html"}]
        request = json.JSONEncoder().encode({"jsonrpc": "2.0", "method": "not_registered",
            "params": params, "id": "A3s23"})
        header = {"Content-type": "application/json"}

        conn.request("POST", "", request, header)
        response = conn.getresponse()
        conn.close()

        expectedResponse = '{"error": {"message": "Method not_registered not supported.", "code": -32601}, "jsonrpc": "2.0", "id": "A3s23"}'

        self.assertEqual(response.read(), expectedResponse, "Wrong response.")

    def test_invalid_filepath(self):
        """
        Tests that the server responds with an error when
        a client attempts to make a function call for a function
        which hasn't been registered to the server.

        Input: A JSON-RPC 2.0 request containing a function name
        which hasn't been registered on the server.

        Expected Result: The returned JSON-RPC 2.0 response 
        string should match the string expectedResponse, which
        contains a response representing an unsupported method
        error.
        """
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        fragment = base64.b64encode(b'<img src=../image.jpg><img src=directory2/image2.jpg>')
        params = [{"files": ["image.jpg", "directory/", "directory/current.html"], "document": fragment, "filename": "directory/current.html"}]
        request = json.JSONEncoder().encode({"jsonrpc": "2.0", "method": "not_registered",
            "params": params, "id": "A3s23"})
        header = {"Content-type": "application/json"}

        conn.request("POST", "", request, header)
        response = conn.getresponse()
        conn.close()

        expectedResponse = '{"error": {"message": "Method not_registered not supported.", "code": -32601}, "jsonrpc": "2.0", "id": "A3s23"}'

        self.assertEqual(response.read(), expectedResponse, "Wrong response.")

    def test_invalid_filepath(self):
        """
        Tests that the server responds with an error when
        a client attempts to make a function call for a function
        which hasn't been registered to the server.

        Input: A JSON-RPC 2.0 request containing a function name
        which hasn't been registered on the server.

        Expected Result: The returned JSON-RPC 2.0 response 
        string should match the string expectedResponse, which
        contains a response representing an unsupported method
        error.
        """
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        fragment = base64.b64encode(b'<img src=../image.jpg><img src=directory2/image2.jpg>')
        params = [{"files": ["image.jpg", "directory/", "directory/current.html"], "document": fragment, "filename": "directory/current.html"}]
        request = json.JSONEncoder().encode({"jsonrpc": "2.0", "method": "not_registered",
            "params": params, "id": "A3s23"})
        header = {"Content-type": "application/json"}

        conn.request("POST", "", request, header)
        response = conn.getresponse()
        conn.close()

        expectedResponse = '{"error": {"message": "Method not_registered not supported.", "code": -32601}, "jsonrpc": "2.0", "id": "A3s23"}'

        self.assertEqual(response.read(), expectedResponse, "Wrong response.")

    def test_invalid_filepath(self):
        """
        Tests that the server responds with an error when
        a client attempts to make a function call for a function
        which hasn't been registered to the server.

        Input: A JSON-RPC 2.0 request containing a function name
        which hasn't been registered on the server.

        Expected Result: The returned JSON-RPC 2.0 response 
        string should match the string expectedResponse, which
        contains a response representing an unsupported method
        error.
        """
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        fragment = base64.b64encode(b'<img src=../image.jpg><img src=directory2/image2.jpg>')
        params = [{"files": ["image.jpg", "directory/", "directory/current.html"], "document": fragment, "filename": "directory/current.html"}]
        request = json.JSONEncoder().encode({"jsonrpc": "2.0", "method": "not_registered",
            "params": params, "id": "A3s23"})
        header = {"Content-type": "application/json"}

        conn.request("POST", "", request, header)
        response = conn.getresponse()
        conn.close()

        expectedResponse = '{"error": {"message": "Method not_registered not supported.", "code": -32601}, "jsonrpc": "2.0", "id": "A3s23"}'

        self.assertEqual(response.read(), expectedResponse, "Wrong response.")

    def test_invalid_filepath(self):
        """
        Tests that the server responds with an error when
        a client attempts to make a function call for a function
        which hasn't been registered to the server.

        Input: A JSON-RPC 2.0 request containing a function name
        which hasn't been registered on the server.

        Expected Result: The returned JSON-RPC 2.0 response 
        string should match the string expectedResponse, which
        contains a response representing an unsupported method
        error.
        """
        conn = httplib.HTTPConnection("127.0.0.1:8080")
        fragment = base64.b64encode(b'<img src=../image.jpg><img src=directory2/image2.jpg>')
        params = [{"files": ["image.jpg", "directory/", "directory/current.html"], "document": fragment, "filename": "directory/current.html"}]
        request = json.JSONEncoder().encode({"jsonrpc": "2.0", "method": "not_registered",
            "params": params, "id": "A3s23"})
        header = {"Content-type": "application/json"}

        conn.request("POST", "", request, header)
        response = conn.getresponse()
        conn.close()

        expectedResponse = '{"error": {"message": "Method not_registered not supported.", "code": -32601}, "jsonrpc": "2.0", "id": "A3s23"}'

        self.assertEqual(response.read(), expectedResponse, "Wrong response.")

if __name__ == '__main__':
    unittest.main()
