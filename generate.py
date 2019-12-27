#!/usr/bin/env python3

import os
import sys
import yaml
import shutil
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
    print("[{}] {}".format(Fore.ORANGE + "W" + Style.RESET_ALL, text))


def print_error(text=""):
    print("[{}] {}".format(Fore.RED + "E" + Style.RESET_ALL, text))


def print_log(text=""):
    print("[{}] {}".format(Fore.GREEN + ">" + Style.RESET_ALL, text))


def print_info(text=""):
    print("[{}] {}".format(Fore.YELLOW + "*" + Style.RESET_ALL, text))


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
        regex_replace=lambda s, x, y: s.replaceAll(x, y)
    )

    return jinja_env


#
# write out template to file
#
def write_tmpl_to_file(src, dst, fn):
    src_file = jinja_env.get_template(os.path.join(src, fn + ".j2"))
    dst_file = os.path.join(dst, fn)

    os.makedirs(dst, exist_ok=True)

    with open(dst_file, "w") as fh:
        fh.write(
            src_file.render({
                'role': ROLE_INFO
            })
        )

    print_info("created {}".format(dst_file))


#
# simply copy a file
#
def copy_file(src, dst, fn):
    src_file = os.path.join(src, fn)
    dst_file = os.path.join(dst, fn)
    shutil.copyfile(src_file, dst_file)
    print_info("created {}".format(dst_file))


#
# MAiN
#
if __name__ == "__main__":

    parser = OptionParser()

    parser.add_option("-r", "--role-dir",     type="string",       dest="role_dir",     metavar="DIR", help="work on role directory")

    parser.add_option("-v", "--verbose",      action="store_true", dest="verbose",      default=False, help="be verbose")
    parser.add_option("-a", "--gen-all",      action="store_true", dest="gen_all",      default=False, help="generate all files")

    parser.add_option("-g", "--github",       action="store_true", dest="gen_gh",       default=False, help="generate only .github/ files")
    parser.add_option("-m", "--meta",         action="store_true", dest="gen_meta",     default=False, help="generate meta/ files only")
    parser.add_option("-t", "--travis",       action="store_true", dest="gen_travis",   default=False, help="generate .travis.yml file only")
    parser.add_option("-c", "--coc",          action="store_true", dest="gen_coc",      default=False, help="generate CODE_OF_CONDUCT.md file only")
    parser.add_option("-n", "--contrib",      action="store_true", dest="gen_contrib",     default=False, help="generate CONTRIBUTING.md file only")
    parser.add_option("-l", "--license",      action="store_true", dest="gen_license",  default=False, help="generate LICENSE file only")
    parser.add_option("-p", "--pr",           action="store_true", dest="gen_pr",       default=False, help="generate PR file only")
    parser.add_option("-e", "--readme",       action="store_true", dest="gen_readme",   default=False, help="generate README.md file only")
    parser.add_option("-s", "--security",     action="store_true", dest="gen_security", default=False, help="generate SECURITY.md file only")
    parser.add_option("-x", "--tox",          action="store_true", dest="gen_tox",      default=False, help="generate tox.ini file only")
    parser.add_option("-y", "--vagrant",      action="store_true", dest="gen_vagrant",  default=False, help="generate Vagrantfile file only")
    parser.add_option("-d", "--deps",         action="store_true", dest="gen_deps",     default=False, help="generate requirements.txt file only")

    (options, args) = parser.parse_args()

    # check if role_dir exists
    ROLE_DIR = ""
    if options.role_dir:
        # ROLE_DIR = os.path.abspath(options.role_dir)
        ROLE_DIR = options.role_dir
        ROLE_INFO_FILE = os.path.join(ROLE_DIR, ".role_info.yml")

        if os.path.exists(ROLE_DIR) and os.path.isdir(ROLE_DIR):
            if not os.listdir(ROLE_DIR):
                print_error("role dir {} is empty. Exiting.".format(ROLE_DIR))
                sys.exit(1)
        else:
            print_error("role dir {} doesn't exist. Exiting.".format(ROLE_DIR))
            sys.exit(1)

        if not os.path.isfile(ROLE_INFO_FILE):
            print_error("No .role_info.yml found in {}. Exiting.".format(ROLE_DIR))
            sys.exit(1)

    else:
        print_error("No role_dir given, use -r/--role_dir <dir of role to work on>. Exiting.")
        sys.exit(1)

    # get info for role
    try:
        with open(ROLE_INFO_FILE) as file:
            ROLE_INFO = yaml.load(file, Loader=yaml.FullLoader)
    except Exception:
        print_error("Error reading role info file. Exiting.")
        sys.exit(1)

    if options.verbose:
        print_log("role info:")
        pp.pprint(ROLE_INFO)

    print_info("all requirements set, starting to fly...")

    # init Jinja2 environment
    tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    print_info("using templates from {}".format(tmpl_dir))
    jinja_env = get_jinja_env(tmpl_dir)

    # generate github files
    if options.gen_all or options.gen_gh:
        print_log("generating github files")

        src_gh_dir = ".github"
        # src_gh_dir = os.path.join(tmpl_dir, ".github")
        src_gh_it_dir = os.path.join(src_gh_dir, "ISSUE_TEMPLATE")

        dst_gh_dir = os.path.join(ROLE_DIR, ".github")
        dst_gh_it_dir = os.path.join(dst_gh_dir, "ISSUE_TEMPLATE")

        os.makedirs(dst_gh_it_dir, exist_ok=True)

        fn = "bug_report.md"
        src_file = jinja_env.get_template(os.path.join(src_gh_it_dir, fn + ".j2"))
        dst_file = os.path.join(dst_gh_it_dir, fn)

        with open(dst_file, "w") as fh:
            fh.write(
                src_file.render({
                    'role': ROLE_INFO
                })
            )

        print_info("creating {}".format(dst_file))

        fn = "feature_request.md"
        src_file = os.path.join(os.path.join(os.path.join(tmpl_dir, ".github"), "ISSUE_TEMPLATE"), fn)
        dst_file = os.path.join(dst_gh_it_dir, fn)

        shutil.copyfile(src_file, dst_file)

        print_info("creating {}".format(dst_file))

        fn = "settings.yml"
        src_file = jinja_env.get_template(os.path.join(src_gh_dir, fn + ".j2"))
        dst_file = os.path.join(dst_gh_dir, fn)

        with open(dst_file, "w") as fh:
            fh.write(
                src_file.render({
                    'role': ROLE_INFO
                })
            )

        print_info("creating {}".format(dst_file))

    # generate meta files
    if options.gen_all or options.gen_meta:
        print_log("generating meta files")

        write_tmpl_to_file(
            "meta",
            os.path.join(ROLE_DIR, "meta"),
            "main.yml"
        )

    # generate travis file
    if options.gen_all or options.gen_travis:
        print_log("generating travis file")

        write_tmpl_to_file(
            ".",
            ROLE_DIR,
            ".travis.yml"
        )

    # generate COC file
    if options.gen_all or options.gen_coc:
        print_log("generating coc file")

        copy_file(
            tmpl_dir,
            ROLE_DIR,
            "CODE_OF_CONDUCT.md"
        )

    # generate contributing file
    if options.gen_all or options.gen_contrib:
        print_log("generating contributing file")

        copy_file(
            tmpl_dir,
            ROLE_DIR,
            "CONTRIBUTING.md"
        )

    # generate license file
    if options.gen_all or options.gen_license:
        print_log("generating license file")

        copy_file(
            tmpl_dir,
            ROLE_DIR,
            "LICENSE"
        )

    # generate PR file
    if options.gen_all or options.gen_pr:
        print_log("generating PR file")

        copy_file(
            tmpl_dir,
            ROLE_DIR,
            "PULL_REQUEST_TEMPLATE.md"
        )

    # generate README file
    if options.gen_all or options.gen_readme:
        print_log("generating README file")

        # ROLE_INFO['example'] = ""
        # ROLE_INFO['prepare'] = ""
        # ROLE_INFO['vars'] = ""

        try:
            fn = os.path.join(os.path.join(os.path.join(ROLE_DIR, "molecule"), "default"), "playbook.yml")
            with open(fn, "r") as fh:
                ROLE_INFO['example'] = fh.read()
        except:
            pass

        try:
            fn = os.path.join(os.path.join(os.path.join(ROLE_DIR, "molecule"), "default"), "prepare.yml")
            with open(fn, "r") as fh:
                ROLE_INFO['prepare'] = fh.read()
        except:
            pass

        try:
            fn = os.path.join(os.path.join(ROLE_DIR, "defaults"), "main.yml")
            with open(fn, "r") as fh:
                ROLE_INFO['vars'] = fh.read()
        except:
            pass

        write_tmpl_to_file(
            ".",
            ROLE_DIR,
            "README.md"
        )

    # generate SECURITY file
    if options.gen_all or options.gen_security:
        print_log("generating SECURITY file")

        write_tmpl_to_file(
            ".",
            ROLE_DIR,
            "SECURITY.md"
        )

    # generate tox file
    if options.gen_all or options.gen_tox:
        print_log("generating tox file")

        copy_file(
            tmpl_dir,
            ROLE_DIR,
            "tox.ini"
        )

    # generate Vagrantfile
    if options.gen_all or options.gen_vagrant:
        print_log("generating Vagrantfile")

        write_tmpl_to_file(
            ".",
            ROLE_DIR,
            "Vagrantfile"
        )

    # generate requirements.yml
    if options.gen_all or options.gen_deps:
        print_log("generating requirements.yml")

        if len(ROLE_INFO['deps']) > 0:
            write_tmpl_to_file(
                ".",
                ROLE_DIR,
                "requirements.yml"
            )

    # exit 0
    sys.exit(0)
