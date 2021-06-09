"""Tubes interface.

make test T=test_csv/test_tubes.py
"""
import pytest
from . import TestCsv


class TestTubes(TestCsv):
    """Test tubes.py module."""

    def setUp(self):
        """Init tube tests."""
        TestCsv.setUp(self)
        from oeg_iv.csvfile import Stream
        from oeg_iv.csvfile.tubes import Tube
        from oeg_iv.csvfile.row import Row

        self.tube = Tube(Row.as_weld(10), Stream())

    def test_add_object(self):
        """Add object."""
        from oeg_iv import Error
        from oeg_iv.csvfile.row import Row

        with pytest.raises(Error) as err:
            self.tube.add_object(Row.as_weld(11))
        assert 'Tube at dist 10 has wrong row:' in str(err.value)

    def test_geo(self):
        """Geo data."""
        self.tube.set_geo(10, 11, 12)
        assert self.tube.latitude == 10
        assert self.tube.longtitude == 11
        assert self.tube.altitude == 12

    def test_radius(self):
        """Curve radius."""
        assert self.tube.radius == ''
        self.tube.set_radius('100')
        assert self.tube.radius == '100'
