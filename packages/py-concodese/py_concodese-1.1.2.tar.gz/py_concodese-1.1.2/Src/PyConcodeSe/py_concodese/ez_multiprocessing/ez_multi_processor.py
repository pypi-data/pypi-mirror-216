from multiprocessing import Pool, cpu_count, set_start_method
from py_concodese.jvm_loader.jvm_loader import JVMLoader


class EzMultiProcessor:
    """ An object that can contain threaded operations """

    def __init__(self, processes=1, java_class_path=""):
        """Processes: number of cpu processes (0 defaults to cpu_count() - 1).
        If 1, multiprocessing is disabled.
        Cannot set to use more than cpu_count() - 1
        """
        # this start method is slower but more robust than forking
        # https://pythonspeed.com/articles/python-multiprocessing/
        # set_start_method can only be called once per python process
        # tests make multiples of these objects which results in errors
        # so we are silencing them. Yes, not great I know.
        try:
            set_start_method("spawn")
        except RuntimeError:
            pass

        max_cpu_count = cpu_count() - 1

        if processes == 0:
            processes = max_cpu_count
        if processes <= 1:
            processes = None
        else:
            processes = min(max_cpu_count, processes)

        self.processes = processes

        self.java_class_path = java_class_path

        self._process_args = []

    def append_to_args(self, *args):
        """ appends a set of args for a single process """
        self._process_args.append(args)

    def set_args(self, process_args):
        """ sets the args for all processes """
        self._process_args = process_args

    def execute_function(
        self, function, disable_grouping=False, start_jvm=False
    ) -> list:
        """Executes a function once for each set of arguments

        IMPORTANT: If the function changes objects, those modified objects MUST be returned,
        otherwise sub-object references can be lost. Be careful and test.
        Arguments are removed from the class after calling.
        disable_grouping - work isn't grouped together into processes prior to starting.
        Dislikes working with database objects, do not use methods that make changes to them
        """
        # do not multiprocess, or start/ stop the jvm on the primary process
        if self.processes is None:
            results = EzMultiProcessor.function_wrapper(function, self._process_args)

        else:
            java_class_path = ""
            if start_jvm:
                java_class_path = self.java_class_path

            # do not group args for most efficient processing of a small number of arg sets
            if disable_grouping or len(self._process_args) <= self.processes:
                args = [
                    [function, [process_arg], java_class_path]
                    for process_arg in self._process_args
                ]
            # group args into pools for most efficient processing of a large number of arg sets
            else:
                args = EzMultiProcessor.make_arg_groups(
                    self._process_args, self.processes, function, java_class_path
                )

            with Pool(self.processes) as p:
                results = p.starmap(EzMultiProcessor.function_wrapper, args)
            # flatten the top level of lists
            results = [item for sublist in results for item in sublist]

        assert len(results) == len(self._process_args)

        # clear args
        self._process_args = []
        return results

    @staticmethod
    def make_arg_groups(process_args, n, function, java_class_path):
        """ divides an iterable process_args in n number of groups"""
        min_split_size = len(process_args) // n
        remainders = len(process_args) % n

        # a split is size n + remainders are shared evenly
        split_sizes = [min_split_size + (1 * m in range(remainders)) for m in range(n)]

        splits = []
        i = 0
        for split_size in split_sizes:
            splits.append(process_args[i : i + split_size])
            i = i + split_size

        # add function to args
        grouped_args = [[function, arg_set, java_class_path] for arg_set in splits]
        return grouped_args

    @staticmethod
    def function_wrapper(function, process_args, java_class_path=""):
        """wraps a function and its arguements up for a single process.
        Processes cannot share JVMs so if a class path is provided, the jvm is started
        for this process."""
        java_loader = JVMLoader()
        java_loader.load_basic_jars()
        java_loader.start_jvm()
        # if java_class_path and not isJVMStarted():
        #     addClassPath(java_class_path)
        #     startJVM()
        try:
            results = [function(*args) for args in process_args]
        except Exception as ex:
            print(f"exception while threading: {ex}")
            raise ex

        # let python shutdown the JVMs as the pool closes.
        # Shutting down manually works fine until the pool tries to end and hangs

        return results
