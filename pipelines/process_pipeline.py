from ast import expr_context
from distutils.log import debug
import os
import fire
from git import Repo

from src.data.dataset_factory import DatasetFactory
from src.data.repo_data import RepoData
from src import Pipeline
from tasks.load_data import LoadData
from tasks.example_task import ExampleTask


LOCATION = '.'
PROJECT = 'example_project'
BRANCH = 'example_branch'

from loguru import logger

def my_filter(txt):
    if 'pipeline' in txt:
        return True
    return False

logger.add("./logs/pipeline.log", filter=my_filter)

@logger.catch
def process_pipeline(threads=1, force=False):
    # repo = Repo(path='.')
    # if repo.is_dirty():
    #     if force:
    #         print('Warning! Current git repo is dirty, this will result in incorrect commit hash in datasets')
    #     else:
    #         raise ValueError("Current git repo is dirty, please commit your work befour you run the pipeline")

    # commit = repo.commit()
    # repoData = RepoData(
    #     branchName=repo.active_branch.name,
    #     commitHash=commit.hexsha,
    #     commitMessage=commit.message,
    #     comitterName=commit.committer.name,
    #     comitterEmail=commit.committer.email
    # )
    repoData = RepoData.get_dummy()

    from data_models.ppg_segment_5_min import PpgSegment5Min
    from src.data.dataset import Dataset
    from src.config.env_manager import get_env_config
    env_config = get_env_config()

    dataset=Dataset(
        dataType=PpgSegment5Min,
        location=env_config['raw_data_folder'],
        project='heart-failure',
        branch=env_config['project_profile'],
        name='raw_ppg_test',
        chunkCount=16,
        repoData=None
    )

    loadData = LoadData(
        outputDataset=dataset,
        exampleParameter='test',
        debug=True
    )
    

    pipeline = Pipeline(
        tasks=[
            loadData
            
        ]
    )
    pipeline.run(threads=threads)


if __name__ == '__main__':
    fire.Fire(process_pipeline)
