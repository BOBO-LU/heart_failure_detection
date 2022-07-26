import os
import pickle

def attempttomakefolder(foldername, recursive=False):
    """Attempts to create a folder with specified name. Does nothing if it already exists.

    Args:
        foldername (str): 
            
        recursive (bool, optional): _description_. Defaults to False.
    """    
    try:
        os.path.isdir(foldername)
    except TypeError:  # https://www.python.org/dev/peps/pep-0519/
        foldername = os.fspath(
            foldername
        )

    if os.path.isdir(foldername):
        pass
    else:
        if recursive:
            os.makedirs(foldername)
        else:
            os.mkdir(foldername)

def read_pickle(filename):
    """ Read the pickle file """
    with open(filename, "rb") as handle:
        return pickle.load(handle)


def write_pickle(filename, data):
    """ Write the pickle file """
    with open(filename, "wb") as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)