from typing import Any, Optional, overload
from enum import Enum
import lagrange.scene

class FacetAllocationStrategy(Enum):
    """
    <attribute '__doc__' of 'FacetAllocationStrategy' objects>
    """

    EvenSplit: Any
    
    RelativeToMeshArea: Any
    
    RelativeToNumFacets: Any
    
class MeshInstance3D:
    """
    A single mesh instance in a scene
    """

    def __init__(self) -> None:
        ...
    
    @property
    def mesh_index(self) -> int:
        ...
    @mesh_index.setter
    def mesh_index(self) -> int:
        ...
    
    @property
    def transform(self) -> numpy.typing.NDArray:
        ...
    @transform.setter
    def transform(self) -> numpy.typing.NDArray:
        ...
    
class RemeshingOptions:

    def __init__(self) -> None:
        ...
    
    @property
    def facet_allocation_strategy(self) -> lagrange.scene.FacetAllocationStrategy:
        ...
    @facet_allocation_strategy.setter
    def facet_allocation_strategy(self) -> lagrange.scene.FacetAllocationStrategy:
        ...
    
    @property
    def min_facets(self) -> int:
        ...
    @min_facets.setter
    def min_facets(self) -> int:
        ...
    
class SimpleScene3D:
    """
    Simple scene container for instanced meshes
    """

    def __init__(self) -> None:
        ...
    
    def add_instance(self, instance: lagrange.scene.MeshInstance3D) -> int:
        ...
    
    def add_mesh(self, mesh: lagrange.core.SurfaceMesh) -> int:
        ...
    
    def get_instance(self, mesh_index: int, instance_index: int) -> lagrange.scene.MeshInstance3D:
        ...
    
    def get_mesh(self, mesh_index: int) -> lagrange.core.SurfaceMesh:
        ...
    
    def num_instances(self, mesh_index: int) -> int:
        ...
    
    @property
    def num_meshes(self) -> int:
        """
        Number of meshes in the scene
        """
        ...
    
    def ref_mesh(self, mesh_index: int) -> lagrange.core.SurfaceMesh:
        ...
    
    def reserve_instances(self, mesh_index: int, num_instances: int) -> None:
        ...
    
    def reserve_meshes(self, num_meshes: int) -> None:
        ...
    
    @property
    def total_num_instances(self) -> int:
        """
        Total number of instances for all meshes in the scene
        """
        ...
    
