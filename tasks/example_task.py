from hypergol import Task
from data_models.other_example import OtherExample


class ExampleTask(Task):

    def __init__(self, exampleParameter, *args, **kwargs):
        super(ExampleTask, self).__init__(*args, **kwargs)
        # TODO: all member variables must be pickle-able, otherwise use the "Delayed" methodology
        # TODO: (e.g. for a DB connection), see the documentation <add link here>
        self.exampleParameter = exampleParameter

    def init(self):
        # TODO: initialise members that are NOT "Delayed" here (e.g. load spacy model)
        pass

    def run(self, exampleInputObject1, exampleInputObject2):
        raise NotImplementedError(f'{self.__class__.__name__} must implement run()')
        self.output.append(exampleOutputObject)

    def finish_job(self, jobReport):
        # TODO: Update jobReport after the last iteration. Close file handlers or release memory of non-python objects here if necessary
        pass

    def finish_task(self, jobReports, threads):
        # User-defined finalisation at the end of the task.
        pass
