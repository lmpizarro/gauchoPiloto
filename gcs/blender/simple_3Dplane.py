'''
refs: https://www.youtube.com/watch?v=1OePNW34-z4
'''

import bpy

import http.client

conn = http.client.HTTPConnection("wanderdrone.appspot.com")
conn.request("GET", "/")
r1 = conn.getresponse()
if r1.status == 200:
    data1 = r1.read()
    print(".....", data1 )

sce = bpy.context.scene

bpy.ops.object.camera_add(view_align=True, enter_editmode=False, 
location=(5, 5, 5), rotation=(1.10871, 0.0132652, 1.14827))

cube_object = bpy.ops.mesh.primitive_cube_add

def create_part(name,resize,translate):
    '''
    create_part(fuse,(0.07, 1.1, 0.05),(0, 0.35, 0)):
    '''
    cube_object(radius=1, view_align=False, enter_editmode=False, 
    location=(0, 0, 0), rotation=(0,0,0))
    bpy.ops.transform.resize(value=resize)
    bpy.ops.transform.translate(value=translate)
    part = bpy.context.object
    part.name = name
    return part



def run ():
    # FUSE
    fuse = create_part('fuse', (0.07, 1.1, 0.05), (0, 0.35, 0))
    # WING
    wing = create_part('wing', (1.6, 0.2, 0.02), (0, 0, 0.03))
    # ELEVATOR
    elevator = create_part('wing', (0.6, 0.15, 0.02), (0, 1.5, 0.02))
    # RUDDER
    rudder = create_part('wing', (0.005, 0.15, 0.15), (0, 1.5, 0.15))

    '''
    blender python boolean modifier
    http://blenderartists.org/forum/showthread.php?243680-Scripting-with-Boolean-Modifiers-Blender-2-6
    '''
    boo = rudder.modifiers.new('Booh', 'BOOLEAN')
    boo.object = elevator
    boo.operation = 'UNION'
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Booh")
    sce.objects.unlink(elevator)
    rudder_ele = bpy.context.object
    rudder_ele.name = 'rudder_ele'

    boo = rudder_ele.modifiers.new('Booh', 'BOOLEAN')
    boo.object = fuse
    boo.operation = 'UNION'
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Booh")
    sce.objects.unlink(fuse)
    rudder_fuse = bpy.context.object
    rudder_fuse.name = 'rudder_fuse'

    boo = rudder_fuse.modifiers.new('Booh', 'BOOLEAN')
    boo.object = wing
    boo.operation = 'UNION'
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Booh")
    sce.objects.unlink(wing)
    plane = bpy.context.object
    plane.name = 'plane'

    '''
    blender python rotation matrix
    http://blender.stackexchange.com/questions/7598/rotation-around-the-cursor-with-low-level-python-no-bpy-ops
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

    bpy.ops.transform.rotate(value=0.1,axis=(1, 1, 0),
		constraint_axis=(False, False, False), 
		constraint_orientation='GLOBAL', 
		mirror=False, 
		proportional='DISABLED', 
		proportional_edit_falloff='SMOOTH', 
		proportional_size=1)

    bpy.ops.transform.translate(value=(0.0, -1, 0.0), 
		    constraint_axis=(False, False, False), 
		    constraint_orientation='GLOBAL', 
		    mirror=False, proportional='DISABLED', 
		    proportional_edit_falloff='SMOOTH', 
		    proportional_size=1)

    ob = bpy.data.objects.get("plane")
    #ob.location = (0, -1, 0)

    '''


if __name__ == "__main__":
    run()
