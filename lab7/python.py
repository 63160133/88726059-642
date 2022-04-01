#!/usr/bin/python

# This is statement is required by the build system to query build info
if _name_ == '_build_':
	raise Exception

'''

cube.py
Converted to Python by Jason Petrone 6/00

/*
 * Copyright (c) 1993-1997, Silicon Graphics, Inc.
 * ALL RIGHTS RESERVED 
 * Permission to use, copy, modify, and distribute this software for 
 * any purpose and without fee is hereby granted, provided that the above
 * copyright notice appear in all copies and that both the copyright notice
 * and this permission notice appear in supporting documentation, and that 
 * the name of Silicon Graphics, Inc. not be used in advertising
 * or publicity pertaining to distribution of the software without specific,
 * written prior permission. 
 *
 * THE MATERIAL EMBODIED ON THIS SOFTWARE IS PROVIDED TO YOU "AS-IS"
 * AND WITHOUT WARRANTY OF ANY KIND, EXPRESS, IMPLIED OR OTHERWISE,
 * INCLUDING WITHOUT LIMITATION, ANY WARRANTY OF MERCHANTABILITY OR
 * FITNESS FOR A PARTICULAR PURPOSE.  IN NO EVENT SHALL SILICON
 * GRAPHICS, INC.  BE LIABLE TO YOU OR ANYONE ELSE FOR ANY DIRECT,
 * SPECIAL, INCIDENTAL, INDIRECT OR CONSEQUENTIAL DAMAGES OF ANY
 * KIND, OR ANY DAMAGES WHATSOEVER, INCLUDING WITHOUT LIMITATION,
 * LOSS OF PROFIT, LOSS OF USE, SAVINGS OR REVENUE, OR THE CLAIMS OF
 * THIRD PARTIES, WHETHER OR NOT SILICON GRAPHICS, INC.  HAS BEEN
 * ADVISED OF THE POSSIBILITY OF SUCH LOSS, HOWEVER CAUSED AND ON
 * ANY THEORY OF LIABILITY, ARISING OUT OF OR IN CONNECTION WITH THE
 * POSSESSION, USE OR PERFORMANCE OF THIS SOFTWARE.
 * 
 * US Government Users Restricted Rights 
 * Use, duplication, or disclosure by the Government is subject to
 * restrictions set forth in FAR 52.227.19(c)(2) or subparagraph
 * (c)(1)(ii) of the Rights in Technical Data and Computer Software
 * clause at DFARS 252.227-7013 and/or in similar or successor
 * clauses in the FAR or the DOD or NASA FAR Supplement.
 * Unpublished-- rights reserved under the copyright laws of the
 * United States.  Contractor/manufacturer is Silicon Graphics,
 * Inc., 2011 N.  Shoreline Blvd., Mountain View, CA 94039-7311.
 *
 * OpenGL(R) is a registered trademark of Silicon Graphics, Inc.
 */

 '''

#  cube.c
#  This program demonstrates a single modeling transformation,
#  glScalef() and a single viewing transformation, gluLookAt().
#  A wireframe cube is rendered.

import sys

from OpenGL.GL.VERSION import GL_1_0
from OpenGL.raw.GLUT import STRING
import msvcrt 
try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print ('''ERROR: PyOpenGL not installed properly.''')

import numpy as np
import math

left = -5.0
right = 5.0
bottom = -20.0
top = 20.0
near = -5.0
far = 5.0

#window size
win_width = 640
win_height = 480

#window position
win_x = 100
win_y = 100

RED = [1.0, 0.0,0.0]
GREEN = [0.0, 1.0, 0.0]
BLUE = [0.0, 0.0, 1.0]
YELLOW = [1.0, 1.0, 0.0]
CYAN = [0.0, 1.0, 1.0]
MAGENTA = [1.0, 0.0, 1.0]
WHITE =[1.0,1.0,1.0]
BLACK = [0.0, 0.0, 0.0]
GRAY50 = [0.5, 0.5, 0.5]
vertices = [
  [-1.0, -1.0, -1.0],
  [1.0, -1.0, -1.0],
  [1.0, 1.0, -1.0],
  [-1.0, 1.0, -1.0],
  [-1.0, -1.0, 1.0],
  [1.0, -1.0, 1.0],
  [1.0, 1.0, 1.0],
  [-1.0, 1.0, 1.0]
]
def polygon(a, b, c, d, color = [1.0,1.0,1.0]):
  global vertices
  glColor3fv(color)
  glBegin(GL_POLYGON)
  glVertex3fv(vertices[a])
  glVertex3fv(vertices[b])
  glVertex3fv(vertices[c])
  glVertex3fv(vertices[d])
  glEnd()

def cube():
  polygon(0,3,2,1, RED)
  polygon(0,4,7,3, BLUE)
  polygon(1,2,6,5, YELLOW) #right
  polygon(4,5,6,7, GREEN) #front
  polygon(3,7,6,2, MAGENTA)#top
  polygon(0,1,5,4, CYAN) #bottom

def cubeInstance(x, y, z):
  glPushMatrix()
  glTranslatef(x,y,z)
  cube()
  glPopMatrix()

def init(): 
  #define background color
  glClearColor (0,0,0,0) 
  glMatrixMode(GL_PROJECTION)
  glLoadIdentity()
  #define display mode to orthographics
  glOrtho(left, right, bottom, top, near, far)
  glShadeModel(GL_SMOOTH)
  glEnable(GL_DEPTH_TEST)

rho = 2
theta = 0
thetaX =0 
thetaY=0
thetaZ =0
phi = math.pi/4

#text for textfield in future
text = ''

numSize =5 #for rectangle
def display():
  global vertices, theta, rho, numSize
  global thetaX, thetaY, thetaZ

  glClear (GL_COLOR_BUFFER_BIT |GL_DEPTH_BUFFER_BIT)
  glMatrixMode(GL_MODELVIEW)
  glLoadIdentity ()             # clear the matrix 
  glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
  #parametric rectangle
  gluLookAt(1,1,1,0,0,0, 0,1,0)

  #radian = theta/360*math.pi*2
  #thetar = [1,0,0,0, 1/math.tan(radian),1,0,0, 0,0,1,0, 0,0,0,1]
  #glMultMatrixf(thetar)
  glTranslatef(2,1,2)
  glRotatef(thetaX, 1,0,0)
  glRotatef(thetaY, 0,1,0)
  glRotatef(thetaZ, 0,0,1)
  glTranslatef(-2,-1,-2)
  cubeInstance(2,1,2) #instance Object
  glFlush()
  glutSwapBuffers()
  glMatrixMode(GL_PROJECTION)


def reshape (w, h):
  global left, right, bottom, top, near, far
  glViewport (0, 0, w, h)
  glMatrixMode (GL_PROJECTION)
  glLoadIdentity ()
  k = (right-left)/(top-bottom)
  # a : aspect ratio
  a = float(w)/h
  
  leftAspect = left
  rightAspect = right
  bottomAspect = bottom
  topAspect = top
  if a>=1.0:
    leftAspect = left*a
    rightAspect= right*a
  else:
    bottomAspect = bottom/a
    topAspect = top/a
  if k>=1:
    leftAspect /= k
    rightAspect /=k
  else:
    bottomAspect *= k
    topAspect *=k
  glOrtho(leftAspect,rightAspect,bottomAspect,topAspect,near,far)
  glutPostRedisplay()

  win_width = w
  win_height = h

def addText(texts, alpha):
  character = str(alpha)
  texts = texts + character
  pass

def keyboard(key, x, y):
  global text


  if key == chr(27): #escape
    import sys
    sys.exit(0)
  if key == chr(45) : #backspace
    pass
  if key == chr(127): #delete
    pass
  if key == chr(13): #carriage return
    pass
  else:
    alpha = str(key,'utf-8')

    text += alpha
    print('text is ' + text)


def mouse(button, state, x, y):
  global theta, thetaX, thetaY, thetaZ
  if(state == GLUT_DOWN):
    if (button==GLUT_LEFT_BUTTON):
      thetaX += 30.0
    if (button==GLUT_MIDDLE_BUTTON):
      thetaY += 30.0
    if(button==GLUT_RIGHT_BUTTON):
      thetaZ += 30.0
  glutPostRedisplay()

def idle():
  global phi, theta
  phi += 0.0005
  
  glutPostRedisplay()

glutInit(sys.argv)
glutInitDisplayMode (GLUT_DOUBLE | GLUT_RGB|GLUT_DEPTH)
glutInitWindowSize (win_width, win_height)
glutInitWindowPosition (win_x, win_y)
glutCreateWindow ('My First Graphics'.encode())
init ()
#callback registers
glutDisplayFunc(display)
glutReshapeFunc(reshape)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouse)
# idle routine
glutIdleFunc(idle)
glutMainLoop()