'''
This simple script takes every selected scene object and sticks a box on top of it named "[ObjectName]_PHYS" 
in accordance with what SL expects the physics object to be named.
It also range-checks your selected objects, presuming a preset scale multiplier between your scene file and SL.
This value is by default 100, due to cm vs meters, but it's changeable in the class call.
SLPhysicsBoxBuilder ( 100 ) 

To use this script, simply create a Python based Maya shelf Icon and drop this script into it.
'''


class SLPhysicsBoxBuilder( ) :

	def AssignBBToXForm ( self , meshXform ) :

		myShape = SLPhysicsBoxBuilder.GetShape ( meshXform )
		if ( myShape != None ) :

			bbMinX = cmds.getAttr ( myShape +  ".boundingBoxMinX" )
			bbMinY = cmds.getAttr ( myShape +  ".boundingBoxMinY" )
			bbMinZ = cmds.getAttr ( myShape +  ".boundingBoxMinZ" )

			bbMaxX = cmds.getAttr ( myShape +  ".boundingBoxMaxX" )
			bbMaxY = cmds.getAttr ( myShape +  ".boundingBoxMaxY" )
			bbMaxZ = cmds.getAttr ( myShape +  ".boundingBoxMaxZ" )

			bbX = (bbMaxX - bbMinX) * self.sceneScale * cmds.getAttr ( meshXform + ".scale.scaleX" )
			bbY = (bbMaxY - bbMinY) * self.sceneScale * cmds.getAttr ( meshXform + ".scale.scaleY" )
			bbZ = (bbMaxZ - bbMinZ) * self.sceneScale * cmds.getAttr ( meshXform + ".scale.scaleZ" )


			if ( bbX > 64.0 ) :
				print ( "BOUNDING ERROR, MESH TOO LARGE" )
				print ( bbX )
			if ( bbY > 64.0 ) :
				print ( "BOUNDING ERROR, MESH TOO LARGE" )
				print ( bbY )
			if ( bbZ  > 64.0 ) :
				print ( "BOUNDING ERROR, MESH TOO LARGE" )
				print ( bbZ )

			newBB = cmds.polyCube( name = meshXform + "_PHYS" )[0]

			cmds.move ( bbMinX , bbMinY , bbMaxZ , newBB + ".vtx[0]" , absolute = True , ws = True  )
			cmds.move ( bbMaxX , bbMinY , bbMaxZ , newBB + ".vtx[1]" , absolute = True , ws = True  )
			cmds.move ( bbMinX , bbMaxY , bbMaxZ , newBB + ".vtx[2]" , absolute = True , ws = True  )
			cmds.move ( bbMaxX , bbMaxY , bbMaxZ , newBB + ".vtx[3]" , absolute = True , ws = True  )

			cmds.move ( bbMinX , bbMaxY , bbMinZ , newBB + ".vtx[4]" , absolute = True , ws = True  )
			cmds.move ( bbMaxX , bbMaxY , bbMinZ , newBB + ".vtx[5]" , absolute = True , ws = True  )
			cmds.move ( bbMinX , bbMinY , bbMinZ , newBB + ".vtx[6]" , absolute = True , ws = True  )
			cmds.move ( bbMaxX , bbMinY , bbMinZ , newBB + ".vtx[7]" , absolute = True , ws = True  )

			mtxDcmp = cmds.createNode ( "decomposeMatrix" , name = newBB + "_DCMP" )
			cmds.connectAttr ( meshXform + ".worldMatrix" , mtxDcmp + ".inputMatrix" )

			cmds.connectAttr ( mtxDcmp + ".outputRotate" , newBB + ".rotate" )
			cmds.connectAttr ( mtxDcmp + ".outputScale" , newBB + ".scale" )
			cmds.connectAttr ( mtxDcmp + ".outputTranslate" , newBB + ".translate" )
			cmds.connectAttr ( mtxDcmp + ".outputShear" , newBB + ".shear" )


		else :
			print ( "No shape found for " + thing )





	@staticmethod
	def GetShape ( xform ) :
		shape_list = cmds.listRelatives ( xform , children = True , shapes = True )
		if shape_list != None :
			return ( shape_list[0] )
		return None

	def __init__ ( self , sceneScale ) :
		self.sceneScale = sceneScale
		self.sel_set = cmds.ls ( selection = True )
		self.warningSG = "SL_BBWarnColor"

		for obj in self.sel_set :
			self.AssignBBToXForm ( obj )


newBuilder = SLPhysicsBoxBuilder ( 100 )
