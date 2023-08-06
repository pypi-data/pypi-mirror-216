import plotly.graph_objects as go
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv(dotenv_path='./.env')

def save_fig(center_lat, center_lon, data, image_path = 'test.png', zoom=13.5):
    
    data = pd.DataFrame(data)
    data['pm2_5'] = data['pm2_5'].astype(float)
    pm2_5_color_dict = [
        {"v": 500.4, "color": "#000000"},
        {"v": 450.5, "color": "#301E12"},
        {"v": 400.5, "color": "#3C230F"},
        {"v": 350.5, "color": "#49280D"},
        {"v": 300.5, "color": "#552E0A"},
        {"v": 250.5, "color": "#623307"},
        {"v": 230.5, "color": "#682c1f"},
        {"v": 210.5, "color": "#6d2537"},
        {"v": 190.5, "color": "#731d4e"},
        {"v": 170.5, "color": "#781666"},
        {"v": 150.5, "color": "#7e0f7e"},
        {"v": 131.3, "color": "#970f6a"},
        {"v": 112.1, "color": "#b10f56"},
        {"v": 92.9, "color": "#ca0e43"},
        {"v": 73.7, "color": "#e30e30"},
        {"v": 54.5, "color": "#fc0e1c"},
        {"v": 50.7, "color": "#fc241d"},
        {"v": 46.9, "color": "#fc3b1f"},
        {"v": 43.1, "color": "#fd5220"},
        {"v": 39.3, "color": "#fd6822"},
        {"v": 35.5, "color": "#fd7e23"},
        {"v": 31.5, "color": "#fd9827"},
        {"v": 27.5, "color": "#feb12b"},
        {"v": 23.5, "color": "#fecb30"},
        {"v": 19.5, "color": "#ffe534"},
        {"v": 15.5, "color": "#fffd38"},
        {"v": 12.4, "color": "#d4fd36"},
        {"v": 9.3, "color": "#a9fd34"},
        {"v": 6.2, "color": "#7EFD32"},
        {"v": 3.1, "color": "#53FD30"},
        {"v": 0, "color": "#29fd2e"}
    ]

    def get_color(value, color_dict):
        for i in range(len(color_dict)):
            if value >= color_dict[i]['v']:
                return color_dict[i]['color']

    data['color'] = data['pm2_5'].apply(lambda x: get_color(x, pm2_5_color_dict))
    color_sequence = [item['color'] for item in reversed(pm2_5_color_dict)]
    layout = go.Layout(
        mapbox=dict(accesstoken=os.getenv('MAPBOX_ACCESS_TOKEN')),
        #mapbox_style="open-street-map",
        mapbox_style="streets",
        mapbox_center={"lat": center_lat, "lon": center_lon},
        mapbox_zoom=zoom,
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    
    data = go.Scattermapbox(
        lat=data['lat'],
        lon=data['lon'],
        mode='markers',
        marker=dict(
            size=10,
            color=data['color'],
            colorscale=color_sequence,
            opacity=0.7
        )
    )
    
    center_trace = go.Scattermapbox(
        lat=[center_lat],
        lon=[center_lon],
        mode='markers',
        marker=dict(
            size=15,
            symbol='circle',
            color='#0000FF'
        )
    )

    fig = go.Figure(data=[center_trace,data], layout=layout)
    #fig.show()
    fig.write_image(image_path, scale=2)

if __name__ == '__main__':
    data = [{'deviceId': '10401411473', 'lat': '25.0072', 'lon': '121.5161', 'pm2_5': '4.31'}, {'deviceId': '10394742841', 'lat': '25.0072', 'lon': '121.5122', 'pm2_5': '2.45'}, {'deviceId': '10394403129', 'lat': '25.0093', 'lon': '121.5105', 'pm2_5': '2.97'}, {'deviceId': '10391606094', 'lat': '25.0037', 'lon': '121.5136', 'pm2_5': '2.97'}, {'deviceId': '10382402966', 'lat': '25.0037', 'lon': '121.5128', 'pm2_5': '3.38'}, {'deviceId': '10382310374', 'lat': '25.0128', 'lon': '121.5070', 'pm2_5': '2.62'}, {'deviceId': '10365063199', 'lat': '25.0092', 'lon': '121.5140', 'pm2_5': '3.60'}, {'deviceId': '10363938282', 'lat': '25.0114', 'lon': '121.5080', 'pm2_5': '2.09'}, {'deviceId': '10363771626', 'lat': '25.0092', 'lon': '121.5049', 'pm2_5': '1.46'}, {'deviceId': '10362311821', 'lat': '25.0049', 'lon': '121.4982', 'pm2_5': '3.35'}]
    center_lat = 25.011319
    center_lon = 121.506297
    image_path = 'scale_2.png'
    save_fig(center_lat, center_lon, data, image_path)