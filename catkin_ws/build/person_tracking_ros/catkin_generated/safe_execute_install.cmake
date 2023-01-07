execute_process(COMMAND "/home/pablocano/Proyecto-moviles/catkin_ws/build/person_tracking_ros/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/pablocano/Proyecto-moviles/catkin_ws/build/person_tracking_ros/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
