# -*- coding: utf-8 -*-

import pytest
from kodz.analizy import *

@pytest.fixture
def analiza():
    return Analiza('./_example_data/Dzialki_test.edz', './_example_data/Kontury_test.edz')


def test_quic_dict(analiza):
    dz_list = analiza.dzialki_lista
    assert analiza._quick_dict(dz_list) == {'5-844': dz_list[0], '5-845': dz_list[1], '5-828': dz_list[2]}


def test_pkt_coords_set(analiza):
    dz_list = analiza.dzialki_lista[0:1]
    assert analiza._pkt_coords_set(dz_list) == {'5583782.96 7553949.02', '5583803.27 7553955.46',
                                                '5583812.71 7553918.92', '5583794.70 7553906.38',
                                                '5583776.80 7553947.08'}


def test_pkt_coords_set_uzytki(analiza):
    kon_dict = analiza.punkty_kontury_dict
    kon_list = analiza.kontury_lista
    assert analiza._pkt_coords_set_uzytki(kon_dict, kon_list) == {'5583805.13 7553913.68',
                                                                  '5583778.17 7553893.26',
                                                                  '5583812.71 7553918.92'}


def test_removable_points(analiza):
    assert analiza.removable_points('dr') == {'5583805.13 7553913.68'}


def test_kon_to_merge(analiza):
    assert '5-2268/B' in analiza._kon_to_merge()[0]
    assert '5-2267/B' in analiza._kon_to_merge()[0]


def test_merge_polygons(analiza):
    assert analiza.merge_polygons() == {'5583776.80 7553947.08', '5583794.70 7553906.38'}