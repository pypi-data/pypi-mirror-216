import math
from dataclasses import dataclass


@dataclass
class PositionGPS:
    """
    lat (degE7): Latitude
    lon (degE7): Longitude
    alt (m): Altitude
    """

    lat: int = 0
    lon: int = 0
    alt: float = 0

    def get_global_position_float(self) -> tuple[float, float, float]:
        return (self.lat / 1.0e7, self.lon / 1.0e7, self.alt)

    def scale_global_position(self, lat: float, lon: float, alt: float) -> None:
        self.lat = int(lat * 1.0e7)
        self.lon = int(lon * 1.0e7)
        self.alt = alt


def distance_between_points(point1: PositionGPS, point2: PositionGPS) -> float:
    """
    Calculates the distance between two GPS points using the Haversine formula.

    Args:
        point1 (PositionGPS): The first GPS position.
        point2 (PositionGPS): The second GPS position.

    Returns:
        float: The distance between the two points in meters.
    """
    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(point1.lat / 1.0e7)
    lon1 = math.radians(point1.lon / 1.0e7)
    lat2 = math.radians(point2.lat / 1.0e7)
    lon2 = math.radians(point2.lon / 1.0e7)

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return 6378137 * c
