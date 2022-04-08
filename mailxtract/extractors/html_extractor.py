from abc import ABC, abstractmethod
from typing import Optional, Any, List, Dict, Union
import lxml.html
from lxml.html import HtmlElement


class HTMLExtractor(ABC):
    """Base HTML Email extractor class."""

    def __init__(self, document: Union[str, HtmlElement]):
        self._document: HtmlElement = self.__load_document(document)
        self._data = dict()

    @staticmethod
    def __load_document(document) -> HtmlElement:
        """Load a given document into a lxml HtmlElement"""

        if isinstance(document, str):
            return lxml.html.fromstring(document)
        elif isinstance(document, HtmlElement):
            return document
        else:
            raise Exception("document need to be a string or an lxml HtmlElement")

    def get_xpath(self, xpath: str) -> Optional[str]:
        """
        Extract and return string data from the HTML document by xpath.
        :param xpath: The xpath selector
        :return: The data extracted, or None
        """
        try:
            return self._document.xpath(xpath)[0]
        except IndexError as error:
            return None

    @abstractmethod
    def as_dict(self, fields: List[str]) -> Dict[str, Optional[Any]]:
        """
        Extract and return the fields.
        :param fields: Fields list to return.
        :return: A key:value dictionary of the fields.
        """
        return {field: self.__getattribute__(field)() for field in fields}
