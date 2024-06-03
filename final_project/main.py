import folium
from folium.plugins import HeatMap
import pandas as pd

data = pd.read_csv("museum_keyword_sentiment.csv", encoding = "UTF-8")
data = data.head(39)
data["Museum"] = data["Museum"].str.strip("\n")
data["city/country"] = data["city/country"].str.strip("\n")

map = folium.Map(location = [data["y"][4], data["x"][4]], zoom_start = 12)

fg = folium.FeatureGroup(name = "博物館點位", show = True).add_to(map)
for index, row in data.iterrows():
	popup_content = f"""
    <h1>{row["博物館"]}</h1>
    <div class="ts-box">
      <div class="ts-content is-dense has-dark">
          {row["Museum"]}, {row["city/country"]}<br>
          {row["縣市"]}, {row["Address"]}
      </div>
      <div class="ts-content">
        關鍵詞：{row["keyword(n)"]}<br>
        <div class="ts-box">
        	{row["tourist arrivals"]}人次到訪
        </div>
        <div class="ts-box">
        	{row["sentimental"]}(情緒指標)
        </div>
      </div>
	</div>
    """
	folium.Marker(
		location = [row['y'], row['x']],
		popup = folium.Popup(popup_content, max_width = 400)
	).add_to(fg)

#fg = folium.FeatureGroup(name = "熱點圖")
heat_data_list = [[row['y'], row['x'], row["tourist arrivals"]] for index, row in data.iterrows()]
HeatMap(heat_data_list).add_to(map)
folium.LayerControl().add_to(map)

# 保存地圖為 HTML 文件
map_file = "museum_map.html"
map.save(map_file)

# 讀取並修改 HTML 文件
with open(map_file, 'r', encoding = 'utf-8') as file:
	html = file.read()

# 自定義 <head> 部分
custom_head = """
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<title>博物館地圖</title>
<!-- 核心：Tocas UI -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/tocas/4.2.5/tocas.min.css" />
<script src="https://cdnjs.cloudflare.com/ajax/libs/tocas/4.2.5/tocas.min.js"></script>
<!-- 字體：Noto Sans TC -->
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet" />
"""

# 將自定義 <head> 插入 HTML
html = html.replace('<head>', f'<head>{custom_head}')

# 將修改後的 HTML 寫回文件
with open(map_file, 'w', encoding = 'utf-8') as file:
	file.write(html)

print("done")
