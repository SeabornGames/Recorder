from seaborn_recorder.recorder import *
import unittest


def generate_calls(recorder, obj_name = 'subject'):
    calls = [record.name for record in recorder.SEABORN_ACCESS_LOG]
    args = [record.args for record in recorder.SEABORN_ACCESS_LOG]
    kwargs = [record.kwargs for record in recorder.SEABORN_ACCESS_LOG]
    ret = ["%s.%s(%s)"%(obj_name,calls[i],
                        ','.join([
                        ','.join([str(item) for item in args[i]]),
                        ','.join(['%s=%s'%(k,v)
                                  for k, v in kwargs[i].items()])]))
            for i in range(len(recorder.SEABORN_ACCESS_LOG))]
    absent = '(,)'
    for i in range(len(ret)):
        for j in [0,1]:
            ret[i] = ret[i].replace(absent[j:j+2],
                                    absent[j:j+2][j])
        ret[i] = ret[i].replace('.init','')
    return ret


class TestClass():
    def __init__(self,a):
        self.a = a

    def hello_world(self, b=None):
        return "Hello, %s!"%str(b or self.a)

    def args_kwargs(self, *args, **kwargs):
        arg = ', '.join([str(i) for i in args])
        kwarg = ', '.join(['%s=%s'%(k,v) for k, v in kwargs.items()])
        return '%s, %s'%(arg,kwarg)


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
        print(generate_calls(self.klass))

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

    def test_args_kwargs(self):
        print(self.subject.args_kwargs(1,2,3,4,a=1,b=2,c=3))
        generate_calls(self.klass)

if __name__ == '__main__':
    unittest.main()
