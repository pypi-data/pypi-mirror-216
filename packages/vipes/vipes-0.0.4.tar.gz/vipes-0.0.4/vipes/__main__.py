import interpreter as i
from utils.log import log
from constants.errors import Errors
from constants.logLevels import LogLevel

def main():
    os = i.get_os()
    instruction = i.get_instruction()
    if not i.is_instruction_valid(instruction):
        log(Errors.INVALID_INSTRUCTION, LogLevel.ERROR)
        return
    command = i.get_command()
    if not i.is_command_valid(i.get_file(), os, command):
        log(Errors.INVALID_COMMAND, LogLevel.ERROR)
        return
    data = i.get_file()
    script = i.get_script(data, os, command)
    i.run_script(script)

if __name__ == "__main__":
    main()