import os
import fire
from git import Repo

from hypergol import DatasetFactory
from hypergol import RepoData
from src import Pipeline
from tasks.load_data import LoadData
from tasks.example_task import ExampleTask
from data_models.example_class import ExampleClass
from data_models.other_example import OtherExample


LOCATION = '.'
PROJECT = 'example_project'
BRANCH = 'example_branch'


def process_pipeline2(threads=1, force=False):
    repo = Repo(path='.')
    if repo.is_dirty():
        if force:
            print('Warning! Current git repo is dirty, this will result in incorrect commit hash in datasets')
        else:
            raise ValueError("Current git repo is dirty, please commit your work befour you run the pipeline")

    commit = repo.commit()
    repoData = RepoData(
        branchName=repo.active_branch.name,
        commitHash=commit.hexsha,
        commitMessage=commit.message,
        comitterName=commit.committer.name,
        comitterEmail=commit.committer.email
    )

    dsf = DatasetFactory(
        location=LOCATION,
        project=PROJECT,
        branch=BRANCH,
        chunkCount=16,
        repoData=repoData
    )
    exampleClasses = dsf.get(dataType=ExampleClass, name='example_classes')
    otherExamples = dsf.get(dataType=OtherExample, name='other_examples')
    loadData = LoadData(
        inputDatasets=[exampleInputDataset1,  exampleInputDataset2],
        outputDataset=exampleOutputDataset,
    )
    exampleTask = ExampleTask(
        inputDatasets=[exampleInputDataset1,  exampleInputDataset2],
        outputDataset=exampleOutputDataset,
    )

    pipeline = Pipeline(
        tasks=[
            loadData,
            exampleTask,
        ]
    )
    pipeline.run(threads=threads)


if __name__ == '__main__':
    fire.Fire(process_pipeline2)
