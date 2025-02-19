class MavlinkTelemetry:
    def __init__(
        self,
        time_boot_ms: int,
        lat: float,
        lon: float,
        alt: float,
        relative_alt: float,
        vx: float,
        vy: float,
        vz: float,
        heading: float,
        airspeed: float,
        groundspeed: float,
        throttle: float,
        battery_voltage: float,
        battery_current: float,
        battery_remaining: float,
        gps_num_satellites: int,
        gps_fix_type: int,
        armed: bool,
    ):
        self.time_boot_ms = time_boot_ms
        self.lat = lat
        self.lon = lon
        self.alt = alt
        self.relative_alt = relative_alt
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.heading = heading
        self.airspeed = airspeed
        self.groundspeed = groundspeed
        self.throttle = throttle
        self.battery_voltage = battery_voltage
        self.battery_current = battery_current
        self.battery_remaining = battery_remaining
        self.gps_num_satellites = gps_num_satellites
        self.gps_fix_type = gps_fix_type
        self.armed = armed

    def to_dict(self) -> dict:
        return {
            "time_boot_ms": self.time_boot_ms,
            "lat": self.lat,
            "lon": self.lon,
            "alt": self.alt,
            "relative_alt": self.relative_alt,
            "vx": self.vx,
            "vy": self.vy,
            "vz": self.vz,
            "heading": self.heading,
            "airspeed": self.airspeed,
            "groundspeed": self.groundspeed,
            "throttle": self.throttle,
            "battery_voltage": self.battery_voltage,
            "battery_current": self.battery_current,
            "battery_remaining": self.battery_remaining,
            "gps_num_satellites": self.gps_num_satellites,
            "gps_fix_type": self.gps_fix_type,
            "armed": self.armed,
        }
