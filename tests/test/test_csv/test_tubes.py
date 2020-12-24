"""
make test T=test_csv/test_tubes.py
"""
from . import TestCsv


class TestTubes(TestCsv):
    """
    tubes.py
    """
    def test_add_object(self):
        """
        add_object
        """
        from oeg_iv import Error
        from oeg_iv.csvfile import Stream
        from oeg_iv.csvfile.tubes import Tube
        from oeg_iv.csvfile.row import Row

        tube = Tube(10, Stream())

        with self.assertRaises(Error) as context:
            tube.add_object(Row.as_weld(11))
        assert 'Tube at dist 10 has wrong row:' in str(context.exception)
