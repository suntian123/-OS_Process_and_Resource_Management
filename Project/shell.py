from Process import *
from Resource import ResourceError
from scheduler import scheduler

class Shell:
    def __init__(self, input_path: str = None, output_path: str = None):
        self.__run(input_path, output_path)

    def _validate_command(self, command: list):
        command_argc = {"init": 1,
                        "cr": 3,
                        "de": 2,
                        "req": 3,
                        "rel": 3,
                        "to": 1,
                        "ps": 1,
                        "rls": 1}

        argc = len(command)
        if argc < 1:
            raise CommandError("ERROR: no command given")

        if len(command) == 1 and command[0] == "quit":
            raise QuitError

        if command[0] not in command_argc:
            raise ShellError("ERROR: command not found")

        if argc != command_argc[command[0]]:
            raise ShellError("ERROR: invalid command arguments")


    def _execute_command(self, command: list):
        commands = {"init": "Shell.init",
                    "cr": "Shell.create_process",
                    "de": "Shell.destroy_process",
                    "req": "Shell.request_resource",
                    "rel": "Shell.release_resource",
                    "to": "Shell.timeout",
                    "ps": "Shell.process_status",
                    "rls": "Shell.ready_list_status"}

        cmd = commands[command[0]]
        param_string = ""
        if (len(command[1:])):
            param_string = ", '" + "', '".join(command[1:]) + "'"

        exec(cmd + "(self" + param_string + ")")

        if(command[0] in ["init", "cr", "de", "req", "rel", "to"]):
            scheduler()

    def init(self):
        for child in self.init.tree.children:
            child.kill()

        PCB.CurrentProcess = self.init

    def create_process(self, PID: str, priority: str):
        priority = int(priority)

        if priority not in [0,1,2]:
            raise ProcessError("Priority must be 0, 1, or 2")

        PCB.CurrentProcess.child_process(PID, priority)

    def destroy_process(self, PID: str):
        if PID not in ProcessTable.table:
            raise ProcessError("ERROR: Process " + PID + " does not exist")

        process = ProcessTable.table[PID]

        if process.priority == 0:
            raise ProcessError("ERROR: Cannot delete the init process")

        if not PCB.CurrentProcess.has_child(process):
            raise ProcessError("ERROR: Process " + PID + " is not the current process nor a descendant of it")

        ProcessTable.table[PID].kill()

    def request_resource(self, RID: str, units: str):
        units = int(units)
        PCB.CurrentProcess.request(RID, units)

    def release_resource(self, RID: str, units: str):
        units = int(units)
        PCB.CurrentProcess.release(RID, units)

    def timeout(self):
        PCB.CurrentProcess.timeout()

    def process_status(self):
        print(ProcessTable())

    def ready_list_status(self):
        print(PCB.ReadyList)

    def __process_command(self, command):
        try:
            self._validate_command(command)
            self._execute_command(command)
            return PCB.CurrentProcess.PID
        except QuitError:
            return
        except CommandError:
            return "\n"
        except (ShellError, ResourceError, ProcessError) as e:
            print("*", e)
            return "error"


    def __run(self, input_path, output_path):

        self.init = PCB("init", 0)
        scheduler()

        if input_path is None:
            while (True):
                print("> ", end="")
                command_line = input()
                command = command_line.split()
                self.__process_command(command)
        else:
            output_list = []
            with open(input_path, mode="r") as in_file:
                line = ["init"]
                for command_line in in_file:
                    if command_line.strip() == '':
                        to_append = " ".join(line)
                        if to_append.strip() != '':
                            output_list.append(to_append)
                        line = []
                    else:
                        result = self.__process_command(command_line.split())
                        line.append(result)

                if len(line):
                    output_list.append(" ".join(line))

            output_str = "\n".join(output_list)
            if output_path is not None:
                with open(output_path, mode="w") as out_file:
                    out_file.write(output_str)
            else:
                print(output_str)


class ShellError(Exception):
    pass

class CommandError(Exception):
    pass

class QuitError(Exception):
    pass
