import Sofa
from data_collector import data_query

plugins =["Sofa.Component.AnimationLoop","Sofa.Component.IO.Mesh",
          "Sofa.Component.Visual","Sofa.Component.Constraint.Lagrangian.Solver","Sofa.Component.Mass",
          "Sofa.Component.ODESolver.Backward","Sofa.Component.StateContainer",
          "Sofa.Component.Topology.Container.Dynamic","Sofa.GL.Component.Rendering3D",
          "Sofa.GL.Component.Shader","Sofa.Component.LinearSolver.Iterative",
          "Sofa.Component.Mapping.Linear", "Sofa.Component.MechanicalLoad",
          "Sofa.Component.SolidMechanics.Spring", "Sofa.Component.SolidMechanics.FEM.Elastic",
          "Sofa.Component.Engine.Select", "Sofa.Component.Engine.Transform",
          "Sofa.Component.Constraint.Projective", "Sofa.Component.LinearSolver.Direct"]


def createScene(root):
    #Caracteristicas de la escena
    root.gravity = [0, 0, 0]
    root.dt = 0.01
    root.addObject("RequiredPlugin", pluginName=plugins)
    
    #Visualizacion
    root.addObject('InteractiveCamera', position="0.1 0.1 0.1", lookAt="0 0 0")
    root.addObject('LightManager')
    
    #Definicion de la animacion
    root.addObject('DefaultAnimationLoop')
    root.addObject('VisualStyle',
                   displayFlags="showVisual showBehaviorModels showForceFields") #Vectores de informacion
    root.addObject('PositionalLight', name="light1",
                   color="1 1 1", attenuation="0.1",
                   position="10 10 10")
    
    #Carga de la malla
    root.addObject('MeshGmshLoader', name="volume",
                   filename="Assets/volumenReal.msh")
    
    #Definicion del actuador
    actuador =  root.addChild('actuador')
    actuador.addObject('EulerImplicitSolver', rayleighStiffness="0.1",
                     rayleighMass="0.1")
    actuador.addObject('CGLinearSolver', iterations="100",
                     tolerance="1e-5", threshold="1e-5")
    actuador.addObject('MechanicalObject', name="StateVectors",
                     template="Vec3", src="@../volume")
    actuador.addObject('TetrahedronSetTopologyContainer', name="volume_tetra",
                     src="@../volume")
    actuador.addObject('TetrahedronSetGeometryAlgorithms', template="Vec3",
                     name="GeomAlgo")
    actuador.addObject('TetrahedronSetTopologyModifier', name="Modifier")
    actuador.addObject('UniformMass', totalMass="45.0e-3")
    
    #Propiedades mecánicas
    actuador.addObject('TetrahedronFEMForceField', template="Vec3",
                     name="FEM", method="large",
                     poissonRatio="0.49", youngModulus="125000")
    
    # Carga de la malla para la fijacion del objeto
    actuador.addObject('MeshSTLLoader', name="fixedMesh",
                     filename="Assets/fixed.stl")

    actuador.addObject('MeshROI', name="fixedROI",
                     src='@fixedMesh', drawMesh="1",
                     drawTetrahedra="1", doUpdate="0",
                     position="@StateVectors.position", tetrahedra="@../volume.tetrahedra",
                     ROIposition="@fixedMesh.position", ROItriangles="@fixedMesh.triangles")
    # Cargar zona de interes del punto

    actuador.addObject('MeshSTLLoader',name='tipMesh',filename='Assets/ROI_pin.stl')
    actuador.addObject('MeshROI',name='tipROI',src='@tipMesh',drawMesh='1',drawTetrahedra='1',doUpdate='0',position='@StateVectors.position',tetrahedra='@../volume.tetrahedra',ROIposition='@tipMesh.position',ROItriangles='@tipMesh.triangles')
    


    actuador.addObject('FixedConstraint', name="fixed", indices='@fixedROI.indices')
    
    #Definicion de la cavidad para el inflado
    cavity = actuador.addChild('cavity')
    cavity.addObject('MeshSTLLoader', name="cavity", filename="Assets/cavidadRealGMSH.stl")
    cavity.addObject('TriangleSetTopologyContainer', name="surface_tris", src="@cavity")
    cavity.addObject('TriangleSetGeometryAlgorithms', template="Vec3", name="GeomAlgo")
    cavity.addObject('MechanicalObject', name="StateVectors", template="Vec3", src="@cavity")
    cavity.addObject('SurfacePressureForceField',name='cavityPressure',pressure='0',pulseMode='false',drawForceScale='0.1',useTangentStiffness='false')
    cavity.addObject('BarycentricMapping')

    actuador.addObject(data_query(node = actuador))

    return root