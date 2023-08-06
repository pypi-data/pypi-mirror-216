"""High-Level Motion Library for the Franka Panda Robot"""
from __future__ import annotations
import franky._franky as _franky
import typing
import numpy
_Shape = typing.Tuple[int, ...]

__all__ = [
    "Affine",
    "CartesianPose",
    "CartesianPoseMotion",
    "CartesianPoseReaction",
    "CartesianPoseStopMotion",
    "CartesianVelocities",
    "CartesianVelocityMotion",
    "CartesianVelocityReaction",
    "CartesianWaypoint",
    "CartesianWaypointMotion",
    "CommandException",
    "Condition",
    "ControlException",
    "ControlSignalType",
    "ControllerMode",
    "Duration",
    "Errors",
    "ExponentialImpedanceMotion",
    "GripperException",
    "GripperInternal",
    "GripperState",
    "ImpedanceMotion",
    "IncompatibleVersionException",
    "InvalidMotionTypeException",
    "InvalidOperationException",
    "JointPositionMotion",
    "JointPositionReaction",
    "JointPositionStopMotion",
    "JointPositions",
    "JointVelocities",
    "JointVelocityMotion",
    "JointVelocityReaction",
    "JointWaypoint",
    "JointWaypointMotion",
    "Kinematics",
    "LinearImpedanceMotion",
    "LinearMotion",
    "Measure",
    "ModelException",
    "NetworkException",
    "NullSpaceHandling",
    "ProtocolException",
    "ReactionRecursionException",
    "RealtimeConfig",
    "RealtimeException",
    "ReferenceType",
    "RelativeDynamicsFactor",
    "RobotInternal",
    "RobotMode",
    "RobotPose",
    "RobotState",
    "TorqueMotion",
    "TorqueReaction",
    "Torques"
]


class Affine():
    @typing.overload
    def __init__(self, translation: numpy.ndarray[numpy.float64, _Shape[3, 1]] = array([0., 0., 0.]), quaternion: numpy.ndarray[numpy.float64, _Shape[4, 1]] = array([0., 0., 0., 1.])) -> None: 
        """
        1. __init__(self: _franky.Affine, transformation_matrix: numpy.ndarray[numpy.float64[4, 4]] = array([[1., 0., 0., 0.],
               [0., 1., 0., 0.],
               [0., 0., 1., 0.],
               [0., 0., 0., 1.]])) -> None
        """
    @typing.overload
    def __init__(self, arg0: Affine) -> None: ...
    def __mul__(self, arg0: Affine) -> Affine: ...
    def __repr__(self) -> str: ...
    @property
    def inverse(self) -> Affine:
        """
        :type: Affine
        """
    @property
    def matrix(self) -> numpy.ndarray[numpy.float64, _Shape[4, 4]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[4, 4]]
        """
    @property
    def quaternion(self) -> numpy.ndarray[numpy.float64, _Shape[4, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[4, 1]]
        """
    @property
    def translation(self) -> numpy.ndarray[numpy.float64, _Shape[3, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[3, 1]]
        """
    pass
class CartesianPose():
    @property
    def O_T_EE(self) -> typing.List[float[16]]:
        """
        :type: typing.List[float[16]]
        """
    pass
class CartesianPoseMotion():
    def add_reaction(self, arg0: CartesianPoseReaction) -> None: ...
    def register_callback(self, callback: typing.Callable[[RobotState, Duration, float, float, CartesianPose], None]) -> None: ...
    @property
    def reactions(self) -> typing.List[CartesianPoseReaction]:
        """
        :type: typing.List[CartesianPoseReaction]
        """
    pass
class CartesianPoseReaction():
    def __init__(self, condition: typing.Union[Condition, bool], motion: CartesianPoseMotion = None) -> None: ...
    def register_callback(self, callback: typing.Callable[[RobotState, float, float], None]) -> None: ...
    pass
class CartesianPoseStopMotion(CartesianPoseMotion):
    def __init__(self) -> None: ...
    pass
class CartesianVelocities():
    @property
    def O_dP_EE(self) -> typing.List[float[6]]:
        """
        :type: typing.List[float[6]]
        """
    pass
class CartesianVelocityMotion():
    def add_reaction(self, arg0: CartesianVelocityReaction) -> None: ...
    def register_callback(self, callback: typing.Callable[[RobotState, Duration, float, float, CartesianVelocities], None]) -> None: ...
    @property
    def reactions(self) -> typing.List[CartesianVelocityReaction]:
        """
        :type: typing.List[CartesianVelocityReaction]
        """
    pass
class CartesianVelocityReaction():
    def __init__(self, condition: typing.Union[Condition, bool], motion: CartesianVelocityMotion = None) -> None: ...
    def register_callback(self, callback: typing.Callable[[RobotState, float, float], None]) -> None: ...
    pass
class CartesianWaypoint():
    def __init__(self, robot_pose: typing.Union[RobotPose, Affine], reference_type: ReferenceType = ReferenceType.Absolute, relative_dynamics_factor: typing.Union[RelativeDynamicsFactor, float] = 1.0, minimum_time: typing.Optional[float] = None) -> None: ...
    @property
    def minimum_time(self) -> typing.Optional[float]:
        """
        :type: typing.Optional[float]
        """
    @property
    def reference_type(self) -> ReferenceType:
        """
        :type: ReferenceType
        """
    @property
    def relative_dynamics_factor(self) -> typing.Union[RelativeDynamicsFactor, float]:
        """
        :type: typing.Union[RelativeDynamicsFactor, float]
        """
    @property
    def target(self) -> typing.Union[RobotPose, Affine]:
        """
        :type: typing.Union[RobotPose, Affine]
        """
    pass
class CartesianWaypointMotion(CartesianPoseMotion):
    def __init__(self, waypoints: typing.List[CartesianWaypoint], frame: typing.Optional[Affine] = None, relative_dynamics_factor: typing.Union[RelativeDynamicsFactor, float] = 1.0, return_when_finished: bool = True) -> None: ...
    pass
class CommandException(Exception, BaseException):
    pass
class Condition():
    @typing.overload
    def __and__(self, arg0: typing.Union[Condition, bool]) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __and__(self, arg0: bool) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __eq__(self, arg0: typing.Union[Condition, bool]) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __eq__(self, arg0: bool) -> typing.Union[Condition, bool]: ...
    def __init__(self, constant_value: bool) -> None: ...
    def __invert__(self) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __ne__(self, arg0: typing.Union[Condition, bool]) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __ne__(self, arg0: bool) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __or__(self, arg0: typing.Union[Condition, bool]) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __or__(self, arg0: bool) -> typing.Union[Condition, bool]: ...
    def __rand__(self, arg0: typing.Union[Condition, bool]) -> typing.Union[Condition, bool]: ...
    def __repr__(self) -> str: ...
    def __ror__(self, arg0: typing.Union[Condition, bool]) -> typing.Union[Condition, bool]: ...
    __hash__ = None
    pass
class ControlException(Exception, BaseException):
    pass
class ControlSignalType():
    """
    Members:

      Torques

      JointVelocities

      JointPositions

      CartesianVelocities

      CartesianPose
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    CartesianPose: _franky.ControlSignalType # value = <ControlSignalType.CartesianPose: 4>
    CartesianVelocities: _franky.ControlSignalType # value = <ControlSignalType.CartesianVelocities: 3>
    JointPositions: _franky.ControlSignalType # value = <ControlSignalType.JointPositions: 2>
    JointVelocities: _franky.ControlSignalType # value = <ControlSignalType.JointVelocities: 1>
    Torques: _franky.ControlSignalType # value = <ControlSignalType.Torques: 0>
    __members__: dict # value = {'Torques': <ControlSignalType.Torques: 0>, 'JointVelocities': <ControlSignalType.JointVelocities: 1>, 'JointPositions': <ControlSignalType.JointPositions: 2>, 'CartesianVelocities': <ControlSignalType.CartesianVelocities: 3>, 'CartesianPose': <ControlSignalType.CartesianPose: 4>}
    pass
class ControllerMode():
    """
    Members:

      JointImpedance

      CartesianImpedance
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    CartesianImpedance: _franky.ControllerMode # value = <ControllerMode.CartesianImpedance: 1>
    JointImpedance: _franky.ControllerMode # value = <ControllerMode.JointImpedance: 0>
    __members__: dict # value = {'JointImpedance': <ControllerMode.JointImpedance: 0>, 'CartesianImpedance': <ControllerMode.CartesianImpedance: 1>}
    pass
class Duration():
    def __add__(self, arg0: Duration) -> Duration: ...
    def __iadd__(self, arg0: Duration) -> Duration: ...
    def __imul__(self, arg0: int) -> Duration: ...
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: int) -> None: ...
    def __isub__(self, arg0: Duration) -> Duration: ...
    def __itruediv__(self, arg0: int) -> Duration: ...
    def __mul__(self, arg0: int) -> Duration: ...
    def __sub__(self, arg0: Duration) -> Duration: ...
    def __truediv__(self, arg0: int) -> Duration: ...
    def to_msec(self) -> int: ...
    def to_sec(self) -> float: ...
    pass
class Errors():
    def __init__(self) -> None: ...
    @property
    def cartesian_motion_generator_acceleration_discontinuity(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_motion_generator_elbow_limit_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_motion_generator_elbow_sign_inconsistent(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_motion_generator_joint_acceleration_discontinuity(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_motion_generator_joint_position_limits_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_motion_generator_joint_velocity_discontinuity(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_motion_generator_joint_velocity_limits_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_motion_generator_start_elbow_invalid(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_motion_generator_velocity_discontinuity(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_motion_generator_velocity_limits_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_position_limits_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_position_motion_generator_invalid_frame(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_position_motion_generator_start_pose_invalid(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_reflex(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_velocity_profile_safety_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def cartesian_velocity_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def communication_constraints_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def controller_torque_discontinuity(self) -> bool:
        """
        :type: bool
        """
    @property
    def force_control_safety_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def force_controller_desired_force_tolerance_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def instability_detected(self) -> bool:
        """
        :type: bool
        """
    @property
    def joint_motion_generator_acceleration_discontinuity(self) -> bool:
        """
        :type: bool
        """
    @property
    def joint_motion_generator_position_limits_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def joint_motion_generator_velocity_discontinuity(self) -> bool:
        """
        :type: bool
        """
    @property
    def joint_motion_generator_velocity_limits_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def joint_move_in_wrong_direction(self) -> bool:
        """
        :type: bool
        """
    @property
    def joint_p2p_insufficient_torque_for_planning(self) -> bool:
        """
        :type: bool
        """
    @property
    def joint_position_limits_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def joint_position_motion_generator_start_pose_invalid(self) -> bool:
        """
        :type: bool
        """
    @property
    def joint_reflex(self) -> bool:
        """
        :type: bool
        """
    @property
    def joint_velocity_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def max_goal_pose_deviation_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def max_path_pose_deviation_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def power_limit_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def self_collision_avoidance_violation(self) -> bool:
        """
        :type: bool
        """
    @property
    def start_elbow_sign_inconsistent(self) -> bool:
        """
        :type: bool
        """
    @property
    def tau_j_range_violation(self) -> bool:
        """
        :type: bool
        """
    pass
class TorqueMotion():
    def add_reaction(self, arg0: TorqueReaction) -> None: ...
    def register_callback(self, callback: typing.Callable[[RobotState, Duration, float, float, Torques], None]) -> None: ...
    @property
    def reactions(self) -> typing.List[TorqueReaction]:
        """
        :type: typing.List[TorqueReaction]
        """
    pass
class GripperException(Exception, BaseException):
    pass
class GripperInternal():
    def __init__(self, fci_hostname: str, speed: float = 0.02, force: float = 20.0) -> None: ...
    @typing.overload
    def clamp(self) -> bool: ...
    @typing.overload
    def clamp(self, arg0: float) -> bool: ...
    def get_state(self) -> GripperState: ...
    def grasp(self, arg0: float, arg1: float, arg2: float, arg3: float, arg4: float) -> bool: ...
    def homing(self) -> bool: ...
    def is_grasping(self) -> bool: ...
    @typing.overload
    def move(self, arg0: float, arg1: float) -> bool: ...
    @typing.overload
    def move(self, arg0: float) -> bool: ...
    def move_unsafe(self, arg0: float) -> bool: ...
    def open(self) -> bool: ...
    def read_once(self) -> GripperState: ...
    @typing.overload
    def release(self) -> bool: ...
    @typing.overload
    def release(self, arg0: float) -> bool: ...
    def releaseRelative(self, arg0: float) -> bool: ...
    def stop(self) -> bool: ...
    def width(self) -> float: ...
    @property
    def gripper_force(self) -> float:
        """
        :type: float
        """
    @gripper_force.setter
    def gripper_force(self, arg0: float) -> None:
        pass
    @property
    def gripper_speed(self) -> float:
        """
        :type: float
        """
    @gripper_speed.setter
    def gripper_speed(self, arg0: float) -> None:
        pass
    @property
    def has_error(self) -> bool:
        """
        :type: bool
        """
    @property
    def max_width(self) -> float:
        """
        :type: float
        """
    @property
    def server_version(self) -> int:
        """
        :type: int
        """
    pass
class GripperState():
    @property
    def is_grasped(self) -> bool:
        """
        :type: bool
        """
    @property
    def max_width(self) -> float:
        """
        :type: float
        """
    @property
    def temperature(self) -> int:
        """
        :type: int
        """
    @property
    def time(self) -> Duration:
        """
        :type: Duration
        """
    @property
    def width(self) -> float:
        """
        :type: float
        """
    pass
class ImpedanceMotion(TorqueMotion):
    pass
class IncompatibleVersionException(Exception, BaseException):
    pass
class InvalidMotionTypeException(Exception, BaseException):
    pass
class InvalidOperationException(Exception, BaseException):
    pass
class JointPositionMotion():
    def add_reaction(self, arg0: JointPositionReaction) -> None: ...
    def register_callback(self, callback: typing.Callable[[RobotState, Duration, float, float, JointPositions], None]) -> None: ...
    @property
    def reactions(self) -> typing.List[JointPositionReaction]:
        """
        :type: typing.List[JointPositionReaction]
        """
    pass
class JointPositionReaction():
    def __init__(self, condition: typing.Union[Condition, bool], motion: JointPositionMotion = None) -> None: ...
    def register_callback(self, callback: typing.Callable[[RobotState, float, float], None]) -> None: ...
    pass
class JointPositionStopMotion(JointPositionMotion):
    def __init__(self) -> None: ...
    pass
class JointPositions():
    @property
    def q(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    pass
class JointVelocities():
    @property
    def dq(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    pass
class JointVelocityMotion():
    def add_reaction(self, arg0: JointVelocityReaction) -> None: ...
    def register_callback(self, callback: typing.Callable[[RobotState, Duration, float, float, JointVelocities], None]) -> None: ...
    @property
    def reactions(self) -> typing.List[JointVelocityReaction]:
        """
        :type: typing.List[JointVelocityReaction]
        """
    pass
class JointVelocityReaction():
    def __init__(self, condition: typing.Union[Condition, bool], motion: JointVelocityMotion = None) -> None: ...
    def register_callback(self, callback: typing.Callable[[RobotState, float, float], None]) -> None: ...
    pass
class JointWaypoint():
    def __init__(self, target: numpy.ndarray[numpy.float64, _Shape[7, 1]], reference_type: ReferenceType = ReferenceType.Absolute, relative_dynamics_factor: typing.Union[RelativeDynamicsFactor, float] = 1.0, minimum_time: typing.Optional[float] = None) -> None: ...
    @property
    def minimum_time(self) -> typing.Optional[float]:
        """
        :type: typing.Optional[float]
        """
    @property
    def reference_type(self) -> ReferenceType:
        """
        :type: ReferenceType
        """
    @property
    def relative_dynamics_factor(self) -> typing.Union[RelativeDynamicsFactor, float]:
        """
        :type: typing.Union[RelativeDynamicsFactor, float]
        """
    @property
    def target(self) -> numpy.ndarray[numpy.float64, _Shape[7, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[7, 1]]
        """
    pass
class JointWaypointMotion(JointPositionMotion):
    def __init__(self, waypoints: typing.List[JointWaypoint], relative_dynamics_factor: typing.Union[RelativeDynamicsFactor, float] = 1.0, return_when_finished: bool = True) -> None: ...
    pass
class Kinematics():
    @staticmethod
    def forward(q: numpy.ndarray[numpy.float64, _Shape[7, 1]]) -> Affine: ...
    @staticmethod
    def forward_elbow(q: numpy.ndarray[numpy.float64, _Shape[7, 1]]) -> Affine: ...
    @staticmethod
    def forward_euler(q: numpy.ndarray[numpy.float64, _Shape[7, 1]]) -> numpy.ndarray[numpy.float64, _Shape[6, 1]]: ...
    @staticmethod
    def inverse(target: numpy.ndarray[numpy.float64, _Shape[6, 1]], q0: numpy.ndarray[numpy.float64, _Shape[7, 1]], null_space: typing.Optional[NullSpaceHandling] = None) -> numpy.ndarray[numpy.float64, _Shape[7, 1]]: ...
    @staticmethod
    def jacobian(q: numpy.ndarray[numpy.float64, _Shape[7, 1]]) -> numpy.ndarray[numpy.float64, _Shape[6, 7]]: ...
    pass
class LinearImpedanceMotion(ImpedanceMotion, TorqueMotion):
    def __init__(self, target: Affine, duration: float, target_type: ReferenceType = ReferenceType.Absolute, translational_stiffness: float = 2000, rotational_stiffness: float = 200, force_constraints: typing.Optional[typing.List[typing.Optional[float][6]]] = None, return_when_finished: bool = True, finish_wait_factor: float = 1.2) -> None: ...
    pass
class LinearMotion(CartesianWaypointMotion, CartesianPoseMotion):
    def __init__(self, target: typing.Union[RobotPose, Affine], reference_type: ReferenceType = ReferenceType.Absolute, frame: typing.Optional[Affine] = None, relative_dynamics_factor: typing.Union[RelativeDynamicsFactor, float] = 1.0, return_when_finished: bool = True) -> None: ...
    pass
class Measure():
    @typing.overload
    def __add__(self, arg0: Measure) -> Measure: ...
    @typing.overload
    def __add__(self, arg0: float) -> Measure: ...
    @typing.overload
    def __eq__(self, arg0: Measure) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __eq__(self, arg0: float) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __ge__(self, arg0: Measure) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __ge__(self, arg0: float) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __gt__(self, arg0: Measure) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __gt__(self, arg0: float) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __le__(self, arg0: Measure) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __le__(self, arg0: float) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __lt__(self, arg0: Measure) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __lt__(self, arg0: float) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __mul__(self, arg0: Measure) -> Measure: ...
    @typing.overload
    def __mul__(self, arg0: float) -> Measure: ...
    @typing.overload
    def __ne__(self, arg0: Measure) -> typing.Union[Condition, bool]: ...
    @typing.overload
    def __ne__(self, arg0: float) -> typing.Union[Condition, bool]: ...
    def __neg__(self) -> Measure: ...
    @typing.overload
    def __pow__(self, arg0: Measure) -> Measure: ...
    @typing.overload
    def __pow__(self, arg0: float) -> Measure: ...
    def __radd__(self, arg0: float) -> Measure: ...
    def __repr__(self) -> str: ...
    def __rmul__(self, arg0: float) -> Measure: ...
    def __rpow__(self, arg0: float) -> Measure: ...
    def __rsub__(self, arg0: float) -> Measure: ...
    def __rtruediv__(self, arg0: float) -> Measure: ...
    @typing.overload
    def __sub__(self, arg0: Measure) -> Measure: ...
    @typing.overload
    def __sub__(self, arg0: float) -> Measure: ...
    @typing.overload
    def __truediv__(self, arg0: Measure) -> Measure: ...
    @typing.overload
    def __truediv__(self, arg0: float) -> Measure: ...
    ABS_TIME: _franky.Measure # value = t
    FORCE_X: _franky.Measure # value = F_x
    FORCE_Y: _franky.Measure # value = F_y
    FORCE_Z: _franky.Measure # value = F_z
    REL_TIME: _franky.Measure # value = t
    __hash__ = None
    pass
class ModelException(Exception, BaseException):
    pass
class NetworkException(Exception, BaseException):
    pass
class NullSpaceHandling():
    def __init__(self, joint_index: int, value: float) -> None: ...
    @property
    def joint_index(self) -> int:
        """
        :type: int
        """
    @joint_index.setter
    def joint_index(self, arg0: int) -> None:
        pass
    @property
    def value(self) -> float:
        """
        :type: float
        """
    @value.setter
    def value(self, arg0: float) -> None:
        pass
    pass
class ProtocolException(Exception, BaseException):
    pass
class ReactionRecursionException(Exception, BaseException):
    pass
class RealtimeConfig():
    """
    Members:

      Enforce

      Ignore
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    Enforce: _franky.RealtimeConfig # value = <RealtimeConfig.Enforce: 0>
    Ignore: _franky.RealtimeConfig # value = <RealtimeConfig.Ignore: 1>
    __members__: dict # value = {'Enforce': <RealtimeConfig.Enforce: 0>, 'Ignore': <RealtimeConfig.Ignore: 1>}
    pass
class RealtimeException(Exception, BaseException):
    pass
class ReferenceType():
    """
    Members:

      Relative

      Absolute
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    Absolute: _franky.ReferenceType # value = <ReferenceType.Absolute: 0>
    Relative: _franky.ReferenceType # value = <ReferenceType.Relative: 1>
    __members__: dict # value = {'Relative': <ReferenceType.Relative: 1>, 'Absolute': <ReferenceType.Absolute: 0>}
    pass
class RelativeDynamicsFactor():
    @typing.overload
    def __init__(self) -> None: ...
    @typing.overload
    def __init__(self, arg0: float) -> None: ...
    @typing.overload
    def __init__(self, arg0: float, arg1: float, arg2: float) -> None: ...
    def __mul__(self, arg0: typing.Union[RelativeDynamicsFactor, float]) -> typing.Union[RelativeDynamicsFactor, float]: ...
    @property
    def acceleration(self) -> float:
        """
        :type: float
        """
    @property
    def jerk(self) -> float:
        """
        :type: float
        """
    @property
    def max_dynamics(self) -> bool:
        """
        :type: bool
        """
    @property
    def velocity(self) -> float:
        """
        :type: float
        """
    MAX_DYNAMICS: _franky.RelativeDynamicsFactor
    pass
class RobotInternal():
    def __init__(self, fci_hostname: str, relative_dynamics_factor: typing.Union[RelativeDynamicsFactor, float] = 1.0, default_torque_threshold: float = 20.0, default_force_threshold: float = 30.0, controller_mode: ControllerMode = ControllerMode.JointImpedance, realtime_config: RealtimeConfig = RealtimeConfig.Enforce) -> None: ...
    @staticmethod
    def forward_kinematics(q: numpy.ndarray[numpy.float64, _Shape[7, 1]]) -> Affine: ...
    @staticmethod
    def inverseKinematics(target: Affine, q0: numpy.ndarray[numpy.float64, _Shape[7, 1]]) -> numpy.ndarray[numpy.float64, _Shape[7, 1]]: ...
    def join_motion(self) -> None: ...
    @typing.overload
    def move(self, motion: CartesianPoseMotion, asynchronous: bool = False) -> None: ...
    @typing.overload
    def move(self, motion: CartesianVelocityMotion, asynchronous: bool = False) -> None: ...
    @typing.overload
    def move(self, motion: JointPositionMotion, asynchronous: bool = False) -> None: ...
    @typing.overload
    def move(self, motion: JointVelocityMotion, asynchronous: bool = False) -> None: ...
    @typing.overload
    def move(self, motion: TorqueMotion, asynchronous: bool = False) -> None: ...
    def recover_from_errors(self) -> bool: ...
    def set_cartesian_impedance(self, K_x: typing.List[float[6]]) -> None: ...
    @typing.overload
    def set_collision_behavior(self, torque_thresholds: typing.Union[float, typing.List[float[7]], numpy.ndarray[numpy.float64, _Shape[7, 1]]], force_thresholds: typing.Union[float, typing.List[float[6]], numpy.ndarray[numpy.float64, _Shape[6, 1]]]) -> None: ...
    @typing.overload
    def set_collision_behavior(self, lower_torque_threshold: typing.Union[float, typing.List[float[7]], numpy.ndarray[numpy.float64, _Shape[7, 1]]], upper_torque_threshold: typing.Union[float, typing.List[float[7]], numpy.ndarray[numpy.float64, _Shape[7, 1]]], lower_force_threshold: typing.Union[float, typing.List[float[6]], numpy.ndarray[numpy.float64, _Shape[6, 1]]], upper_force_threshold: typing.Union[float, typing.List[float[6]], numpy.ndarray[numpy.float64, _Shape[6, 1]]]) -> None: ...
    @typing.overload
    def set_collision_behavior(self, lower_torque_threshold_acceleration: typing.Union[float, typing.List[float[7]], numpy.ndarray[numpy.float64, _Shape[7, 1]]], upper_torque_threshold_acceleration: typing.Union[float, typing.List[float[7]], numpy.ndarray[numpy.float64, _Shape[7, 1]]], lower_torque_threshold_nominal: typing.Union[float, typing.List[float[7]], numpy.ndarray[numpy.float64, _Shape[7, 1]]], upper_torque_threshold_nominal: typing.Union[float, typing.List[float[7]], numpy.ndarray[numpy.float64, _Shape[7, 1]]], lower_force_threshold_acceleration: typing.Union[float, typing.List[float[6]], numpy.ndarray[numpy.float64, _Shape[6, 1]]], upper_force_threshold_acceleration: typing.Union[float, typing.List[float[6]], numpy.ndarray[numpy.float64, _Shape[6, 1]]], lower_force_threshold_nominal: typing.Union[float, typing.List[float[6]], numpy.ndarray[numpy.float64, _Shape[6, 1]]], upper_force_threshold_nominal: typing.Union[float, typing.List[float[6]], numpy.ndarray[numpy.float64, _Shape[6, 1]]]) -> None: ...
    def set_ee(self, NE_T_EE: typing.List[float[16]]) -> None: ...
    def set_guiding_mode(self, guiding_mode: typing.List[bool[6]], elbow: bool) -> None: ...
    def set_joint_impedance(self, K_theta: typing.List[float[7]]) -> None: ...
    def set_k(self, EE_T_K: typing.List[float[16]]) -> None: ...
    def set_load(self, load_mass: float, F_x_Cload: typing.List[float[3]], load_inertia: typing.List[float[9]]) -> None: ...
    def stop(self) -> None: ...
    @property
    def current_control_signal_type(self) -> typing.Optional[ControlSignalType]:
        """
        :type: typing.Optional[ControlSignalType]
        """
    @property
    def current_joint_positions(self) -> numpy.ndarray[numpy.float64, _Shape[7, 1]]:
        """
        :type: numpy.ndarray[numpy.float64, _Shape[7, 1]]
        """
    @property
    def current_pose(self) -> typing.Union[RobotPose, Affine]:
        """
        :type: typing.Union[RobotPose, Affine]
        """
    @property
    def fci_hostname(self) -> str:
        """
        :type: str
        """
    @property
    def has_errors(self) -> bool:
        """
        :type: bool
        """
    @property
    def is_in_control(self) -> bool:
        """
        :type: bool
        """
    @property
    def relative_dynamics_factor(self) -> typing.Union[RelativeDynamicsFactor, float]:
        """
        :type: typing.Union[RelativeDynamicsFactor, float]
        """
    @relative_dynamics_factor.setter
    def relative_dynamics_factor(self, arg1: typing.Union[RelativeDynamicsFactor, float]) -> None:
        pass
    @property
    def state(self) -> RobotState:
        """
        :type: RobotState
        """
    control_rate = 0.001
    degrees_of_freedom = 7
    max_elbow_acceleration = 10.0
    max_elbow_jerk = 5000.0
    max_elbow_velocity = 2.175
    max_joint_acceleration: numpy.ndarray # value = array([15. ,  7.5, 10. , 12.5, 15. , 20. , 20. ])
    max_joint_jerk: numpy.ndarray # value = array([ 7500.,  3750.,  5000.,  6250.,  7500., 10000., 10000.])
    max_joint_velocity: numpy.ndarray # value = array([2.175, 2.175, 2.175, 2.175, 2.61 , 2.61 , 2.61 ])
    max_rotation_acceleration = 25.0
    max_rotation_jerk = 12500.0
    max_rotation_velocity = 2.5
    max_translation_acceleration = 13.0
    max_translation_jerk = 6500.0
    max_translation_velocity = 1.7
    pass
class RobotMode():
    """
    Members:

      Other

      Idle

      Move

      Guiding

      Reflex

      UserStopped

      AutomaticErrorRecovery
    """
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> None: ...
    @property
    def name(self) -> str:
        """
        :type: str
        """
    @property
    def value(self) -> int:
        """
        :type: int
        """
    AutomaticErrorRecovery: _franky.RobotMode # value = <RobotMode.AutomaticErrorRecovery: 6>
    Guiding: _franky.RobotMode # value = <RobotMode.Guiding: 3>
    Idle: _franky.RobotMode # value = <RobotMode.Idle: 1>
    Move: _franky.RobotMode # value = <RobotMode.Move: 2>
    Other: _franky.RobotMode # value = <RobotMode.Other: 0>
    Reflex: _franky.RobotMode # value = <RobotMode.Reflex: 4>
    UserStopped: _franky.RobotMode # value = <RobotMode.UserStopped: 5>
    __members__: dict # value = {'Other': <RobotMode.Other: 0>, 'Idle': <RobotMode.Idle: 1>, 'Move': <RobotMode.Move: 2>, 'Guiding': <RobotMode.Guiding: 3>, 'Reflex': <RobotMode.Reflex: 4>, 'UserStopped': <RobotMode.UserStopped: 5>, 'AutomaticErrorRecovery': <RobotMode.AutomaticErrorRecovery: 6>}
    pass
class RobotPose():
    @typing.overload
    def __init__(self, end_effector_pose: Affine, elbow_position: typing.Optional[float] = None) -> None: ...
    @typing.overload
    def __init__(self, arg0: typing.Union[RobotPose, Affine]) -> None: ...
    def __mul__(self, arg0: Affine) -> typing.Union[RobotPose, Affine]: ...
    def __repr__(self) -> str: ...
    def __rmul__(self, arg0: Affine) -> typing.Union[RobotPose, Affine]: ...
    def with_elbow_position(self, elbow_position: typing.Optional[float]) -> typing.Union[RobotPose, Affine]: ...
    @property
    def elbow_position(self) -> typing.Optional[float]:
        """
        :type: typing.Optional[float]
        """
    @property
    def end_effector_pose(self) -> Affine:
        """
        :type: Affine
        """
    pass
class RobotState():
    @property
    def EE_T_K(self) -> typing.List[float[16]]:
        """
        :type: typing.List[float[16]]
        """
    @property
    def F_T_EE(self) -> typing.List[float[16]]:
        """
        :type: typing.List[float[16]]
        """
    @property
    def F_x_Cee(self) -> typing.List[float[3]]:
        """
        :type: typing.List[float[3]]
        """
    @property
    def F_x_Cload(self) -> typing.List[float[3]]:
        """
        :type: typing.List[float[3]]
        """
    @property
    def F_x_Ctotal(self) -> typing.List[float[3]]:
        """
        :type: typing.List[float[3]]
        """
    @property
    def I_ee(self) -> typing.List[float[9]]:
        """
        :type: typing.List[float[9]]
        """
    @property
    def I_load(self) -> typing.List[float[9]]:
        """
        :type: typing.List[float[9]]
        """
    @property
    def I_total(self) -> typing.List[float[9]]:
        """
        :type: typing.List[float[9]]
        """
    @property
    def K_F_ext_hat_K(self) -> typing.List[float[6]]:
        """
        :type: typing.List[float[6]]
        """
    @property
    def O_F_ext_hat_K(self) -> typing.List[float[6]]:
        """
        :type: typing.List[float[6]]
        """
    @property
    def O_T_EE(self) -> typing.List[float[16]]:
        """
        :type: typing.List[float[16]]
        """
    @property
    def O_T_EE_c(self) -> typing.List[float[16]]:
        """
        :type: typing.List[float[16]]
        """
    @property
    def O_T_EE_d(self) -> typing.List[float[16]]:
        """
        :type: typing.List[float[16]]
        """
    @property
    def O_dP_EE_c(self) -> typing.List[float[6]]:
        """
        :type: typing.List[float[6]]
        """
    @property
    def O_ddP_EE_c(self) -> typing.List[float[6]]:
        """
        :type: typing.List[float[6]]
        """
    @property
    def cartesian_collision(self) -> typing.List[float[6]]:
        """
        :type: typing.List[float[6]]
        """
    @property
    def cartesian_contact(self) -> typing.List[float[6]]:
        """
        :type: typing.List[float[6]]
        """
    @property
    def control_command_success_rate(self) -> float:
        """
        :type: float
        """
    @property
    def current_errors(self) -> Errors:
        """
        :type: Errors
        """
    @property
    def ddelbow_c(self) -> typing.List[float[2]]:
        """
        :type: typing.List[float[2]]
        """
    @property
    def ddq_d(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    @property
    def delbow_c(self) -> typing.List[float[2]]:
        """
        :type: typing.List[float[2]]
        """
    @property
    def dq(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    @property
    def dq_d(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    @property
    def dtau_J(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    @property
    def dtheta(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    @property
    def elbow(self) -> typing.List[float[2]]:
        """
        :type: typing.List[float[2]]
        """
    @property
    def elbow_c(self) -> typing.List[float[2]]:
        """
        :type: typing.List[float[2]]
        """
    @property
    def elbow_d(self) -> typing.List[float[2]]:
        """
        :type: typing.List[float[2]]
        """
    @property
    def joint_collision(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    @property
    def joint_contact(self) -> float:
        """
        :type: float
        """
    @property
    def last_motion_errors(self) -> Errors:
        """
        :type: Errors
        """
    @property
    def m_ee(self) -> float:
        """
        :type: float
        """
    @property
    def m_load(self) -> float:
        """
        :type: float
        """
    @property
    def m_total(self) -> float:
        """
        :type: float
        """
    @property
    def q(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    @property
    def q_d(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    @property
    def robot_mode(self) -> RobotMode:
        """
        :type: RobotMode
        """
    @property
    def tau_J(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    @property
    def tau_J_d(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    @property
    def tau_ext_hat_filtered(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    @property
    def theta(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    @property
    def time(self) -> Duration:
        """
        :type: Duration
        """
    pass
class ExponentialImpedanceMotion(ImpedanceMotion, TorqueMotion):
    def __init__(self, target: Affine, target_type: ReferenceType = ReferenceType.Absolute, translational_stiffness: float = 2000, rotational_stiffness: float = 200, force_constraints: typing.Optional[typing.List[typing.Optional[float][6]]] = None, exponential_decay: float = 0.005) -> None: ...
    pass
class TorqueReaction():
    def __init__(self, condition: typing.Union[Condition, bool], motion: TorqueMotion = None) -> None: ...
    def register_callback(self, callback: typing.Callable[[RobotState, float, float], None]) -> None: ...
    pass
class Torques():
    @property
    def tau_J(self) -> typing.List[float[7]]:
        """
        :type: typing.List[float[7]]
        """
    pass
