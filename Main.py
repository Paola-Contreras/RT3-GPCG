from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 600
height = 600

# Materiales
white = Material(diffuse = (1, 1, 1), spec = 8)
grey = Material(diffuse = (0.4, 0.4, 0.4), spec = 8)
blue = Material(diffuse = (0.12, 0.30, 0.45), spec = 16)
canye = Material(diffuse = (0.023, 0.48, 0.64), spec = 8)
darkBlue = Material(diffuse = (0.113, 0.215, 0.322), spec = 16)

mirror = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, matType = REFLECTIVE)
glass = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, ior = 1.5, matType = TRANSPARENT)
diamond = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, ior = 2.417, matType = TRANSPARENT)
marble = Material(diffuse = (0.8,0.8,0.8), texture = Texture("marble.bmp"), spec = 32, matType= REFLECTIVE)
canica = Material(diffuse = (0.8,0.8,1.0), texture = Texture("whiteMarble.bmp"), spec = 32, ior = 1.5, matType= REFLECTIVE)


rtx = Raytracer(width, height)


rtx.lights.append( AmbientLight(intensity = 0.8 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.5 ))

rtx.scene.append(Plane(position = V3(-45,0,0), normal = V3(1,0,0), material = blue))
rtx.scene.append(Plane(position = V3(45,0,0),  normal = V3(1,0,0), material = blue))
rtx.scene.append(Plane(position = V3(0,0,-150),normal = V3(0,0,1), material = white))
rtx.scene.append(Plane(position = V3(0,-20,0), normal = V3(0,1,0), material = marble))
rtx.scene.append(Plane(position = V3(0,30,0),  normal = V3(0,1,0), material = darkBlue))

rtx.scene.append(AABB(position=(2,2,-10), size=(2,2,2), material=glass))
rtx.scene.append(AABB(position=(-1.5,0.5,-10), size=(2,2,2), material=grey))

rtx.glRender()

rtx.glFinish("output.bmp") 
