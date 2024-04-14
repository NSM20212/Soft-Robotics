import Sofa 

plugins =["Sofa.Component.AnimationLoop","Sofa.Component.IO.Mesh",
          "Sofa.Component.Visual","Sofa.Component.Constraint.Lagrangian.Solver","Sofa.Component.Mass",
          "Sofa.Component.ODESolver.Backward","Sofa.Component.StateContainer",
          "Sofa.Component.Topology.Container.Dynamic","Sofa.GL.Component.Rendering3D",
          "Sofa.GL.Component.Shader","Sofa.Component.LinearSolver.Iterative",
          "Sofa.Component.Mapping.Linear","Sofa.Component.MechanicalLoad",
          "Sofa.Component.SolidMechanics.Spring","Sofa.Component.SolidMechanics.FEM.Elastic",
          "Sofa.Component.Engine.Select","Sofa.Component.Engine.Transform",
          "Sofa.Component.Constraint.Projective","Sofa.Component.LinearSolver.Direct",
          "Sofa.Component.Collision.Detection.Algorithm","Sofa.Component.Collision.Detection.Intersection",
          "Sofa.Component.Collision.Geometry","Sofa.Component.Collision.Response.Contact",
          "Sofa.Component.Topology.Container.Constant", 'Multithreading']

def createScene(root):
    #Caracteristicas de la escena
    root.gravity = [0, 0, -9.81]
    root.dt = 0.01
    root.addObject("RequiredPlugin", pluginName=plugins)
    
    #Visualizacion
    root.addObject('InteractiveCamera', position="0.1 0.1 0.1", lookAt="0 0 0")
    root.addObject('LightManager')
    
    #Definicion de la animacion
    root.addObject('DefaultAnimationLoop')
    root.addObject('VisualStyle',
                   displayFlags="showVisual showBehaviorModels showForceFields showInteractionForceFields showCollisionModels") #Vectores de informacion
    root.addObject('PositionalLight', name="light1",
                   color="1 1 1", attenuation="0.1",
                   position="10 10 10")
    
    #Definicioin de colisiones
    root.addObject('CollisionPipeline', verbose="1",
                   depth="12", draw="0")
    root.addObject('ParallelBruteForceBroadPhase')
    root.addObject('ParallelBVHNarrowPhase')
    root.addObject('MinProximityIntersection', name="Proximity",
                   alarmDistance="5e-3", contactDistance="5e-4")
    root.addObject('CollisionResponse')
    
    #Mallas (Unicamente objetos deformables)
    #TODO Nombres de archivos y objetos en la simulación
    root.addObject('MeshGmshLoader', name="Anillo_Torniquete",
                   filename="Assets/NOMBRE_ARCHIVO.msh")
    
    
    #Definicion del objeto anillo torniquete
    anillo =  root.addChild('anillo')
    anillo.addObject('EulerImplicitSolver', rayleighStiffness="0.1",
                     rayleighMass="0.1")
    anillo.addObject('CGLinearSolver', iterations="100",
                     tolerance="1e-5", threshold="1e-5")
    #TODO Nombre de la malla en las dos src siguientes
    anillo.addObject('MechanicalObject', name="StateVectors",
                     template="Vec3", src="@../Anillo_Torniquete")
    anillo.addObject('TetrahedronSetTopologyContainer', name="volume_tetra",
                     src="@../Anillo_Torniquete")
    anillo.addObject('TetrahedronSetGeometryAlgorithms', template="Vec3",
                     name="GeomAlgo")
    anillo.addObject('TetrahedronSetTopologyModifier', name="Modifier")
    anillo.addObject('UniformMass', totalMass="45.0e-3")
    
    #Propiedades mecánicas
    #TODO Establecer las propiedades
    anillo.addObject('ParallelTetrahedronFEMForceField', template="Vec3",
                     name="FEM", method="large",
                     poissonRatio="0.49", youngModulus="125000")
    
    #Carga de la malla para la fijacion del objeto
    #TODO Nombre del STL a cargar del fijador.
    anillo.addObject('MeshSTLLoader', name="fixedMesh",
                     filename="Assets/NOMBRE_MALLA.stl")
    anillo.addObject('MeshROI', name="fixedROI",
                     src='@fixedMesh', drawMesh="1",
                     drawTetrahedra="1", doUpdate="0",
                     position="@StateVectors.position", tetrahedra="@../Anillo_Torniquete.tetrahedra",
                     ROIposition="@fixedMesh.position", ROItriangles="@fixedMesh.triangles")
    anillo.addObject('FixedConstraint', name="fixed", indices='@fixedROI.indices')
    
    #Definicion de la cavidad para el inflado
    cavity = anillo.addChild('cavity')
    #TODO Nombre del stl de la cavidad
    cavity.addObject('MeshSTLLoader', name="cavity", filename="Assets/cavity.stl")
    cavity.addObject('TriangleSetTopologyContainer', name="surface_tris", src="@cavity")
    cavity.addObject('TriangleSetGeometryAlgorithms', template="Vec3", name="GeomAlgo")
    cavity.addObject('MechanicalObject', name="StateVectors", template="Vec3", src="@cavity")
    cavity.addObject('SurfacePressureForceField', pressure="30000",
                     pulseMode="true", pressureSpeed="10000",
                     drawForceScale="0.1", useTangentStiffness="false")
    cavity.addObject('BarycentricMapping')
    
    #Superficie del actuador
    surf = anillo.addChild('surf')
    #TODO Archivo .stl del exterior del actuador
    surf.addObject('MeshSTLLoader', filename="Assets/outside.stl", name="loadersurf")
    surf.addObject('MeshTopology', src="@loadersurf")
    surf.addObject('MechanicalObject', src="@loadersurf")
    surf.addObject('PointCollisionModel')
    surf.addObject('TriangleCollisionModel')
    surf.addObject('BarycentricMapping')
    
    #Objeto rigido para el actuador (cilindro)
    cilindro = root.addObject('cilindro')
    #TODO agrgar stl del clindro
    cilindro.addObject('MeshSTLLoader', filename="Assets/cilindro.stl", name="loader")
    cilindro.addObject('MeshTopology', src="@loader")
    cilindro.addObject('MechanicalObject')
    cilindro.addObject('PointCollisionModel', contactStiffness="1")
    cilindro.addObject('LineCollisionModel', contactStiffness="1")
    cilindro.addObject('TriangleCollisionModel', contactStiffness="1")
    