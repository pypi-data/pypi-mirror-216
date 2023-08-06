
from importlib.resources import files, path

import pathlib
from os.path import join
from jpype import JClass
from jpype import startJVM, shutdownJVM, addClassPath, isJVMStarted
import functools


class JVMLoader:

    def __init__(self):
        pass

    def start_jvm(self):
        if not isJVMStarted():
            startJVM()

    def stop_jvm(self):
        if isJVMStarted():
            shutdownJVM()

    def load_basic_jars(self):
        self._load_jars('jars')

    def load_other_jars(self):
        self._load_jars('jars_other')

    def get_classpath(self):
        with path('py_concodese', 'jars') as java_folder:
            return java_folder.absolute()

    def _load_jars(self, jars='jars'):
        if not isJVMStarted():
            for jar_path in files('py_concodese').joinpath(jars).iterdir():
                print(f'Loading jar: {jar_path}')
                addClassPath(jar_path)
            # with files('py_concodese').joinpath(jars) as jar_folder:
            #     for jar_path in jar_folder.iterdir():
            #         print(f'Loading jar: {jar_path}')
            #         addClassPath(jar_path)
        else:
            print("Warning: JVM already started")

