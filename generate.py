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
    parser.add_option("-g", "--github", action="store_true", dest="gen_gh", default=False, help="generate only .github/ files")
    parser.add_option("-m", "--meta", action="store_true", dest="gen_meta", default=False, help="generate meta/ files only")
    parser.add_option("-t", "--travis", action="store_true", dest="gen_travis", default=False, help="generate .travis.yml file only")
    parser.add_option("-c", "--coc", action="store_true", dest="gen_coc", default=False, help="generate CODE_OF_CONDUCT.md file only")
    parser.add_option("-n", "--contributing", action="store_true", dest="gen_cont", default=False, help="generate CONTRIBUTING.md file only")
    parser.add_option("-l", "--license", action="store_true", dest="gen_license", default=False, help="generate LICENSE file only")
    parser.add_option("-p", "--pr", action="store_true", dest="gen_pr", default=False, help="generate PR file only")
    parser.add_option("-r", "--readme", action="store_true", dest="gen_readme", default=False, help="generate README.md file only")
    parser.add_option("-s", "--security", action="store_true", dest="gen_security", default=False, help="generate SECURITY.md file only")
    parser.add_option("-x", "--tox", action="store_true", dest="gen_tox", default=False, help="generate tox.ini file only")
    parser.add_option("-y", "--vagrant", action="store_true", dest="gen_vagrant", default=False, help="generate Vagrantfile file only")

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
