import os
from pathlib import Path
from unittest import TestCase
import testingconf
from src.utils import latest_log,log_filename


class TestUtils(TestCase):
    def setUp(self):
        self.names = ["asp001","asp002",""]
        self.file_list = os.listdir(Path(".") / "data")

    def test_log_filename(self):
        for name in self.names:
            result = log_filename(name,"1","pickle")
            self.assertIn("pickle",result)
            self.assertIn(name,result)
            self.assertNotIn("json",result)
        for name in self.names:
            result = log_filename(name,"1","json")
            self.assertIn("json",result)
            self.assertIn(name,result)
            self.assertNotIn("pickle",result)

    def test_latest_log(self):
        result = latest_log(self.file_list,"pickle")
        self.assertIn("pickle",result.name)
        self.assertIn(result.name,self.file_list)
        result = latest_log(self.file_list,"json")
        self.assertIn("json",result.name)
        self.assertIn(result.name,self.file_list)
