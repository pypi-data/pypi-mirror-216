import json
from constants.commands import commands
import sys

path = "scripts.json"

def get_file() -> dict:
    """Return the json file as a dictionary"""
    with open(path, "r") as f:
        return json.load(f)
    
def get_os() -> str:
    """Return the current operating system"""
    import platform
    return platform.system()

def get_instruction() -> str:
    """Return the instruction given by the user (argv[1])"""
    return sys.argv[1]

def get_command() -> str:
    """Return the command given by the user (argv[2])"""
    return sys.argv[2]

def get_instruction() -> str:
    """Return the instruction given by the user (argv[1])"""
    return sys.argv[1]

def is_instruction_valid(instruction: str) -> bool:
    """Return True if the instruction is valid"""
    return instruction in commands

def is_command_valid(data: dict, os, command) -> bool:
    """Return True if the command is valid"""
    return os in data and command in data[os]

def get_script(data: dict, os, command) -> str:
    """Return the script from the json file"""
    return data[os][command]

def run_script(script: str):
    """Run the script"""
    import os
    os.system(script)