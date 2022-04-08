from typing import Optional, Any, List, Dict, Union, Callable
import lxml.html
from lxml.html import HtmlElement


class HTMLExtractor:
    """Base HTML Email extractor class."""

    def __init__(self, document: Union[str, HtmlElement]):
        self.document: HtmlElement = self.__load_document(document)
        self.fields = list()
        self.data = dict()

    @staticmethod
    def __load_document(document) -> HtmlElement:
        """Load a given document into a lxml HtmlElement"""

        if isinstance(document, str):
            return lxml.html.fromstring(document)
        elif isinstance(document, HtmlElement):
            return document
        else:
            raise Exception("document need to be a string or an lxml HtmlElement")

    def get_xpath(self, xpath: str, first: bool = False) -> Optional[str]:
        """
        Extract and return string data from the HTML document by xpath.
        :param xpath: The xpath selector
        :param first: If set to True, return the first element of the xpath
        :return: The data extracted, or None
        """
        # Select data by xpath
        data = self.document.xpath(xpath)

        # Return the first element
        if first:
            try:
                return data[0]
            except IndexError as error:
                return None

        return data

    def as_dict(self) -> Dict[str, Optional[Any]]:
        """
        Extract and return the fields.
        :return: A key:value dictionary of the fields.
        """
        fields: List[Callable] = []

        # Get the list of all methods decorated as "field"
        for attribute_name in dir(self):
            attribute: Callable = self.__getattribute__(attribute_name)
            try:
                if attribute.__dict__.get("is_field"):
                    fields.append(attribute)
            except AttributeError as error:
                pass

        return {field.__name__: field() for field in fields}
