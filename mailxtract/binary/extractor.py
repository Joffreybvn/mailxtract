import quopri
import unicodedata
from email.message import Message
from typing import Dict, Any


class BinaryExtractor:

    def __init__(self, message: Message):
        self.message: Message = message

    def _extract(self, content_type: str) -> str:
        """Get the part of the message corresponding to the given content type."""
        for part in self.message.walk():
            if part.get_content_type() == content_type:
                return part.get_payload()

    @staticmethod
    def decode_html(html_message: str) -> str:
        """Decode an HTML email into its usable form for a web browser."""

        # Decode quoted-printable
        utf8_string: str = quopri.decodestring(html_message).decode("utf-8")

        # Replace unicode by their utf-8 counterpart
        uni_decoded: str = unicodedata.normalize("NFKD", utf8_string)

        # Remove remaining ASCII characters
        ascii_removed: str = uni_decoded.encode('ascii', 'ignore').decode('utf-8')

        # Remove line breaks
        no_break: str = ascii_removed.splitlines()[0]
        return no_break

    def get_html(self) -> str:
        """Return the HTML content of the email."""
        raw_html = self._extract(content_type='text/html')
        return self.decode_html(raw_html)

    def get_header(self) -> Dict[str, Any]:
        """Return the headers in the form of a dictionary."""
        return dict(self.message.items())

    def get_text(self):
        raise NotImplemented()
