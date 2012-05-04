email-address-parser
====================

Parse email addresses from an outlook-like "To:" field.

The nice thing about this parser is you could give it a ridiculously jacked up list of emails: no commas, no names, names and emails stuck together (no spaces), and it'll still parse that string and give you a pretty list back.


To use: 

    from eparser.parsers import email_address_parser
    
    ...
    
    emails = email_address_parser.parse(some_email_list)


Alternatively, you can instantiate your own with a list of additional bad tokens you want stripped from names:

    from eparser.parsers import EmailAddressParser 
    
    parser = EmailAddressParser(bad_tokens=[";"])
    
    emails = parser.parse(some_email_list)

String and Unicode representations are in the format: `"Foo Bar" <foo@bar.com>` 
If there is no name, it's just the email.



