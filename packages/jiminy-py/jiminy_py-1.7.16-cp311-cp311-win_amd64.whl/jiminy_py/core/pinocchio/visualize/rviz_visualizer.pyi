from . import BaseVisualizer
from _typeshed import Incomplete

class RVizVisualizer(BaseVisualizer):
    class Viewer:
        app: Incomplete
        viz: Incomplete
        viz_manager: Incomplete
    viewer: Incomplete
    def initViewer(self, viewer: Incomplete | None = ..., windowName: str = ..., loadModel: bool = ..., initRosNode: bool = ...): ...
    visuals_publisher: Incomplete
    visual_Display: Incomplete
    visual_ids: Incomplete
    collisions_publisher: Incomplete
    collision_Display: Incomplete
    collision_ids: Incomplete
    group_Display: Incomplete
    seq: int
    def loadViewerModel(self, rootNodeName: str = ...) -> None: ...
    def clean(self) -> None: ...
    def display(self, q: Incomplete | None = ...) -> None: ...
    def displayCollisions(self, visibility) -> None: ...
    def displayVisuals(self, visibility) -> None: ...
    def sleep(self, dt) -> None: ...
