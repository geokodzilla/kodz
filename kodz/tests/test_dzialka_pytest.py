# -*- coding: utf-8 -*-

import pytest
from kodz.src.dzialka import *
from kodz.src.punkt import *


@pytest.fixture
def dzialka():
    """Zwraca postawową dzialkę"""
    return Dzialka(numer='1')


@pytest.fixture
def p1():
    return Punkt(numer='1', x='100', y='100')


@pytest.fixture
def p2():
    return Punkt(numer='2', x='200', y='200')


@pytest.fixture
def p3():
    return Punkt(numer='3', x='100', y='200')


def test_add_punkt(dzialka, p1, p2, p3):
    dzialka.add_punkt(p1)
    dzialka.add_punkt(p2)
    dzialka.add_punkt(p3)
    dzialka.add_punkt(p3) # weryfikacja dodawania tych samych punktów
    assert len(dzialka.punkty) == 3
    assert dzialka.lista_pkt_numer() == ['1', '2', '3']
