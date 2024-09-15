import unittest
from client import send_query_to_server

class TestDictionary(unittest.TestCase):
    def test_number_match(self):
        test_match = send_query_to_server('172.22.95.32', 9999, "153.60.117.184 - - [17/Aug/2022:18:30:32 -0500]")
        expected_match = 1
        self.assertEqual(test_match, expected_match)

        test_match = send_query_to_server('172.22.157.33', 9999, "GET")
        expected_match = 160563
        self.assertEqual(test_match, expected_match)

        test_match = send_query_to_server('172.22.159.33', 9999, "\"POST /wp-admin HTTP/1.0\" [0-3]")
        expected_match = 3198
        self.assertEqual(test_match, expected_match)

        test_match1 = send_query_to_server('172.22.95.32', 9999, "\"POST /wp-admin HTTP/1.0\" [0-3]")
        test_match2 = send_query_to_server('172.22.157.33', 9999, "\"POST /wp-admin HTTP/1.0\" [0-3]")
        test_match3 = send_query_to_server('172.22.159.33', 9999, "\"POST /wp-admin HTTP/1.0\" [0-3]")
        test_match4 = send_query_to_server('172.22.95.33', 9999, "\"POST /wp-admin HTTP/1.0\" [0-3]")
        test_match5 = send_query_to_server('172.22.157.34', 9999, "\"POST /wp-admin HTTP/1.0\" [0-3]")
        test_match6 = send_query_to_server('172.22.159.34', 9999, "\"POST /wp-admin HTTP/1.0\" [0-3]")
        test_match7 = send_query_to_server('172.22.95.34', 9999, "\"POST /wp-admin HTTP/1.0\" [0-3]")
        test_match8 = send_query_to_server('172.22.157.35', 9999, "\"POST /wp-admin HTTP/1.0\" [0-3]")
        test_match9 = send_query_to_server('172.22.159.35', 9999, "\"POST /wp-admin HTTP/1.0\" [0-3]")
        test_match10 = send_query_to_server('172.22.95.35', 9999, "\"POST /wp-admin HTTP/1.0\" [0-3]")
        total_match = test_match1 + test_match2 + test_match3 + test_match4 + test_match5 + test_match6 + test_match7 + test_match8 + test_match9 + test_match10 

        expected_match = 32093
        self.assertEqual(total_match, expected_match)


if __name__ == '__main__':
    unittest.main()
