from .core import *
from .core import __raw_version__ as __raw_version__

def get_cmake_module_path() -> str: ...
def get_include() -> str: ...
def get_libraries() -> str: ...

# Names in __all__ with no definition:
#   AbstractConstraint
#   AbstractController
#   AbstractControllerFunctor
#   AbstractMotor
#   AbstractPerlinProcess
#   AbstractSensor
#   BaseConstraint
#   BaseController
#   ConstraintsHolder
#   ContactSensor
#   ControllerFunctor
#   DistanceConstraint
#   EffortSensor
#   EncoderSensor
#   Engine
#   EngineMultiRobot
#   FixedFrameConstraint
#   ForceCoupling
#   ForceCouplingVector
#   ForceImpulse
#   ForceImpulseVector
#   ForceProfile
#   ForceProfileVector
#   ForceSensor
#   HeightmapFunctor
#   ImuSensor
#   JointConstraint
#   Model
#   PeriodicFourierProcess
#   PeriodicGaussianProcess
#   PeriodicPerlinProcess
#   RandomPerlinProcess
#   Robot
#   SimpleMotor
#   SphereConstraint
#   StepperState
#   SystemState
#   TimeStateFunctorBool
#   TimeStateFunctorPinocchioForce
#   WheelConstraint
#   aba
#   build_geom_from_urdf
#   build_models_from_urdf
#   computeJMinvJt
#   computeKineticEnergy
#   crba
#   discretize_heightmap
#   getNumpyType
#   get_joint_position_idx
#   get_joint_type
#   get_random_seed
#   heightmapType_t
#   hresult_t
#   interpolate
#   is_position_valid
#   joint_t
#   merge_heightmap
#   random_tile_ground
#   reset_random_generator
#   rnea
#   seed
#   sensorsData
#   setNumpyType
#   sharedMemory
#   solveJMinvJtv
#   sum_heightmap
#   switchToNumpyArray
#   switchToNumpyMatrix
#   system
#   systemVector
