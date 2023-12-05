import os
import matplotlib as mpl
import numpy as np
import FreeCAD as App



import matplotlib as mpl
import numpy as np
import FreeCAD as App

doc = FreeCAD.newDocument()

filename = '/home/robert/data_zurik/fibrilas/dla_mode_s_ts_2_nb_30000_seed_130_.dat'

def colorfade(c1,c2,mix = 0):
    c1 = np.array(mpl.colors.to_rgb(c1))
    c2 = np.array(mpl.colors.to_rgb(c2))
    return mpl.colors.to_rgb((1-mix)*c1+mix*c2)

c1 = "firebrick"
c2 = "gold"
N = 30001
cores = [colorfade(c1,c2,i/N) for i in range(N+1)]

j = 0
with open (filename, 'r') as fid:
    for row in fid:
        row = row.split()
        id = j
        x = int(row[2])
        y = int(row[3])
        z = int(row[4])
        id = 1
        b = doc.addObject("Part::Box", "B%d" % 1)
        b.ViewObject.ShapeColor = cores[j]
        b.Length = 1
        b.Width =  18
        b.Height = 1
        b.Placement = App.Placement(App.Vector(x,y+1,z), App.Rotation(0,0,0), App.Vector(0,0,0))
        j+=1
        



doc = App.activeDocument()

box = doc.addObject("Part::Box", "myBox")
box.Length = 1
box.Width = 1
box.Height = 1
box.Placement = App.Placement(App.Vector(1, 2, 3), App.Rotation(0, 0, 0))

doc.recompute()
