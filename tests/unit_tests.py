import unittest
from lambda_function import *
import logging


class TestMethods(unittest.TestCase):
	def test_logging(self):
		# Arrange
		payload = ""
		with open("test_payload_db_stream.json", "r") as f:
			payload = f.read()
			f.close()
		event = json.loads(payload)

		print(json.dumps(event, indent=True))

		# Act
		print("Calling lambda_handler ...")
		result = lambda_handler(event, "")

		# Assert
		self.assertEqual(result, 3)



if __name__ == '__main__':
	unittest.main()		


