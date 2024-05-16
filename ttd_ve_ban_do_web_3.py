import streamlit as st
import streamlit.components.v1 as components

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np
from search import *

import os

thuduc_map = UndirectedGraph(dict(
    BinhChieu=dict(TamBinh=180, BinhPhuoc=374),
    TamBinh=dict(BinhPhuoc=234, TamPhu=108),
    BinhPhuoc=dict(TamPhu=210, AnLoiDong=208),
    TamPhu=dict(LinhTay=140, LinhDong=218, AnLoiDong=320),
    AnLoiDong=dict(LinhDong=291),
    LinhTay=dict(LinhTrung=235, LinhChieu=110, LinhDong=175),
    LinhDong=dict(TruongTho=170),
    LinhTrung=dict(LinhXuan=220, LinhChieu=206),
    LinhChieu=dict(BinhTho=108, TruongTho=210),
    TruongTho=dict(BinhTho=140)))

thuduc_map.locations = dict(
    BinhChieu=(190, 760), TamBinh=(240, 640), BinhPhuoc=(90, 440),
    TamPhu=(280, 540), AnLoiDong=(120, 240), LinhTay=(460, 560),
    LinhDong=(360, 430), LinhTrung=(700, 580), LinhXuan=(640, 760),
    LinhChieu=(510, 500), TruongTho=(480, 310), BinhTho=(550, 410)
)

city_name = dict(
    BinhChieu=(-80, 0), TamBinh=(20, -10), BinhPhuoc=(-80, 20),
    TamPhu=(0, -30), AnLoiDong=(20, 0), LinhTay=(-20, -20),
    LinhDong=(-35, 35), LinhTrung=(-90, -20), LinhXuan=(-80, 0),
    LinhChieu=(20, 10), TruongTho=(-90, 0), BinhTho=(5, -25)
)

map_locations = thuduc_map.locations
graph_dict = thuduc_map.graph_dict

lst_city = []
for city in city_name:
    lst_city.append(city)

xmin = 0
xmax = 800
ymin = 0
ymax = 900

def ve_diem(ax):
    for key in graph_dict:
        x0 = map_locations[key][0]
        y0 = map_locations[key][1]

        dx = city_name[key][0]
        dy = city_name[key][1]
        ten = ax.text(x0+dx, y0-dy, key, fontsize=6)
        ax.plot(x0, y0, 'bo')

def ve_doan_thang(ax):
    for key in graph_dict:
        city = graph_dict[key]
        x0 = map_locations[key][0]
        y0 = map_locations[key][1]

        for neighbor in city:
            x1 = map_locations[neighbor][0]
            y1 = map_locations[neighbor][1]
            ax.plot([x0, x1], [y0, y1], 'lightgray')

def ve_ban_do():
    fig, ax = plt.subplots()
    ax.axis([xmin, xmax, ymin, ymax])
    ax.imshow(Image.open("thuduc_map.png"), extent=[xmin, xmax, ymin, ymax], aspect='auto')
    ve_doan_thang(ax)
    ve_diem(ax)
    return fig

if "flag_anim" not in st.session_state:
    if "flag_ve_ban_do" not in st.session_state:
        st.session_state["flag_ve_ban_do"] = True
        fig = ve_ban_do()
        st.session_state['fig'] = fig
        st.pyplot(fig)
        print(st.session_state["flag_ve_ban_do"])
        print('Vẽ bản đồ lần đầu')
    else:
        print('Đã vẽ bản đồ')
        st.pyplot(st.session_state['fig'])
else:
    components.html(st.session_state["anim"].to_jshtml(), height=600)

lst_city = []
for city in city_name:
    lst_city.append(city)

start_city = st.selectbox('Thành phố bắt đầu:', lst_city)
dest_city = st.selectbox('Thành phố đích:', lst_city)

st.session_state['start_city'] = start_city
st.session_state['dest_city'] = dest_city

if st.button('Direction'):
    duong_di_ngan_nhat = GraphProblem(start_city, dest_city, thuduc_map)
    c = astar_search(duong_di_ngan_nhat)
    lst_path = c.path()
    print('Đường đi ngắn nhất là: ')

    for data in lst_path:
        city = data.state 
        print(city, end = '-')
    print()
    path_locations = {}
    for data in lst_path:
        city = data.state
        path_locations[city] = map_locations[city]
    print(path_locations)

    lst_path_location_x = []
    lst_path_location_y = []

    for city in path_locations:
        lst_path_location_x.append(path_locations[city][0])
        lst_path_location_y.append(path_locations[city][1])

    print(lst_path_location_x)
    print(lst_path_location_y)


    fig, ax = plt.subplots()
    ax.axis([xmin, xmax, ymin, ymax])
    ve_doan_thang(ax)
    path_tim_thay, = ax.plot(lst_path_location_x, lst_path_location_y, 'gray', linewidth=3)
    ve_diem(ax)
    print('Đã gán fig có hướng dẫn')
    st.session_state['fig'] = fig
    st.rerun()

if st.button('Run'):
    start_city = st.session_state['start_city']
    dest_city = st.session_state['dest_city']

    duong_di_ngan_nhat = GraphProblem(start_city, dest_city, thuduc_map)
    c = astar_search(duong_di_ngan_nhat)
    lst_path = c.path()
    print('Đường đi: ')

    for data in lst_path:
        city = data.state 
        print(city, end = '-')
    print()

    path_locations = {}
    for data in lst_path:
        city = data.state
        path_locations[city] = map_locations[city]
    print(path_locations)

    lst_path_location_x = []
    lst_path_location_y = []

    for city in path_locations:
        lst_path_location_x.append(path_locations[city][0])
        lst_path_location_y.append(path_locations[city][1])

    print(lst_path_location_x)
    print(lst_path_location_y)

    fig, ax = plt.subplots()
    ax.axis([xmin, xmax, ymin, ymax])
    dem = 0
    lst_doan_thang = []
    
    for key in graph_dict:
        city = graph_dict[key]
        x0 = map_locations[key][0]
        y0 = map_locations[key][1]

        for neighbor in city:
            x1 = map_locations[neighbor][0]
            y1 = map_locations[neighbor][1]
            doan_thang, = ax.plot([x0, x1], [y0, y1], 'lightgray')
            lst_doan_thang.append(doan_thang)
            dem = dem + 1

        path_tim_thay, = ax.plot(lst_path_location_x, lst_path_location_y, 'gray')
        lst_doan_thang.append(path_tim_thay)

    for key in graph_dict:
        city = graph_dict[key]
        x0 = map_locations[key][0]
        y0 = map_locations[key][1]
        diem, = ax.plot(x0, y0, 'bo')
        lst_doan_thang.append(diem)

        dx = city_name[key][0]
        dy = city_name[key][1]
        ten = ax.text(x0+dx,y0-dy,key)
        lst_doan_thang.append(ten)

    print('Dem: ', dem)

    N = 11
    d = 100
    lst_vi_tri_x = []
    lst_vi_tri_y = []

    L = len(lst_path_location_x)
    for i in range(0,L-1):
        x1 = lst_path_location_x[i]
        y1 = lst_path_location_y[i]
        x2 = lst_path_location_x[i+1]
        y2 = lst_path_location_y[i+1]
        
        d0 = np.sqrt((x2-x1)**2 + (y2-y1)**2)
        N0 = int(N*d0/d)
        dt = 1/(N0-1)
        
        for j in range(0, N0):
            t = j*dt
            x = x1 + (x2-x1)*t
            y = y1 + (y2-y1)*t
            lst_vi_tri_x.append(x)
            lst_vi_tri_y.append(y)
    for i in range(0, L-1):
        x1 = lst_path_location_x[i]
        y1 = lst_path_location_y[i]
        x2 = lst_path_location_x[i+1]
        y2 = lst_path_location_y[i+1]

        dx = x2 - x1
        dy = y2 - y1

    red_circle, = ax.plot([],[],"ro",markersize = 10)

    FRAME = len(lst_vi_tri_x)

    def init():
        ax.axis([xmin, xmax, ymin, ymax])
        return lst_doan_thang, red_circle

    def animate(i):
        red_circle.set_data(lst_vi_tri_x[i], lst_vi_tri_y[i])
        return lst_doan_thang, red_circle 

    anim = FuncAnimation(fig, animate, frames=FRAME, interval=100, init_func=init, repeat=False)

    st.session_state["flag_anim"] = True
    st.session_state['anim'] = anim
    st.rerun()