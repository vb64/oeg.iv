"""
make test T=test_iv/test_csv/test_init.py
"""
import os
from . import TestCsv


class TestInit(TestCsv):
    """
    __init__.py
    """
    @staticmethod
    def check_objects(objects, val_list):
        """
        compare objrcts list with expected values
        """
        assert len(objects) == len(val_list)
        for item, vals in zip(objects, val_list):
            assert item.dist_od == vals[0]
            assert item.depth_max == vals[1]

    def test_no_thick_category(self):
        """
        reverse data file without thick and category objects
        """
        from oeg_iv.csvfile import File

        csv_file = File.from_file(self.fixture('no_thicks.csv'))
        assert len(csv_file.data) == 8

        csv_file.reverse()
        assert len(csv_file.data) == 8

    def test_no_welds(self):
        """
        reverse data file without welds
        """
        from oeg_iv.csvfile import File

        csv_file = File.from_file(self.fixture('no_welds.csv'))
        assert len(csv_file.data) == 1

        csv_file.reverse()
        assert len(csv_file.data) == 1

    def test_reverse(self):
        """
        reverse
        """
        from oeg_iv.csvfile import File

        csv_file = File.from_file(self.fixture('DefTable.csv'))
        assert len(csv_file.data) == 178

        expected = [
          ('1000', '1'),
          ('52428', '3'),
          ('308392', '2'),
        ]
        self.check_objects(csv_file.categories, expected)

        expected = [
          ('1300', '90'),
          ('63628', '70'),
          ('306232', '100'),
        ]
        self.check_objects(csv_file.thicks, expected)

        assert len(csv_file.data[0].values()) == len(File.COLUMN_HEADS)
        assert csv_file.total_length == 426625

        csv_file.reverse()

        assert len(csv_file.data) == 178
        assert csv_file.total_length == 426625

        expected = [
          ('0', ''),
          ('1', ''),
          ('2', '100'),
          ('3', '2'),
        ]
        self.check_objects(csv_file.data[:4], expected)

        fname = os.path.join('build', 'output.csv')
        if os.path.exists(fname):
            os.remove(fname)

        csv_file.to_file(fname)
        assert os.path.exists(fname)
        csv_file = File.from_file(fname)

        assert len(csv_file.data) == 178
        assert csv_file.total_length == 426625

        expected = [
          ('3', '2'),
          ('374197', '3'),
          ('425625', '1'),
        ]
        self.check_objects(csv_file.categories, expected)

        expected = [
          ('2', '100'),
          ('362997', '70'),
          ('425325', '90'),
        ]
        self.check_objects(csv_file.thicks, expected)

        os.remove(fname)

    def test_join(self):
        """
        join
        """
        from oeg_iv.csvfile import File

        fname = self.fixture('DefTable.csv')
        csv_file = File.from_file(fname)

        assert len(csv_file.data) == 178
        assert csv_file.total_length == 426625

        csv_file.join(['11000', fname])

        assert len(csv_file.data) == (178 * 2 + 1)
        assert csv_file.total_length == (426625 * 2 + 11000)

    def test_join_short(self):
        """
        join short file
        """
        from oeg_iv.csvfile import File

        fname = self.fixture('1.csv')
        csv_file = File.from_file(fname)

        assert len(csv_file.data) == 7
        assert csv_file.total_length == 8800

        csv_file.join(['11000', fname])

        assert len(csv_file.data) == (7 * 2 + 1)
        assert csv_file.total_length == (8800 * 2 + 11000)

        fname = os.path.join('build', '1.csv')
        if os.path.exists(fname):
            os.remove(fname)

        csv_file.to_file(fname)
        assert os.path.exists(fname)

    @staticmethod
    def test_transform_length_wrong():
        """
        transform_length with wrong data
        """
        from oeg_iv.csvfile import transform_length

        table = [[0, 0], [10, 5]]
        assert transform_length(0, '-', table, 0) == '-'

    @staticmethod
    def test_transform_length():
        """
        transform_length
        """
        from oeg_iv.csvfile import transform_length

        table = [[0, 0], [100, 50]]
        assert transform_length(10, '40', table, 0) == 20

    @staticmethod
    def test_transform_dist():
        """
        transform_dist
        """
        from oeg_iv.csvfile import transform_dist

        table = [[0, 0], [10, 5]]
        indx = 0

        new_indx, pos = transform_dist(0, table, indx)
        assert pos == 0
        assert new_indx == indx

        new_indx, pos = transform_dist(10, table, indx)
        assert pos == 5
        assert new_indx == indx

        new_indx, pos = transform_dist(5, table, indx)
        assert pos == 3
        assert new_indx == indx

        new_indx, pos = transform_dist(-10, table, indx)
        assert pos == -10
        assert new_indx == indx

        new_indx, pos = transform_dist(20, table, indx)
        assert pos == 15
        assert new_indx == indx

        table = [[2, 5], [10, 15]]
        indx = 0

        new_indx, pos = transform_dist(5, table, indx)
        assert pos == 9
        assert new_indx == indx

    def test_load_dist_modify(self):
        """
        load_dist_modify
        """
        from oeg_iv.csvfile import File

        table = File.load_dist_modify(self.fixture('unsorted_modifi.csv'))
        assert table[0] == [0, 0]
        assert table[-1] == [4656750, 4665340]

    def test_dist_modify(self):
        """
        dist_modify
        """
        from oeg_iv.csvfile import File
        from oeg_iv import Error

        fname = self.fixture('infotech.csv')
        csv_file = File.from_file(fname)

        assert len(csv_file.data) == 30897
        assert csv_file.total_length == 130111900

        mname = self.fixture('dist_modifi.csv')
        table = File.load_dist_modify(mname)
        assert len(table) == 38

        assert int(csv_file.data[0].dist_od) == 0
        assert int(csv_file.data[-1].dist_od) == 130111900

        csv_file.dist_modify(table)

        assert int(csv_file.data[0].dist_od) == 0
        assert int(csv_file.data[-1].dist_od) == 130889155

        from oeg_iv.csvfile.row import Row

        csv_file.data = [
          Row.as_thick(0, 105),
        ]
        table = [[10, 10], [50, 50]]

        with self.assertRaises(Error) as context:
            csv_file.dist_modify(table)
        assert 'dist 0 < node 10' in str(context.exception)

        csv_file.data = [
          Row.as_thick(20, 105),
        ]
        csv_file.dist_modify(table)
        assert csv_file.data[0].dist_od == 20

        csv_file.data = [
          Row.as_thick(150, 105),
        ]
        csv_file.dist_modify(table)
        assert csv_file.data[0].dist_od == 150
