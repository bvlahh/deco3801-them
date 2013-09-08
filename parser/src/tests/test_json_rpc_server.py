from __future__ import absolute_import, division, unicode_literals

#from . import support
import unittest
import time
import jsonrpclib
from multiprocessing import Pool
from jsonrpclib import Server

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
		Test that a multiple-instance-singular-tag error is thrown
		for cases where more than one instance of the html tag is included.

		Input: Attempt to execute a known function on the server.

		Expected Result: No exception being raised, associated with the server
		not currently running.
		"""

		exceptionRaised = False;
		try:
			getTime(self.startTime)
		except:
			exceptionRaised = True

		self.assertFalse(exceptionRaised, "Server hasn't been started.")

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

if __name__ == '__main__':
	unittest.main()