import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(1,1,1,projection='3d')     #subplotの追加 (行/列/描画対象インデックス,3次元軸の追加)

# xy平面にsin関数を描画する
xs = np.linspace(-np.pi, np.pi, 100)
ys = np.sin(xs)
ax.plot(xs, ys, zs=0, zdir='z', label='sin (x, y)')

# xz平面にcos関数を描画する
xs = np.linspace(-np.pi, np.pi, 100)
ys= np.zeros([100])
zs = np.cos(xs)
ax.scatter(xs, ys, zs, zdir='z', label='cos (x, y)',color="red")

ax.legend()
ax.set_xlim(-np.pi, np.pi)
ax.set_ylim(-np.pi, np.pi)
ax.set_zlim(-np.pi, np.pi)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()