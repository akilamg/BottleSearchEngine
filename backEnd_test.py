from backEnd import backEnd_run
import unittest

class backEndTestCase(unittest.TestCase):

    def write_to_urls(self, content):
        "overwrite the file 'urls.txt' with the input URL(s)"
        f = open('urls.txt', 'w')
        f.write(content)
        f.close()

    def test_depth0_google_dot_com(self):
        "test the crawler with single URL and depth 0"
        self.write_to_urls('')
        self.write_to_urls('http://google.com\n')
        # The words in expected can all be found on 'http://google.com'
        expected = ["images", "gmail", "privacy"]
        result = backEnd_run(0)[6]

        for word in expected:
            self.assertEqual(word in result, True, word + " Not found in google.com")

    def test_depth0_multipleURLs(self):
        "test the crawler with multiple URLs and depth 0"
        self.write_to_urls('')
        self.write_to_urls('http://google.com\nhttp://bing.com\n')
        # The words in expected_google can all be found on 'http://google.com'
        expected_google = ["images", "gmail"]
        # The words in expected_bing can all be found on 'http://bing.com'
        expected_bing = ["images", "explore"]
        result = backEnd_run(0)[6]

        for word in expected_google:
            self.assertEqual('http://google.com' in result[word], True, word + " Not found in google.com")
        for word in expected_bing:
            self.assertEqual('http://bing.com' in result[word], True, word + " Not found in bing.com")

    def test_depth1_google_dot_com(self):
        "test the crawler with single URL and depth 1"
        self.write_to_urls('')
        self.write_to_urls('http://google.com\n')
        # The first two words in expected can be found on 'http://google.com'
        expected = ["images", "gmail"]
        result = backEnd_run(1)[6]

        for word in expected:
            self.assertEqual(word in result, True, word + " Not found in google.com")

    def test_page_rank(self):
        "test the crawler with single URL and depth 1"
        self.write_to_urls('')
        self.write_to_urls('http://google.com\n')
        result = backEnd_run(0)[4]
        # Each page must have a larger page rank than google.com (which is 0 since its the starting point)
        for r in result.values():
            self.assertEqual(r > 0, True, "Incorrect page rank for google.com link")

    def test_anchor_db(self):
        "test the crawler with single URL and depth 1"
        self.write_to_urls('')
        self.write_to_urls('http://google.com\n')
        # The expected out-going link found in google.com
        expected = "http://google.com/intl/en/about.html"
        output = backEnd_run(1)
        result = output[3]
        self.assertEqual(output[0][expected] in result, True, expected + " was not found as a link in google.com")

    def test_lexicon(self):
        "test the crawler with single URL and depth 0"
        self.write_to_urls('')
        self.write_to_urls('http://google.com\n')
        # The first two words in expected can be found on 'http://google.com'
        expected = ["images", "gmail"]
        result = backEnd_run(0)[2]
        for word in expected:
            self.assertEqual(word in result, True, word + " Not found in google.com")

