#!/usr/bin/env python

import tkinter as tk
import rospy
from nav_msgs.msg import OccupancyGrid
from PIL import Image, ImageTk
import numpy as np
import re

def map_callback(data):
    global map_data
    map_data = data
    # print ("hola 2")
    print ((map_data.info))
    # res = int.from_bytes(map_data.data, byteorder ='big')
    # map_image = Image.frombytes("L", (map_data.info.width, map_data.info.height), res, "raw", "L", 0, 1)

    # # Display image in GUI
    # map_label = tk.Label(window, image=map_image)
    # map_label.pack()
# Global variable to store image
image = None

def load_map():
    canvas = tk.Canvas(window, width = 384, height = 384)      
    canvas.pack()      
    img = tk.PhotoImage(map_data.data)
    canvas.create_image(384,384, anchor=tk.NW, image=img)  
    tk.Label(window, image=img).pack()
  
def clear_map():
  global map_data
  map_data = None

def listener():

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/map", OccupancyGrid, map_callback)

    # spin() simply keeps python from exiting until this node is stopped
    window.mainloop()

if __name__ == '__main__':
    window = tk.Tk()
    window.title("ROS Map Loader")

    # Create buttons
    load_button = tk.Button(window, text="Load Map", command=load_map)
    clear_button = tk.Button(window, text="Clear Map", command=clear_map)

    # Place buttons in window
    load_button.pack()
    clear_button.pack()
    listener()

