from seaborn_recorder.recorder import *
import unittest

class TestClass():
    def __init__(self,a):
        self.a = a

class TestRecorder(unittest.TestCase):
    def setUp(self):
        self.klass = SeabornRecorder.get_seaborn_recorder(TestClass)
        self.subject = self.klass(1)

    def test_getattr(self):
        result = self.subject.a
        self.assertEqual(1, result)
        print(self.klass.access_log)

if __name__ == '__main__':
    unittest.main()

