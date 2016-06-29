
import os,sys,gzip,zipfile
from xml.etree.ElementTree import ElementTree
import numpy as np




class FEBParser(object):
	def __init__(self, fname):
		self.fname     = fname
		self.root      = None
		self.tree      = None
		self.ext       = os.path.splitext(fname)[1].upper()
		self._parse_xml()
	def _parse_xml(self):
		self.tree      = ElementTree()
		### parse FEB:
		if self.ext == '.FEB':
			with open(self.fname, 'r') as fid:
				self.tree.parse(fid)
		### parse GZIP:
		elif self.ext == '.GZ':
			with gzip.open(self.fname, 'r') as fid:
				self.tree.parse(fid)
		### parse ZIP:
		elif self.ext == '.ZIP':
			fnameFEB   = os.path.split(   os.path.splitext(self.fname)[0]   )[1]
			with zipfile.ZipFile(self.fname, 'r') as zfid:
				with zfid.open(fnameFEB) as fid:
					tree      = ElementTree()
					self.tree.parse(fid)
		self.root      = self.tree.getroot()
	def read_elements(self, start_with=0):
		el   = self.root.find('Geometry/Elements').getchildren()
		CONN = np.array([e.text.split(',')   for e in el], dtype=int)
		return CONN - 1 + start_with
	def read_materials(self):
		el   = self.root.find('Geometry/Elements').getchildren()
		MAT  = np.array([e.attrib['mat']   for e in el], dtype=int)
		return MAT
	def read_nodes(self):
		nodes = self.root.find('Geometry/Nodes').getchildren()
		XYZ   = np.array([node.text.split(',')   for node in nodes], dtype=float)
		return XYZ
	



class FEBioLogFileParser(object):
	def __init__(self, fname):
		self.ilines  = None
		self.fname   = fname
		self.nlines  = None
		self.ext     = os.path.splitext(fname)[1].upper()
		self._readlines()
	
	def _readlines(self):
		### parse LOG:
		if self.ext == '.LOG':
			with open(self.fname, 'r') as fid:
				self.ilines = fid.readlines()
		### parse GZIP:
		elif self.ext == '.GZ':
			with gzip.open(self.fname, 'r') as fid:
				self.ilines = fid.readlines()
		### parse ZIP:
		elif self.ext == '.ZIP':
			fnameFEB   = os.path.split(   os.path.splitext(self.fname)[0]   )[1]
			with zipfile.ZipFile(self.fname, 'r') as zfid:
				with zfid.open(fnameFEB) as fid:
					self.ilines = fid.readlines()
		self.nlines     = len(self.ilines)
		
	def find(self, target, i0=0):
		i  = i0
		i1 = -1
		while i<self.nlines:
			iline = self.ilines[i]
			if iline.startswith(target):
				i1 = i
				break
			i += 1
		return i1
		
	def find_all(self, target, i0=0):
		i   = i0
		IND = []
		while True:
			ind = self.find(target, i)
			if ind==-1:
				break
			else:
				IND.append(ind)
				i   = ind+1
		return IND
		
	def parse_record(self, i):
		i = i + 5
		s = self.ilines[i]
		A = []
		while True:
			s = self.ilines[i]
			a = str(s).strip().strip("\\n'").split(' ')[1:]
			if a==[]:
				break
			else:
				A.append(a)
				i += 1
		return np.array(A, dtype=float)



def load_geometry(fnameFEB):
	parser    = FEBParser(fnameFEB)
	nodes     = parser.read_nodes()
	elements  = parser.read_elements()
	return nodes, elements

def load_materials(fnameFEB):
	parser    = FEBParser(fnameFEB)
	materials = parser.read_materials()
	return materials


def load_log(fnameLOG):
	parser = FEBioLogFileParser(fnameLOG)
	target = 'Data Record'
	if sys.version_info.major == 3:
		if parser.ext in ['.GZ', '.ZIP']:
			target = bytes(target, 'utf-8')
	inds   = parser.find_all(target)
	Y      = parser.parse_record(inds[-1])
	return Y


