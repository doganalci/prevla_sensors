# Install script for directory: /home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/leap_motion/msg" TYPE FILE FILES
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/msg/Arm.msg"
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/msg/Bone.msg"
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/msg/Finger.msg"
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/msg/Gesture.msg"
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/msg/Hand.msg"
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/msg/Human.msg"
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/msg/leap.msg"
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/msg/leapros.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/leap_motion/cmake" TYPE FILE FILES "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/build/leap_motion/catkin_generated/installspace/leap_motion-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/devel/include/leap_motion")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/devel/share/roseus/ros/leap_motion")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/devel/share/common-lisp/ros/leap_motion")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/devel/share/gennodejs/ros/leap_motion")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python2" -m compileall "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/devel/lib/python2.7/dist-packages/leap_motion")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python2.7/dist-packages" TYPE DIRECTORY FILES "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/devel/lib/python2.7/dist-packages/leap_motion")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/build/leap_motion/catkin_generated/installspace/leap_motion.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/leap_motion/cmake" TYPE FILE FILES "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/build/leap_motion/catkin_generated/installspace/leap_motion-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/leap_motion/cmake" TYPE FILE FILES
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/build/leap_motion/catkin_generated/installspace/leap_motionConfig.cmake"
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/build/leap_motion/catkin_generated/installspace/leap_motionConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/leap_motion" TYPE FILE FILES "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/leap_motion/leap_camera" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/leap_motion/leap_camera")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/leap_motion/leap_camera"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/leap_motion" TYPE EXECUTABLE FILES "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/devel/lib/leap_motion/leap_camera")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/leap_motion/leap_camera" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/leap_motion/leap_camera")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/leap_motion/leap_camera"
         OLD_RPATH "/opt/ros/melodic/lib:/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/LeapSDK/lib/x64:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/leap_motion/leap_camera")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/leap_motion/leap_hands" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/leap_motion/leap_hands")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/leap_motion/leap_hands"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/leap_motion" TYPE EXECUTABLE FILES "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/devel/lib/leap_motion/leap_hands")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/leap_motion/leap_hands" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/leap_motion/leap_hands")
    file(RPATH_CHANGE
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/leap_motion/leap_hands"
         OLD_RPATH "/opt/ros/melodic/lib:/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/LeapSDK/lib/x64:"
         NEW_RPATH "")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/lib/leap_motion/leap_hands")
    endif()
  endif()
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/leap_motion" TYPE PROGRAM FILES
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/scripts/leap_interface.py"
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/scripts/sender.py"
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/scripts/subscriber.py"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/leap_motion" TYPE DIRECTORY FILES
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/launch"
    "/home/inosens/Desktop/prevla_sensors/prevla_leap_doga/catkin_ws/src/leap_motion/config/camera_info"
    )
endif()

