#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Modified version of trufflehog, for detecting secrets in
# the history of git repositories.


from __future__ import print_function

import codecs
import shutil
import sys
import math
import datetime
import argparse
import tempfile
import os
import stat
from git import Repo
from false_positives import false_positive
from dupin.utils import printerr

def main():
    parser = argparse.ArgumentParser(description='Find secrets hidden in the depths of git.')
    parser.add_argument('-o', '--output-file', dest="output_file", help="Filename to write output to (defaults to stdout)")
    parser.add_argument('git_url', type=str, help='URL for secret searching')
    args = parser.parse_args()

    project_path = tempfile.mkdtemp()
    Repo.clone_from(args.git_url, project_path)
    repo = Repo(project_path)

    if args.output_file is not None:
        with open(args.output_file, "w") as f:
            utf8_output = codecs.getwriter('utf8')
            utf8_file = utf8_output(f)
            find_strings(repo, output_file=utf8_file)
    else:
        find_strings(repo)
    shutil.rmtree(project_path, onerror=del_rw)


BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
HEX_CHARS = "1234567890abcdefABCDEF"

def del_rw(action, name, exc):
    os.chmod(name, stat.S_IWRITE)
    os.remove(name)

def shannon_entropy(data, iterator):
    """
    Borrowed from http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html
    """
    if not data:
        return 0
    entropy = 0
    for x in iterator:
        p_x = float(data.count(x))/len(data)
        if p_x > 0:
            entropy += - p_x*math.log(p_x, 2)
    return entropy


def get_strings_of_set(word, char_set, threshold=20):
    count = 0
    letters = ""
    strings = []
    for char in word:
        if char in char_set:
            letters += char
            count += 1
        else:
            if count > threshold:
                strings.append(letters)
            letters = ""
            count = 0
    if count > threshold:
        strings.append(letters)
    return strings

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def focus_diff(diffText, search):
    """Focus diff's text on the relevant parts"""
    prev_1 = None
    prev_2 = None
    context_count = 0
    result = []
    for line in diffText.split("\n"):
        if search in line:
            if prev_2 is not None:
                result.append(prev_2)
                prev_2 = None
            if prev_1 is not None:
                result.append(prev_1)
                prev_1 = None
            result.append(line)
            context_count = 2
        else:
            if context_count > 0:
                result.append(line)
                context_count = context_count - 1
            prev_2 = prev_1
            prev_1 = line
    return "\n".join(result)

def find_strings(repo, output_file=sys.stdout):
    already_searched = set()
    # for remote_branch in itertools.chain(["origin/master"], repo.remotes.origin.fetch()):
    for remote_branch in repo.remotes.origin.fetch():
        branch_name = str(remote_branch).split('/')[1]
        try:
            repo.git.checkout(remote_branch, b=branch_name)
        except:
            printerr("Could not check out remote branch {remote_branch}".format(remote_branch=remote_branch))
            continue
        for commit in repo.iter_commits():
            hash = str(commit)
            if hash in already_searched:
                # avoid searching the same diffs
                continue
            already_searched.add(hash)
            # don't search diff for merge commits
            if len(commit.parents) == 1:
                diff = commit.parents[0].diff(commit, create_patch=True)
                diffs = search_diff(diff)
                if len(diffs) > 0:
                    print_diff_details(diffs, commit, branch_name, output_file)
    return

def search_diff(diff):
    printableDiffs = []
    for blob in diff:
        stringsFound = False
        printableDiff = blob.diff.decode('utf-8', errors='replace')
        if printableDiff.startswith("Binary files"):
            continue
        lines = blob.diff.decode('utf-8', errors='replace').split("\n")
        for line in (l for l in lines if l.startswith("+")):
            if false_positive(line[1:]) is False:
                for word in line.split():
                    base64_strings = get_strings_of_set(word, BASE64_CHARS)
                    hex_strings = get_strings_of_set(word, HEX_CHARS)
                    for string in base64_strings:
                        b64Entropy = shannon_entropy(string, BASE64_CHARS)
                        if b64Entropy > 4.5 and "abcdefghijklmnopqrstuvwxyz" not in string.lower():
                            stringsFound = True
                            printableDiff = printableDiff.replace(string, bcolors.WARNING + string + bcolors.ENDC)
                    for string in hex_strings:
                        hexEntropy = shannon_entropy(string, HEX_CHARS)
                        if hexEntropy > 3 and "abcdefghijklmnopqrstuvwxyz" not in string.lower():
                            stringsFound = True
                            printableDiff = printableDiff.replace(string, bcolors.WARNING + string + bcolors.ENDC)
        if stringsFound:
            printableDiffs.append(printableDiff)

    return printableDiffs

def print_diff_details(diffs, commit, branch, output_file):
    commit_time =  datetime.datetime.fromtimestamp(commit.committed_date).strftime('%Y-%m-%d %H:%M:%S')
    print(bcolors.OKGREEN + commit.hexsha + bcolors.ENDC, file=output_file)
    print(bcolors.OKGREEN + "Date: " + commit_time + bcolors.ENDC, file=output_file)
    print(bcolors.OKGREEN + "Branch: " + branch + bcolors.ENDC, file=output_file)
    print(bcolors.OKGREEN + "Commit: " + commit.message + bcolors.ENDC, file=output_file)
    for diff in diffs:
        print(focus_diff(diff, bcolors.WARNING), file=output_file)


if __name__ == "__main__":
    main()
