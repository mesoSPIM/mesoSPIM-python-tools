import os
from glob import glob

from . import metadata


def is_mesoSPIM_dir(path_to_test):
    """Return true if path_to_test contains mesoSPIM data

    Purpose
    -------
    Test whether the path defined by path_to_test contains a mesoSPIM acquisition.
    There is currently no particularly good test for this, so we simple check for
    the presence of meta-data files.


    Arguments
    ---------
    path_to_test : str
        Relative or absolute path of a directory that may contain mesoSPIM data


    Outputs
    -------
    Returns true if path_to_test contains mesoSPIM data

    """

    glob_to_search = os.path.join(
        path_to_test, "*tiff_meta*"
    )  # So only handless TIFF stacks
    return file_glob_exist(glob_to_search)


def file_glob_exist(t_path):
    """Test whether a particular file path (which can include a wildcard) exists

    Purpose
    -------
    Return true if t_path exists. Can be used to test for wildcards.
    e.g. To test if there are there are any text files in the current directory:

    t_path = './*.txt'


    Arguments
    ---------
    t_path : str
        Path to test


    Outputs
    -------
    Returns true if t_path exists
    """

    if len(glob(t_path)) == 0:
        return False

    return True


def return_mesoSPIM_files_in_path(t_path):
    """Return a list of dictionaries containing the files which are mesoSPIM acquisitions

    Purpose
    -------
    Returns all the information needed to load a series of acquisitions. The function
    returns a list of dictionaries with each entry corresponding to one file.


    Arguments
    ---------
    t_path : str
        Directory path to search for mesoSPIM data


    Outputs
    -------
    List of dictionaries containing the following information

    {
     'image_file_name'       : str  : string describing the file name
     'absolute_path_to_file' : str  : path to image_file_name
     'meta_data'             : dict : dictionary containing meta-data for image_file_name
    }
    """

    t_path = os.path.abspath(t_path)
    meta_data_files = glob(
        os.path.join(t_path, "*tiff_meta*")
    )  # So only handless TIFF stacks
    out = []

    if len(meta_data_files) == 0:
        return out

    for t_file in meta_data_files:
        split_path = os.path.split(t_file)

        out.append(
            {
                "image_file_name": split_path[1].replace("_meta.txt", ""),
                "absolute_path_to_file": split_path[0],
                "meta_data": metadata.read(t_file),
            }
        )

    return out
