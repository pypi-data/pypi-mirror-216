# Metamaterial Analysis Code

## 1. Introduction

This code is the core of the TFM (Final Master Project) "Simulación Mediante  Elementos Finitos Del Comportamiento No
Lineal De Metamateriales Auxéticos En Grandes Desplazamientos Para Uso Ingenieril." It is an OOP pacakage that
allows the user to generate .fem files with the mesh of components based on metamaterial structure.
This means that the material is not solid but consists of cells. Only works for Optistruct.

## 2. Version update

As this is the first version, there are no updates.

## 3. Property and License

The code is property of Manuel Sanchez and the ETSIAE. It follows the MIT license.

The Patent used in the code is exclusively property of their creators. Copy or modifying are not allowed
without permission of their owners.

## 4. Documentation

The package can be used by calling the functions that gets the different objects that are instances of
the different "MACClasses" defined in the code.

Importing the package:
````python
import metamaterialanalysiscode as mac
````

An example of generating a model:
````python
material1 = mac.set_material(id=1, type="MATS1", stressstrain=tabla_strainstress1, nonlinearity="PLASTIC",
                             yieldstress=0.02)

material2 = mac.set_material(id=2, type="MAT1", e=70000, nu=0.3)

beam2 = mac.set_property(id=2, type="PBEAM", material=[material2], area=2000, i1=0.0001, i2=1, i12=1, j=1)

beam1 = mac.set_property(id=1, type="PBEAML", material=[material2], section="ROD", dim1=1.0)

cellstructure1 = mac.set_structure(type="Auxetic", djoint=5.3, dstar=-0.3, heightstar=0.3, hcapas=3,
                                   hprisma=15, stepx=10, stepy=10, nelem=4)


modelo1 = mac.set_model(modeldimensions=(150, 300, 70), cellstructure=cellstructure1, cellmaterial=[material2],
                        cellproperty=[beam1])
````
 Printing the model into a .fem file:

````python
modelo1.write_fem(r"C:\Users\admin\Desktop\test1_model.fem")
````

Generating and printing an analyisis:
````python
enforcedispl1 = MAC.set_load(id=1, type="SPC", nodes=nodesdisp, components=[3], displacement=-0.5, load=True)

constraint1 = MAC.set_constraint(id=2, nodes=nodesdisp, components=[3], displacement=-0.5)

constraint2 = MAC.set_constraint(id=2, nodes=nodespc, components=[1, 2, 3, 4, 5, 6], displacement=0)

subcase1 = MAC.set_subcase(id=1, label="linear", loads=[enforcedispl1], constraints=[constraint1, constraint2])

analysis2 = MAC.set_analysis(model=modelo1, subcases=[subcase1])

analysis2.write_fem(r"C:\Users\admin\Desktop\test1_analysis.fem")
````

As all the nodes and elements are saved in two dictionaries, the user can modify coords, properties, materials,
etc. 

A basic knowledge of OOP is needed to understand and use the advance functionalities that the package brings

Example:
```python
elementtodel = set()
nodetodel = set()
for elementkey in modelo1.ElementDict.keys():
    for node in modelo1.ElementDict[elementkey].Nodes:
        if node.Coords[2] < (minz+0.1) or node.Coords[2] > (maxz-0.1):
            nodetodel.add(node.ID)
            elementtodel.add(elementkey)

for elementkey in elementtodel:
    del modelo1.ElementDict[elementkey]

for nodekey in nodetodel:
    del modelo1.NodeDict[nodekey]
```