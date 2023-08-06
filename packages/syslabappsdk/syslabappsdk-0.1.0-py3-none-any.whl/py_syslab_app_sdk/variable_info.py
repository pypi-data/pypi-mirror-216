#!/usr/bin/python
# -*- coding: utf-8 -*-

class VariableInfo:
	def __init__(self, name, type):
		self.name = name
		self.type = type

	def get_name(self):
		return self.name
	
	def get_type(self):
		return self.type
