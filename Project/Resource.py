class ResourceControlBlock:
    def __init__(self, RID: str, units: int):
        self.RID = RID
        self.units_max = units
        self.units_available = units
        self.units_allocated = 0
        self.waiting_list = []
        self.allocated_to = dict()

    def request(self, units: int, process: 'Process') -> bool:
        if units > self.units_max:
            raise ResourceError("ERROR: Cannot request more units than max")

        if units <= 0:
            raise ResourceError("ERROR: Cannot request 0/negative units")

        if self.RID in process.resources:
            if process.resources[self.RID] + units > self.units_max:
                raise ResourceError("ERROR: Units requested would allow process to have more than the existing units")

        if units <= self.units_available:
            self.units_allocated += units
            self.units_available -= units
            self.allocated_to[process] = units
            return True
        else:
            self.waiting_list.append((process, units))
            return False

    def release(self, units: int, process: 'Process'):

        if self.allocated_to[process] < units:
            raise ResourceError("ERROR: cannot release more units than held")

        if units <= 0:
            raise ResourceError("ERROR: cannot release 0/negative units")

        self.units_available += units
        self.units_allocated -= units

        self.allocated_to[process] -= units
        if self.allocated_to[process] == 0:
            self.allocated_to.pop(process, None)


    def status(self) -> bool:
        return self.units_available > 0

class ResourceTable():
    _instance = None
    table = dict()

    for i in range(1, 5):
        id = "R" + str(i)
        table[id] = ResourceControlBlock(id, i)

    def __init__(self):
        self.table = ResourceTable.table

class ResourceError(Exception):
    pass