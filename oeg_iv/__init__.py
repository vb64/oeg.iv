# -*- coding: windows-1251 -*-
"""Interfaces for InspectionViewer stuff."""


class Error(Exception):
    """
    IV exception
    """
    pass


class ObjectClass:  # pylint: disable=too-few-public-methods,no-init,old-style-class
    """
    classes of csv objects
    """
    WELD = 0
    MARKER = 1
    DEFEKT = 2
    THICK = 3
    HOR_WELD = 4
    PIPELINE_CATEGORY = 5


class TypeMarker:  # pylint: disable=too-few-public-methods,no-init,old-style-class
    """
    types of marker
    """
    VALVE = 0
    MARKER = 1
    MAGNET = 2
    OTVOD = 3
    TROYNIK = 4
    CASE_START = 5
    CASE_END = 6
    REPAIR = 7
    LOAD = 8
    TURN_START = 9
    TURN_END = 10
    FEATURE = 11
    CURVE_SECTION = 12
    TURN_SEGMENT = 13


class TypeDefekt:  # pylint: disable=too-few-public-methods,no-init,old-style-class
    """
    types of defekt
    """
    CORROZ = 0
    MECHANIC = 1
    DENT = 2
    DENT_METAL_LOSS = 3
    GOFRA = 4
    GWAN = 5
    TECHNOLOGY = 6
    FACTORY = 7
    ADDITIONAL_METAL = 8
    OTHER = 9
    CRACKS_HOR = 10
    CRACK_LIKE = 11
    CRACK_WELD = 12
    LAMINATION = 13
    ANOMALY_HOR_WELD = 14
    ANOMALY_SPIRAL_WELD = 15
    ELLIPSE = 16
    PODZHIG = 17
    GRINDING = 18


class TypeHorWeld:  # pylint: disable=too-few-public-methods,no-init,old-style-class
    """
    types of horizontal weld
    """
    HORIZONTAL = 0
    SECOND = 1
    NO_WELD = 2
    SPIRAL = 3


class DefektSide:  # pylint: disable=too-few-public-methods,no-init,old-style-class
    """
    types of defekt location
    """
    UNKNOWN = 0
    OUTSIDE = 1
    INSIDE = 2
    IN_WALL = 3


COMMON = {
  ObjectClass.WELD: "���",
  ObjectClass.THICK: "��������� ������� ������ �����",
  ObjectClass.PIPELINE_CATEGORY: "��������� ������������",
}

SEAM = {
  TypeHorWeld.HORIZONTAL: "���������� ���",
  TypeHorWeld.SECOND: "������� ����. ���",
  TypeHorWeld.NO_WELD: "������������� �����",
  TypeHorWeld.SPIRAL: "���������� ���",
}

LINEOBJ = {
  TypeMarker.VALVE: "����",
  TypeMarker.MARKER: "������",
  TypeMarker.MAGNET: "������ ���������",
  TypeMarker.OTVOD: "�����-������",
  TypeMarker.TROYNIK: "�������",
  TypeMarker.CASE_START: "������ ������",
  TypeMarker.CASE_END: "������ �����",
  TypeMarker.REPAIR: "����� �������",
  TypeMarker.LOAD: "�������",
  TypeMarker.TURN_START: "����� (�������) ������",
  TypeMarker.TURN_END: "����� (�������) �����",
  TypeMarker.FEATURE: "�����������",
  TypeMarker.CURVE_SECTION: "������ ������",
  TypeMarker.TURN_SEGMENT: "������� ��������",
}

DEFEKTS = {
  TypeDefekt.CORROZ: "�������� ",
  TypeDefekt.MECHANIC: "������������ �����������",
  TypeDefekt.DENT: "�������",
  TypeDefekt.DENT_METAL_LOSS: "������� � ��������� ������ �������",
  TypeDefekt.GOFRA: "�����",
  TypeDefekt.GWAN: "�������� ���������� ��� GWAN",
  TypeDefekt.TECHNOLOGY: "��������������� ������",
  TypeDefekt.FACTORY: "��������� ������",
  TypeDefekt.ADDITIONAL_METAL: "�������������� ������/��������",
  TypeDefekt.OTHER: "������",
  TypeDefekt.CRACKS_HOR: "���� ���������� ������",
  TypeDefekt.CRACK_LIKE: "��������������� ������",
  TypeDefekt.CRACK_WELD: "������� �� ��������� ���",
  TypeDefekt.LAMINATION: "����������",
  TypeDefekt.ANOMALY_HOR_WELD: "�������� ����������� ���",
  TypeDefekt.ANOMALY_SPIRAL_WELD: "�������� ����������� ���",
  TypeDefekt.ELLIPSE: "�����������",
  TypeDefekt.PODZHIG: "������",
  TypeDefekt.GRINDING: "����������",
}

MARKERS = [
  TypeMarker.VALVE,
  TypeMarker.MARKER,
  TypeMarker.MAGNET,
]
