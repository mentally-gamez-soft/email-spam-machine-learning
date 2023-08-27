import unittest
import factory
from faker import Faker
import pandas as pd
from faker.config import AVAILABLE_LOCALES

from core.utils.data_sanitizer import DataSanitizer

class TestDataSanitizer(unittest.TestCase):

    def setUp(self) -> None:
        self.locales = [local for local in AVAILABLE_LOCALES]

    def test_str_sanitize_email(self):
        data_sanitizer = DataSanitizer("I only haf msn. It's yijue@hotmail.com how much does it cost krFr@aol.fr")
        result = data_sanitizer.sanitize_email() 
        self.assertEqual(result,"I only haf msn. It's emailaddress how much does it cost emailaddress")
    
    def test_series_sanitize_email(self):
        data_sanitizer = DataSanitizer(pd.Series(["I only haf msn. It's yijue@hotmail.com how much does it cost krFr@aol.fr"]))
        result = data_sanitizer.sanitize_email()
        self.assertEqual(result.item(),"I only haf msn. It's emailaddress how much does it cost emailaddress")

    def test_str_sanitize_currency(self):
        data_sanitizer = DataSanitizer("Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax")
        result = data_sanitizer.sanitize_currency()
        self.assertEqual(result,"Hey...Great deal...Farm tour 9am to 5pm currency95/pax or currency80/pax or currency50/pax")
    
    def test_series_sanitize_currency(self):
        data_sanitizer = DataSanitizer(pd.Series(["Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax"]))
        result = data_sanitizer.sanitize_currency()
        self.assertEqual(result.item(),"Hey...Great deal...Farm tour 9am to 5pm currency95/pax or currency80/pax or currency50/pax")
    
    def test_str_sanitize_leading_whitespace(self):
        data_sanitizer = DataSanitizer("     Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax")
        result = data_sanitizer.sanitize_leading_whitespace()
        self.assertEqual(result,"Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax")

    def test_series_sanitize_leading_whitespace(self):
        data_sanitizer = DataSanitizer(pd.Series(["     Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax"]))
        result = data_sanitizer.sanitize_leading_whitespace()
        self.assertEqual(result.item(),"Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax")

    def test_str_sanitize_leading_whitespace_when_no_whitespace(self):
        data_sanitizer = DataSanitizer("Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax")
        result = data_sanitizer.sanitize_leading_whitespace()
        self.assertEqual(result,"Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax")

    def test_series_sanitize_leading_whitespace_when_no_whitespace(self):
        data_sanitizer = DataSanitizer(pd.Series(["Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax"]))
        result = data_sanitizer.sanitize_leading_whitespace()
        self.assertEqual(result.item(),"Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax")
    
    def test_str_sanitize_trailing_whitespace(self):
        data_sanitizer = DataSanitizer("Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax         ")
        result = data_sanitizer.sanitize_trailing_whitespace()
        self.assertEqual(result,"Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax")

    def test_series_sanitize_trailing_whitespace(self):
        data_sanitizer = DataSanitizer(pd.Series(["Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax         "]))
        result = data_sanitizer.sanitize_trailing_whitespace()
        self.assertEqual(result.item(),"Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax")

    def test_str_sanitize_trailing_whitespace_when_no_whitespace(self):
        data_sanitizer = DataSanitizer("Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax")
        result = data_sanitizer.sanitize_trailing_whitespace()
        self.assertEqual(result,"Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax")

    def test_series_sanitize_trailing_whitespace(self):
        data_sanitizer = DataSanitizer(pd.Series(["Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax         "]))
        result = data_sanitizer.sanitize_trailing_whitespace()
        self.assertEqual(result.item(),"Hey...Great deal...Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax")

    def test_str_sanitize_multiple_whitespace(self):
        data_sanitizer = DataSanitizer("Hey   Great deal   Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax         .")
        result = data_sanitizer.sanitize_whitespace()
        self.assertEqual(result,"Hey Great deal Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax .")

    def test_series_sanitize_multiple_whitespace(self):
        data_sanitizer = DataSanitizer(pd.Series(["Hey   Great deal   Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax         ."]))
        result = data_sanitizer.sanitize_whitespace()
        self.assertEqual(result.item(),"Hey Great deal Farm tour 9am to 5pm $95/pax or €80/pax or £50/pax .")

    def test_str_sanitize_punctuation(self):
        data_sanitizer = DataSanitizer("Hey,Great deal! Farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax.")
        result = data_sanitizer.sanitize_punctuation()
        self.assertEqual(result,"Hey Great deal  Farm tour  9am to 5pm    95 pax or  80 pax or  50 pax ")

    def test_series_sanitize_punctuation(self):
        data_sanitizer = DataSanitizer(pd.Series(["Hey,Great deal! Farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax."]))
        result = data_sanitizer.sanitize_punctuation()
        self.assertEqual(result.item(),"Hey Great deal  Farm tour  9am to 5pm    95 pax or  80 pax or  50 pax ")

    def test_str_sanitize_number(self):
        data_sanitizer = DataSanitizer("Hey,Great deal! Farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax.")
        result = data_sanitizer.sanitize_number()
        self.assertEqual(result,"Hey,Great deal! Farm tour: number am to number pm ? $number /pax or €number /pax or £number /pax.")

    def test_series_sanitize_number(self):
        data_sanitizer = DataSanitizer(pd.Series(["Hey,Great deal! Farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax."]))
        result = data_sanitizer.sanitize_number()
        self.assertEqual(result.item(),"Hey,Great deal! Farm tour: number am to number pm ? $number /pax or €number /pax or £number /pax.")

    def test_str_sanitize_phonenumber(self):
        data_sanitizer = DataSanitizer("Hey,Great deal! Farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax. Call to +420 123 123 123")
        result = data_sanitizer.sanitize_phonenumber()
        self.assertEqual(result,"Hey,Great deal! Farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax. Call to +420 123 123 123")

    def test_series_sanitize_phonenumber(self):
        data_sanitizer = DataSanitizer(pd.Series(["Hey,Great deal! Farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax. Call to +420 123 123 123"]))
        result = data_sanitizer.sanitize_phonenumber()
        self.assertEqual(result.item(),"Hey,Great deal! Farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax. Call to +420 123 123 123")

    def test_str_sanitize_web_url(self):
        data_sanitizer = DataSanitizer("Hey,Great deal on https://stackoverflow.com/questions/60456814/get-list-of-supported-countries-from-faker Farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax. Call to +420 123 123 123")
        result = data_sanitizer.sanitize_web_url()
        self.assertEqual(result,"Hey,Great deal on webaddress Farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax. Call to +420 123 123 123")

    def test_series_sanitize_web_url(self):
        data_sanitizer = DataSanitizer(pd.Series(["Hey,Great deal on https://stackoverflow.com/questions/60456814/get-list-of-supported-countries-from-faker Farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax. Call to +420 123 123 123"]))
        result = data_sanitizer.sanitize_web_url()
        self.assertEqual(result.item(),"Hey,Great deal on webaddress Farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax. Call to +420 123 123 123")

    def test_series_sanitize_font(self):
        data_sanitizer = DataSanitizer(pd.Series(["Hey,Great deal on https://stackoverflow.com/questions/60456814/get-list-of-supported-countries-from-faker Farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax. Call to +420 123 123 123"]))
        result = data_sanitizer.sanitize_font()
        self.assertEqual(result.item(),"hey,great deal on https://stackoverflow.com/questions/60456814/get-list-of-supported-countries-from-faker farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax. call to +420 123 123 123")

    def test_str_sanitize_font(self):
        data_sanitizer = DataSanitizer("Hey,Great deal on https://stackoverflow.com/questions/60456814/get-list-of-supported-countries-from-faker Farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax. Call to +420 123 123 123")
        result = data_sanitizer.sanitize_font()
        self.assertEqual(result,"hey,great deal on https://stackoverflow.com/questions/60456814/get-list-of-supported-countries-from-faker farm tour: 9am to 5pm ? $95/pax or €80/pax or £50/pax. call to +420 123 123 123")