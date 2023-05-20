import requests as req
import json
import folium as foli
import pandas as pd
from selenium import webdriver
import time
import schedule

TOKEN = 'your token'
api_url = 'https://notify-api.line.me/api/notify'

def main():
    typhoon = req.get("https://www.jma.go.jp/bosai/typhoon/data/TC2304/forecast.json")
    typhoon = typhoon.json()

    times=typhoon[0]["issue"]["JST"]
    lat_0=typhoon[1]["center"][0]
    lon_0=typhoon[1]["center"][1]
    time_0=typhoon[1]["validtime"]["JST"]
    lat_1=typhoon[2]["center"][0]
    lon_1=typhoon[2]["center"][1]
    time_1=typhoon[2]["validtime"]["JST"]
    lat_2=typhoon[3]["center"][0]
    lon_2=typhoon[3]["center"][1]
    time_2=typhoon[3]["validtime"]["JST"]
    lat_3=typhoon[4]["center"][0]
    lon_3=typhoon[4]["center"][1]
    time_3=typhoon[4]["validtime"]["JST"]
    lat_4=typhoon[5]["center"][0]
    lon_4=typhoon[5]["center"][1]
    time_4=typhoon[5]["validtime"]["JST"]
    lat_5=typhoon[6]["center"][0]
    lon_5=typhoon[6]["center"][1]
    time_5=typhoon[6]["validtime"]["JST"]

    typ = pd.DataFrame({
        "times":[time_0,time_1,time_2,time_3,time_4,time_5],
        "latitude":[lat_0,lat_1,lat_2,lat_3,lat_4,lat_5],
        "longtude":[lon_0,lon_1,lon_2,lon_3,lon_4,lon_5]
    })

    lat=0
    lon=0

    for i,r in typ.iterrows():
        lat+=r["latitude"]
        lon+=r["longtude"]

    lat=lat/6
    lon=lon/6

    map=foli.Map(location=[lat,lon],zoom_start=4.5)

    for i,r in typ.iterrows():
        foli.Marker(location=[r["latitude"],r["longtude"]],popup=r["times"]).add_to(map)

    map.save("typhoon.html")

    browser=webdriver.Chrome()
    browser.maximize_window()
    browser.get("C:\\Users\\REI\\Documents\\Programs\\typhoon.html")
    time.sleep(3)
    browser.save_screenshot("C:\\Users\\REI\\Documents\\Programs\\typhoon.png")
    browser.quit()

    send_contents=f"**台風情報**\n{times}の情報(β)"
    TOKEN_dic = {'Authorization': 'Bearer'+' '+TOKEN}
    send_dic = {'message': send_contents}
    image_dic = {'imageFile': open("typhoon.png", "rb")}
    try:
        req.post(api_url, headers=TOKEN_dic, data=send_dic,files=image_dic)
    except Exception as e:
        print(f"Error {e}")

schedule.every().day.at("19:00").do(main)
schedule.every().day.at("07:00").do(main)

while True:
    schedule.run_pending()
    time.sleep(60)
