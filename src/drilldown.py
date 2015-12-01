"""
This is the new main file for Box Sync edits. From main(), we call functions 
from box-dev/src/rename_tools.py to make edits directly to our local Box Sync 
files.
"""
import rename_tools as rt
import os
import argparse
import sys
import subprocess
from glob import glob

####################################################################################################
# ----------------------------------- (MODULE-)GLOBAL VARIABLES ---------------------------------- #
####################################################################################################

root = "/Users/kault/Box Sync/CIN Study (RGS001D)/"
working_dir = os.path.join(root, "Data Management")

# Completed directories to exclude/ignore
complete = ['.DS_Store', 'Clinical Sites']

# Regex pattern to match
# pattern = ('^(\d{4}-\d{2}-\d{2})(_)(.*)')
pattern = ('(.*)')

# Dictionary for sanitization
my_dict = {
    # ",":"_",
    # "+":"_",
    "__":"_",
    "RGS001D":""
    }

####################################################################################################
# ------------------------------------------ FUNCTIONS ------------------------------------------- #
####################################################################################################

def main():
    """
    Executive function to handle all output and renaming functionality by interpreting
    arguments.
    """
    
    print "Working directory: " + working_dir
    #print next(os.walk(working_dir))[1]

    # Parse options and output/perform changes accordingly
    shell = op_parser()
    args = shell.parse_args()
    print str(args) + '\n'

    # Instantiate lists for -b/-d calls
    full_paths, parent_paths, filenames = [], [], []

    # Check arguments from required group...
    if args.bedrock:
        full_paths, parent_paths, filenames = bedrock(working_dir, output=False)
        #print '\n'.join(filenames)
    elif args.dirs:
        full_paths, parent_paths, filenames = dirs(working_dir, output=True)
        #print '\n'.join(filenames)
    elif args.drilldown:
        #print '@@@@' + str(args.drilldown)
        drilldown(working_dir, args.drilldown, output=True)

    # ... then check optional arguments
    if args.list:
        #print '\n'.join([file for file in os.listdir(working_dir) if file not in complete])
        pass
    elif args.sanitize:
        rt.sanitize(filenames, working_dir, my_dict, False)
    elif args.filter:
        rt.regex_filter_list(filenames, pattern, output=True)
    elif args.check:
        rt.regex_group_split(rt.regex_filter_list(filenames, pattern), pattern)
    elif args.rename:
        rt.rename_files(rt.regex_filter_list(filenames, pattern), working_dir, pattern)
    elif args.empty:
        empty(root, True)


def bedrock(src_dir, output=True):
    """
    Creates a list of all files in source directory, then works on it.
    Returns 3 values: list of all files, paths, and filenames.
    """
    # Recursively create list of all files ending w/ ".[a-z]{3}*" (approx. file extension).
    result_files = [y for x in os.walk(src_dir) for y in glob(os.path.join(x[0], '*.[a-z][a-z][a-z]*'))]

    if output:
        # Print src_dir name, then list files within.
        # Alternative to below: file[len(str(src_dir)):] returns? everything after src_dir in the path.
        print rt.colors.PURPLE + rt.colors.BOLD + "# # # " + src_dir.upper() + " # # #" + rt.colors.ENDC
        print '\n'.join([os.path.split(file)[1] for file in result_files])

    # Populate two lists, heads and tails, with the filepaths and filenames from result_files
    heads, tails = [], []
    for file in result_files:
        hd, tl = os.path.split(file)
        heads.append(hd + "/")
        tails.append(tl)
    assert len(heads) == len(tails)

    return result_files, heads, tails


def dirs(src_dir, output=True, limit=100):
    """
    Creates a list of all subdirectories in source directory, then works on it.
    Returns 3 values: list of all subdirectories, list of paths, and directory names.
    """
    result_dirs = [x[0] for x in os.walk(src_dir)]

    if output:
        print rt.colors.PURPLE + rt.colors.BOLD + "# # # " + \
            src_dir.upper() + " # # #" + rt.colors.ENDC
        result_dirs.pop(0)
        print '\n'.join([os.path.split(dir)[1] for dir in result_dirs])
        #for dir in result_dirs:
        #    print dir[len(str(src_dir)):]

    heads, tails = [], []
    for dir in result_dirs:
        hd, tl = os.path.split(dir)
        heads.append(hd + "/")
        tails.append(tl)
    assert len(heads) == len(tails)

    # for parent_dir, dir in zip(heads, tails):
    #     # rt.sanitize_and_rename([dir], parent_dir, my_dict, False)
    #     rt.regex_filter_list([dir], pattern, output=True)
    #     # rt.regex_group_split(rt.regex_filter_list([dir], pattern), pattern)
    #     # rt.rename_files(rt.regex_filter_list([dir], pattern, False), parent_dir, pattern, True)

    return result_dirs, heads, tails


def drilldown(src_dir, drill_count, output=True, tabs=0):
    """
    Recurses a specified number of times and returns a list of files.
    """
    result_files = []
    result_dirs = []

    if drill_count == 0:
        return result_files, result_dirs
    else:
        # Print name of src_dir (aka rootpath below)
        # if tabs != 0:
        global working_dir
        if (working_dir == src_dir):
            print (rt.colors.PURPLE + rt.colors.ULINE + rt.colors.BOLD + \
                os.path.split(src_dir)[1] + " " + rt.colors.ENDC).expandtabs(4)
        else:
            print (rt.colors.PURPLE+ "|" + rt.colors.ULINE + ("\t"* (tabs)) + rt.colors.BOLD +\
                os.path.split(src_dir)[1] + " " + rt.colors.ENDC).expandtabs(4)

        # Find all local files (non-directories) directly in src_dir and add them to result_files
        local_list = os.listdir(src_dir)

        local_files = [os.path.join(src_dir,f) for f in local_list if os.path.isfile(os.path.join(src_dir, f))]
        local_dirs = [os.path.join(src_dir,d) for d in local_list if os.path.isdir(os.path.join(src_dir, d))]

        result_files += local_files
        result_dirs += local_dirs

        # Print non-directory files in src_dir
        if len(local_files) + len(local_dirs) == 0:
            print (rt.colors.RED + "|" + ('\t' * tabs) + "|" + (u"" + unichr(746)).encode(sys.stdout.encoding) + " EMPTY " + rt.colors.ENDC).expandtabs(4)

        #
        if not (len(local_files) == 0):
            mew = local_files[-1:]
            for rfile in local_files:
                #if (rfile == mew[0]):
                print (rt.colors.PURPLE + "|" + ('\t' * tabs) + "|" +\
                 (u"" + unichr(746)).encode(sys.stdout.encoding) + " " + rt.colors.ENDC + os.path.split(rfile)[1]).expandtabs(4)

        # Create iterator, then os.walk src_dir and drilldown into each subdir (drill_count-1, tabs+1)
        # walk_iter = os.walk(src_dir)
        # for rootpath, subdirs, subfiles in walk_iter:
        #     for sd in subdirs:
        #         print ('\t' * tabs) + "SD: " + sd            
        #         dril_files, dril_dirs = drilldown(os.path.join(rootpath,sd), int(drill_count) - 1, output, tabs + 1)
        #         result_files += dril_files

        for rd in result_dirs:
            #print rt.colors.PURPLE + (get_terminal_width()/4 * (u" " + unichr(1154)).encode(sys.stdout.encoding)) + rt.colors.ENDC
            #print os.path.join(src_dir,rd)
            dril_files, dril_dirs = drilldown(os.path.join(src_dir,rd), int(drill_count) - 1, output, tabs + 1)
            result_files += [f for f in dril_files if f not in result_files]
            result_dirs += [d for d in dril_dirs if d not in result_dirs]


    if tabs == 0:
        print "\n# of files: " + str(len(result_files))
        print "# of dirs:  " + str(len(result_dirs))

    return result_files,result_dirs


def get_terminal_width():
    """
    mrermwek
    """   
    command = ['tput', 'cols']

    try:
        width = int(subprocess.check_output(command))
    except OSError as e:
        print("Invalid Command '{0}': exit status ({1})".format(
              command[0], e.errno))
    except subprocess.CalledProcessError as e:
        print("Command '{0}' returned non-zero exit status: ({1})".format(
              command, e.returncode))
    else:
        return width


def empty(src_dir, output=True):
    """
    Returns list of all empty directories within src_dir.
    """
    dir_list = [x[0] for x in os.walk(src_dir)]
    empties = []
    for dir in dir_list:
        if os.listdir(dir) == []:
            empties.append(dir[len(str(src_dir)):])

    print '\n'.join(empties)
    print len(empties)


def op_parser():
    """
    Create a parser and add options. Mostly just wanted to move this out of main().
    TODO: separate class?
    """
    # Instantiate argument parser and subparser
    parser = argparse.ArgumentParser(prog="bedrock") #prog = 'bedrock'
    sp = parser.add_subparsers(dest="cmd")

    # Instantiate groups of mutually exclusive options and add main arguments
    main_args = parser.add_mutually_exclusive_group(required=True)
    main_args.add_argument( '-b', '--bedrock', action='store_true',
                        help="Lists all filenames in directory (recursive).")
    main_args.add_argument( '-d', '--dirs', action='store_true',
                        help="Lists all subdirectories in directory (recursive).")
    main_args.add_argument('-dril', '--drilldown', 
                        help="Specify subdirectory.")

    # Add subparser cmd_parser (called w/ "eval") and add argument 
    cmd_parser = sp.add_parser('eval')
    cmd_parser.add_argument( '-l', '--list', action='store_true',
                        help="List files in directory.")
    cmd_parser.add_argument( '-f', '--filter', action='store_true',
                        help="Filter list according to pattern regex.")
    cmd_parser.add_argument( '-s', '--sanitize', action='store_true',
                        help="Sanitizes according to k-v dictionary.")
    cmd_parser.add_argument( '-c', '--check', action='store_true',
                        help="Check renaming of files before proceeding.")
    cmd_parser.add_argument( '-e', '--empty', action='store_true',
                        help="List all empty files.")
    cmd_parser.add_argument( '-rn', '--rename', action='store_true',
                        help="Rename files (it is recommended to run -c first!).")

    return parser


if __name__ == "__main__":
    main()
