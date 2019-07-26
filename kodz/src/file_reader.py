# -*- coding: utf-8 -*-
from collections import defaultdict
from kodz.src.punkt import Punkt
from kodz.src.dzialka import Dzialka


class FileReader(object):
    def __init__(self, filename):
        self.filename = filename

    def _file_reader(self):
        """
        funkcja wczytująca dane z plików tekstowych
        """
        data = [i.strip().split() for i in open(self.filename)]
        return data

    def edz_file_process(self):
        """
        funkcja przetwarzająca pliki edz pochodzące z programu ewmapa
        zwraca listę działek w której każdy element jest instancją obiektu dzialka
        oraz slownik punktow w którym każdemu numerowi punktu przypisane są wszystkie
        działki w których występuje
        """
        dzialki = []
        punkty = defaultdict(set)
        edz_data = self._file_reader()
        for row in edz_data:
            if len(row) == 1 and '-' in row[0]:
                dz = Dzialka(numer=row[0])
                dzialki.append(dz)
            elif len(row) == 10:
                pkt = Punkt(numer=row[0], x=row[1], y=row[2])
                punkty[row[0]].add(dz.numer)
                dz.add_punkt(pkt)
        return dzialki, punkty