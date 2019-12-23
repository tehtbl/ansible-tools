#!/usr/bin/env python3

import os
import sys
import yaml
import errno
import pprint
import random
import colorama

from colorama import Fore, Style
from optparse import OptionParser

colorama.init(autoreset=True)
pp = pprint.PrettyPrinter(indent=4)


#
# prints
#
def print_warn(text=""):
    print("[{}] {}".format(Fore.GREEN + "W" + Style.RESET_ALL, text))


def print_error(text=""):
    print("[{}] {}".format(Fore.RED + "E" + Style.RESET_ALL, text))


def print_log(text=""):
    print("[{}] {}".format(Fore.YELLOW + ">" + Style.RESET_ALL, text))


#
# MAiN
#
if __name__ == "__main__":

    # usage = "usage: %prog [options]"
    # parser = OptionParser(usage=usage)

    parser = OptionParser()
    parser.add_option("-o", "--overview", dest="overviewfile", type="string", help="overview file to use",
                      metavar="FILE")
    parser.add_option("-w", "--working-dir", dest="workingdir", type="string",
                      help="working directory where roles are stored", metavar="DIR")

    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="be verbose")

    parser.add_option("-a", "--all", action="store_true", dest="gen_all", default=False, help="generate all files")
    parser.add_option("-r", "--readme", action="store_true", dest="gen_readme", default=False, help="generate only README")
    parser.add_option("-r", "--readme", action="store_true", dest="gen_readme", default=False, help="generate only README")
    parser.add_option("-r", "--readme", action="store_true", dest="gen_readme", default=False, help="generate only README")
    parser.add_option("-r", "--readme", action="store_true", dest="gen_readme", default=False, help="generate only README")
    parser.add_option("-r", "--readme", action="store_true", dest="gen_readme", default=False, help="generate only README")
    parser.add_option("-r", "--readme", action="store_true", dest="gen_readme", default=False, help="generate only README")



    (options, args) = parser.parse_args()

    # print_warn("test")
    # print_error("test")
    # print_log("test")

    try:
        with open(options.overviewfile) as file:
            OVERVIEW = yaml.load(file, Loader=yaml.FullLoader)
    except Exception:
        print_error("Error reading overview file ... Exiting.")
        sys.exit(1)

    if options.verbose:
        print_log("Overview:")
        pp.pprint(OVERVIEW)

    if os.path.exists(options.workingdir) and os.path.isdir(options.workingdir):
        if not os.listdir(options.workingdir):
            print_error("working directory is empty ... exiting")
            sys.exit(1)
    else:
        print_error("working directory doesn't exist ... exiting")
        sys.exit(1)

    if options.verbose:
        print_log("working dir is ready for take off")

    print_log("all requirements set, starting to fly...")

    # TODO: init Jinja environment

    # 

    # generate README.md
    if options.gen_all or options.gen_readme:
        pass
