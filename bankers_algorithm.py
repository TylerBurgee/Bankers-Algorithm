"""
Author: Tyler J. Burgee
Date: 27 March 2023
Course: CIS 390 - Operating Systems
"""

class Request:
    """Class to represent a resource allocation request"""

    def __init__(self, process: object, resources: list) -> None:
        """Defines the constructor for a Request object"""
        self.process = process
        self.resources = resources

    def __str__(self) -> str:
        """Returns the string representation of a Request object"""
        return "Request -- Process: {}, Resources: {}".format(
            self.process, self.resources)

class Process:
    """Class to represent an operating system process"""

    def __init__(self, name: str, max_need: tuple, allocation=None) -> None:
        """Defines the constructor for a Process object"""
        self.name = name
        self.max = max_need
        self.need = list(self.max)

        if allocation is None:
            self.allocation = [0] * len(self.max)
        else:
            self.allocation = allocation
            self.need = list(map(
                    lambda x, y: x - y,
                    self.max, self.allocation))

    def __str__(self) -> str:
        """Returns the string representation of a Process object"""
        return "{} -- Max: {}, Need: {}, Allocation: {}".format(
            self.name, self.max, self.need, self.allocation)

class OperatingSystem:
    """
    Class to represent an operating system using Banker's Algorithm
    to allocate system resources to processes
    """

    def __init__(self, resources: list, processes: list) -> None:
        """Defines the constructor for an OperatingSystem object"""
        self.resources = resources
        self.available = resources

        self.processes = processes

        # SUBTRACT RESOURCES ALLOCATED IN PROCESSES FROM AVAILABLE
        for process in self.processes:
            self.available = list(map(
                lambda x, y: x - y,
                self.available, process.allocation))

    def __str__(self) -> str:
        """Returns the string representation of an OperatingSystem object"""
        return "OS -- Total Resources: {} Available Resources: {}".format(
            self.resources, self.available)

    def _check_safe_(self) -> bool:
        """
        Safety algorithm for Banker's algorithm.
        Returns true if system is in safe state
        """
        work = self.available
        finish = [False for x in self.processes]
        count = len(self.processes)
        safe_sequence = []
        while count > 0:
            for i, process in enumerate(self.processes):
                if process.need <= work and not finish[i]:
                    # ADD PROCESS'S ALLOCATED RESOURCES TO WORK
                    work = list(map(
                        lambda x, y: x + y,
                        work, process.allocation))
                    finish[i] = True
                    count -= 1
                    safe_sequence.append(process.name)

        if all(finish):
            print('[%s]' % ', '.join(map(str, safe_sequence)))
            return True
        else:
            return False

    def handle_request(self, request: object) -> bool:
        """
        Resource allocation algorithm for Banker's algorithm.
        Returns true if resources were successfull allocated
        """
        # SAVE CURRENT SYSTEM STATE
        snapshot = (self.available, request.process.allocation, request.process.need)

        if request.resources <= tuple(request.process.need):
            if request.resources <= tuple(self.available):
                # PRETEND TO ALLOCATE RESOURCES
                self.available = list(map(
                    lambda x, y: x - y,
                    self.available, request.resources))

                request.process.allocation = list(map(
                    lambda x, y: x + y,
                    request.process.allocation, request.resources))

                request.process.need = list(map(
                    lambda x, y: x - y,
                    request.process.need, request.resources))

                safe = self._check_safe_()

                if safe:
                    print("\nSystem is in safe state.")
                    print("Resources {} have been allocated to {}.".format(request.resources, request.process.name))
                    return True
                else:
                    print("{} must wait to be allocated resouces.".format(request.process.name, request.resources))
                    # RESTORE SYSTEM RESOURCES TO SNAPSHOT
                    self.available, request.process.allocation, request.process.need = snapshot
            else:
                print("Requested resources are not available.\n"+
                      "{} must wait.".format(request.process.name))
        else:
            raise Exception("Request exceeded the maximum need of {}.".format(request.process.name))
        return False
    
if __name__ == "__main__":
    # DEFINE PROCESSES TO BE RUN ON OPERATING SYSTEM
    processes = [
        Process( "p0", (7, 5, 3), (0, 1, 0) ),
        Process( "p1", (3, 2, 2), (2, 0, 0) ),
        Process( "p2", (9, 0, 2), (3, 0, 2) ),
        Process( "p3", (2, 2, 2), (2, 1, 1) ),
        Process( "p4", (4, 3, 3), (0, 0, 2) )
    ]

    # INSTANTIATE OperatingSystem OBJECT
    resources = [10, 5, 7]
    os = OperatingSystem(resources, processes)

    # DISPLAY SYSTEM SNAPSHOTS
    print("-"*15, "Snapshot of OS Resources at t=0", "-"*16)
    print(os, "\n")
    print("-"*13, "Snapshot of OS Processes at t=0", "-"*14)
    for process in processes:
        print(process)
    print("-"*60)

    # CREATE REQUEST FOR PROCESS P1
    request = Request(processes[1], (1, 0, 2))
    print("\nReceived request from {} for resources {}".format(request.process.name, request.resources))

    # CHECK IF REQUEST CAN BE GRANTED
    print("Checking if request can be granted...\n")
    print("-"*11, "Safe Sequence for Resource Allocation", "-"*10)
    os.handle_request(request)

    print()

    # DISPLAY SYSTEM SNAPSHOTS
    print("-"*15, "Snapshot of OS Resources at t=1", "-"*16)
    print(os, "\n")
    print("-"*13, "Snapshot of OS Processes at t=1", "-"*14)
    for process in processes:
        print(process)
    print("-"*60)
