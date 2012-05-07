import re


# RFC 2822 compliant (mostly) regular expression for pulling email addresses. (http://snipplr.com/view/19594/)
EMAIL_RE = '''[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?'''


class EmailAddress:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        if len(self.name) > 0:
            return "\"%s\" <%s>" % (self.name, self.email)
        return "<%s>" % self.email

    def __repr__(self):
        return "'%s'" % self.__str__()

    def __unicode__(self):
        return unicode(self.__str__())


class EmailAddressParser:
    def __init__(self, bad_tokens=None):
        self._splitter = re.compile("\s")
        self._splitter_tokens = ["<", ">", "\"", "'", ",", " "]

        if bad_tokens is not None:
            # Only accept lists or tuples of strings as additional tokens, if they give us something else: ignore it.
            if isinstance(bad_tokens, list) or isinstance(bad_tokens, tuple):
                bad_tokens = list(bad_tokens)
                for token in bad_tokens:
                    if isinstance(token, basestring):  # basestring because we care about both unicode and str
                        self._splitter_tokens.append(str(token))

    def _remove_tokens(self, section, leave=None):
        leave = leave or []
        cleaned = section
        for token in self._splitter_tokens:
            if token not in leave:
                cleaned = cleaned.replace(token, "")
        return cleaned

    def parse(self, emails, as_unicode=False):
        """Parses email addresses from a string or unicode list.

        Allows you to specify whether your returned list of email/name combos are unicode or regular strings.

        """
        parsed_addresses = []
        if isinstance(emails, basestring):
            name_stack, _emails = [], self._splitter.split(str(emails))
            _emails = filter(lambda token: token != "" and token != u"", _emails)  # Ignore noise.
            for part in _emails:
                m = re.search(EMAIL_RE, part)
                if m is None:  # I know this looks a bit confusing, but it's this is part of a name, not an email.
                    name_stack.append(self._remove_tokens(part, leave=","))
                else:
                    name, _email = "", m.group(0)

                    left_over = part.split(_email)

                    if len(left_over) > 0:  # When there are no spaces inbetween anything.
                        cleaned = self._remove_tokens(left_over[0])
                        if cleaned is not None and cleaned != "":
                            name_stack.append(cleaned)

                    # Pop the name off of our stack.
                    while len(name_stack) > 0:
                        name = "%s %s" % (name_stack.pop(), name)
                    name = name[:len(name) - 1]  # strip out the trailing space.

                    if len(left_over) > 1:
                        cleaned = self._remove_tokens(left_over[1])
                        if cleaned is not None and cleaned != "":
                            name_stack.append(cleaned)

                    # In theory, "part" is just the email now, but the regex got it reliably. Why would we junk that?
                    if as_unicode:
                        name = unicode(name)
                        _email = unicode(_email)
                    pair = EmailAddress(name, _email)
                    parsed_addresses.append(pair)
        return parsed_addresses


email_address_parser = EmailAddressParser()
