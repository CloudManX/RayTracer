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