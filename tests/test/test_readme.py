"""
make test T=test_readme.py
"""
import os
from . import TestIV


class TestReadme(TestIV):
    """
    example code for readme.md
    """
    @staticmethod
    def test_readme():
        """
        example code
        """
        from oeg_iv import TypeHorWeld, TypeDefekt, DefektSide
        from oeg_iv.orientation import Orientation
        from oeg_iv.csvfile import File
        from oeg_iv.csvfile.row import Row

        # create empty csv
        csv_file = File()

        # define tube at distance 1.0 m
        # length = 11.0 m, thick = 10.5 mm
        # with one seam with orientation 3 hour 00 minutes
        csv_file.data = [
          Row.as_weld(1000),
          Row.as_thick(1010, 105),
          Row.as_seam(1020, TypeHorWeld.HORIZONTAL, Orientation(3, 0), None),
          Row.as_weld(12000),
        ]

        # add defect to tube at distance 5.0 m from left tube weld
        # length = 20 mm, width = 10 mm, depth = 30% tube wall thickness
        # orientation from 4 hours 00 minutes to 5 hours 00 minutes
        # max depth point at 10 mm from left border of defect, orientation 4 hours 30 minutes
        # with comment 'metal loss'
        csv_file.data.append(Row.as_defekt(
          6000,
          TypeDefekt.CORROZ,
          DefektSide.INSIDE,
          '20', '10', '30',
          Orientation(4, 0), Orientation(5, 0),
          Orientation(4, 30), 6010,
          'metal loss'
        ))

        # save csv to file
        csv_file.to_file('example.csv')
        assert os.path.getsize('example.csv') > 0

        # create copy from saved file
        csv_copy = File.from_file('example.csv')

        # check distance of the last object in copy
        assert csv_copy.total_length == 12000
        assert len(csv_copy.data) == 5

        # check defect orientation
        defect_row = csv_copy.data[3]
        assert defect_row.is_defect
        assert defect_row.orient_td == '4,00'
        assert defect_row.orient_bd == '5,00'
        assert defect_row.mpoint_orient == '4,30'

        # reverse copy
        csv_copy.reverse()

        # relative position of defekt must change
        defect_row = csv_copy.data[2]
        assert defect_row.is_defect

        # defect orientation must be mirrored
        assert defect_row.orient_td == '7,00'
        assert defect_row.orient_bd == '8,00'
        assert defect_row.mpoint_orient == '7,30'

        # save reversed copy to file
        csv_file.to_file('reversed.csv')
        assert os.path.getsize('reversed.csv') > 0

        # append to initial csv empty tube with length = 10.0 m and reversed copy from file
        csv_file.join([10000, 'reversed.csv'])
        assert csv_file.total_length == 28000
        assert len(csv_file.data) == 11

        # compress distances and length of all objects in half
        csv_file.dist_modify([[0, 0], [28000, 14000]])
        assert csv_file.total_length == 14000

        # save file with compress distances
        csv_file.to_file('transformed.csv')
        assert os.path.getsize('transformed.csv') > 0

        # load new copy
        csv_trans = File.from_file('transformed.csv')

        # iterate by tubes
        warnings = []
        current_dist = 0
        for tube in csv_trans.get_tubes(warnings):
            assert tube.dist >= current_dist
            current_dist = tube.dist

        assert not warnings

        os. remove('example.csv')
        os. remove('reversed.csv')
        os. remove('transformed.csv')
