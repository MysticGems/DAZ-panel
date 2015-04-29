# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Jack's Tools",
    "version": (0, 2),
    "author": "Jack of Spades",
    "blender": (2, 72, 0),
    "description": "Miscellaneous tools",
    "category": "3D View"}

import bpy

#============================================================================
# DEFINE FUNCTIONS
#============================================================================

def findImage(name):
    if( name == "" ):
        return( 0 )
    for img in bpy.data.images:
        if( img.name == name ):
            return( img )
    return( 0 );

#============================================================================
# DEFINE OPERATORS
#============================================================================

# Removes duplicate images, defined as:
# - having a third component (. delimited)
# - not used in any material node
class cleanupExtraImages(bpy.types.Operator):
    """Clean up extra images in imports"""
    bl_label = "With Rename"
    bl_idname = "view3d.clean_up_images"

    # Do that thing
    def execute(self, context):
        print('new run')
        img_names = []
        materials = bpy.data.materials

        # find images in material nodes
        for mat in materials:
            if hasattr( mat, 'node_tree' ):
                if hasattr( mat.node_tree, 'nodes' ):
                    nodes = mat.node_tree.nodes
                    print( mat.name )
                    for node in nodes:
                        if type(node) == bpy.types.ShaderNodeTexImage:
                            # Get the image name
                            # Drop all but the first two name parts
                            try:
                                nam = node.image.name
                                parts = nam.split(".")
                                nam = parts[0] + "." + parts[1]
                                newImage = findImage( nam )
                                if newImage:
                                    node.image = newImage
                                    nam = node.image.name
                                print( "- Using image " + nam)
                                img_names.append(nam)
                            except:
                                print('- No image')
         
        # Iterate through all images and remove those we
        # haven't identified as used
        imgs = bpy.data.images
        count = 0
        for image in imgs:
            name = image.name
            if name not in img_names:
                print( 'Removing image ' + name )
                count = count + 1
                image.user_clear()
        self.report({'INFO'}, "Removed: %s images" % count)
        return{'FINISHED'}

# Removes duplicate images, defined as:
# - not used in any material node
class cleanupExtraImagesNoRename(bpy.types.Operator):
    """Clean up extra images in imports"""
    bl_label = "No Rename"
    bl_idname = "view3d.clean_up_images_no_rename"

    # Do that thing
    def execute(self, context):
        print('new run')
        img_names = []
        materials = bpy.data.materials

        # find images in material nodes
        for mat in materials:
            if hasattr( mat, 'node_tree' ):
                if hasattr( mat.node_tree, 'nodes' ):
                    nodes = mat.node_tree.nodes
                    print( mat.name )
                    for node in nodes:
                        if type(node) == bpy.types.ShaderNodeTexImage:
                            # Get the image name
                            try:
                                nam = node.image.name
                                print( "- Using image " + nam)
                                img_names.append(nam)
                            except:
                                print('- No image')
         
        # Iterate through all images and remove those we
        # haven't identified as used
        imgs = bpy.data.images
        count = 0
        for image in imgs:
            name = image.name
            if name not in img_names:
                print( 'Removing image ' + name )
                count = count + 1
                image.user_clear()
        self.report({'INFO'}, "Removed: %s images" % count)
        return{'FINISHED'}
    
class loadTeleBlenderExport(bpy.types.Operator):
    """Import mcjTeleBlender export from my usual location"""
    bl_label = "mcjTeleBlender"
    bl_idname = "view3d.jack_import"
    
    def execute(self, context):
        filename = '/Users/jspade/Documents/DAZ 3D/Studio/Exports/scene.py'
        print('Importing from ' + filename)
        exec(compile(open(filename).read(), filename, 'exec'))
#        text = bpy.data.texts.load(path)
#
#        for area in bpy.context.screen.areas:
#           if area.type == 'TEXT_EDITOR':
#                area.spaces[0].text = text # make loaded text file visible
#
#                ctx = bpy.context.copy()
#                ctx['edit_text'] = text
#                ctx['area'] = area
#                ctx['region'] = area.regions[-1]
#                bpy.ops.text.run_script(ctx)
        return{'FINISHED'}

# Create the toolbar panel
class JackPanel(bpy.types.Panel):
    """Miscellaneous personal tools"""
    bl_label = "Personal"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
     
    def draw( self, context ):
         layout = self.layout
         
         row = layout.row()
         row.label(text="Import")
         
         split = layout.split()
         col = split.column( align = True )
         col.operator("view3d.jack_import")
         
         row = layout.row()
         row.label(text="Global Cleanup")

         split = layout.split()
         col = split.column( align = True )
         # Button for image cleanup
         col.operator("view3d.clean_up_images", icon='IMAGE_DATA')
         col.operator("view3d.clean_up_images_no_rename", icon='IMAGE_DATA')
                
#============================================================================
# REGISTER AND UNREGISTER
#============================================================================

def register():
    bpy.utils.register_class(JackPanel)
    bpy.utils.register_class(cleanupExtraImages)
    bpy.utils.register_class(cleanupExtraImagesNoRename)
    bpy.utils.register_class(loadTeleBlenderExport)
def unregister():
    bpy.utils.unregister_class(JackPanel)
    bpy.utils.unregister_class(cleanupExtraImages)
    bpy.utils.unregister_class(cleanupExtraImagesNoRename)
    bpy.utils.unregister_class(loadTeleBlenderExport)

if __name__ == "__main__":
    register()