from Resource import *
from Process import *






def _preempt(process: PCB):
    prev_process = PCB.CurrentProcess
    if prev_process is not None and prev_process.status.type == Status.RUNNING:
            prev_process.status.type = Status.READY

    process.status.type = Status.RUNNING
    output = "* "
    current = PCB.CurrentProcess

    if current is not None and current.status.type == Status.BLOCKED:
        output += "Process " + current.PID + " is blocked; "
    output += "Process " + process.PID + " is running"
    PCB.CurrentProcess = process
    print(output)

def scheduler():
    process = PCB.ReadyList.find_priority()
    if (PCB.CurrentProcess is None or
        PCB.CurrentProcess.priority < process.priority or
        PCB.CurrentProcess.status.type != Status.RUNNING):
        _preempt(process)

