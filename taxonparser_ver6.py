#! /usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re

parser = argparse.ArgumentParser(description="This script extracts taxon information from GenBank file.")

parser.add_argument('input', help='input file')
parser.add_argument('-o', '--out', default='output.txt' ,help='output file')

args = parser.parse_args()

# ファイルの読み込み
with open(args.input) as f:
	# accessionごとに分割
	entry = f.read().split('//')
	num = len(entry)
	out = []
	for i in entry[0:num - 1]:
		# 分類群を行ごとに抜き出してリストに格納
		sep1 = i.split('ORGANISM')
		sep2_lst = sep1[1].split('REFERENCE')[0].split("\n")
		
		# 空のリストを削除
		sep2_lst.remove("")
		
		# 分類群の各行の先頭に含まれる余分なスペースを削除
		for j, name in enumerate(sep2_lst):
			if sep2_lst[j].endswith("."):
				sep2_lst[j] = name.strip().rstrip(".") + ";"
			else:
				sep2_lst[j] = name.strip()

		# 種小名を末尾に移動
		sep3_lst = sep2_lst[1:]
		sep3_lst.append(sep2_lst[0])

		# 文字列に変換
		sep3 = " ".join(sep3_lst)

		# ";"で分割してリスト化
		sep4_lst = sep3.split("; ")

		# リストを逆順にする
		sep4_lst.reverse()

		# 余分な高次分類群を削除
		sep4_lst.remove("Eukaryota")
		sep4_lst.remove("Metazoa")
		sep4_lst.remove("Chordata")
		sep4_lst.remove("Craniata")
		sep4_lst.remove("Vertebrata")
		sep4_lst.remove("Euteleostomi")
		
		# 分類群名に小文字で始まるものがあれば削除
		for k, taxa in enumerate(sep4_lst):
			if re.match(r"[a-z]", taxa):
				sep4_lst[k] = ""

		if "" in sep4_lst:
			sep4_lst.remove("")

		# 分類群名に重複があれば削除し、outリストに加える
		out.append("; ".join(sorted(list(set(sep4_lst)), key=sep4_lst.index)))
		

# outをファイルへ書き込む
with open(args.out, mode="w") as g:
    g.write("\n".join(out))
