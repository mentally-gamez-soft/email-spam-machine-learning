import re
from pandas.core.strings.accessor import StringMethods

class DataSanitizer():

    def __init__(self, text) -> None:
        self.text = text
        print(type(self.text))

    def set_text(self,search_pattern:str=None,replace:str=''):
        if type(self.text) == str:
            self.text = re.sub(search_pattern,replace,self.text)
        elif type(self.text) == StringMethods:
            self.text = self.text.replace(search_pattern,replace,regex=True)

    def __sanitize_data(self,search_pattern:str=None,replace:str='',overwright_text:bool=False):
        if overwright_text:
            self.set_text(search_pattern,replace)
            return self.text

        return re.sub(search_pattern,replace,self.text) if type(self.text) == str else self.text.replace(search_pattern,replace,regex=True)

    def sanitize_email(self,replace:str='emailaddress',overwright_text:bool=False):
        pattern = "[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*"
        return self.__sanitize_data(search_pattern=pattern,replace=replace,overwright_text=overwright_text)

    def sanitize_currency(self,replace:str='currency',overwright_text:bool=False):
        pattern = "£|\$|€"
        return self.__sanitize_data(search_pattern=pattern,replace=replace,overwright_text=overwright_text)

    def sanitize_leading_whitespace(self,replace:str='',overwright_text:bool=False):
        pattern = "^\s+"
        return self.__sanitize_data(search_pattern=pattern,replace=replace,overwright_text=overwright_text)

    def sanitize_trailing_whitespace(self,replace:str='',overwright_text:bool=False):
        pattern = "\s+?$"
        return self.__sanitize_data(search_pattern=pattern,replace=replace,overwright_text=overwright_text)

    def sanitize_whitespace(self,replace:str=' ',overwright_text:bool=False):
        pattern = "\s+"
        return self.__sanitize_data(search_pattern=pattern,replace=replace,overwright_text=overwright_text)

    def sanitize_punctuation(self,replace:str=' ',overwright_text:bool=False):
        pattern = "[^\w\d\s]"
        return self.__sanitize_data(search_pattern=pattern,replace=replace,overwright_text=overwright_text)

    def sanitize_number(self,replace:str='number ',overwright_text:bool=False):
        pattern = "\d+(\.\d+)?"
        return self.__sanitize_data(search_pattern=pattern,replace=replace,overwright_text=overwright_text)

    def sanitize_phonenumber(self,replace:str='phonenumber ',overwright_text:bool=False):
        pattern = "(^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$)|^\(?[\d]{3}\)?[\s-]?[\d]{3}[\s-]?[\d]{4}$"
        return self.__sanitize_data(search_pattern=pattern,replace=replace,overwright_text=overwright_text)

    def sanitize_web_url(self,replace:str='webaddress',overwright_text:bool=False):
        pattern = "http(s){0,1}\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)"
        return self.__sanitize_data(search_pattern=pattern,replace=replace,overwright_text=overwright_text)


 