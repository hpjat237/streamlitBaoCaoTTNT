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