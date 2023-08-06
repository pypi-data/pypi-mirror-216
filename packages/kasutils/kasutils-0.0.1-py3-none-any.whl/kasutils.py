# -*- coding: UTF-8 -*-
# ToolName   : MaxPhisher
# Author     : Kas-Utils
# License    : MIT
# Copyright  : KasRoudra 2023
# Github     : https://github.com/KasRoudra
# Contact    : https://m.me/KasRoudra
# Description: A utility library in python
# Tags       : utility, library
# 1st Commit : 08/9/2022
# Language   : Python
# Portable file/script
# If you copy open source code, consider giving credit


"""
MIT License

Copyright (c) 2022-2023 KasRoudra

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, iNCluding without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be iNCluded in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from importlib import (
    import_module as eximport
)
from inspect import (
    isfunction,
    getdoc,
    getmembers,
)
from json import (
    dumps as stringify,
    loads as parse
)
from os import (
    getenv,
    kill,
    listdir,
    makedirs,
    mkdir,
    remove,
    rename as rn,
)
from os.path import (
    dirname,
    isdir,
    isfile,
    join,
)
from re import (
    search
)
from shutil import (
    move as mv,
    copy2 as cp,
    get_terminal_size,
    rmtree,
)
from signal import (
    SIGKILL,
)
from subprocess import (
    CompletedProcess,
    DEVNULL,
    PIPE,
    Popen,
    run
)
from smtplib import (
    SMTP_SSL as smtp
)
from socket import (
    AF_INET as inet,
    SOCK_STREAM as stream,
    setdefaulttimeout,
    socket,
    error as SocketError
)
from sys import (
    stdout as sout,
)
from tarfile import (
    open as taropen
)
from time import (
    sleep,
)
from zipfile import (
    ZipFile
)


# Color snippets
BLACK="\033[0;30m"
RED="\033[0;31m"
BRED="\033[1;31m"
GREEN="\033[0;32m"
BGREEN="\033[1;32m"
YELLOW="\033[0;33m"
BYELLOW="\033[1;33m"
BLUE="\033[0;34m"
BBLUE="\033[1;34m"
PURPLE="\033[0;35m"
BPURPLE="\033[1;35m"
CYAN="\033[0;36m"
BCYAN="\033[1;36m"
WHITE="\033[0;37m"
NC="\033[00m"

ENCODING = "utf-8"

# Regular Snippets
ask     =   f"{GREEN}[{WHITE}?{GREEN}] {YELLOW}"
success =   f"{YELLOW}[{WHITE}√{YELLOW}] {GREEN}"
error   =   f"{BLUE}[{WHITE}!{BLUE}] {RED}"
info    =   f"{YELLOW}[{WHITE}+{YELLOW}] {CYAN}"
info2   =   f"{GREEN}[{WHITE}•{GREEN}] {PURPLE}"

def inst_module(module: str):
    """ 
    Try to install pip modules
    """
    try:
        eximport(module)
        return True
    except ImportError:
        try:
            shell(f"pip3 install {module} --break-system-packages")
        except ImportError:
            return False
    try:
        eximport(module)
        return True
    except ImportError:
        return False


home = getenv("HOME")


def is_installed(package: str) -> bool:
    """
    Check if a process is running by 'command -v' command. 
    If it has a output exit_code will be 0 and package is already installed
    """
    return bgtask(f"command -v {package}").wait() == 0

def is_running(process: str) -> bool:
    """
    Check if a process is running by 'pidof' command.
    If pidof has a output exit_code will be 0 and process is running
    """
    return bgtask(f"pidof {process}").wait() == 0

def is_json(myjson: str) -> bool:
    """
    Check if a json is valid
    """
    try:
        parse(myjson)
        return True
    except ValueError:
        return False


def copy(path1: str, path2: str):
    """
    Copies files or folders
    """
    if isdir(path1):
        for item in listdir(path1):
            old_file = join(path1, item)
            new_file = join(path2, item)
            if isdir(old_file):
                copy(old_file, new_file)
            else:
                makedirs(dirname(new_file), exist_ok=True)
                cp(old_file, new_file)
    if isfile(path1):
        if isdir(path2):
            cp(path1, path2)

def move(path1: str, path2: str):
    """
    Copies files or folders
    """
    if isdir(path1):
        for item in listdir(path1):
            old_file = join(path1, item)
            new_file = join(path2, item)
            if isdir(old_file):
                move(old_file, new_file)
            else:
                makedirs(dirname(new_file), exist_ok=True)
                mv(old_file, new_file)
    if isfile(path1):
        if isdir(path2):
            mv(path1, path2)

def rename(path1: str, path2: str):
    """
    Copies files or folders
    """
    if isdir(path1):
        for item in listdir(path1):
            old_file = join(path1, item)
            new_file = join(path2, item)
            if isdir(old_file):
                rename(old_file, new_file)
            else:
                makedirs(dirname(new_file), exist_ok=True)
                rn(old_file, new_file)
    if isfile(path1):
        if isdir(path2):
            rn(path1, path2)

def delete(*paths, recreate=False):
    """ 
    Delete files/folders if exist
    """
    for path in paths:
        if isdir(path):
            rmtree(path)
            if recreate:
                mkdir(path)
        if isfile(path):
            remove(path)

def cat(file: str) -> str:
    """
    A poor alternative of GNU/Linux 'cat' command returning file content
    """
    if isfile(file):
        with open(file, "r", encoding=ENCODING) as filedata:
            return filedata.read()
    return ""

def sed(text1: str, text2: str, filename1: str, filename2=None, occurences=None):
    """ 
    Another poor alternative of GNU/Linux 'sed' command to replace and write
    """
    filedata1 = cat(filename1)
    if filename2 is None:
        filename2 = filename1
    if occurences is None:
        filedata2 = filedata1.replace(text1, text2)
    else:
        filedata2 = filedata1.replace(text1, text2, occurences)
    write(filedata2, filename2)

def grep(regex: str, target:str) -> str:
    """
    Another poor alternative of GNU/Linux 'grep' command for regex search
    """
    if isfile(target):
        content = cat(target)
    else:
        content = target
    results = search(regex, content)
    if results is not None:
        return results.group(1)
    return ""

def write(text: str, filename: str):
    """
    Write texts to a file
    """
    with open(filename, "w", encoding=ENCODING) as file:
        file.write(str(text)+"\n")

def append(text: str, filename: str):
    """ 
    Append texts to a file
    """
    with open(filename, "a", encoding=ENCODING) as file:
        file.write(str(text)+"\n")

def get_toml_ver(toml_path="pyproject.toml") -> str:
    """
    Grab version from toml file
    """
    toml_data = cat(toml_path)
    pattern = r'version\s*=\s*"([^"]+)"'
    match = search(pattern, toml_data)
    if match:
        return match.group(1)
    return "0.0.0"


def get_ver(ver: str) -> int:
    """
    Converts 1.2.3 to 123 for easy comparison
    """
    return int(ver.replace(".", "", 2))

def sprint(text: str, second=0.05):
    """
    Print lines slowly
    """
    for line in text + '\n':
        sout.write(line)
        sout.flush()
        sleep(second)

def lolcat(text: str):
    """
    Prints colorful texts
    """
    if is_installed("lolcat"):
        run(["lolcat"], input=text, text=True, check=True)
    else:
        print(text)

def pretty_print(
        file: str,
        character="*",
        character_color=WHITE,
        bracket_color=YELLOW,
        line_color=GREEN
    ):
    """ 
    Print decorated file content
    """
    lines = cat(file).splitlines()
    for line in lines:
        print(f"{bracket_color}[{character_color}{character}{bracket_color}]: {line_color}{line}")

def add_json(json: str, filename: str):
    """ 
    Append new entry in array and write in json file
    """
    content = cat(filename)
    if is_json(content) or content == "":
        if content == "":
            new_content = []
        if is_json(content):
            new_content = parse(content)
        if isinstance(new_content, list):
            new_content.append(json)
            string = stringify(new_content, indent=2)
            write(string, filename)

def shell(command: str, capture_output=False) -> CompletedProcess:
    """ 
    Run shell commands in python
    """
    return run(command, shell=True, capture_output=capture_output, check=True)

def bgtask(command: str, stdout=PIPE, stderr=DEVNULL, cwd="./") -> Popen:
    """ 
    Run task in background supressing output by setting stdout and stderr to devnull
    """
    return Popen(command, shell=True, stdout=stdout, stderr=stderr, cwd=cwd)


def clear(fast=False, lol=False, logo=""):
    """
    Clear the screen and show logo
    """
    shell("clear")
    if fast:
        print(logo)
    elif lol:
        lolcat(logo)
    else:
        sprint(logo, 0.01)

def is_online(host="8.8.8.8", port=53, timeout=3) -> bool:
    """
    Checks for a valid internet connection
    """
    try:
        setdefaulttimeout(timeout)
        socket(inet, stream).connect((host, port))
        return True
    except SocketError:
        return False

def installer(package: str, package_name=None) -> bool:
    """ 
    Install package by shell command. Specify a package name if it is different than the executable
    """
    if package_name is None:
        package_name = package
    for pacman in ["pkg", "apt", "apt-get", "apk", "yum", "dnf", "brew", "pacman"]:
        # Check if package manager is present but package isn't present
        if is_installed(pacman):
            if not is_installed(package):
                if pacman=="pacman":
                    shell(f"sudo {pacman} -S {package_name} --noconfirm")
                elif pacman=="apk":
                    if is_installed("sudo"):
                        shell(f"sudo {pacman} add -y {package_name}")
                    else:
                        shell(f"{pacman} add -y {package_name}")
                elif is_installed("sudo"):
                    shell(f"sudo {pacman} install -y {package_name}")
                else:
                    shell(f"{pacman} install -y {package_name}")
                break
    if is_installed(package_name):
        return True
    return False


def killer(process: str, signal=SIGKILL):
    """ 
    Kill processes by pid
    """
    if is_running(process):
        output = shell(f"pidof {process}", True).stdout.decode("utf-8").strip()
        if " " in output:
            for pid in output.split(" "):
                kill(int(pid), signal)
        elif output != "":
            kill(int(output), signal)
        else:
            pass

def send_mail(sender: str, password: str, receiver: str, subject: str, message: str):
    """ 
    Send mail by smtp library
    """
    body = f"From: {sender}\nTo: {receiver}\nSubject: {subject}\n\n{message}"
    with smtp('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, body)

def readable(byte: float, precision = 2, is_speed = False):
    """
    Bytes to KB, MB converter
    """
    for unit in ["Bt","KB","MB","GB"]:
        floatbyte = round(byte, precision)
        space = ' ' * (6 - len(str(floatbyte)))
        if byte < 1024.0:
            if is_speed:
                size = f"{floatbyte} {unit}/s{space}"
            else:
                size = f"{floatbyte} {unit}{space}"
            break
        byte /= 1024.0
    return size

def center_text(text: str, is_print=True) -> str:
    """
    Centers texts to terminal
    """
    columns = get_terminal_size().columns
    lines = text.splitlines()
    if len(lines) > 1:
        minlen = min([len(line) for line in lines if len(line)!=0]) + 8
        new_text = ""
        for line in lines:
            padding = columns + len(line) - minlen
            if columns % 2 == 0 and padding % 2 == 0:
                padding += 1
            new_text += line.center(padding) + "\n"
        if is_print:
            print(new_text)
        return new_text
    if is_print:
        print(text.center(columns+8))
    return text.center(columns+8)

def extract(filename: str, extract_path='.'):
    """ 
    Extract zip/tar/tgz files
    """
    directory = dirname(extract_path)
    if directory!="" and not isdir(directory):
        mkdir(directory)
    if ".zip" in filename:
        with ZipFile(filename, 'r') as zip_ref:
            if zip_ref.testzip() is None:
                zip_ref.extractall(extract_path)
    if ".tar" in filename or ".tgz" in filename:
        tar = taropen(filename, 'r')
        for item in tar:
            tar.extract(item, extract_path)
            # Recursion if childs are tarfile
            if ".tgz" in item.name or ".tar" in item.name:
                extract(item.name, "./" + item.name[:item.name.rfind('/')])

def get_docstrings(module=__import__(__name__)):
    """
    Returns a dictionary of function name as key and docstring as value
    """
    functions = getmembers(module, isfunction)
    docstrings = {}
    for name, func in functions:
        if func.__module__ == __name__:
            docstrings[name] = getdoc(func)
    return docstrings

def generate_readme(head_level=5):
    """
    Geneated markdown with function name and docstring
    """
    docstrings = get_docstrings()
    for name, docstring in docstrings.items():
        docstring = docstring.replace("\n", "")
        print(f"{'#'*head_level} {name}\n - ***{docstring}***")

generate_readme()
