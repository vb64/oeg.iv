# Python package for communication with InspectionViewer app
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/oeg.iv/pep257.yml?label=Pep257&style=plastic&branch=main)](https://github.com/vb64/oeg.iv/actions?query=workflow%3Apep257)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/oeg.iv/py2.yml?label=Python%202.7&style=plastic&branch=main)](https://github.com/vb64/oeg.iv/actions?query=workflow%3Apy2)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/vb64/oeg.iv/py3.yml?label=Python%203.7-3.10&style=plastic&branch=main)](https://github.com/vb64/oeg.iv/actions?query=workflow%3Apy3)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/aa5f850432ca45408ab72c002f0689ea)](https://www.codacy.com/gh/vb64/oeg.iv/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=vb64/oeg.iv&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/aa5f850432ca45408ab72c002f0689ea)](https://www.codacy.com/gh/vb64/oeg.iv/dashboard?utm_source=github.com&utm_medium=referral&utm_content=vb64/oeg.iv&utm_campaign=Badge_Coverage)

The library provides a set of high-level operations with export/import CSV file of the InspectionViewer, the Win32 app for analyzing in-line flaw detection data.

Data can be

-   mirrored
-   glued together from several CSV files
-   stretched/compressed along the distance according to a given set of intermediate points
-   interpreted as an iterable sequence of pipes with geodata

## Install
```bash
pip install oeg-iv
```

## Usage

Construct new csv file from scratch.

```python
import os

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
# maximum depth point at distance 5.01 m from left tube weld,
# orientation 4 hours 30 minutes
# with comment 'metal loss'
csv_file.data.append(Row.as_defekt(
  6000,
  TypeDefekt.CORROZ,
  DefektSide.OUTSIDE
  '20', '10', '30',
  Orientation(4, 0), Orientation(5, 0),
  6010, Orientation(4, 30),
  'metal loss'
))

# save csv to file
csv_file.to_file('example.csv')
assert os.path.getsize('example.csv') > 0
```

Reversing the data.

```python
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

# reverse copy
csv_copy.reverse()

# relative position of defekt must change
defect_row = csv_copy.data[2]
assert defect_row.is_defect

# defect orientation must be mirrored
assert defect_row.orient_td == '7,00'
assert defect_row.orient_bd == '8,00'

# save reversed copy to file
csv_file.to_file('reversed.csv')
assert os.path.getsize('reversed.csv') > 0
```

Append to initial CSV empty pipe with length = 10.0 m and reversed copy from the file.

```python
csv_file.join([10000, 'reversed.csv'])
assert csv_file.total_length == 28000
assert len(csv_file.data) == 11
```

Compress distances and length of all objects in half.

```python
csv_file.dist_modify(
  # table of corrections
  # each node define as pair 'existing distance', 'new distance'
  [[0, 0],
  [28000, 14000],
])
assert csv_file.total_length == 14000

# save file with compress distances
csv_file.to_file('transformed.csv')
assert os.path.getsize('transformed.csv') > 0
```

Iterate by pipes and modify data.

```python
csv_trans = File.from_file('transformed.csv')
warnings = []
current_dist = 0
for i in csv_trans.get_tubes(warnings):
    assert i.dist >= current_dist
    current_dist = i.dist
    tube = i

assert not warnings

# set geodata for tube
assert tube.latitude == ''
assert tube.longtitude == ''
assert tube.altitude == ''

tube.set_geo(10, 11, 12)

assert tube.latitude == 10
assert tube.longtitude == 11
assert tube.altitude == 12

csv_trans.to_file('geo.csv')
assert os.path.getsize('geo.csv') > 0

# load from saved file and check geodata from last pipe
csv_geo = File.from_file('geo.csv')
last_tube = list(csv_geo.get_tubes(warnings))[-1]

assert last_tube.latitude == '10'
assert last_tube.longtitude == '11'
assert last_tube.altitude == '12'
```

## Development

```bash
git clone git@github.com:vb64/oeg.iv.git
cd oeg.iv
```

With Python3

```bash
make setup PYTHON_BIN=/path/to/python3/executable
make tests
```

With Python2

```bash
make setup2 PYTHON_BIN=/path/to/python27/executable
make tests2
```
