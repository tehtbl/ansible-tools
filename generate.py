#!/usr/bin/env python3

import os
import sys
import yaml
import jinja2
import pprint
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
# build jinja environment
#
def get_jinja_env(local_tmpl_dir):
    jinja_env = jinja2.Environment(
        # trim_blocks=True,
        trim_blocks=False,
        autoescape=False,
        loader=jinja2.FileSystemLoader(local_tmpl_dir),
    )

    jinja_env.globals.update(
        strfmtdate=lambda d, lang: d.strftime('%d.%m.%Y') if lang is 'deutsch' else d.strftime('%Y-%m-%d'),
    )

    return jinja_env


#
# MAiN
#
if __name__ == "__main__":

    parser = OptionParser()

    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="be verbose")

    parser.add_option("-r", "--role-dir", dest="role_dir", type="string", help="work on role directory", metavar="DIR")
    parser.add_option("-a", "--gen-all", action="store_true", dest="gen_all", default=False, help="generate all files")

    parser.add_option("-g", "--github", action="store_true", dest="gen_gh", default=False, help="generate only .github/ files")
    parser.add_option("-m", "--meta", action="store_true", dest="gen_meta", default=False, help="generate meta/ files only")
    parser.add_option("-t", "--travis", action="store_true", dest="gen_travis", default=False, help="generate .travis.yml file only")
    parser.add_option("-c", "--coc", action="store_true", dest="gen_coc", default=False, help="generate CODE_OF_CONDUCT.md file only")
    parser.add_option("-n", "--contributing", action="store_true", dest="gen_cont", default=False, help="generate CONTRIBUTING.md file only")
    parser.add_option("-l", "--license", action="store_true", dest="gen_license", default=False, help="generate LICENSE file only")
    parser.add_option("-p", "--pr", action="store_true", dest="gen_pr", default=False, help="generate PR file only")
    parser.add_option("-e", "--readme", action="store_true", dest="gen_readme", default=False, help="generate README.md file only")
    parser.add_option("-s", "--security", action="store_true", dest="gen_security", default=False, help="generate SECURITY.md file only")
    parser.add_option("-x", "--tox", action="store_true", dest="gen_tox", default=False, help="generate tox.ini file only")
    parser.add_option("-y", "--vagrant", action="store_true", dest="gen_vagrant", default=False, help="generate Vagrantfile file only")

    (options, args) = parser.parse_args()

    # check for role overview file
    try:
        with open(options.roleoverviewfile) as file:
            ALL_ROLES = yaml.load(file, Loader=yaml.FullLoader)
    except Exception:
        print_error("Error reading overview file ... Exiting.")
        sys.exit(1)

    if options.verbose:
        print_log("Overview:")
        pp.pprint(ALL_ROLES)

    # check for role dir
    if options.roledir:
        if os.path.exists(options.roledir) and os.path.isdir(options.roledir):
            if not os.listdir(options.roledir):
                print_error("working directory is empty ... exiting")
                sys.exit(1)
        else:
            print_error("working directory doesn't exist ... exiting")
            sys.exit(1)
    else:
        print_error("no working dir given ... exiting")
        sys.exit(1)

    if options.verbose:
        print_log("working dir is ready for take off")

    print_log("all requirements set, starting to fly...")

    # init Jinja environment
    tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    print_log("using templates from {}".format(tmpl_dir))
    jinja_env = get_jinja_env(tmpl_dir)

    # generate github files
    if options.gen_all or options.gen_gh:
        print_log("generating github files")

        # gh_dir = os.path.join(tmpl_dir, ".github")
        gh_dir = ".github"
        gh_it_dir = os.path.join(gh_dir, "ISSUE_TEMPLATE")

        tmpl = jinja_env.get_template(os.path.join(gh_it_dir, "bug_report.md.j2"))
        for r in ALL_ROLES['roles']:
            out = tmpl.render({'role': r}).encode('utf-8')
            print(out)

        tmpl = jinja_env.get_template(os.path.join(gh_dir, "settings.yml.j2"))
        for r in ALL_ROLES['roles']:
            out = tmpl.render({'role': r}).encode('utf-8')
            print(out)

        # fd = open(os.path.join(django_swrts_settings.SWRTS_PRJ_REPORT_CUST_DIR, 'base_information.tex'), 'w')
        # fd.write(out)
        # fd.close()

    sys.exit(0)
