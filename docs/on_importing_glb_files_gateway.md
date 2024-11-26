The following steps were taken:

1. Use Blender to import the full .glb file, which contains the assembly of the Gateway model. This assembly consists of 7 differentiated collections (Blender term, which for our purposes just means high-level parts composed by smaller parts).
2. From the 7 collections, 5 are mostly static, so they can be each be exported to a single collada file. 
3. The 2 remaining entities correspond to the big and the small arms, with 7 DOF each. You need to create individual files (meshes) per each link.
4. For the 5 static collections: Copy and paste each collection. When selecting for copying, right-click and select to include hierarchies too. Then select the new collection and export it to collada. Check the boxes where it says that only the selected part will be exported, as well as the rest in the main section (export armature, and so on, it is 4 options).
5. For the 2 arms: The easiest way is to do similarly to the previous step: Copy and paste the whole "arm" collection, then you can open the collada file containing all the robot links with a text editor and then manually extract the individual links. It is surprisingly easy as collada uses the xml format.

Things I tried before being able to export the stuff
======================================================
1. Use onShape: Normally it is my workhorse but it failed me this time: The importing had topology errors. I wasn't able to export individual "parts" to collada.
2. Use Blender and NOT copy-paste stuff, just try to select the "collection" and export it: Either it exported the whole gateway or it didn't export anything. The copy-and-paste method was by far the easiest.
3. Sometimes collada will do things like creating textures named "XXX.png-BaseColor.png".  This will fail due to the presence of 2 ".png" in the texture name. Use grep/sed to get rid of these things.
4. When creating the robot links files, set the matrices for the nodes to identity, and then in the urdf, the matrices' original transformations will be the ones that are used to define the joint positions. You can either calculate xyz, rpy from matrices, or (what I did) just open the full collada file in Blender, click on each link and copy the transform values, which are the same.
