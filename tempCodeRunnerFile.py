
def ve_ban_do():
    fig, ax = plt.subplots()
    ax.axis([xmin, xmax, ymin, ymax])
    ax.axis('off')  # Ẩn trục tọa độ
    ve_doan_thang(ax)
    ve_diem(ax)
