from seaborn.recorder.recorder import *
import unittest

class TestClass():
    def __init__(self,a):
        self.a = a

    def hello_world(self):
        return "Hello, %s!"%str(self.a)

class TestRecorder(unittest.TestCase):

    def test_getattr(self):
        self.klass = SeabornRecorder.get_seaborn_recorder(TestClass)
        self.subject = self.klass(1)
        result = self.subject.a
        self.assertEqual(1, result)
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertListEqual(['init(1)', 'init(1)', 'a()'],result)

    def test_null_getattr(self):
        self.klass = SeabornRecorder.get_seaborn_recorder(TestClass)
        self.subject = self.klass(1)
        result = self.subject.b
        self.assertEqual(result, None)  # TODO:  double-check that this
                                        #        isn't supposed to fail
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertListEqual(['init(1)', 'init(1)', 'b()'], result)

    def test_setattr(self):
        self.klass = SeabornRecorder.get_seaborn_recorder(TestClass)
        self.subject = self.klass(1)
        self.subject.a = 2
        self.assertEqual(2, self.subject.a)
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertListEqual(['init(1)', 'init(1)', 'a(2)', 'a()'], result)

    def test_null_setattr(self):
        self.klass = SeabornRecorder.get_seaborn_recorder(TestClass)
        self.subject = self.klass(1)
        self.subject.b = 2
        self.assertEqual(2, self.subject.b)
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertListEqual(['init(1)', 'init(1)', 'b(2)', 'b()'],result)

    def test_mem_func(self):
        self.klass = SeabornRecorder.get_seaborn_recorder(TestClass)
        self.subject = self.klass(1)
        self.assertEqual("Hello, 1!",self.subject.hello_world())
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertListEqual(['init(1)', 'init(1)', 'hello_world()'],result)

    def test_ret_mem_func(self):
        self.klass = SeabornRecorder.get_seaborn_recorder(TestClass)
        self.subject = self.klass(1)
        _ = self.subject.hello_world
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertEqual(result, ['init(1)', 'init(1)', 'hello_world()'])
        # TODO: Attend to recorder's naming conventions


if __name__ == '__main__':
    unittest.main()

