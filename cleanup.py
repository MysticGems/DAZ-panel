import bpy
print('new run')
img_names = []
materials = bpy.data.materials

def findImage(name):
    if( name == "" ):
        return( 0 )
    for img in bpy.data.images:
        if( img.name == name ):
            return( img )
    return( 0 );

for mat in materials:
    if hasattr( mat, 'node_tree' ):
        if hasattr( mat.node_tree, 'nodes' ):
            nodes = mat.node_tree.nodes
            print( mat.name )
            for node in nodes:
                if type(node) == bpy.types.ShaderNodeTexImage:
                    try:
                        nam = node.image.name
                        parts = nam.split(".")
                        nam = parts[0] + "." + parts[1]
                        newImage = findImage( nam )
                        if newImage:
                            node.image = newImage
                            nam = node.image.name
                        # newImage = bpy.data.images( nam )
                        print( "- Using image " + nam)
                        img_names.append(nam)
                    except:
                        print('- No texture')
 
imgs = bpy.data.images
for image in imgs:
    name = image.name
    if name not in img_names:
        print( 'Removing image ' + name )
        image.user_clear()