# -*- coding: utf-8 -*-

import pytest
from kodz.src.file_reader import *

@pytest.fixture
def plik():
    return FileReader('./_example_data/Dzialki_test.edz')


def test_file_reader(plik):
    data = plik.file_reader()
    assert len(data) == 341
    assert data[0] == ['5-844']
    assert data[-1] == ['5-7808', '5582354.78', '7553073.03', '5582354.78', '7553073.03',
                        '80', 'N', 'N', '7', '8#P.1806.2017.547']


def test_edz_file_process(plik):
    dzialki, punkty = plik.edz_file_process()
    assert punkty['5-4478'] == {'5-844', '5-845'}
    assert [i.numer for i in dzialki] == ['5-844', '5-845', '5-828']