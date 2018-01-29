from seaborn.recorder.recorder import *
import unittest


class TestClass():
    def __init__(self,a):
        self.a = a

    def hello_world(self, b=None):
        return "Hello, %s!"%str(b or self.a)


class TestRecorder(unittest.TestCase):

    def setUp(self):
        self.klass = SeabornRecorder.get_seaborn_recorder((TestClass))
        self.subject = self.klass(1)

    def test_init(self):
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertListEqual(['init(1)'],result)

    def test_getattr(self):
        result = self.subject.a
        self.assertEqual(1, result)
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertListEqual(['init(1)', 'a()'],result)

    def test_null_getattr(self):
        try:
            error = 'None'
            _ = self.subject.b
        except Exception as e:
            error = e.__class__.__name__
        self.assertEqual('AttributeError',error)
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertListEqual(['init(1)', 'b()'], result)

    def test_setattr(self):
        self.subject.a = 2
        self.assertEqual(2, self.subject.a)
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertListEqual(['init(1)', 'a(2)', 'a()'], result)

    def test_null_setattr(self):
        self.subject.b = 2
        self.assertEqual(2, self.subject.b)
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertListEqual(['init(1)', 'b(2)', 'b()'],result)

    def test_mem_func(self):
        self.assertEqual("Hello, 2!",self.subject.hello_world(2))
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertListEqual(
            ['init(1)', 'hello_world()', 'hello_world(2)'],result)

    def test_ret_mem_func(self):
        _ = self.subject.hello_world
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertListEqual(['init(1)', 'hello_world()'], result)
        # TODO: Attend to recorder's naming conventions

    def test_iadd(self):
        self.subject.a += 1
        self.assertEqual(2, self.subject.a)
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertListEqual(
            ['init(1)', 'a()', 'a(2)', 'a()'], result)

    def test_null_iadd(self):
        try:
            error = 'None'
            self.subject.b += 1
        except Exception as e:
            error = e.__class__.__name__
        self.assertEqual('AttributeError',error)
        result = [str(i) for i in self.klass.SEABORN_ACCESS_LOG]
        self.assertListEqual(['init(1)', 'b()'], result)

if __name__ == '__main__':
    unittest.main()

