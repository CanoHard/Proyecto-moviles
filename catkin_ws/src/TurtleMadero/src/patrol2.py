#!/usr/bin/env python

import rospy
import actionlib
from smach import State,StateMachine
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Float32MultiArray


ori = (0.0, 0.0, 0.0, 1.0)

waypoints = []
patrol = StateMachine('success')

class Waypoint(State):
    def __init__(self, position, orientation):
        State.__init__(self, outcomes=['success'])

        # Get an action client
        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.client.wait_for_server()

        # Define the goal
        self.goal = MoveBaseGoal()
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.pose.position.x = position[0]
        self.goal.target_pose.pose.position.y = position[1]
        self.goal.target_pose.pose.position.z = 0.0
        self.goal.target_pose.pose.orientation.x = orientation[0]
        self.goal.target_pose.pose.orientation.y = orientation[1]
        self.goal.target_pose.pose.orientation.z = orientation[2]
        self.goal.target_pose.pose.orientation.w = orientation[3]

    def execute(self, userdata):
        self.client.send_goal(self.goal)
        print ("Waypoints: ", waypoints)
        global recvy
        global recvx

        # if the result is not success, then return 'failure'
        while (self.client.get_result() is None):
            if recvy == True and recvx == True:
                return 'failure'
        return 'success'


recvx = False
recvy = False

def callbacky(data):
    # add data to waypoints
    global recvx
    global recvy

    if recvx == False:
        for dat in data.data:
            cord = (0, dat)
            point = [cord, ori]
            waypoints.append(point)
    else :
        for i,dat in enumerate(data.data):
            waypoints[i][0] = (waypoints[i][0][0], dat)
    recvy = True


def callbackx(data):
    global recvx
    global recvy

    if recvy == False:
        for dat in data.data:
            cord = (dat, 0)
            point = [cord, ori]
            waypoints.append(point)
    else :
        for i,dat in enumerate(data.data):
            waypoints[i][0] = (dat, waypoints[i][0][1])
    recvx = True

    
    


if __name__ == '__main__':
    rospy.init_node('patrol')
    # Subscribe to topic /patrol/coords/y
    
    rospy.Subscriber("/patrol/coords/y", Float32MultiArray, callbacky)
    rospy.Subscriber("/patrol/coords/x", Float32MultiArray, callbackx)

    while True:
        ds =8 
        if recvy == True and recvx == True:
            recvy = False
            recvx = False            
            # add label to waypoints
            for i,w in enumerate(waypoints):
                w.insert(0, str(i))
            print ("Waypoints: ", waypoints)
            patrol = StateMachine('success')
            with patrol:
                for i,w in enumerate(waypoints):
                    StateMachine.add(w[0],
                                    Waypoint(w[1], w[2]),
                                    transitions={'success':waypoints[(i + 1) % \
                                    len(waypoints)][0]})
            waypoints = []
            try:
                patrol.execute()
            except:
                print("Patrol execution failed")

        # exit when ctrl+c is pressed
        if rospy.is_shutdown():
            break

    # with patrol:
    #     for i,w in enumerate(waypoints):
    #         StateMachine.add(w[0],
    #                          Waypoint(w[1], w[2]),
    #                          transitions={'success':waypoints[(i + 1) % \
    #                          len(waypoints)][0]})

    # patrol.execute()
