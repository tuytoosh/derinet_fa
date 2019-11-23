from __future__ import unicode_literals
import os
from hazm import *

class DataProvider :
	ourDataRoute = 'data/FINAL_10_june.csv'
	morfessorDataRoute = 'data/test_corpus.segmented'
	ufalFormatRoute = 'data/PWSTreesUfalFormat.tsv'

	def get(self, morfessor):
		if morfessor :
			return self.morfessorData()
		return self.ourData()

	def ourData(self):
		segmentations = {}
		fileOpen = open(self.ourDataRoute, 'r')
		fileRead = fileOpen.read()
		lines = fileRead.split()
		words = []
		for l in lines:
		    l = l.split(',')
		    word = [v for v in l[7:] if v != '']
		    word = ''.join(word)
		    word = word.split('X')
		    segmentations[''.join(word)] = word
		    words.append(word)
		return words, segmentations

	def morfessorData(self):
		fileOpen = open(self.morfessorDataRoute, 'r')
		fileRead = fileOpen.read()
		lines = fileRead.split("\n")
		words = []
		for l in lines[1:]:
		    words.append([w.strip() for w in l.split(' ')])
		return words

	def exceptions(self, morfessorData):
		if morfessorData:
			return [30, 40, 42, 59, 79, 81, 83, 90, 93, 94, 95, 97, 99, 101, 102, 103, 104, 105, 106, 107, 108, 113, 114, 119, 121, 132, 133, 134, 135, 141, 143, 146, 147, 149, 151, 153, 154, 155, 156, 157, 159, 160, 165, 170, 171, 175, 178, 183, 184, 185, 186, 190, 197, 199, 200]
		else:
			return [18, 19, 26, 28, 31, 36, 40, 48, 53, 58, 59, 60, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 74, 79, 80, 85, 87, 88, 90, 91, 92, 93, 94, 96, 98, 100, 102, 103, 104, 105, 107, 110, 11, 112, 116, 117, 118, 120, 121, 123, 126,130, 131, 132, 133, 134, 137, 139, 141, 142, 145, 147, 148,149, 151, 154, 155, 156, 157, 158, 160, 163, 164, 166, 167, 170, 172, 173, 175, 176, 177, 180, 181, 182, 189, 191, 193, 195, 196, 198, 199]

	def write_ufal_format(self, rels, segmentations):
		output = open(self.ufalFormatRoute, 'w+')
		tagger = POSTagger(model='data/resources/postagger.model')
		ids = {}
		i = 0
		for child in rels:
			for parent in set(rels[child]):
				if parent in segmentations:
					seg = ' '.join(segmentations[parent])
				else:
					seg = parent
				if parent not in ids:
					ids[parent] = i
					output.write(str(i) + ' ' + parent + ' ' + parent + ' ' + tagger.tag([child])[0][1] + ' ' + seg + "\n")
					i += 1

				if child in segmentations:
					seg = ' '.join(segmentations[child])
				else:
					seg = child
				output.write(str(i) + ' ' + child + ' ' + child + ' ' + tagger.tag([child])[0][1] + ' ' + str(ids[parent]) + ' ' + seg + "\n")
				ids[child] = i
				i += 1
		output.close()
		return self.ufalFormatRoute;
