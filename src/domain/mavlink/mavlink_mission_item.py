class MavlinkMissionItem:
    def __init__(
        self,
        target_system: int,
        target_component: int,
        seq: int,
        frame: int,
        command: int,
        current: int,
        autocontinue: int,
        param1: float,
        param2: float,
        param3: float,
        param4: float,
        x: float,
        y: float,
        z: float,
    ):
        self.target_system = target_system
        self.target_component = target_component
        self.seq = seq
        self.frame = frame
        self.command = command
        self.current = current
        self.autocontinue = autocontinue
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3
        self.param4 = param4
        self.x = x
        self.y = y
        self.z = z

    def to_dict(self) -> dict:
        return {
            "target_system": self.target_system,
            "target_component": self.target_component,
            "seq": self.seq,
            "frame": self.frame,
            "command": self.command,
            "current": self.current,
            "autocontinue": self.autocontinue,
            "param1": self.param1,
            "param2": self.param2,
            "param3": self.param3,
            "param4": self.param4,
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }
