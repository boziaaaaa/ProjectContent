#coding=utf8
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image
import numpy
global corner
import shutil
corner = 0.0
global flag
flag = 1
texName = 0

def draw_tellurion():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    qobj = gluNewQuadric()
    glPushMatrix()
    glTranslatef(0.0,0.0,0.0)
    glBindTexture(GL_TEXTURE_2D,texName)
    glEnable(GL_TEXTURE_2D)
    gluQuadricTexture(qobj,GL_TRUE)
    glRotatef(90.0, 1.0, 0.0, 0.0)
    # glRotatef(20,0, 1.0, .0)
    glRotatef(-corner,0, 0.0, 1.0)
    gluSphere(qobj,1,32,32)
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
    # light_position = (1.2, 1.0, 1.0, 0.0)
    # glLight(GL_LIGHT0,GL_POSITION,light_position)
    # glEnable(GL_LIGHTING)
    # glEnable(GL_LIGHT0)
    glutSwapBuffers()

def init():
    glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)
    glGenTextures(1,texName)
    glBindTexture(GL_TEXTURE_2D,texName)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_NEAREST)
    glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_NEAREST)
    inputPicture = "blue2.jpg"
    # inputPicture = "daodao.jpg"

    img = Image.open(inputPicture,"r")
    y,x = img.size
    img_array = numpy.array(img)
    img_array2 = img_array
    glTexImage2D(GL_TEXTURE_2D,0,GL_RGB,x,y,0,GL_RGB,GL_UNSIGNED_BYTE,img_array2)
    img.close()
    # glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    glEnable(GL_DEPTH_TEST)
    glClearDepth(1.0)

    glDepthFunc(GL_LEQUAL)
    glClearColor(0,0,0,0)
    glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()
    # glOrtho(-1.0,1.0,-1.0,1.0,-1.0,1.0)
def Moving():
    global corner
    if flag==1:
        corner = 0.015 + corner
        glutPostRedisplay()
if __name__=="__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE|GLUT_RGB|GLUT_DEPTH)
    # glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB|GLUT_DEPTH)
    glutInitWindowSize(100,100)
    glutInitWindowPosition(0,500)
    glutCreateWindow("OpenGL  earth")
    glutDisplayFunc(draw_tellurion)
    glutIdleFunc(Moving)
    init()
    glutMainLoop()

