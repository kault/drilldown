"""
This is the current accumulated set of tools for searching, filtering,
and renaming filenames programmatically, generally with the use of regular
expressions. Also included are output options, which will eventually be
abstracted (hopefully).
"""

import re
import os
from distutils.dir_util import copy_tree

#root = "/Users/kault/Box Sync/CIN Study (RGS001D)/"
root = "/"
sub_dir = ""
hide_empty_dirs = False


class colors:
    """ Sparkly """
    BLUE = '\033[94m'
    RED = '\033[31m'
    PURPLE = '\033[35m'
    BOLD = '\033[1m'
    ENDC = '\033[0m'


####################################################################################################
# ------------------------------------------ FUNCTIIONS ------------------------------------------ #
####################################################################################################

def orig_filepath_list(filename_list, src_path):
    """
    Returns list of original filenames (pre-name change)
    TODO: is this necessary? Why even print the full thing?
    """
    orig_filepaths = list([])
    i = 0
    for filename in filename_list:
        orig_filepaths.append(src_path + filename_list[i])
        i += 1
    return orig_filepaths


def replace_all(filename, dic):
    """
    Given a string filename and dictionary dic, returns the filename w/ keys k
    replaced by values v.
    """
    for k, v in dic.iteritems():
        filename = filename.replace(k, v)

    return filename


def sanitize(file_list, dic={}):
    """
    Calls replace_all on a list of filename strings and returns the
    sanitized list.
    """
    sanitized_list = list([])

    for file in file_list:
        file = replace_all(file, dic)
        sanitized_list.append(file)

    return sanitized_list


def sanitize_and_rename(file_list, src_dir, dic={}, rename=False):
    """
    TODO: Why is sanitize its own function?
    """
    sanitized_list = list([])

    for file in file_list:
        filez = replace_all(file, dic)
        sanitized_list.append(filez)

    i = 0
    orig_fp_list = orig_filepath_list(file_list, src_dir)

    san_w_path = [src_dir + fn for fn in sanitized_list]

    for filename in file_list:
        if not (orig_fp_list[i] == san_w_path[i]):
            print (colors.BLUE + "_ORIGINAL_: " + orig_fp_list[i].replace(src_dir, "") + colors.ENDC)
            print (colors.RED + "__UPDATE__: " + san_w_path[i].replace(src_dir, "") + colors.ENDC)
        if rename:
            os.rename(orig_fp_list[i], san_w_path[i])
        i += 1


def list_files(filepath, ignore=[], output=True):
    """
    Returns a list of all filenames in the filepath directory.
    TODO: turn hide_empty_dirs into a parameter?
    """
    files = []

    # Append all files in filepath to files
    for name in os.listdir(filepath):
        files.append(name)

    # Check if ignore list is non-empty (i.e., True):
    if ignore:
        # Filter files according to the ignore list
        files = filter(lambda x: x not in ignore, files)

    # Output filecount:
    if (len(files) > 0 and output is True):
        print '\033[1m' + "file count: " + '\033[0m' + str(len(files))
        print '\n'.join(files)

    return files


def print_list_of_files(file_list):
    """
    Prints list of strings (usually filenames) to console.
    TODO: delete this. newstring join works fine
    """
    for filename in file_list:
        print filename


def regex_filter_list(file_list, pattern, output=True):
    """
    Filters files in file_list according to regex r and returns the list
    of matches.
    """
    r = re.compile(pattern)
    matches = filter(r.match, file_list)

    if (len(matches) > 0 and output is True):
        #print colors.BLUE + '\033[1m' + "matches:" + '\033[0m'
        for match in matches:
            print colors.BLUE + match + colors.ENDC

    return matches


def regex_group_split(file_list, pattern, output=True):
    """
    Renames files that match the pattern regex
    TODO: rename this and make the pattern a parameter
    """
    split_list = list([])   # tuple probz

    dicdic ={   "Jan":"01","Feb":"02","Mar":"03",
                "Apr":"04","May":"05","June":"06","Jun":"06",
                "July":"07","Jul":"07","Aug":"08","Sep":"09",
                "Oct":"10","Nov":"11","Dec":"12",
                "JAN":"01","FEB":"02","MAR":"03",
                "APR":"04","MAY":"05","JUN":"06",
                "JUL":"07","AUG":"08","SEP":"09",
                "OCT":"10","NOV":"11","DEC":"12"}

    for file in file_list:
        split_file = list(re.match(pattern, file).groups())
        #pattern = ('(PLC_PM_Report_)(.*)(\w{3,4})(-| )(\d{4})(.*)')
        #split_file[0], split_file[1], split_file[2], split_file[3], split_file[4] = \
        #    split_file[0], split_file[1] + "-0", split_file[2] + "-", split_file[3], split_file[4]
        #split_file[0], split_file[1], split_file[2], split_file[3], split_file[4] = \
        #     split_file[0],'20'+split_file[3] + '-0', split_file[1] + '-', split_file[2], split_file[4]
             #split_file[0],''+split_file[3] + '-', replace_all(split_file[2], dicdic) + '-', split_file[1], split_file[4]
        #split_file[0], split_file[1], split_file[2] = split_file[0],"_",split_file[2]
        #split_file[0], split_file[1], split_file[2], split_file[3], split_file[4] = \
        #    split_file[0], split_file[3] + '-0', split_file[1] + "-", split_file[2], split_file[4]
        #split_list.append(file.replace(" ", ""))
        split_file[0], split_file[1], split_file[2], split_file[3], split_file[4], split_file[5] = \
        split_file[0] + " ", split_file[1], split_file[2] + "-", split_file[3]+ "-", split_file[4], split_file[5]
        split_list.append("".join(split_file))
        

    if (len(split_list) > 0 and output):
        #print colors.RED + '\033[1m' + "renames:" + '\033[0m'
        for split in split_list:
            print colors.RED + split + colors.ENDC

    return split_list


def rename_files(file_list, src_dir, pattern, rename=False):
    """
    Renames files in file_list (usually the return of regex group split)
    """
    i = 0
    renamed = regex_group_split(file_list, pattern, False)
    renamed_w_path = [src_dir + fn for fn in renamed]
    orig_fp_list = orig_filepath_list(file_list, src_dir)

    for filename in file_list:
        if not (orig_fp_list[i] == renamed_w_path[i]):
            print (colors.BLUE + "_ORIGINAL_: " + orig_fp_list[i].replace(src_dir, "") + colors.ENDC)
            print (colors.RED + "__UPDATE__: " + renamed_w_path[i].replace(src_dir, "") + colors.ENDC)
            #print (colors.BLUE + "_ORIGINAL_: " + orig_fp_list[i] + colors.ENDC)
            #print (colors.RED + "__UPDATE__: " + renamed_w_path[i] + colors.ENDC)
        if rename:
            os.rename(orig_fp_list[i], renamed_w_path[i])
        i += 1
