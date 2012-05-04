import unittest
from parsers import EmailAddressParser


class TestEmailAddressParser(unittest.TestCase):
    def setUp(self, *args, **kwargs):
        self.parser = EmailAddressParser()

    def test_as_unicode(self):
        emails = u"""
        'Foo Bar' <foo@bar.com>
        "Foo Baz" <foo@baz.com>
        """
        pairs = self.parser.parse(emails, True)

        first_pair, second_pair = pairs[0], pairs[1]

        self.failIf(first_pair.name != u"Foo Bar")

        self.failIf(first_pair.email != u"foo@bar.com")

        self.failIf(second_pair.name != u"Foo Baz")

        self.failIf(second_pair.email != u"foo@baz.com")

    def test_common_cases(self):
        emails = """\"Bar, Foo\" <foo@bar.com>, Foo Bar <foo@bar.com>, \"Foo B.\" <foo@bar.com> foo@bar.com, <foo@bar.com>, \"\"foo@bar.com, \"\"<foo@bar.com>"""

        pairs = self.parser.parse(emails)

        self.failIf(len(pairs) != 7)

        for pair in pairs:
            self.failIf(pair.email != "foo@bar.com")

        self.failIf(pairs[0].name != "Bar, Foo")

        self.failIf(pairs[1].name != "Foo Bar")

        self.failIf(pairs[2].name != "Foo B.")

        self.failIf(pairs[3].name != "")
