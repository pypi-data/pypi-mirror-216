from email.utils import parseaddr


class MailSender:
    """General method to send mails"""
    address_book = {}  #: Mail address book

    @classmethod
    def get_sender_dict(cls, mail_adr: str):
        """Get sender information from mail address

        Args:
            mail_adr (str): Full Email address. Like "John Smith" <john.smith@x-i-a.com>

        Returns:
            dict: name and email
        """
        if mail_adr in cls.address_book:
            # Using Mail Address Book as Priority
            mail_adr = cls.address_book[mail_adr]
        mail_dict = dict()
        parsed_adr = parseaddr(mail_adr)
        mail_dict["email"] = parsed_adr[1]
        if parsed_adr[0]:
            mail_dict["name"] = parsed_adr[0]
        else:
            mail_dict["name"] = parsed_adr[1].split("@")[0].replace(".", " ").replace("_", " ").title()
        return mail_dict

    @classmethod
    def send_mail_plain(cls, sender: str, to: list, subject: str, content: str):
        """Send a plain mail (txt or html without attachment)

        Args:
            sender (str): sender could be a validated mail or sth in the address mail book
            to (str): to could be a validated mail list or sth in the address mail book
            subject (str): mail subject
            content (str): mail content
        """
