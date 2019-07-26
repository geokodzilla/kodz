# -*- coding: utf-8 -*-

import pytest
from kodz.src.punkt import *

@pytest.fixture
def simple_point():
	"""Zwraca postawowy punkt"""
	return Punkt(numer='1')


def test_str(simple_point):
	assert str(simple_point) == '0.0 0.0'
	simple_point.set_coords('101.23', '205.32')
	assert str(simple_point) == '101.23 205.32'


def test_set_x(simple_point):
	simple_point.set_x('100.1')
	assert simple_point.x == '100.1'


def test_set_y(simple_point):
	simple_point.set_y(100.25)
	assert  simple_point.y == '100.25'


def test_set_coords(simple_point):
	simple_point.set_coords(201.25, '362.21')
	assert simple_point.x == '201.25'
	assert simple_point.y == '362.21'