# -*- coding: utf-8 -*-
from __future__ import print_function

import os
import stat
import sys

# find the import for catkin's python package - either from source space or from an installed underlay
if os.path.exists(os.path.join('/opt/ros/noetic/share/catkin/cmake', 'catkinConfig.cmake.in')):
    sys.path.insert(0, os.path.join('/opt/ros/noetic/share/catkin/cmake', '..', 'python'))
try:
    from catkin.environment_cache import generate_environment_script
except ImportError:
    # search for catkin package in all workspaces and prepend to path
    for workspace in '/root/tb2_ws/devel_isolated/yujin_ocs;/root/tb2_ws/devel_isolated/yocs_waypoints_navi;/root/tb2_ws/devel_isolated/yocs_waypoint_provider;/root/tb2_ws/devel_isolated/yocs_virtual_sensor;/root/tb2_ws/devel_isolated/kobuki_qtestsuite;/root/tb2_ws/devel_isolated/kobuki_testsuite;/root/tb2_ws/devel_isolated/kobuki_node;/root/tb2_ws/devel_isolated/yocs_velocity_smoother;/root/tb2_ws/devel_isolated/yocs_safety_controller;/root/tb2_ws/devel_isolated/yocs_rapps;/root/tb2_ws/devel_isolated/yocs_navigator;/root/tb2_ws/devel_isolated/yocs_navi_toolkit;/root/tb2_ws/devel_isolated/yocs_joyop;/root/tb2_ws/devel_isolated/yocs_ar_pair_tracking;/root/tb2_ws/devel_isolated/yocs_msgs;/root/tb2_ws/devel_isolated/yocs_diff_drive_pose_controller;/root/tb2_ws/devel_isolated/yocs_ar_marker_tracking;/root/tb2_ws/devel_isolated/yocs_math_toolkit;/root/tb2_ws/devel_isolated/yocs_localization_manager;/root/tb2_ws/devel_isolated/yocs_keyop;/root/tb2_ws/devel_isolated/kobuki_safety_controller;/root/tb2_ws/devel_isolated/kobuki_random_walker;/root/tb2_ws/devel_isolated/kobuki_controller_tutorial;/root/tb2_ws/devel_isolated/yocs_controllers;/root/tb2_ws/devel_isolated/yocs_cmd_vel_mux;/root/tb2_ws/devel_isolated/yocs_ar_pair_approach;/root/tb2_ws/devel_isolated/turtlebot_teleop;/root/tb2_ws/devel_isolated/turtlebot_stdr;/root/tb2_ws/devel_isolated/turtlebot_stage;/root/tb2_ws/devel_isolated/turtlebot_simulator;/root/tb2_ws/devel_isolated/turtlebot_rviz_launchers;/root/tb2_ws/devel_isolated/turtlebot_rapps;/root/tb2_ws/devel_isolated/turtlebot_navigation;/root/tb2_ws/devel_isolated/turtlebot_follower;/root/tb2_ws/devel_isolated/turtlebot_msgs;/root/tb2_ws/devel_isolated/turtlebot_interactive_markers;/root/tb2_ws/devel_isolated/turtlebot_interactions;/root/tb2_ws/devel_isolated/turtlebot_gazebo;/root/tb2_ws/devel_isolated/turtlebot_description;/root/tb2_ws/devel_isolated/turtlebot_dashboard;/root/tb2_ws/devel_isolated/turtlebot_capabilities;/root/tb2_ws/devel_isolated/turtlebot_calibration;/root/tb2_ws/devel_isolated/turtlebot_bringup;/root/tb2_ws/devel_isolated/turtlebot_apps;/root/tb2_ws/devel_isolated/turtlebot_actions;/root/tb2_ws/devel_isolated/turtlebot;/root/tb2_ws/devel_isolated/kobuki_driver;/root/tb2_ws/devel_isolated/kobuki_auto_docking;/root/tb2_ws/devel_isolated/kobuki_dock_drive;/root/tb2_ws/devel_isolated/ecl_statistics;/root/tb2_ws/devel_isolated/ecl_mobile_robot;/root/tb2_ws/devel_isolated/ecl_core_apps;/root/tb2_ws/devel_isolated/ecl_geometry;/root/tb2_ws/devel_isolated/ecl_linear_algebra;/root/tb2_ws/devel_isolated/slam_gmapping;/root/tb2_ws/devel_isolated/kobuki_rviz_launchers;/root/tb2_ws/devel_isolated/kobuki_rapps;/root/tb2_ws/devel_isolated/kobuki_keyop;/root/tb2_ws/devel_isolated/kobuki_gazebo_plugins;/root/tb2_ws/devel_isolated/kobuki_dashboard;/root/tb2_ws/devel_isolated/kobuki_bumper2pc;/root/tb2_ws/devel_isolated/kobuki_msgs;/root/tb2_ws/devel_isolated/kobuki_gazebo;/root/tb2_ws/devel_isolated/kobuki_ftdi;/root/tb2_ws/devel_isolated/kobuki_desktop;/root/tb2_ws/devel_isolated/kobuki_description;/root/tb2_ws/devel_isolated/kobuki_core;/root/tb2_ws/devel_isolated/kobuki_capabilities;/root/tb2_ws/devel_isolated/kobuki;/root/tb2_ws/devel_isolated/gmapping;/root/tb2_ws/devel_isolated/ecl_streams;/root/tb2_ws/devel_isolated/ecl_sigslots;/root/tb2_ws/devel_isolated/ecl_devices;/root/tb2_ws/devel_isolated/ecl_threads;/root/tb2_ws/devel_isolated/ecl_containers;/root/tb2_ws/devel_isolated/ecl_utilities;/root/tb2_ws/devel_isolated/ecl_math;/root/tb2_ws/devel_isolated/ecl_formatters;/root/tb2_ws/devel_isolated/ecl_converters;/root/tb2_ws/devel_isolated/ecl_concepts;/root/tb2_ws/devel_isolated/ecl_type_traits;/root/tb2_ws/devel_isolated/ecl_tools;/root/tb2_ws/devel_isolated/ecl_ipc;/root/tb2_ws/devel_isolated/ecl_time;/root/tb2_ws/devel_isolated/ecl_time_lite;/root/tb2_ws/devel_isolated/ecl_sigslots_lite;/root/tb2_ws/devel_isolated/ecl_navigation;/root/tb2_ws/devel_isolated/ecl_mpl;/root/tb2_ws/devel_isolated/ecl_lite;/root/tb2_ws/devel_isolated/ecl_io;/root/tb2_ws/devel_isolated/ecl_filesystem;/root/tb2_ws/devel_isolated/ecl_exceptions;/root/tb2_ws/devel_isolated/ecl_errors;/root/tb2_ws/devel_isolated/ecl_eigen;/root/tb2_ws/devel_isolated/ecl_converters_lite;/root/tb2_ws/devel_isolated/ecl_console;/root/tb2_ws/devel_isolated/ecl_config;/root/tb2_ws/devel_isolated/ecl_command_line;/root/tb2_ws/devel_isolated/ecl_build;/root/tb2_ws/devel_isolated/ecl_license;/root/tb2_ws/devel_isolated/ecl_core;/root/tb2_ws/devel_isolated/depthimage_to_laserscan;/root/tb2_ws/devel_isolated/ddynamic_reconfigure;/root/tb2_ws/devel_isolated/ar_track_alvar_msgs;/opt/ros/noetic'.split(';'):
        python_path = os.path.join(workspace, 'lib/python3/dist-packages')
        if os.path.isdir(os.path.join(python_path, 'catkin')):
            sys.path.insert(0, python_path)
            break
    from catkin.environment_cache import generate_environment_script

code = generate_environment_script('/home/pablocano/Proyecto-moviles/catkin_ws/devel_isolated/TurtleMadero/env.sh')

output_filename = '/home/pablocano/Proyecto-moviles/catkin_ws/build_isolated/TurtleMadero/catkin_generated/setup_cached.sh'
with open(output_filename, 'w') as f:
    # print('Generate script for cached setup "%s"' % output_filename)
    f.write('\n'.join(code))

mode = os.stat(output_filename).st_mode
os.chmod(output_filename, mode | stat.S_IXUSR)
