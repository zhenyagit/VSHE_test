import pandas as pd
import random


class Colors:
	def __init__(self, colors):
		self.colors = colors.copy()
		self.index = 0
		self.shuffle()

	def shuffle(self):
		random.shuffle(self.colors)
		self.index = 0

	def get_color(self):
		color = self.colors[self.index]
		self.index += 1
		return color


def add_colors(data, color_palette):
	data_copy = data.copy()[["area", "cluster"]]
	data_copy["color"] = 'null'
	area_groups = data_copy.groupby(["area", "cluster"])

	palettes = {}
	for cluster_name, _ in area_groups.groups.keys():
		if palettes.get(cluster_name) is None:
			palettes[cluster_name] = Colors(color_palette)

	def transform_func(x, palettes_):
		cluster_n, _ = x.name
		colors = palettes_[cluster_n]
		x = colors.get_color()
		return x

	data["color"] = area_groups["color"].transform(transform_func, palettes)
	return data


def delete_duplicates(data):
	data_copy = data.copy()
	grouped_keyword = data_copy.groupby(["area", "keyword"])
	return grouped_keyword.apply(lambda x: x.iloc[0]).reset_index(drop=True)


def to_numeric(data):
	data_copy = data.copy()
	need_columns = ["cluster", "x", "y", "count"]
	data_copy[need_columns] = data_copy[need_columns].apply(pd.to_numeric, errors='coerce')
	return data_copy


def sorting(data):
	return data.sort_values(["area", "cluster", "cluster_name", "count"], ascending=[True, True, True, False])


def main():
	color_palette_tableau_10 = ['#17becf', '#bcbd22', '#7f7f7f', '#e377c2', '#8c564b', '#9467bd', '#d62728', '#2ca02c', '#ff7f0e', '#1f77b4']
	data_format = {"cluster": 'int64', "x": 'float64', "y": 'float64', "count": 'int64'}
	on_output = ["area", "cluster", "cluster_name", "keyword", "x", "y", "count"]
	path_to_file = 'zad_1_data.csv'
	path_to_output = 'zad_1_output.csv'
	df = pd.read_csv(path_to_file)
	df = df[on_output]
	if len(df.groupby('cluster').groups) > len(color_palette_tableau_10):
		raise Exception('Not enough colors in the palette')

	df = add_colors(df, color_palette_tableau_10)  		# добавить колонку color
	df = delete_duplicates(df)  						# удалить дубликаты
	df = to_numeric(df)  								# распарсить числа, если не получается заполнить null
	df = df.dropna(axis='index', how='any')  			# удалить строки содержащие null
	df = df.astype(data_format)  						# приведение типов
	df = sorting(df)  									# сортировка
	df.to_csv(path_to_output, index=False)  			# сохранение


if __name__ == '__main__':
	main()
