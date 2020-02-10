# -*- coding: utf-8 -*-
import os
import argparse
import subprocess
import shutil


FOR_REMOVING = (
    '.idea',
    '.git',
    '.gitignore',
)

IGNORE_FILES = (
    'LICENSE',
    'README.md'
)

CLONED_REPO_PATH = None
REPO_NAME = None


def set_repo_name(remote_repo):
    global REPO_NAME
    REPO_NAME = remote_repo.split('/')[-1].replace('.git', '')


def get_full_path_to_repo():
    global REPO_NAME
    return os.path.join(
        os.getcwd(), REPO_NAME
    )


def clone_repo(remote_repo):
    code = subprocess.call(['git', 'clone', remote_repo])
    if code != 0:
        raise Exception(f'Remote repository {remote_repo} not cloned.')

    global CLONED_REPO_PATH
    CLONED_REPO_PATH = get_full_path_to_repo()


def remove(path):
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)
    elif os.path.isdir(path):
        shutil.rmtree(path)
    else:
        raise ValueError(f'File {path} is not file or dir.')


def delete_selected():
    global CLONED_REPO_PATH
    for elem in FOR_REMOVING:
        remove(
            os.path.join(CLONED_REPO_PATH, elem)
        )


def is_license_text_in_file(file):
    with open(file, 'r') as f:
        for i, line in enumerate(f):
            if line.startswith('# This file is part of'):
                return True

            if i == 6:
                return False


def check_license_in_files():
    global CLONED_REPO_PATH
    for root, dirs, files in os.walk(CLONED_REPO_PATH):
        for file in files:
            path = os.path.join(root, file)
            if file not in IGNORE_FILES and not is_license_text_in_file(path):
                raise Exception(f'File {path} has no license!')


def create_archive():
    shutil.make_archive(
        CLONED_REPO_PATH.split('/')[-1], 'zip', CLONED_REPO_PATH
    )


def remove_cloned_repo():
    shutil.rmtree(CLONED_REPO_PATH)


def preparator_handler(**kwargs):
    remote_repo = kwargs.get('remote_repository')
    check_license_flag, archive_flag = kwargs.get('check_license'), kwargs.get('archive')

    set_repo_name(remote_repo)
    clone_repo(remote_repo)
    delete_selected()

    if check_license_flag:
        check_license_in_files()

    if archive_flag:
        create_archive()

    remove_cloned_repo()


def cli():
    parser = argparse.ArgumentParser('ProgSalePreparator')
    parser.add_argument('-r', '--remote-repository', metavar='', required=True)
    parser.add_argument('-c', '--check-license', action='store_true')
    parser.add_argument('-a', '--archive', action='store_true')

    args = parser.parse_args()
    preparator_handler(**vars(args))


if __name__ == '__main__':
    cli()
