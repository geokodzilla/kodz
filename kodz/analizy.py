# -*- coding: utf-8 -*-

from kodz.src.file_reader import FileReader


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

	def removable_points(self, uzytek):
		set_kontury_pkt = self._pkt_coords_set_uzytki(self.punkty_kontury_dict, self.kontury_lista, uzytek=uzytek)
		set_dzialki_pkt = self._pkt_coords_set(self.dzialki_lista)
		err_file = open('./Błędy_kontury.txt', 'w')
		# roznica pkt_konturów z dzialkami daje nam pkt konturów należące w tym konkretnym przypadku do dróg w których brak jest pkt granicznego działki
		for i in set_kontury_pkt - set_dzialki_pkt:
			print(i, file=err_file)

				
if __name__ == "__main__":
	pass