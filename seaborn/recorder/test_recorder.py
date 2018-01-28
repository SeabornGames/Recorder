from seaborn.recorder.recorder import SeabornRecorder
from seaborn.calling_function.calling_function import *


class TestRecorder(SeabornRecorder):
    SEABORN_TEST_LOG = []
    SEABORN_TEST_FILE = ''

    @classmethod
    def get_seaborn_recorder(cls, obj, name=None, is_recorded=None,
                             shared_access_log=None, shared_init_objs=None,
                             shared_test_log=None, test_file=None):
        """
            Called to replace obj with an obj that will record calls
        :param obj: obj to be recorded
        :param name: str of the name of the object if not passing a class
        :param is_recorded: func that returns if the call is to be recorded
            accepts one argument of AttributeRecorder
        :param shared_access_log: list to append access to
        :param shared_init_objs: list to append created object to
        :param shared_test_log: dict of {'<test_name>': [<AccessRecord>]
        :param test_file: str of the name of the file to save the test
        :return: SeabornRecorder
        """
        if shared_access_log is None:
            shared_access_log = []

        if shared_init_objs is None:
            shared_init_objs = []

        if shared_test_log is None:
            shared_test_log = []
        class CustomRecorder(cls):
            SEABORN_NAME = name or obj.__name__
            SEABORN_RECORDED_OBJ = obj
            SEABORN_ACCESS_LOG = shared_access_log
            SEABORN_INIT_OBJS = shared_init_objs
            SEABORN_TEST_LOG = shared_test_log
            SEABORN_TEST_FILE = test_file

        if is_recorded is not None:
            setattr(CustomRecorder, 'is_recorded_for_seaborn_recorder',
                    is_recorded)
        return CustomRecorder

    # todo wrap all access with function to determine the testing function

    # on closing save results as test