"""Tubes iterator interface for InspectionViewer export csv file."""
from .. import Error, LINEOBJ, DEFEKTS


def count_items(items):
    """Return dict with counted item codes."""
    result = {}
    for item in items:
        code = int(item.object_code)
        if code in result:
            result[code] += 1
        else:
            result[code] = 1

    return result


def defects_summary(defects):
    """Return string with given defects summary by types."""
    result = count_items(defects)
    return ', '.join(["{}: {}".format(DEFEKTS[key], result[key]) for key in sorted(result.keys())])


def lineobj_summary(lineobjects):
    """Return string with given lineobjects summary."""
    result = count_items(lineobjects)
    return ', '.join(["{}: {}".format(LINEOBJ[key], result[key]) for key in sorted(result.keys())])


class Tube:
    """Represent one pipe."""

    def __init__(self, row, stream):
        """Construct new tube object from IV csv row with given data stream state."""
        self.row = row
        self.dist = int(row.dist_od)
        self.stream = stream

        self.typ = None
        self.length = None
        self.thick = None
        self.category = None

        self.is_thick_change = False
        self.is_category_change = False

        self.seams = []
        self.lineobjects = []
        self.defects = []
        self.categories = []
        self.thicks = []

    def finalize(self, dist, _warns):
        """Finalize tube data at given dist."""
        self.length = int(dist) - self.dist

    def add_object(self, row):
        """Add data to tube from IV csv row."""
        if row.is_defect:
            self.defects.append(row)
        elif row.is_lineobj:
            self.lineobjects.append(row)
        elif row.is_seam:
            self.seams.append(row)
        elif row.is_category:
            self.categories.append(row)
        elif row.is_thick:
            self.thicks.append(row)

        else:
            raise Error("Tube at dist {} has wrong row: {}".format(self.dist, str(row)))

    def set_geo(self, latitude, longtitude, altitude):
        """Set geo coords for tube."""
        self.row.set_geo(latitude, longtitude, altitude)

    @property
    def latitude(self):
        """Tube start latitude."""
        return self.row.latitude

    @property
    def longtitude(self):
        """Tube start longtitude."""
        return self.row.longtitude

    @property
    def altitude(self):
        """Tube start altitude."""
        return self.row.altitude

    @property
    def radius(self):
        """Return tube curve radius."""
        return self.row.depth_min

    def set_radius(self, val):
        """Set tube curve radius."""
        self.row.depth_min = val

    @property
    def number(self):
        """Tube custom number."""
        return self.row.object_name.strip()

    @property
    def summary(self):
        """Return string with summary for given tube."""
        result = []

        line = defects_summary(self.defects)
        if line:
            result.append(line)

        line = lineobj_summary(self.lineobjects)
        if line:
            result.append(line)

        return ', '.join(result)
