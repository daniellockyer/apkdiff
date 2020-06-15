#!/usr/bin/python

import sys
import os
import zipfile
from filecmp import *
from subprocess import call, STDOUT
import shutil
import re
import argparse
import difflib

at = "at/"
ignore = ".*(align|apktool.yml|pak|MF|RSA|SF|bin|so)"
count = 0
args = None
d = difflib.Differ()

class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'

def format(string, col):
    return col + string + '\033[0m'

def main():

    print("")
    print("\t\t\t apktool")
    print("")

    parser = argparse.ArgumentParser(description='Diff two versions of an APK file.')
    parser.add_argument('apk1', metavar='apk1', help='Location of the first APK.')
    parser.add_argument('apk2', metavar='apk2', help='Location of the second APK.')
    parser.add_argument('-c', '--cleanup', action='store_true', help='Remove all extracted files after computation.')
    parser.add_argument('-m', '--meld', action='store_true', help='Open meld to compare directories after.')
    parser.add_argument('-o', '--output', default="/tmp/apkdiff/", help='The location to output the extracted files to.')
    
    global args
    args = parser.parse_args()

    # Make sure the APKs exist.
    exists(args.apk1)
    exists(args.apk2)
    
    # Check the temporary folder exists & clear it.
    folderExists(args.output, True)

    # Individual folders for each APK.
    temp1 = args.output + "1/"
    temp2 = args.output + "2/"

    # Extracted code + resources from Apktool.
    at1 = temp1 + at
    at2 = temp2 + at

    folderExists(temp1, True)
    folderExists(temp2, True)

    extract(args.apk1, temp1)
    extract(args.apk2, temp2)

    apktoolit(args.apk1, at1)
    apktoolit(args.apk2, at2)

    compare(at1, at2)

    # Remove all the stuff we have created.
    if args.cleanup and os.path.exists(temp1):
        shutil.rmtree(temp1)

    if args.cleanup and os.path.exists(temp2):
        shutil.rmtree(temp2)

    if args.meld:
        call(["meld", at1, at2])

def apktoolit(file, dir):
    print("Running apktool against '" + format(file, bcolors.OKBLUE) + "'")
    call(["apktool", "d", "--no-debug-info", "-o", dir, file], stdout=open(os.devnull, 'w'), stderr=STDOUT)
    print("[" + format("OK", bcolors.OKGREEN) + "]")

def compare(folder1, folder2):
    print("")
    compared = dircmp(folder1, folder2)
    report_full_closure(compared)
    print("\n\t" + format(str(count), bcolors.OKBLUE) + " files are different.\n")

def report_full_closure(self):
    for name in self.diff_files:

        if not re.match(ignore, name):
            print("[" + format(name, bcolors.OKGREEN)  + "] " + 
                    format(self.left.replace(args.output + "1",""), bcolors.OKBLUE))

            content1 = reader(self.left + "/" + name).splitlines(1)
            content2 = reader(self.right + "/" + name).splitlines(1)

            diff = difflib.unified_diff(content1, content2)
            tidy(list(diff))

            global count
            count += 1

    for sd in self.subdirs.values():
        report_full_closure(sd)

def tidy(lines):
    sorted = ""

    for line in lines:
        if line[:1] == "+":
            line = format(line, bcolors.OKGREEN)
        elif line[:1] == "-":
            line = format(line, bcolors.FAIL)

        sorted += line

    print(sorted)

def reader(file):
    f = open(file, 'r', encoding='utf8', errors='ignore')
    data = f.read()
    f.close()
    return data

def folderExists(path, clean=False):
    if clean and os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)

def exists(file):
    if not os.path.isfile(file):
        print(format("'{}' does not exist.".format(file), bcolors.FAIL))
        exit(0)

def extract(apk, dir):
    zipfi = zipfile.ZipFile(apk, 'r')
    zipfi.extract("classes.dex", dir)
    zipfi.close()
    print("Extracted '" + format("classes.dex", bcolors.OKBLUE) + "' from '" + format(apk, bcolors.OKBLUE) + "'.")

if __name__ == '__main__':
    main()
