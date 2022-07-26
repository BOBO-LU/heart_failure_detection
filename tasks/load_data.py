from fileinput import filename
import traceback
from src.basic.job import Job
from src.task import Task
from data_models.ppg_segment_5_min import PpgSegment5Min

from loguru import logger
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import heartpy as hp

import sys
import os
logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")
logger.add("./logs/load_data.log")
logger.add("./logs/trace_back.log", backtrace=True, diagnose=True)
logger.add("./logs/enqueue.log", enqueue=True)

col_name = ['datetime', 'ppg_ts', 'ppg', 'acc_ts', 'x', 'y', 'z']
TIME_FORMAT = '%Y%m%d%H%M%S'

def interpolate_acc(df):
    
    acc = df[['acc_ts', 'x', 'y', 'z']].copy()
    ppg = df[['datetime', 'ppg_ts', 'ppg']].copy()

    acc.dropna(inplace=True)
    ppg.dropna(inplace=True)

    x = np.arange(acc.shape[0])
    y_x = np.array(acc['x'])
    y_y = np.array(acc['y'])
    y_z = np.array(acc['z'])

    xnew = np.arange(0, acc.shape[0], acc.shape[0]/ppg.shape[0])
    f_x = interp1d(x, y_x, bounds_error=False, fill_value="extrapolate")
    f_y = interp1d(x, y_y, bounds_error=False, fill_value="extrapolate")
    f_z = interp1d(x, y_z, bounds_error=False, fill_value="extrapolate")

    x_xnew, x_ynew, x_znew = f_x(xnew), f_y(xnew), f_z(xnew)

    print(x.shape, xnew.shape)
    print(y_x.shape, x_xnew.shape)
    df['x_new'], df['y_new'], df['z_new'] = [x_xnew, x_ynew, x_znew]
    return df

def Pythagorean_3d(arr):
    """
    ab = Pythagorean_3d(ppg_df[['x_new', 'y_new', 'z_new']].to_numpy())
    ppg_df['tri_acc'] = np.array(ab)
    """
    a,b,c = np.hsplit(arr, 3)
    return np.around(((a**2 + b**2 + c**2) ** (1/2)), 5)

def df_preprocess(fpath: str):
    
    ppg_df = pd.read_csv(fpath, names=col_name, header=None)

    #  data preprocess
    try:
        # timestsamp preprocessing
        ppg_df['datetime'] = ppg_df['datetime'].replace(
            to_replace=0, method='bfill')
        ppg_df = ppg_df[ppg_df['datetime'] > 0]
        ppg_df['time'] = pd.to_datetime(ppg_df['datetime'], format=TIME_FORMAT)
        ppg_df.index = pd.to_datetime(ppg_df['datetime'], format=TIME_FORMAT)

        # interpolate
        ppg_df = interpolate_acc(ppg_df)
        ppg_df = ppg_df.dropna()

        # get trixial
        ab = Pythagorean_3d(ppg_df[['x_new', 'y_new', 'z_new']].to_numpy())
        ppg_df['tri_acc'] = np.array(ab)
        return ppg_df

    except Exception as e:
        print(e)
        raise RuntimeError


class LoadData(Task):

    def __init__(self, exampleParameter, *args, **kwargs):
        super(LoadData, self).__init__(*args, **kwargs)
        # TODO: all member variables must be pickle-able, otherwise use the "Delayed" methodology
        # TODO: (e.g. for a DB connection), see the documentation <add link here>
        self.exampleParameter = exampleParameter

    def init(self):
        # TODO: initialise members that are NOT "Delayed" here (e.g. load spacy model)
        pass

    def get_jobs(self):
        # raise NotImplementedError(f'{self.__class__.__name__} must implement get_jobs()')
        # TODO: Return a list of Job classes here that will be passed on to the source_iterator
       
        label_df = pd.read_csv("/Users/bobo/Code/ftp_data/patient_data.csv", index_col=0)
        patient_folders = next(os.walk('/Users/bobo/Code/ftp_data/聯發科PPG Raw Data'), (None, None, []))[1]
        patient_id_list = sorted([int(f[4:]) for f in patient_folders if (
            f.find('TVGH') != -1 and not f.endswith("(x)"))])

        # TODO: change patient_id_list
        patient_id_list = patient_id_list[:6]
        
        return [Job(id_=k, total=len(patient_id_list) ,parameters={
            'pid' : pid,
            'attr' : label_df.loc[pid][['patient_id', 'csv num', 'Age ', 'Gender', 'NYHA', 'Event label']].to_list(),
            'patient_num' : 'TVGH%03d' % pid,
            'root' : os.path.join('/Users/bobo/Code/ftp_data/聯發科PPG Raw Data', 'TVGH%03d' % pid),
        }) for k, pid in enumerate(
            patient_id_list
        )]

    def source_iterator(self, parameters):
        logger.info("start source_iterator")
        # raise NotImplementedError(f'{self.__class__.__name__} must implement source_iterator()')
        # TODO: use the parameters (from Job) to open
        # TODO: use yield in this function instead of return while you are consuming your source data
        # TODO: return type must be list or tuple as the * operator will be used on it
        root = parameters['root']
        pid = parameters['pid']
        attr = parameters['attr']
        logger.info(f"start pid: {pid}")
        filenames = next(os.walk(root), (None, None, []))[2]
        filenames = [f for f in filenames if f.find('.csv') != -1]

        counter = 0
        # TODO: change filenames[0] to filenames
        for f in filenames[:1]:
            fpath = os.path.join(root, f)
            logger.info(f"start pid: {pid}, start file: {f}")
            try:
                ppg_df = df_preprocess(fpath)
            except Exception as e:
                logger.error(f"PID={pid}, id : {counter}, file: {f}, status: {'preprocess error'}: {e}", )
                continue
            window = hp.peakdetection.make_windows(ppg_df['ppg'], 64, windowsize=5*60, overlap=0, min_size=19200)
            for w_start, w_end in window:
                try:
                    sample = ppg_df.iloc[w_start:w_end]['ppg'].to_list()[:19200]
                    acc = ppg_df.iloc[w_start:w_end]['tri_acc'].to_list()[:19200]
                    start = ppg_df.iloc[w_start].time
                    
                    new_data = PpgSegment5Min(
                        id = counter,
                        age = attr[2], 
                        pid = attr[0],
                        event = attr[5],
                        nyha = attr[4],
                        start_time = start,
                        ppg = sample, 
                        tri_acc = acc
                    )
                    counter += 1
                except Exception as e:
                    logger.error(f"PID={pid}, id : {counter}, file: {f}, status: {'writing error'}: {e}", )
                    continue
                yield [new_data]

    def run(self, exampleData):
        # raise NotImplementedError(f'{self.__class__.__name__} must implement run()')
        # TODO: Use the exampleData from source_iterator to construct a domain object
        self.output.append(exampleData)

    def finish_job(self, jobReport):
        # TODO: Update jobReport after the last iteration. Close file handlers or release memory of non-python objects here if necessary

        pass

    def finish_task(self, jobReports, threads):
        # User-defined finalisation at the end of the task.
        pass
