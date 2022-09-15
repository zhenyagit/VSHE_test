import pandas as pd
from matplotlib import pyplot as plt
from adjustText import adjust_text


def main():
	path_to_file = 'zad_1_output.csv'
	df = pd.read_csv(path_to_file)
	grouped_area = df.groupby(["area"])
	for key in grouped_area.groups.keys():
		group = grouped_area.get_group(key)
		fig, ax = plt.subplots()
		x, y = group["x"].to_numpy(), group["y"].to_numpy()
		titles = group["keyword"].to_numpy()
		colors = group["color"].to_numpy()
		uniq_colors = group["color"].unique()
		uniq_labels = group["cluster_name"].unique()
		ax.scatter(x, y, c=colors, marker="o", edgecolor="black", linewidths=0.5)

		texts = []
		for x, y, s in zip(x, y, titles):
			text = plt.text(x, y, s, size=8, wrap=True)
			text._get_wrap_line_width = lambda: 800
			texts.append(text)

		force_points = 0.5
		ax.set_title("Area: %s" % key, y=-0.13)
		adjust_text(
			texts,
			force_points=force_points,
			arrowprops=dict(arrowstyle="-", color="k", lw=0.5),
			ax=ax,
			expand_text=(1.05, 2.0)
		)
		handlers = []
		for i in uniq_colors:
			a = plt.scatter(None, None, c=i, marker='o', edgecolor="black", linewidths=0.5)
			handlers.append(a)

		ax.legend(handlers, uniq_labels, bbox_to_anchor=(-0.05, 1.05), loc='center')
		if key == "ar\\vr":
			key = "ar-vr"
		fig.savefig("images/"+key + ".png", dpi=400)


if __name__ == "__main__":
	main()
