import cv2
import ast
from threading import Thread
import numpy as np
import sqlite3
import sys

sys.setrecursionlimit(9999999)

maze = cv2.imread('image.png')
conn = sqlite3.connect('file:cachedb?mode=memory&cache=shared')
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE data (
        maze_path BLOB NOT NULL
);
""")
cursor.execute("""delete from data where 1=1""")
conn.commit()

def node(maze_path):
    global maze
    global cursor
    position = maze_path[-1]
    maze[position[0]][position[1]] = np.array([255, 0, 0])
    try:
        if str(maze[position[0]+1][position[1]]) != '[0 0 0]' and [position[0]+1, position[1]] not in maze_path:
            temp_A = maze_path[:]
            temp_A.append([position[0]+1, position[1]])
            cursor.execute("""INSERT INTO data(maze_path)
                VALUES (?);""", (str(temp_A),))
            conn.commit()
            node(temp_A)
    except:
        pass

    try:
        if str(maze[position[0]][position[1]+1]) != '[0 0 0]' and [position[0], position[1]+1] not in maze_path:
            temp_B = maze_path[:]
            temp_B.append([position[0], position[1]+1])
            cursor.execute("""INSERT INTO data(maze_path)
               VALUES (?);""", (str(temp_B),))
            conn.commit()
            node(temp_B)
    except:
        pass

    try:
        if str(maze[position[0]][position[1]-1]) != '[0 0 0]' and [position[0], position[1]-1] not in maze_path:
            temp_C = maze_path[:]
            temp_C.append([position[0], position[1]-1])
            cursor.execute("""INSERT INTO data(maze_path)
               VALUES (?);""", (str(temp_C),))
            conn.commit()
            node(temp_C)
    except:
        pass

    try:
        if str(maze[position[0]-1][position[1]]) != '[0 0 0]' and [position[0]-1, position[1]] not in maze_path:
            temp_D = maze_path[:]
            temp_D.append([position[0]-1, position[1]])
            cursor.execute("""INSERT INTO data(maze_path)
               VALUES (?);""", (str(temp_D),))
            conn.commit()
            node(temp_D)

    except:
        pass


def showmaze():
    while True:
        global maze
        cv2.imshow('image', maze)
        cv2.waitKey(1)


Thread(target=showmaze).start()
node([[0, 1]])

maze_final = '[499, 498]'
maze_path_final = cursor.execute("select * from data where maze_path like ?", ('%'+maze_final+'%',))
maze_path_final = maze_path_final.fetchone()[0]
array_cordinates = ast.literal_eval(maze_path_final)
for cordinate in array_cordinates:
    maze[cordinate[0]][cordinate[1]] = np.array([0, 0, 255])
