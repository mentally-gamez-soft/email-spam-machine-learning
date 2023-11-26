"""Clean dataset for analyzing it."""

import re

from pandas.core.series import Series
from pandas.core.strings.accessor import StringMethods


class DataSanitizer:
    """Set of functions to sanitize and clean dataset for analisis."""

    def __init__(self, text) -> None:
        """Init the DataSanitizer instance.

        Args:
            text (str|pandas.core.strings.accessor.StringMethods|pandas.core.series.Series): the text string to analyze.
        """
        self.text = text

    def set_text(self, search_pattern: str = None, replace: str = ""):
        """Replace a pattern in the string by another one.

        Args:
            search_pattern (str, optional): The pattern to find in the string. Defaults to None.
            replace (str, optional): The string to put in place. Defaults to ''.
        """
        if type(self.text) == str:
            self.text = re.sub(search_pattern, replace, self.text)
        elif type(self.text) in (StringMethods, Series):
            self.text = self.text.replace(search_pattern, replace, regex=True)

    def __sanitize_data(
        self,
        search_pattern: str = None,
        replace: str = "",
        overwright_text: bool = False,
    ):
        if overwright_text:
            self.set_text(search_pattern, replace)
            return self.text

        return (
            re.sub(search_pattern, replace, self.text)
            if type(self.text) == str
            else self.text.replace(
                r"{}".format(search_pattern), replace, regex=True
            )
        )

    def sanitize_font(self, overwright_text: bool = False):
        """Set the string all to lower case.

        Args:
            overwright_text (bool, optional): option to overwright the value of self__text. Defaults to False.

        Returns:
            str|pandas.core.strings.accessor.StringMethods|pandas.core.series.Series: the text string to analyze.
        """
        if overwright_text:
            if type(self.text) == str:
                self.text = self.text.lower()
            elif type(self.text) == StringMethods:
                self.text = self.text.str.lower()

        return (
            self.text.lower()
            if type(self.text) == str
            else self.text.str.lower()
        )

    def sanitize_email(
        self, replace: str = "emailaddress", overwright_text: bool = False
    ):
        """Set all email patterns to a specific value.

        Args:
            replace (str, optional): Any email address will be replaced by this string. Defaults to 'emailaddress'.
            overwright_text (bool, optional): option to overwright the value of self__text. Defaults to False.

        Returns:
            str|pandas.core.strings.accessor.StringMethods|pandas.core.series.Series: the text string to analyze.
        """
        pattern = "[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"
        return self.__sanitize_data(
            search_pattern=pattern,
            replace=replace,
            overwright_text=overwright_text,
        )

    def sanitize_currency(
        self, replace: str = "currency", overwright_text: bool = False
    ):
        """Set all currency symbols to a specific string value.

        Args:
            replace (str, optional): Any currency symbol will be replaced by this string. Defaults to 'currency'.
            overwright_text (bool, optional): option to overwright the value of self__text. Defaults to False.

        Returns:
            str|pandas.core.strings.accessor.StringMethods|pandas.core.series.Series: the text string to analyze.
        """
        pattern = "£|\$|€"
        return self.__sanitize_data(
            search_pattern=pattern,
            replace=replace,
            overwright_text=overwright_text,
        )

    def sanitize_leading_whitespace(
        self, replace: str = "", overwright_text: bool = False
    ):
        """Replace any leading whitespace by the specified string value.

        Args:
            replace (str, optional): Trim the leading whitespaces. Defaults to ''.
            overwright_text (bool, optional): option to overwright the value of self__text. Defaults to False.

        Returns:
            str|pandas.core.strings.accessor.StringMethods|pandas.core.series.Series: the text string to analyze.
        """
        pattern = "^\s+"
        return self.__sanitize_data(
            search_pattern=pattern,
            replace=replace,
            overwright_text=overwright_text,
        )

    def sanitize_trailing_whitespace(
        self, replace: str = "", overwright_text: bool = False
    ):
        """Replace any trailing whitespace by the specified string value.

        Args:
            replace (str, optional): Trim the trailing whitespaces. Defaults to ''.
            overwright_text (bool, optional): option to overwright the value of self__text. Defaults to False.

        Returns:
            str|pandas.core.strings.accessor.StringMethods|pandas.core.series.Series: the text string to analyze.
        """
        pattern = "\s+?$"
        return self.__sanitize_data(
            search_pattern=pattern,
            replace=replace,
            overwright_text=overwright_text,
        )

    def sanitize_whitespace(
        self, replace: str = " ", overwright_text: bool = False
    ):
        """Replace any whitespace by the specified string value.

        Args:
            replace (str, optional): Replace any whitespaces by one whitespace. Defaults to ' '.
            overwright_text (bool, optional): option to overwright the value of self__text. Defaults to False.

        Returns:
            str|pandas.core.strings.accessor.StringMethods|pandas.core.series.Series: the text string to analyze.
        """
        pattern = "\s+"
        return self.__sanitize_data(
            search_pattern=pattern,
            replace=replace,
            overwright_text=overwright_text,
        )

    def sanitize_punctuation(
        self, replace: str = " ", overwright_text: bool = False
    ):
        """Replace any punctuation by the specified string value.

        Args:
            replace (str, optional): Delete punctuation. Defaults to ' '.
            overwright_text (bool, optional): option to overwright the value of self__text. Defaults to False.

        Returns:
            str|pandas.core.strings.accessor.StringMethods|pandas.core.series.Series: the text string to analyze.
        """
        pattern = "[^\w\d\s]"
        return self.__sanitize_data(
            search_pattern=pattern,
            replace=replace,
            overwright_text=overwright_text,
        )

    def sanitize_number(
        self, replace: str = "number ", overwright_text: bool = False
    ):
        """Replace any number by the specified string value.

        Args:
            replace (str, optional): Replace numbers by the string value 'number '. Defaults to 'number '.
            overwright_text (bool, optional): option to overwright the value of self__text. Defaults to False.

        Returns:
            str|pandas.core.strings.accessor.StringMethods|pandas.core.series.Series: the text string to analyze.
        """
        pattern = "\d+(\.\d+)?"
        return self.__sanitize_data(
            search_pattern=pattern,
            replace=replace,
            overwright_text=overwright_text,
        )

    def sanitize_phonenumber(
        self, replace: str = "phonenumber ", overwright_text: bool = False
    ):
        """Replace any phonenumber by the specified string value.

        Args:
            replace (str, optional): Replace phone numbers by the string 'phonenumber '. Defaults to 'phonenumber '.
            overwright_text (bool, optional): option to overwright the value of self__text. Defaults to False.

        Returns:
            str|pandas.core.strings.accessor.StringMethods|pandas.core.series.Series: the text string to analyze.
        """
        pattern = "(^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$)|^\(?[\d]{3}\)?[\s-]?[\d]{3}[\s-]?[\d]{4}$"
        return self.__sanitize_data(
            search_pattern=pattern,
            replace=replace,
            overwright_text=overwright_text,
        )

    def sanitize_web_url(
        self, replace: str = "webaddress", overwright_text: bool = False
    ):
        """Replace any url by the specified string value.

        Args:
            replace (str, optional): Replace web urls by the string 'webaddress'. Defaults to 'webaddress'.
            overwright_text (bool, optional): option to overwright the value of self__text. Defaults to False.

        Returns:
            str|pandas.core.strings.accessor.StringMethods|pandas.core.series.Series: the text string to analyze.
        """
        pattern = "http(s){0,1}\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)"
        return self.__sanitize_data(
            search_pattern=pattern,
            replace=replace,
            overwright_text=overwright_text,
        )
