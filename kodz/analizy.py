# -*- coding: utf-8 -*-

from kodz.src.file_reader import FileReader
from collections import Counter
import logging

logging.basicConfig(filename='analizy.log', filemode='w',
					format='%(name)s - %(levelname)s - %(message)s')


class Analiza(object):

	def __init__(self, dz_filename, kon_filename):
		self.dz_filename = dz_filename
		self.kon_filename = kon_filename
		self.file_reader_dz = FileReader(self.dz_filename)
		self.file_reader_kon = FileReader(self.kon_filename)
		self.dzialki_lista, self.punkty_dzialki_dict = self.file_reader_dz.edz_file_process()
		self.kontury_lista, self.punkty_kontury_dict = self.file_reader_kon.edz_file_process()

	def _pkt_coords_set(self, dzialki_lista):
		"""
		na podstawie listy dzialek tworzy zbior wspolrzednych wszystkich punktów
		tych dzialek
		"""
		pkt_set = set([])
		for dz in dzialki_lista:
			for pkt in dz.punkty:
				pkt_set.add(pkt.get_coords_str())
		return pkt_set

	def _quick_dict(self, lista):
		"""
		funkcja z listy obiektów tworzy słownik w którym kluczem są
		numery obiektów a wartościami obiekty
		"""
		return {i.numer: i for i in lista}
	
	def _pkt_coords_set_uzytki(self, punkty_dict, dzialki_lista, uzytek='dr'):
		"""
		funkcja tworzy zbior wspolrzednych które potencjalnie mogą być usunięte z bazy
		dziala z dowolnym rodzajem uzytku, domyślnie chodzi o drogi. Znajdujemy wszystkie
		punkty konturów które należą do dwóch konturów w tym przynajmniej jeden musi zawierać
		w sobie wskazany uzytek
		"""
		pkt_set = set([])
		pkt_uzytek = []
		pkt_dict = {}
		for pnumer, dz in punkty_dict.items():
			dz = list(dz)
			if len(dz) == 2 and (uzytek in dz[0] or uzytek in dz[1]):
				pkt_uzytek.append(pnumer)
		for dz in dzialki_lista:
			pkt_dict.update(self._quick_dict(dz.punkty))
		for p_uz in pkt_uzytek:
			pkt_set.add(pkt_dict[p_uz].get_coords_str())
		return pkt_set

	def _err_to_file(self, filename, data):
		err_file = open(filename, 'w')
		for i in data:
			print(i, file=err_file)

	def removable_points(self, uzytek):
		set_kontury_pkt = self._pkt_coords_set_uzytki(self.punkty_kontury_dict, self.kontury_lista, uzytek=uzytek)
		set_dzialki_pkt = self._pkt_coords_set(self.dzialki_lista)
		# roznica pkt_konturów z dzialkami daje nam pkt konturów należące w tym konkretnym przypadku do dróg w których brak jest pkt granicznego działki
		data = set_kontury_pkt - set_dzialki_pkt
		self._err_to_file('./Błedy_kontury.txt', data)
		return data

	def _kon_to_merge(self):
		"""
		Tworzy listę konturów które mogą podlegać połączeniu
		:return:
		"""
		kon_to_merge = []
		for pktk, kon in self.punkty_kontury_dict.items():
			konl = list(kon)
			for nr, ozn in enumerate(konl):
				try:
					ozn_short = ozn[0:ozn.index('-') + 1] + ozn[ozn.index('/') + 1:]
					konl[nr] = [ozn_short, ozn]
				except ValueError:
					logging.warning('Błędne oznaczenie konturu - %s' % ozn)
			c = Counter([i[0] for i in konl])
			for ozn_s, counter in c.items():
				row = []
				if counter > 1:
					for i in konl:
						if i[0] == ozn_s:
							row.append(i[1])
				if len(row) > 0 and row not in kon_to_merge: kon_to_merge.append(row)
		return kon_to_merge

	def _ignore_kon(self, data, ignorowane):
		"""
		W anzlizie sytkow umożliwia ignorowanie pewnych konturów określonych
		przez użytkownika, najcześciej dotyczy to uzytków dr.
		:param data:
		:param ignorowane:
		:return:
		"""
		remove = set([])
		for nr, row in enumerate(data):
			for i in ignorowane:
				for ozn in row:
					if i in ozn:
						remove.add(nr)
		remove = list(remove)
		remove.sort() # sortowanie ignorowanych indeksów
		for i in list(remove)[::-1]:
			data.pop(i)
		return data

	def merge_polygons(self, ignorowane=None):
		"""
		Metoda wskazuje miesjca w których stykają się kontury z tego samego obrębu
		o tych samych oznaczeniach
		:return:
		"""
		if ignorowane is None: ignorowane = []
		data = set([])
		kon_dict = self._quick_dict(self.kontury_lista)
		data_kon = self._kon_to_merge()
		for i in self._ignore_kon(data_kon, ignorowane):
			if len(i) == 2:
				k1 = kon_dict[i[0]]
				k2 = kon_dict[i[1]]
				k1_pkt = {p.get_coords_str() for p in k1.punkty}
				k2_pkt = {p.get_coords_str() for p in k2.punkty}
				intersection = k1_pkt & k2_pkt
				if len(intersection) > 1:
					for i in intersection:
						data.add(i)
		self._err_to_file('./Błedy_kontury_styki.txt', data)
		return data
if __name__ == "__main__":
	analiza = Analiza('f:/PROGRAMOWANIE/PROJEKTY/ewmapa/Dzialki.edz', 'f:/PROGRAMOWANIE/PROJEKTY/ewmapa/Kontury.edz')
	analiza.merge_polygons(ignorowane=['dr'])
