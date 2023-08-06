from __future__ import annotations
import jiminy_py.core
import typing
import Boost.Python
import ctypes
import inspect
import logging
import numpy
import os
import pinocchio.pinocchio_pywrap.serialization
import re
import sys
_Shape = typing.Tuple[int, ...]

__all__ = [
    "AbstractConstraint",
    "AbstractController",
    "AbstractControllerFunctor",
    "AbstractMotor",
    "AbstractPerlinProcess",
    "AbstractSensor",
    "BaseConstraint",
    "BaseController",
    "ConstraintsHolder",
    "ContactSensor",
    "ControllerFunctor",
    "DistanceConstraint",
    "EffortSensor",
    "EncoderSensor",
    "Engine",
    "EngineMultiRobot",
    "FixedFrameConstraint",
    "ForceCoupling",
    "ForceCouplingVector",
    "ForceImpulse",
    "ForceImpulseVector",
    "ForceProfile",
    "ForceProfileVector",
    "ForceSensor",
    "HeightmapFunctor",
    "ImuSensor",
    "JointConstraint",
    "Model",
    "PeriodicFourierProcess",
    "PeriodicGaussianProcess",
    "PeriodicPerlinProcess",
    "RandomPerlinProcess",
    "Robot",
    "SimpleMotor",
    "SphereConstraint",
    "StepperState",
    "SystemState",
    "TimeStateFunctorBool",
    "TimeStateFunctorPinocchioForce",
    "WheelConstraint",
    "__raw_version__",
    "__version__",
    "aba",
    "build_geom_from_urdf",
    "build_models_from_urdf",
    "computeJMinvJt",
    "computeKineticEnergy",
    "crba",
    "discretize_heightmap",
    "getNumpyType",
    "get_cmake_module_path",
    "get_include",
    "get_joint_position_idx",
    "get_joint_type",
    "get_libraries",
    "get_random_seed",
    "heightmapType_t",
    "hresult_t",
    "interpolate",
    "is_position_valid",
    "joint_t",
    "merge_heightmap",
    "random_tile_ground",
    "reset_random_generator",
    "rnea",
    "seed",
    "sensorsData",
    "setNumpyType",
    "sharedMemory",
    "solveJMinvJtv",
    "sum_heightmap",
    "switchToNumpyArray",
    "switchToNumpyMatrix",
    "system",
    "systemVector"
]


class AbstractConstraint():
    def compute_jacobian_and_drift(self, q: numpy.ndarray, v: numpy.ndarray) -> hresult_t: ...
    def reset(self, q: numpy.ndarray, v: numpy.ndarray) -> hresult_t: ...
    @property
    def baumgarte_freq(self) -> float:
        """
        :type: float
        """
    @baumgarte_freq.setter
    def baumgarte_freq(self: AbstractConstraint) -> None:
        pass
    @property
    def drift(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def is_enabled(self) -> bool:
        """
        :type: bool
        """
    @is_enabled.setter
    def is_enabled(self: AbstractConstraint) -> None:
        pass
    @property
    def jacobian(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def lambda_c(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def type(self) -> str:
        """
        :type: str
        """
    pass
class AbstractController():
    def get_options(self) -> dict: 
        """
        Get the configuration options of the controller.


        :return:     Dictionary with the parameters of the controller
        """
    def initialize(self, robot: Robot) -> hresult_t: 
        """
        Set the parameters of the controller.

        :param robot:
            Robot


            :return:     Return code to determine whether the execution of the method was successful.
        """
    def register_constants(self, fieldnames: str, values: typing.Any) -> hresult_t: ...
    def register_variable(self, fieldname: str, value: typing.Any) -> hresult_t: 
        """
        Dynamically registered a Eigen Vector to the telemetry.

        Internally, all it does is to store a reference to the variable, then it logs
        its value periodically. There is no update mechanism what so ever nor safety
        check. So the user has to take care of the life span of the variable, and to
        update it manually whenever it is necessary to do so.

        :param fieldnames:
            Name of each element of the variable. It will appear in the header of the log.
        :param values:
            Eigen vector to add to the telemetry. It accepts non-contiguous temporary.


            :return:     Return code to determine whether the execution of the method was successful.
        """
    def register_variables(self, fieldnames: list, values: typing.Any) -> hresult_t: ...
    def remove_entries(self) -> None: 
        """
        Remove all variables dynamically registered to the telemetry.

        Note that one must reset Jiminy Engine for this to take effect.
        """
    def reset(self, reset_dynamic_telemetry: bool = False) -> hresult_t: 
        """
        Reset the internal state of the controller.

        Note that it resets the configuration of the telemetry.


        .. note::
            This method is not intended to be called manually. The Engine is taking care
            of it when its own `reset` method is called.

        :param resetDynamicTelemetry:
            Whether variables dynamically registered to the
            telemetry must be removed.
            Optional: False by default
        """
    def set_options(self, arg2: dict) -> hresult_t: 
        """
        Set the configuration options of the controller.

        Note that one must reset Jiminy Engine for this to take effect.

        :param ctrlOptions:
            Dictionary with the parameters of the controller


            :return:     Return code to determine whether the execution of the method was successful.
        """
    @property
    def is_initialized(self) -> bool:
        """
        Get isInitialized_.

        It is a flag used to determine if the controller has been initialized.


        .. note::
            Note that a controller can be considered initialized even if its telemetry is
            not properly configured. If not, it is the only to do before being ready to
            use.

        :type: bool
        """
    @property
    def robot(self) -> Robot:
        """
        :type: Robot
        """
    @property
    def sensors_data(self) -> sensorsData:
        """
        :type: sensorsData
        """
    pass
class AbstractControllerFunctor(AbstractController):
    def compute_command(self, t: float, q: numpy.ndarray, v: numpy.ndarray, command: numpy.ndarray) -> hresult_t: 
        """
        Compute the command.

        It assumes that the robot internal state (including sensors) is consistent
        with other input arguments. It fetches the sensor data automatically.

        :param t:
            Current time
        :param q:
            Current configuration vector
        :param v:
            Current velocity vector
        :param command:
            Output effort vector


            :return:     Return code to determine whether the execution of the method was successful.
        """
    def internal_dynamics(self, t: float, q: numpy.ndarray, v: numpy.ndarray, u_custom: numpy.ndarray) -> hresult_t: 
        """
        Emulate internal dynamics of the system at are not included in the
        physics engine.

        :param t:
            Current time
        :param q:
            Current configuration vector
        :param v:
            Current velocity vector
        :param uCustom:
            Output effort vector


            :return:     Return code to determine whether the execution of the method was successful.
        """
    pass
class AbstractMotor():
    def get_options(self) -> dict: ...
    def set_options(self, arg2: dict) -> hresult_t: 
        """
        Set the configuration options of the motor.

        :param motorOptions:
            Dictionary with the parameters of the motor
        """
    @property
    def armature(self) -> float:
        """
        :type: float
        """
    @property
    def command_limit(self) -> float:
        """
        :type: float
        """
    @property
    def idx(self) -> int:
        """
        :type: int
        """
    @property
    def is_initialized(self) -> bool:
        """
        :type: bool
        """
    @property
    def joint_idx(self) -> int:
        """
        :type: int
        """
    @property
    def joint_name(self) -> str:
        """
        :type: str
        """
    @property
    def joint_position_idx(self) -> int:
        """
        :type: int
        """
    @property
    def joint_type(self) -> joint_t:
        """
        :type: joint_t
        """
    @property
    def joint_velocity_idx(self) -> int:
        """
        :type: int
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    pass
class AbstractPerlinProcess():
    def __call__(self, time: float) -> float: ...
    def reset(self) -> None: ...
    @property
    def num_octaves(self) -> int:
        """
        :type: int
        """
    @property
    def scale(self) -> float:
        """
        :type: float
        """
    @property
    def wavelength(self) -> float:
        """
        :type: float
        """
    pass
class AbstractSensor():
    def __repr__(self) -> str: ...
    def get_options(self) -> dict: ...
    def set_options(self, arg2: dict) -> hresult_t: 
        """
        Set the configuration options of the sensor.

        :param sensorOptions:
            Dictionary with the parameters of the sensor
        """
    @property
    def data(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @data.setter
    def data(self: AbstractSensor) -> None:
        pass
    @property
    def fieldnames(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def idx(self) -> int:
        """
        :type: int
        """
    @property
    def is_initialized(self) -> bool:
        """
        :type: bool
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def type(self) -> str:
        """
        :type: str
        """
    pass
class BaseConstraint(AbstractConstraint):
    def __init__(self) -> None: ...
    @typing.overload
    def compute_jacobian_and_drift(self, arg2: numpy.ndarray, arg3: numpy.ndarray) -> hresult_t: ...
    @typing.overload
    def compute_jacobian_and_drift(self, arg2: numpy.ndarray, arg3: numpy.ndarray) -> None: ...
    @typing.overload
    def reset(self, arg2: numpy.ndarray, arg3: numpy.ndarray) -> hresult_t: ...
    @typing.overload
    def reset(self, arg2: numpy.ndarray, arg3: numpy.ndarray) -> None: ...
    __instance_size__ = 32
    type = 'UserConstraint'
    pass
class BaseController(AbstractController):
    def __init__(self) -> None: ...
    @typing.overload
    def compute_command(self, t: float, q: numpy.ndarray, v: numpy.ndarray, command: numpy.ndarray) -> hresult_t: 
        """
        Compute the command.

        It assumes that the robot internal state (including sensors) is consistent
        with other input arguments. It fetches the sensor data automatically.

        :param t:
            Current time
        :param q:
            Current configuration vector
        :param v:
            Current velocity vector
        :param command:
            Output effort vector


            :return:     Return code to determine whether the execution of the method was successful.
        """
    @typing.overload
    def compute_command(self, arg2: float, arg3: numpy.ndarray, arg4: numpy.ndarray, arg5: numpy.ndarray) -> None: ...
    @typing.overload
    def internal_dynamics(self, t: float, q: numpy.ndarray, v: numpy.ndarray, u_custom: numpy.ndarray) -> hresult_t: 
        """
        Emulate internal dynamics of the system at are not included in the
        physics engine.

        :param t:
            Current time
        :param q:
            Current configuration vector
        :param v:
            Current velocity vector
        :param uCustom:
            Output effort vector


            :return:     Return code to determine whether the execution of the method was successful.
        """
    @typing.overload
    def internal_dynamics(self, arg2: float, arg3: numpy.ndarray, arg4: numpy.ndarray, arg5: numpy.ndarray) -> None: ...
    def reset(self, reset_dynamic_telemetry: bool = False) -> hresult_t: ...
    __instance_size__ = 32
    pass
class ConstraintsHolder():
    @property
    def bounds_joints(self) -> dict:
        """
        :type: dict
        """
    @property
    def collision_bodies(self) -> list:
        """
        :type: list
        """
    @property
    def contact_frames(self) -> dict:
        """
        :type: dict
        """
    @property
    def registered(self) -> dict:
        """
        :type: dict
        """
    pass
class ContactSensor(AbstractSensor):
    def __init__(self, frame_name: str) -> None: ...
    def initialize(self, arg2: str) -> hresult_t: ...
    @property
    def frame_idx(self) -> int:
        """
        :type: int
        """
    @property
    def frame_name(self) -> str:
        """
        :type: str
        """
    __instance_size__ = 32
    fieldnames = ['FX', 'FY', 'FZ']
    has_prefix = False
    type = 'ContactSensor'
    pass
class ControllerFunctor(AbstractControllerFunctor, AbstractController):
    def __init__(self, compute_command: typing.Any = None, internal_dynamics: typing.Any = None) -> None: ...
    def reset(self, reset_dynamic_telemetry: bool = False) -> hresult_t: ...
    pass
class DistanceConstraint(AbstractConstraint):
    def __init__(self, first_frame_name: str, second_frame_name: str) -> None: ...
    @property
    def frames_idx(self) -> StdVec_Index:
        """
        :type: StdVec_Index
        """
    @property
    def frames_names(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def reference_distance(self) -> float:
        """
        :type: float
        """
    @reference_distance.setter
    def reference_distance(self: DistanceConstraint) -> None:
        pass
    __instance_size__ = 32
    type = 'DistanceConstraint'
    pass
class EffortSensor(AbstractSensor):
    def __init__(self, joint_name: str) -> None: ...
    def initialize(self, arg2: str) -> hresult_t: ...
    @property
    def motor_idx(self) -> int:
        """
        :type: int
        """
    @property
    def motor_name(self) -> str:
        """
        :type: str
        """
    __instance_size__ = 32
    fieldnames = ['U']
    has_prefix = True
    type = 'EffortSensor'
    pass
class EncoderSensor(AbstractSensor):
    def __init__(self, joint_name: str) -> None: ...
    def initialize(self, arg2: str) -> hresult_t: ...
    @property
    def joint_idx(self) -> int:
        """
        :type: int
        """
    @property
    def joint_name(self) -> str:
        """
        :type: str
        """
    @property
    def joint_type(self) -> joint_t:
        """
        :type: joint_t
        """
    __instance_size__ = 32
    fieldnames = ['Q', 'V']
    has_prefix = True
    type = 'EncoderSensor'
    pass
class EngineMultiRobot():
    def __init__(self) -> None: ...
    def add_system(self, system_name: str, robot: Robot, controller: typing.Any = None, callback_function: typing.Any = None) -> hresult_t: ...
    @staticmethod
    def compute_forward_kinematics(system: system, q: numpy.ndarray, v: numpy.ndarray, a: numpy.ndarray) -> None: ...
    def compute_systems_dynamics(self, t_end: float, q_list: list, v_list: list) -> list: ...
    def get_options(self) -> dict: ...
    @staticmethod
    def read_log(fullpath: str, format: typing.Any = None) -> dict: 
        """
        Read a logfile from jiminy.

        .. note::
            This function supports both binary and hdf5 log.

        :param fullpath: Name of the file to load.
        :param format: Name of the file to load.

        :returns: Dictionary containing the logged constants and variables.
        """
    def register_force_coupling(self, system_name_1: str, system_name_2: str, frame_name_1: str, frame_name_2: str, force_function: typing.Any) -> hresult_t: 
        """
        Add a force linking both systems together

        This function registers a callback function forceFct that links
        both systems by a given force. This function must return the
        force that the second systems applies to the first system,
        in the global frame of the first frame (i.e. expressed at the origin
        of the first frame, in word coordinates).

        :param systemName1:
            Name of the first system (the one receiving the force)
        :param systemName2:
            Name of the second system (the one applying the force)
        :param frameName1:
            Frame on the first system where the force is applied.
        :param frameName2:
            Frame on the second system where
            (the opposite of) the force is applied.
        :param forceFct:
            Callback function returning the force that systemName2
            applies on systemName1, in the global frame of frameName1.
        """
    def register_force_impulse(self, system_name: str, frame_name: str, t: float, dt: float, F: numpy.ndarray) -> hresult_t: 
        """
        Apply an impulse force on a frame for a given duration at the desired time.
        The force must be given in the world frame.
        """
    def register_force_profile(self, system_name: str, frame_name: str, force_function: typing.Any, update_period: float = 0.0) -> hresult_t: ...
    @typing.overload
    def register_viscoelastic_directional_force_coupling(self, system_name_1: str, system_name_2: str, frame_name_1: str, frame_name_2: str, stiffness: float, damping: float, rest_length: float = 0.0) -> hresult_t: ...
    @typing.overload
    def register_viscoelastic_directional_force_coupling(self, system_name: str, frame_name_1: str, frame_name_2: str, stiffness: float, damping: float, rest_length: float = 0.0) -> hresult_t: ...
    @typing.overload
    def register_viscoelastic_force_coupling(self, system_name_1: str, system_name_2: str, frame_name_1: str, frame_name_2: str, stiffness: numpy.ndarray, damping: numpy.ndarray, alpha: float = 0.5) -> hresult_t: ...
    @typing.overload
    def register_viscoelastic_force_coupling(self, system_name: str, frame_name_1: str, frame_name_2: str, stiffness: numpy.ndarray, damping: numpy.ndarray, alpha: float = 0.5) -> hresult_t: ...
    def remove_all_forces(self) -> hresult_t: ...
    @typing.overload
    def remove_forces_coupling(self, system_name_1: str, system_name_2: str) -> hresult_t: ...
    @typing.overload
    def remove_forces_coupling(self, system_name: str) -> hresult_t: ...
    def remove_forces_impulse(self, system_name: str) -> hresult_t: ...
    def remove_forces_profile(self, system_name: str) -> hresult_t: ...
    def remove_system(self, system_name: str) -> hresult_t: ...
    def reset(self, reset_random_generator: bool = False, remove_all_forces: bool = False) -> None: ...
    def set_controller(self, system_name: str, controller: AbstractController) -> hresult_t: ...
    def set_options(self, arg2: dict) -> hresult_t: ...
    def simulate(self, t_end: float, q_init_list: dict, v_init_list: dict, a_init_list: typing.Any = None) -> hresult_t: 
        """
        Run a simulation of duration tEnd, starting at xInit.

        :param tEnd:
            End time, i.e. amount of time to simulate.
        :param qInit:
            Initial configuration of every system, i.e. at t=0.0.
        :param vInit:
            Initial velocity of every system, i.e. at t=0.0.
        :param aInit:
            Initial acceleration of every system, i.e. at t=0.0. Optional: Zero by default.
        """
    def start(self, q_init_list: dict, v_init_list: dict, a_init_list: typing.Any = None) -> hresult_t: 
        """
        Reset the engine and compute initial state.

        This function does NOT reset the engine, robot and controller.
        It is up to the user to do so, by calling `reset` method first.

        :param qInit:
            Initial configuration of every system.
        :param vInit:
            Initial velocity of every system.
        :param aInit:
            Initial acceleration of every system. Optional: Zero by default.
        """
    def step(self, dt_desired: float = -1) -> hresult_t: 
        """
        Integrate system from current state for a duration equal to stepSize

        This function performs a single 'integration step', in the sense that only
        the endpoint is added to the log. The integrator object is allowed to perform
        multiple steps inside of this interval.
        One may specify a negative timestep to use the default update value.

        :param stepSize:
            Duration for which to integrate ; set to negative value to use default update value.
        """
    def stop(self) -> None: 
        """
        Stop the simulation.

        It releases the lock on the robot and the telemetry, so that
        it is possible again to update the robot (for example to update
        the options, add or remove sensors...) and to register new
        variables or forces.
        """
    def write_log(self, fullpath: str, format: str) -> hresult_t: ...
    @property
    def forces_coupling(self) -> ForceCouplingVector:
        """
        :type: ForceCouplingVector
        """
    @property
    def forces_impulse(self) -> dict:
        """
        :type: dict
        """
    @property
    def forces_profile(self) -> dict:
        """
        :type: dict
        """
    @property
    def is_simulation_running(self) -> bool:
        """
        :type: bool
        """
    @property
    def log_data(self) -> dict:
        """
        :type: dict
        """
    @property
    def stepper_state(self) -> StepperState:
        """
        :type: StepperState
        """
    @property
    def systems(self) -> systemVector:
        """
        :type: systemVector
        """
    @property
    def systems_names(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def systems_states(self) -> dict:
        """
        :type: dict
        """
    __instance_size__ = 32
    simulation_duration_max = 922337203.6854776
    telemetry_time_unit = 1e-10
    pass
class Engine(EngineMultiRobot):
    def __init__(self) -> None: ...
    def initialize(self, robot: Robot, controller: AbstractController = None, callback_function: typing.Any = None) -> hresult_t: ...
    def register_force_coupling(self, frame_name_1: str, frame_name_2: str, force_function: typing.Any) -> hresult_t: ...
    def register_force_impulse(self, frame_name: str, t: float, dt: float, F: numpy.ndarray) -> hresult_t: ...
    def register_force_profile(self, frame_name: str, force_function: typing.Any, update_period: float = 0.0) -> hresult_t: ...
    def register_viscoelastic_directional_force_coupling(self, frame_name_1: str, frame_name_2: str, stiffness: float, damping: float, rest_length: float = 0.0) -> hresult_t: ...
    def register_viscoelastic_force_coupling(self, frame_name_1: str, frame_name_2: str, stiffness: numpy.ndarray, damping: numpy.ndarray, alpha: float = 0.5) -> hresult_t: ...
    def remove_system(self, system_name: str) -> hresult_t: ...
    def set_controller(self, controller: AbstractController) -> hresult_t: ...
    def simulate(self, t_end: float, q_init: numpy.ndarray, v_init: numpy.ndarray, a_init: typing.Any = None, is_state_theoretical: bool = False) -> hresult_t: ...
    def start(self, q_init: numpy.ndarray, v_init: numpy.ndarray, a_init: typing.Any = None, is_state_theoretical: bool = False) -> hresult_t: ...
    @property
    def controller(self) -> AbstractController:
        """
        :type: AbstractController
        """
    @property
    def forces_impulse(self) -> ForceImpulseVector:
        """
        :type: ForceImpulseVector
        """
    @property
    def forces_profile(self) -> ForceProfileVector:
        """
        :type: ForceProfileVector
        """
    @property
    def is_initialized(self) -> bool:
        """
        :type: bool
        """
    @property
    def robot(self) -> Robot:
        """
        :type: Robot
        """
    @property
    def stepper_state(self) -> StepperState:
        """
        :type: StepperState
        """
    @property
    def system(self) -> system:
        """
        :type: system
        """
    @property
    def system_state(self) -> SystemState:
        """
        :type: SystemState
        """
    __instance_size__ = 32
    simulation_duration_max = 922337203.6854776
    telemetry_time_unit = 1e-10
    pass
class FixedFrameConstraint(AbstractConstraint):
    def __init__(self, frame_name: str, mask_fixed: typing.Any = None) -> None: ...
    def set_normal(self, arg2: numpy.ndarray) -> None: ...
    @property
    def dofs_fixed(self) -> list:
        """
        :type: list
        """
    @property
    def frame_idx(self) -> int:
        """
        :type: int
        """
    @property
    def frame_name(self) -> str:
        """
        :type: str
        """
    @property
    def local_rotation(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def reference_transform(self) -> SE3:
        """
        :type: SE3
        """
    @reference_transform.setter
    def reference_transform(self: FixedFrameConstraint) -> None:
        pass
    type = 'FixedFrameConstraint'
    pass
class ForceCoupling():
    @property
    def force_func(self) -> typing.Any:
        """
        :type: typing.Any
        """
    @property
    def system_idx_1(self) -> int:
        """
        :type: int
        """
    @property
    def system_idx_2(self) -> int:
        """
        :type: int
        """
    @property
    def system_name_1(self) -> str:
        """
        :type: str
        """
    @property
    def system_name_2(self) -> str:
        """
        :type: str
        """
    pass
class ForceCouplingVector():
    def __contains__(self, arg2: typing.Any) -> bool: ...
    def __delitem__(self, arg2: typing.Any) -> None: ...
    def __getitem__(self, arg2: typing.Any) -> typing.Any: ...
    def __iter__(self) -> typing.Any: ...
    def __len__(self) -> int: ...
    def __setitem__(self, arg2: typing.Any, arg3: typing.Any) -> None: ...
    def append(self, arg2: typing.Any) -> None: ...
    def extend(self, arg2: typing.Any) -> None: ...
    pass
class ForceImpulse():
    @property
    def F(self) -> Force:
        """
        :type: Force
        """
    @property
    def dt(self) -> float:
        """
        :type: float
        """
    @property
    def frame_idx(self) -> int:
        """
        :type: int
        """
    @property
    def frame_name(self) -> str:
        """
        :type: str
        """
    @property
    def t(self) -> float:
        """
        :type: float
        """
    pass
class ForceImpulseVector():
    def __contains__(self, arg2: typing.Any) -> bool: ...
    def __delitem__(self, arg2: typing.Any) -> None: ...
    def __getitem__(self, arg2: typing.Any) -> typing.Any: ...
    def __iter__(self) -> typing.Any: ...
    def __len__(self) -> int: ...
    def __setitem__(self, arg2: typing.Any, arg3: typing.Any) -> None: ...
    def append(self, arg2: typing.Any) -> None: ...
    def extend(self, arg2: typing.Any) -> None: ...
    pass
class ForceProfile():
    @property
    def force_func(self) -> typing.Any:
        """
        :type: typing.Any
        """
    @property
    def force_prev(self) -> Force:
        """
        :type: Force
        """
    @property
    def frame_idx(self) -> int:
        """
        :type: int
        """
    @property
    def frame_name(self) -> str:
        """
        :type: str
        """
    @property
    def update_period(self) -> float:
        """
        :type: float
        """
    pass
class ForceProfileVector():
    def __contains__(self, arg2: typing.Any) -> bool: ...
    def __delitem__(self, arg2: typing.Any) -> None: ...
    def __getitem__(self, arg2: typing.Any) -> typing.Any: ...
    def __iter__(self) -> typing.Any: ...
    def __len__(self) -> int: ...
    def __setitem__(self, arg2: typing.Any, arg3: typing.Any) -> None: ...
    def append(self, arg2: typing.Any) -> None: ...
    def extend(self, arg2: typing.Any) -> None: ...
    pass
class ForceSensor(AbstractSensor):
    def __init__(self, frame_name: str) -> None: ...
    def initialize(self, arg2: str) -> hresult_t: ...
    @property
    def frame_idx(self) -> int:
        """
        :type: int
        """
    @property
    def frame_name(self) -> str:
        """
        :type: str
        """
    @property
    def joint_idx(self) -> int:
        """
        :type: int
        """
    __instance_size__ = 32
    fieldnames = ['FX', 'FY', 'FZ', 'MX', 'MY', 'MZ']
    has_prefix = False
    type = 'ForceSensor'
    pass
class HeightmapFunctor():
    def __call__(self, position: numpy.ndarray) -> tuple: ...
    def __init__(self, heightmap_function: typing.Any, heightmap_type: heightmapType_t = heightmapType_t.GENERIC) -> None: ...
    @property
    def py_function(self) -> typing.Any:
        """
        :type: typing.Any
        """
    pass
class ImuSensor(AbstractSensor):
    def __init__(self, frame_name: str) -> None: ...
    def initialize(self, arg2: str) -> hresult_t: ...
    @property
    def frame_idx(self) -> int:
        """
        :type: int
        """
    @property
    def frame_name(self) -> str:
        """
        :type: str
        """
    __instance_size__ = 32
    fieldnames = ['Gyrox', 'Gyroy', 'Gyroz', 'Accelx', 'Accely', 'Accelz']
    has_prefix = False
    type = 'ImuSensor'
    pass
class JointConstraint(AbstractConstraint):
    def __init__(self, joint_name: str) -> None: ...
    @property
    def is_enabled(self) -> bool:
        """
        :type: bool
        """
    @is_enabled.setter
    def is_enabled(self: JointConstraint) -> None:
        pass
    @property
    def joint_idx(self) -> int:
        """
        :type: int
        """
    @property
    def joint_name(self) -> str:
        """
        :type: str
        """
    @property
    def reference_configuration(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @reference_configuration.setter
    def reference_configuration(self: JointConstraint) -> None:
        pass
    __instance_size__ = 32
    type = 'JointConstraint'
    pass
class Model():
    def add_collision_bodies(self, bodies_names: list = [], ignore_meshes: bool = False) -> hresult_t: ...
    def add_constraint(self, name: str, constraint: AbstractConstraint) -> hresult_t: ...
    def add_contact_points(self, frame_names: list = []) -> hresult_t: ...
    def add_frame(self, frame_name: str, parent_body_name: str, frame_placement: SE3) -> hresult_t: ...
    def compute_constraints(self, q: numpy.ndarray, v: numpy.ndarray) -> None: 
        """
        Compute jacobian and drift associated to all the constraints.

        The results are accessible using getConstraintsJacobian and
        getConstraintsDrift.

        .. note::
            It is assumed frames forward kinematics has already been called.

        :param q:
            Joint position.
        :param v:
            Joint velocity.
        """
    def exist_constraint(self, constraint_name: str) -> bool: ...
    def get_constraint(self, constraint_name: str) -> AbstractConstraint: 
        """
        Get a pointer to the constraint referenced by constraintName

        :param constraintName:
            Name of the constraint to get.

            :return:     ERROR_BAD_INPUT if constraintName does not exist, SUCCESS otherwise.
        """
    def get_constraints_jacobian_and_drift(self) -> tuple: ...
    def get_flexible_configuration_from_rigid(self, rigid_position: numpy.ndarray) -> numpy.ndarray: ...
    def get_flexible_velocity_from_rigid(self, rigid_velocity: numpy.ndarray) -> numpy.ndarray: ...
    def get_rigid_configuration_from_flexible(self, flexible_position: numpy.ndarray) -> numpy.ndarray: ...
    def get_rigid_velocity_from_flexible(self, flexible_velocity: numpy.ndarray) -> numpy.ndarray: ...
    def remove_collision_bodies(self, bodies_names: list) -> hresult_t: ...
    def remove_constraint(self, name: str) -> hresult_t: ...
    def remove_contact_points(self, frame_names: list) -> hresult_t: ...
    def remove_frame(self, frame_name: str) -> hresult_t: ...
    @property
    def collision_bodies_idx(self) -> StdVec_Index:
        """
        :type: StdVec_Index
        """
    @property
    def collision_bodies_names(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def collision_data(self) -> GeometryData:
        """
        :type: GeometryData
        """
    @property
    def collision_model(self) -> GeometryModel:
        """
        :type: GeometryModel
        """
    @property
    def collision_model_th(self) -> GeometryModel:
        """
        :type: GeometryModel
        """
    @property
    def collision_pairs_idx_by_body(self) -> StdVec_IndexVector:
        """
        :type: StdVec_IndexVector
        """
    @property
    def constraints(self) -> ConstraintsHolder:
        """
        :type: ConstraintsHolder
        """
    @property
    def contact_frames_idx(self) -> StdVec_Index:
        """
        :type: StdVec_Index
        """
    @property
    def contact_frames_names(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def flexible_joints_idx(self) -> StdVec_Index:
        """
        :type: StdVec_Index
        """
    @property
    def flexible_joints_names(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def has_constraints(self) -> bool:
        """
        Returns true if at least one constraint is active on the robot.

        :type: bool
        """
    @property
    def has_freeflyer(self) -> bool:
        """
        :type: bool
        """
    @property
    def is_flexible(self) -> bool:
        """
        :type: bool
        """
    @property
    def is_initialized(self) -> bool:
        """
        :type: bool
        """
    @property
    def log_fieldnames_acceleration(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def log_fieldnames_f_external(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def log_fieldnames_position(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def log_fieldnames_velocity(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def mesh_package_dirs(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def nq(self) -> int:
        """
        :type: int
        """
    @property
    def nv(self) -> int:
        """
        :type: int
        """
    @property
    def nx(self) -> int:
        """
        :type: int
        """
    @property
    def pinocchio_data(self) -> Data:
        """
        :type: Data
        """
    @property
    def pinocchio_data_th(self) -> Data:
        """
        :type: Data
        """
    @property
    def pinocchio_model(self) -> pinocchio.Model:
        """
        :type: pinocchio.Model
        """
    @property
    def pinocchio_model_th(self) -> pinocchio.Model:
        """
        :type: pinocchio.Model
        """
    @property
    def position_limit_lower(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def position_limit_upper(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def rigid_joints_idx(self) -> StdVec_Index:
        """
        :type: StdVec_Index
        """
    @property
    def rigid_joints_names(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def rigid_joints_position_idx(self) -> StdVec_Int:
        """
        :type: StdVec_Int
        """
    @property
    def rigid_joints_velocity_idx(self) -> StdVec_Int:
        """
        :type: StdVec_Int
        """
    @property
    def urdf_path(self) -> str:
        """
        :type: str
        """
    @property
    def velocity_limit(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def visual_data(self) -> GeometryData:
        """
        :type: GeometryData
        """
    @property
    def visual_model(self) -> GeometryModel:
        """
        :type: GeometryModel
        """
    @property
    def visual_model_th(self) -> GeometryModel:
        """
        :type: GeometryModel
        """
    pass
class PeriodicFourierProcess():
    def __call__(self, time: float) -> float: ...
    def __init__(self, wavelength: float, period: float, scale: float = 1.0) -> None: ...
    def reset(self) -> None: ...
    @property
    def dt(self) -> float:
        """
        :type: float
        """
    @property
    def num_harmonics(self) -> int:
        """
        :type: int
        """
    @property
    def period(self) -> float:
        """
        :type: float
        """
    @property
    def wavelength(self) -> float:
        """
        :type: float
        """
    __instance_size__ = 32
    pass
class PeriodicGaussianProcess():
    def __call__(self, time: float) -> float: ...
    def __init__(self, wavelength: float, period: float, scale: float = 1.0) -> None: ...
    def reset(self) -> None: ...
    @property
    def dt(self) -> float:
        """
        :type: float
        """
    @property
    def period(self) -> float:
        """
        :type: float
        """
    @property
    def wavelength(self) -> float:
        """
        :type: float
        """
    __instance_size__ = 32
    pass
class PeriodicPerlinProcess(AbstractPerlinProcess):
    def __init__(self, wavelength: float, period: float, scale: float = 1.0, num_octaves: int = 6) -> None: ...
    @property
    def period(self) -> float:
        """
        :type: float
        """
    __instance_size__ = 32
    pass
class RandomPerlinProcess(AbstractPerlinProcess):
    def __init__(self, wavelength: float, scale: float = 1.0, num_octaves: int = 6) -> None: ...
    __instance_size__ = 32
    pass
class Robot(Model):
    def __init__(self) -> None: ...
    def attach_motor(self, motor: AbstractMotor) -> hresult_t: ...
    def attach_sensor(self, sensor: AbstractSensor) -> hresult_t: ...
    def detach_motor(self, joint_name: str) -> hresult_t: ...
    def detach_motors(self, joints_names: list = []) -> hresult_t: ...
    def detach_sensor(self, sensor_type: str, sensor_name: str) -> hresult_t: ...
    def detach_sensors(self, sensor_type: str = '') -> hresult_t: ...
    def dump_options(self, json_filename: str) -> hresult_t: ...
    def get_model_options(self) -> dict: ...
    def get_motor(self, motor_name: str) -> AbstractMotor: ...
    def get_motors_options(self) -> dict: ...
    def get_options(self) -> dict: ...
    def get_sensor(self, sensor_type: str, sensor_name: str) -> AbstractSensor: ...
    def get_sensors_options(self) -> dict: ...
    def get_telemetry_options(self) -> dict: ...
    @typing.overload
    def initialize(self, urdf_path: str, has_freeflyer: bool = False, mesh_package_dirs: list = [], load_visual_meshes: bool = False) -> hresult_t: ...
    @typing.overload
    def initialize(self, pinocchio_model: Model, collision_model: GeometryModel, visual_model: GeometryModel) -> hresult_t: ...
    def load_options(self, json_filename: str) -> hresult_t: ...
    def set_model_options(self, model_options: dict) -> hresult_t: ...
    def set_motors_options(self, motors_options: dict) -> hresult_t: ...
    def set_options(self, robot_options: dict) -> hresult_t: ...
    def set_sensors_options(self, sensors_options: dict) -> hresult_t: ...
    def set_telemetry_options(self, telemetry_options: dict) -> hresult_t: ...
    @property
    def armatures(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def command_limit(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def is_locked(self) -> bool:
        """
        :type: bool
        """
    @property
    def log_fieldnames_command(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def log_fieldnames_motor_effort(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def motors_names(self) -> StdVec_StdString:
        """
        :type: StdVec_StdString
        """
    @property
    def motors_position_idx(self) -> list:
        """
        :type: list
        """
    @property
    def motors_velocity_idx(self) -> StdVec_Int:
        """
        :type: StdVec_Int
        """
    @property
    def nmotors(self) -> int:
        """
        :type: int
        """
    @property
    def sensors_data(self) -> sensorsData:
        """
        :type: sensorsData
        """
    @property
    def sensors_names(self) -> dict:
        """
        :type: dict
        """
    __instance_size__ = 32
    pass
class SimpleMotor(AbstractMotor):
    def __init__(self, motor_name: str) -> None: ...
    def initialize(self, arg2: str) -> hresult_t: ...
    __instance_size__ = 32
    pass
class SphereConstraint(AbstractConstraint):
    def __init__(self, frame_name: str, radius: float) -> None: ...
    @property
    def frame_idx(self) -> int:
        """
        :type: int
        """
    @property
    def frame_name(self) -> str:
        """
        :type: str
        """
    @property
    def reference_transform(self) -> SE3:
        """
        :type: SE3
        """
    @reference_transform.setter
    def reference_transform(self: SphereConstraint) -> None:
        pass
    __instance_size__ = 32
    type = 'SphereConstraint'
    pass
class StepperState():
    def __repr__(self) -> str: ...
    @property
    def a(self) -> list:
        """
        :type: list
        """
    @property
    def dt(self) -> float:
        """
        :type: float
        """
    @property
    def iter(self) -> int:
        """
        :type: int
        """
    @property
    def iter_failed(self) -> int:
        """
        :type: int
        """
    @property
    def q(self) -> list:
        """
        :type: list
        """
    @property
    def t(self) -> float:
        """
        :type: float
        """
    @property
    def v(self) -> list:
        """
        :type: list
        """
    pass
class SystemState():
    def __repr__(self) -> str: ...
    @property
    def a(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def command(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def f_external(self) -> StdVec_Force:
        """
        :type: StdVec_Force
        """
    @property
    def q(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def u(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def u_custom(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def u_internal(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def u_motor(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    @property
    def v(self) -> numpy.ndarray:
        """
        :type: numpy.ndarray
        """
    pass
class TimeStateFunctorBool():
    def __call__(self, t: float, q: numpy.ndarray, v: numpy.ndarray) -> bool: ...
    pass
class TimeStateFunctorPinocchioForce():
    def __call__(self, t: float, q: numpy.ndarray, v: numpy.ndarray) -> Force: ...
    pass
class WheelConstraint(AbstractConstraint):
    def __init__(self, frame_name: str, radius: float, ground_normal: numpy.ndarray, wheel_axis: numpy.ndarray) -> None: ...
    @property
    def frame_idx(self) -> int:
        """
        :type: int
        """
    @property
    def frame_name(self) -> str:
        """
        :type: str
        """
    @property
    def reference_transform(self) -> SE3:
        """
        :type: SE3
        """
    @reference_transform.setter
    def reference_transform(self: WheelConstraint) -> None:
        pass
    __instance_size__ = 32
    type = 'WheelConstraint'
    pass
class heightmapType_t(Boost.Python.enum, int):
    CONSTANT = jiminy_py.core.heightmapType_t.CONSTANT
    GENERIC = jiminy_py.core.heightmapType_t.GENERIC
    STAIRS = jiminy_py.core.heightmapType_t.STAIRS
    __slots__ = ()
    names = {'CONSTANT': jiminy_py.core.heightmapType_t.CONSTANT, 'STAIRS': jiminy_py.core.heightmapType_t.STAIRS, 'GENERIC': jiminy_py.core.heightmapType_t.GENERIC}
    values = {1: jiminy_py.core.heightmapType_t.CONSTANT, 2: jiminy_py.core.heightmapType_t.STAIRS, 3: jiminy_py.core.heightmapType_t.GENERIC}
    pass
class hresult_t(Boost.Python.enum, int):
    ERROR_BAD_INPUT = jiminy_py.core.hresult_t.ERROR_BAD_INPUT
    ERROR_GENERIC = jiminy_py.core.hresult_t.ERROR_GENERIC
    ERROR_INIT_FAILED = jiminy_py.core.hresult_t.ERROR_INIT_FAILED
    SUCCESS = jiminy_py.core.hresult_t.SUCCESS
    __slots__ = ()
    names = {'SUCCESS': jiminy_py.core.hresult_t.SUCCESS, 'ERROR_GENERIC': jiminy_py.core.hresult_t.ERROR_GENERIC, 'ERROR_BAD_INPUT': jiminy_py.core.hresult_t.ERROR_BAD_INPUT, 'ERROR_INIT_FAILED': jiminy_py.core.hresult_t.ERROR_INIT_FAILED}
    values = {1: jiminy_py.core.hresult_t.SUCCESS, -1: jiminy_py.core.hresult_t.ERROR_GENERIC, -2: jiminy_py.core.hresult_t.ERROR_BAD_INPUT, -3: jiminy_py.core.hresult_t.ERROR_INIT_FAILED}
    pass
class joint_t(Boost.Python.enum, int):
    FREE = jiminy_py.core.joint_t.FREE
    LINEAR = jiminy_py.core.joint_t.LINEAR
    NONE = jiminy_py.core.joint_t.NONE
    PLANAR = jiminy_py.core.joint_t.PLANAR
    ROTARY = jiminy_py.core.joint_t.ROTARY
    ROTARY_UNBOUNDED = jiminy_py.core.joint_t.ROTARY_UNBOUNDED
    SPHERICAL = jiminy_py.core.joint_t.SPHERICAL
    __slots__ = ()
    names = {'NONE': jiminy_py.core.joint_t.NONE, 'LINEAR': jiminy_py.core.joint_t.LINEAR, 'ROTARY': jiminy_py.core.joint_t.ROTARY, 'ROTARY_UNBOUNDED': jiminy_py.core.joint_t.ROTARY_UNBOUNDED, 'PLANAR': jiminy_py.core.joint_t.PLANAR, 'SPHERICAL': jiminy_py.core.joint_t.SPHERICAL, 'FREE': jiminy_py.core.joint_t.FREE}
    values = {0: jiminy_py.core.joint_t.NONE, 1: jiminy_py.core.joint_t.LINEAR, 2: jiminy_py.core.joint_t.ROTARY, 3: jiminy_py.core.joint_t.ROTARY_UNBOUNDED, 4: jiminy_py.core.joint_t.PLANAR, 6: jiminy_py.core.joint_t.SPHERICAL, 7: jiminy_py.core.joint_t.FREE}
    pass
class sensorsData():
    def __contains__(self, key: tuple) -> bool: ...
    @typing.overload
    def __getitem__(self, sensor_info: tuple) -> numpy.ndarray: ...
    @typing.overload
    def __getitem__(self, sensor_type: str, sensor_name: str) -> numpy.ndarray: ...
    @typing.overload
    def __getitem__(self, sensor_type: str) -> numpy.ndarray: ...
    def __init__(self, sensors_data_dict: dict) -> None: ...
    def __iter__(self) -> typing.Any: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str: ...
    def items(self) -> list: ...
    @typing.overload
    def keys(self) -> list: ...
    @typing.overload
    def keys(self, sensor_type: str) -> list: ...
    def values(self) -> list: ...
    pass
class system():
    @property
    def callbackFct(self) -> TimeStateFunctorBool:
        """
        :type: TimeStateFunctorBool
        """
    @property
    def controller(self) -> AbstractController:
        """
        :type: AbstractController
        """
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def robot(self) -> Robot:
        """
        :type: Robot
        """
    pass
class systemVector():
    def __contains__(self, arg2: typing.Any) -> bool: ...
    def __delitem__(self, arg2: typing.Any) -> None: ...
    def __getitem__(self, arg2: typing.Any) -> typing.Any: ...
    def __iter__(self) -> typing.Any: ...
    def __len__(self) -> int: ...
    def __setitem__(self, arg2: typing.Any, arg3: typing.Any) -> None: ...
    def append(self, arg2: typing.Any) -> None: ...
    def extend(self, arg2: typing.Any) -> None: ...
    pass
def aba(pinocchio_model: Model, pinocchio_data: Data, q: numpy.ndarray, v: numpy.ndarray, u: numpy.ndarray, fext: StdVec_Force) -> numpy.ndarray:
    """
    Compute ABA with external forces, store the result in Data::ddq and return it.
    """
def build_geom_from_urdf(pinocchio_model: Model, urdf_filename: str, geom_type: int, mesh_package_dirs: list = [], load_meshes: bool = True, make_meshes_convex: bool = False) -> GeometryModel:
    pass
def build_models_from_urdf(urdf_path: str, has_freeflyer: bool, mesh_package_dirs: list = [], build_visual_model: bool = False, load_visual_meshes: bool = False) -> tuple:
    pass
def computeJMinvJt(pinocchio_model: Model, pinocchio_data: Data, J: numpy.ndarray, update_decomposition: bool = True) -> hresult_t:
    pass
def computeKineticEnergy(pinocchio_model: Model, pinocchio_data: Data, q: numpy.ndarray, v: numpy.ndarray) -> float:
    """
    Computes the forward kinematics and the kinematic energy of the model for the given joint configuration and velocity given as input. The result is accessible through data.kinetic_energy.
    """
def crba(pinocchio_model: Model, pinocchio_data: Data, q: numpy.ndarray) -> numpy.ndarray:
    """
    Computes CRBA, store the result in Data and return it.
    """
def discretize_heightmap(heightmap: HeightmapFunctor, grid_size: float, grid_unit: float) -> numpy.ndarray:
    pass
def getNumpyType() -> typing.Any:
    """
    Get the Numpy type returned by the converters from an Eigen object.

    C++ signature :
        boost::python::api::object getNumpyType()
    """
def get_joint_position_idx(pinocchio_model: Model, joint_name: str) -> int:
    pass
def get_joint_type(pinocchio_model: Model, joint_idx: int) -> joint_t:
    pass
def get_random_seed() -> int:
    pass
def interpolate(pinocchio_model: Model, times_in: numpy.ndarray, positions_in: numpy.ndarray, times_out: numpy.ndarray) -> numpy.ndarray:
    pass
def is_position_valid(pinocchio_model: Model, position: numpy.ndarray) -> bool:
    pass
def merge_heightmap(heightmaps: list) -> HeightmapFunctor:
    pass
def random_tile_ground(size: numpy.ndarray, height_max: float, interp_delta: numpy.ndarray, sparsity: int, orientation: float, seed: int) -> HeightmapFunctor:
    pass
def reset_random_generator(seed: typing.Any = None) -> None:
    pass
@typing.overload
def rnea(pinocchio_model: Model, pinocchio_data: Data, q: numpy.ndarray, v: numpy.ndarray, a: numpy.ndarray) -> numpy.ndarray:
    """
    Compute the RNEA without external forces, store the result in Data and return it.

    Compute the RNEA with external forces, store the result in Data and return it.
    """
@typing.overload
def rnea(pinocchio_model: Model, pinocchio_data: Data, q: numpy.ndarray, v: numpy.ndarray, a: numpy.ndarray, fext: StdVec_Force) -> numpy.ndarray:
    pass
def seed(seed_value: int) -> None:
    """
    Initialize the pseudo-random number generator with the argument seed_value.

    C++ signature :
        void seed(unsigned int)
    """
def setNumpyType(numpy_type: typing.Any) -> None:
    """
    Change the Numpy type returned by the converters from an Eigen object.

    C++ signature :
        void setNumpyType(boost::python::api::object {lvalue})
    """
@typing.overload
def sharedMemory(value: bool) -> None:
    """
    Share the memory when converting from Eigen to Numpy.

    C++ signature :
        void sharedMemory(bool)

    Status of the shared memory when converting from Eigen to Numpy.
    If True, the memory is shared when converting an Eigen::Matrix to a numpy.array.
    Otherwise, a deep copy of the Eigen::Matrix is performed.

    C++ signature :
        bool sharedMemory()
    """
@typing.overload
def sharedMemory() -> bool:
    pass
def solveJMinvJtv(pinocchio_data: Data, v: numpy.ndarray, update_decomposition: bool = True) -> numpy.ndarray:
    pass
def sum_heightmap(heightmaps: list) -> HeightmapFunctor:
    pass
def switchToNumpyArray() -> None:
    """
    Set the conversion from Eigen::Matrix to numpy.ndarray.

    C++ signature :
        void switchToNumpyArray()
    """
def switchToNumpyMatrix() -> None:
    """
    Set the conversion from Eigen::Matrix to numpy.matrix.

    C++ signature :
        void switchToNumpyMatrix()
    """
__all__ = ['AbstractConstraint', 'AbstractController', 'AbstractControllerFunctor', 'AbstractMotor', 'AbstractPerlinProcess', 'AbstractSensor', 'BaseConstraint', 'BaseController', 'ConstraintsHolder', 'ContactSensor', 'ControllerFunctor', 'DistanceConstraint', 'EffortSensor', 'EncoderSensor', 'Engine', 'EngineMultiRobot', 'FixedFrameConstraint', 'ForceCoupling', 'ForceCouplingVector', 'ForceImpulse', 'ForceImpulseVector', 'ForceProfile', 'ForceProfileVector', 'ForceSensor', 'HeightmapFunctor', 'ImuSensor', 'JointConstraint', 'Model', 'PeriodicFourierProcess', 'PeriodicGaussianProcess', 'PeriodicPerlinProcess', 'RandomPerlinProcess', 'Robot', 'SimpleMotor', 'SphereConstraint', 'StepperState', 'SystemState', 'TimeStateFunctorBool', 'TimeStateFunctorPinocchioForce', 'WheelConstraint', 'aba', 'build_geom_from_urdf', 'build_models_from_urdf', 'computeJMinvJt', 'computeKineticEnergy', 'crba', 'discretize_heightmap', 'getNumpyType', 'get_joint_position_idx', 'get_joint_type', 'get_random_seed', 'heightmapType_t', 'hresult_t', 'interpolate', 'is_position_valid', 'joint_t', 'merge_heightmap', 'random_tile_ground', 'reset_random_generator', 'rnea', 'seed', 'sensorsData', 'setNumpyType', 'sharedMemory', 'solveJMinvJtv', 'sum_heightmap', 'switchToNumpyArray', 'switchToNumpyMatrix', 'system', 'systemVector', 'get_cmake_module_path', 'get_include', 'get_libraries', '__version__', '__raw_version__']
__raw_version__ = '1.7.16'
__version__ = '1.7.16'
_boost_python_lib = 'libboost_python39.so'
_is_boost_shared = True
_is_dependency_available = True
_lib_prefix = 'lib'
_lib_suffix = '.so'
_module_name = 'serialization'
_module_real_path = 'pinocchio.pinocchio_pywrap.serialization'
_module_sym_path = 'pinocchio.serialization'
_pyver_suffix = '39'
_submodules: list # value = [('cholesky', <module 'pinocchio.pinocchio_pywrap.cholesky'>), ('liegroups', <module 'pinocchio.pinocchio_pywrap.liegroups'>), ('rpy', <module 'pinocchio.pinocchio_pywrap.rpy'>), ('serialization', <module 'pinocchio.pinocchio_pywrap.serialization'>)]
name = 'systemVector'
_find_spec = importlib.util.find_spec
_get_config_var = sysconfig.get_config_var
_import_module = importlib.import_module
attrib = jiminy_py.core.systemVector
