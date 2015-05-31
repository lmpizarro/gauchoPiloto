'''
http://blenderscripting.blogspot.com.ar/2012/09/python-driven-animaion.html
'''
import bpy
import math

# for demo it creates a cube if it doesn't exist,
# but this can be any existing named object.
if not 'Cube' in bpy.data.objects:
    bpy.ops.mesh.primitive_cube_add()

frames_per_revolution = 120.0
step_size = 2*math.pi / frames_per_revolution


def set_object_location(n):
    x = math.sin(n) * 5
    y = math.cos(n) * 5
    z = 0.0
    ob = bpy.data.objects.get("Cube")
    ob.location = (x, y, z)

# every frame change, this function is called.
def my_handler(scene):
    frame = scene.frame_current
    n = frame % frames_per_revolution
    
    if n == 0:
        set_object_location(n)
    else:
        set_object_location(n*step_size)


bpy.app.handlers.frame_change_pre.append(my_handler)
