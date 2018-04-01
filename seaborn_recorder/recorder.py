"""
    SeabornRecorder will proxy an object and record all
        all getattr, setattr, method calls, and instantiations
        
    Example:
        from seaborn.recorder.recorder import SeabornRecorder
        SeabornTable = SeabornRecorder.get_seaborn_recorder(SeabornTable)
        table = SeabornTable(data)
        table.deliminator = '/'
        print(str(table))
        ...
        SeabornTable.access_log would have three AttributeRecorders
            1. init SeabornTable
            2. set attribute value
            3. method call to str
"""
import time
import inspect


class SeabornRecorder:
    # it is important that these names not show up in the recorded obj
    SEABORN_NAME = ''
    SEABORN_RECORDED_OBJ = None
    SEABORN_INSTANCE = None
    SEABORN_ACCESS_LOG = []
    SEABORN_INIT_OBJS = []
    SEABORN_OBJ = None

    def __init__(self,*args, **kwargs):
        attribute_recorder = AccessRecord(self, '__init__', 'init',
                                                *args, **kwargs)
        if 'seaborn_recorder_obj' in kwargs: # needed for cloning
            self.SEABORN_OBJ = kwargs['seaborn_recorder_obj']
            return
        obj = self.SEABORN_RECORDED_OBJ(*args, **kwargs)
        self.SEABORN_OBJ = obj
        attribute_recorder.response = self.SEABORN_OBJ
        self.SEABORN_INIT_OBJS.append(self.SEABORN_OBJ)

    @staticmethod
    def is_recorded_for_seaborn_recorder(attribute_recorder):
        """
            It is important that this name not be used in the obj
        :param attribute_recorder: AttributeRecorder
        :return: bool of True if the attribute_recorder should be recorded
        """
        return True

    def __getattr__(self, item):
        attribute_recorder = AccessRecord(self, 'get', item)
        try:
            ret = getattr(self.SEABORN_OBJ, item)
        except Exception as ex:
            attribute_recorder.exception = ex
            raise
        attribute_recorder.response = ret
        if inspect.ismethod(ret):
            return attribute_recorder
        return ret

    def __setattr__(self, name, value):
        if "SEABORN_" in name or name == 'is_recorded_for_seaborn_recorder':
            super().__setattr__(name, value)
            return
        attribute_recorder = AccessRecord(self, 'set', name, value)
        try:
            setattr(self.SEABORN_OBJ, name, value)
        except Exception as ex:
            attribute_recorder.exception = ex
            raise
        attribute_recorder.response = None

    @classmethod
    def get_seaborn_recorder(cls, obj, name=None, is_recorded=None,
                             shared_access_log=None, shared_init_objs=None):
        """
            Called to replace obj with an obj that will record calls
        :param obj: obj to be recorded
        :param name: str of the name of the object if not passing a class
        :param is_recorded: func that returns if the call is to be recorded
            accepts one argument of AttributeRecorder
        :param shared_access_log: list to append access to
        :param shared_init_objs: list to append created object to
        :return: SeabornRecorder
        """
        if shared_access_log is None:
            shared_access_log = []

        if shared_init_objs is None:
            shared_init_objs = []

        class CustomRecorder(cls):
            SEABORN_NAME = name or obj.__name__
            SEABORN_RECORDED_OBJ = obj
            SEABORN_ACCESS_LOG = shared_access_log
            SEABORN_INIT_OBJS = shared_init_objs

        if is_recorded is not None:
            setattr(CustomRecorder, 'is_recorded_for_seaborn_recorder',
                    is_recorded)
        return CustomRecorder


class AccessRecord:
    def __init__(self, parent_recorder, group, name, *args, **kwargs):
        self.parent_recorder = parent_recorder
        self.group = group
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self._exception = None
        self._response = None
        self.end = None
        self.start = time.time()

    def __call__(self, *args, **kwargs):
        new_attribute_recorder = AccessRecord(
            self.parent_recorder, 'call', self.name, *args, **kwargs)
        ret = getattr(self.parent_recorder.SEABORN_OBJ, self.name)(*args, **kwargs)
        new_attribute_recorder.response = ret
        if inspect.isclass(self.parent_recorder.SEABORN_OBJ):
            if isinstance(ret, self.parent_recorder.SEABORN_OBJ):
                ret = self.parent_recorder(seaborn_recorder_obj=ret)
            # todo review what if it returns a subclass of itself
        elif isinstance(ret, self.parent_recorder.SEABORN_OBJ.__class__):
            ret = self.parent_recorder(seaborn_recorder_obj=ret)
        return ret

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, value):
        self._response = value
        self.end = time.time()
        if self.parent_recorder.is_recorded_for_seaborn_recorder(self):
            self.parent_recorder.SEABORN_ACCESS_LOG.append(self)

    @property
    def exception(self):
        return self._exception

    @exception.setter
    def exception(self, value):
        self._exception = value
        self.end = time.time()
        if self.parent_recorder.is_recorded_for_seaborn_recorder(self):
            self.parent_recorder.SEABORN_ACCESS_LOG.append(self)

    @property
    def time_delta(self):
        if self.end is None:
            return None
        return self.end - self.start

    def __str__(self):
        args = [str(a) for a in self.args]
        args += ['%s=%s' % (k, v) for k, v in self.kwargs.items()]
        return '%s(%s)' % (self.name, ','.join(args))