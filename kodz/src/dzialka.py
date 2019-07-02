# -*- coding: utf-8 -*-


class Dzialka(object):

	def __init__(self, numer):
		self.numer = numer
		self.punkty = []

	def add_punkt(self, p):
		"""
		Metoda umożliwająca dodanie unikatowych punktów do listy
		"""
		if p.numer not in [i.numer for i in self.punkty]:
			self.punkty.append(p)

	def lista_pkt_numer(self):
		return [p.numer for p in self.punkty]