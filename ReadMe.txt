MP1:

These files work as a simple barebone ray-tracer which can generate image with a 3D objects and a moving camera.

Used Library: Numpy and PIL
Main file: Mp_1_Test.py

1. Generated graphs are in the "Graph" folder
2. Muti-jittering affected can be seen if zoom in

MP2:
https://docs.google.com/document/d/1BYT4-aQE75DIKYjQzBi883DREkrrzi8qStRyn1I7DJo/edit?ts=56ecc24c

1. The raytracer now can render complex meshes with a grid acceleration data structre
2. The point light and directional light are functional
3. The ambiient, diffuse and specular lights are rendered with BRDF

Added Files:
	GameObjects:
		bbox.py
		grid.py
		mesh.py
		meshTriangle.py
	Intangibles:
		lambertian.py
		light.py
		material.py
		shadowRec.py
		Specular.py
	Utils:
		Color.py
		World.py
Modified Files:
	GameObjects:
		planes.py
		sphere.py
		triangle.py
The canvass is 1000 x 1000 pixels
171.583251953 s of running time for 20 balls
236.175794125 s of running time for 200 balls
364.946992159 s of running time for 2000 balls
436.716289997 s of running time for mesh

MP3:

Added Files:
	GameObjects:
		instance.py
		Primitives:
		    rectangle.py
	Intangibles:
		emissive.py
		reflective.py
	Samplers:
	    sampler.py
Modified Files:
	Intangibles:
		material.py
		light.py


1 ray per pixel is traced, with 16 sampling of each ray

picture size 1024 x 1024

3133.15981243 s of running time for the first scene
4287.97799993 s of running time for the second scene

MP4:

Added Files:
   Intangibles:
        BRDF:
            glossySpecular.py
            SV_Lambertian.py
        BTDF:
            perfectTransmitter.py
   Materials:
        glossyReflective.py
        textureMatt.py
        trasparent.py
   Textures:
        checkerTexture.py
        Texture.py

1 ray per pixel is traced, with 25 sampling of each ray

picsize 1600 x 1200

1337.7679998875　s for the first scene with glossy exp of 10000.0
1029.75399995 s　for the first scene with glossy exp of 100.0