'''tk_mouse_click_shape1.py
show xy coordinates of mouse click position
relative to root or relative within a shape
tested with Python27/Python33   by  vegaseat
'''
try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk
def showxy(event):
    '''
    show x, y coordinates of mouse click position
    event.x, event.y relative to ulc of widget (here root) 
    '''
    # xy relative to ulc of root
    #xy = 'root x=%s  y=%s' % (event.x, event.y)
    # optional xy relative to blue rectangle
    xy = 'rectangle x=%s  y=%s' % (event.x-x1, event.y-y1)
    root.title(xy)
root = tk.Tk()
root.title("Mouse click within blue rectangle ...")
# create a canvas for drawing
w = 400
h = 400
cv = tk.Canvas(root, width=w, height=h, bg='white')
cv.pack()
# draw a blue rectangle shape with 
# upper left corner coordinates x1, y1
# lower right corner coordinates x2, y2
x1 = 20
y1 = 30
x2 = 380
y2 = 370
cv.create_rectangle(x1, y1, x2, y2, fill="blue", tag='rectangle')
# bind left mouse click within shape rectangle
cv.tag_bind('rectangle', '<Button-1>', showxy)
root.mainloop()