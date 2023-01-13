#!/usr/bin/env python
 
import rospy
import actionlib
from smach import State,StateMachine
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from std_msgs.msg import Float32MultiArray


ori = (0.0, 0.0, 0.0, 1.0)

waypoints = [] # lista de tuplas (x,y) 
patrol = StateMachine('success') # maquina de estados

class Waypoint(State): # clase que define un waypoint
    def __init__(self, position, orientation): # constructor 
        State.__init__(self, outcomes=['success']) # define el estado de salida


        self.client = actionlib.SimpleActionClient('move_base', MoveBaseAction) # crea un cliente de accion
        self.client.wait_for_server() # espera a que el servidor este listo

        # Crea un goal para el servidor de accion
        self.goal = MoveBaseGoal()
        self.goal.target_pose.header.frame_id = 'map'
        self.goal.target_pose.pose.position.x = position[0] # posicion x
        self.goal.target_pose.pose.position.y = position[1] # posicion y 
        self.goal.target_pose.pose.position.z = 0.0
        self.goal.target_pose.pose.orientation.x = orientation[0] # orientacion x
        self.goal.target_pose.pose.orientation.y = orientation[1] # orientacion y
        self.goal.target_pose.pose.orientation.z = orientation[2] # orientacion z 
        self.goal.target_pose.pose.orientation.w = orientation[3] # orientacion w

    def execute(self, userdata): # ejecuta el waypoint 
        self.client.send_goal(self.goal) # envia el goal al servidor de accion
        print ("Waypoints: ", waypoints) # imprime los waypoints
        global recvy # variable global recvy
        global recvx # variable global recvx

        #  Espera a que el servidor de accion termine
        while (self.client.get_result() is None): # mientras el resultado sea nulo
            if recvy == True and recvx == True: # si recvy y recvx son verdaderos 
                return 'failure' # retorna failure
        return 'success' 


recvx = False
recvy = False

def callbacky(data): 

    global recvx 
    global recvy

    if recvx == False: # si recvx es falso 
        for dat in data.data: # para cada dato en data.data 
            cord = (0, dat) # cord es una tupla con 0 y dat 
            point = [cord, ori] # point es una lista con cord y ori 
            waypoints.append(point) # agrega point a waypoints 
    else : 
        for i,dat in enumerate(data.data): # para cada i y dat en enumerate(data.data) 
            waypoints[i][0] = (waypoints[i][0][0], dat) # waypoints[i][0] es una tupla con waypoints[i][0][0] y dat 
    recvy = True


def callbackx(data): # funcion callbackx
    global recvx # variable global recvx
    global recvy 

    if recvy == False: # si recvy es falso
        for dat in data.data: # para cada dato en data.data
            cord = (dat, 0) # cord es una tupla con dat y 0
            point = [cord, ori] # point es una lista con cord y ori
            waypoints.append(point) # agrega point a waypoints
    else :
        for i,dat in enumerate(data.data): # para cada i y dat en enumerate(data.data)
            waypoints[i][0] = (dat, waypoints[i][0][1]) # waypoints[i][0] es una tupla con dat y waypoints[i][0][1]
    recvx = True

    
    


if __name__ == '__main__': 
    rospy.init_node('patrol') # inicializa el nodo patrol

    
    rospy.Subscriber("/patrol/coords/y", Float32MultiArray, callbacky) # subscripcion al topic /patrol/coords/y
    rospy.Subscriber("/patrol/coords/x", Float32MultiArray, callbackx) 

    while True:
        
        if recvy == True and recvx == True: # si recvy y recvx son verdaderos
            recvy = False 
            recvx = False              
            # Añade las etiquetas a los waypoints 
            for i,w in enumerate(waypoints):
                w.insert(0, str(i))
            print ("Waypoints: ", waypoints)
            patrol = StateMachine('success')
            with patrol: 
                for i,w in enumerate(waypoints): # Se añaden los waypoints a la maquina de estados
                    StateMachine.add(w[0], 
                                    Waypoint(w[1], w[2]),
                                    transitions={'success':waypoints[(i + 1) % \ 
                                    len(waypoints)][0]})
            waypoints = [] # se vacia la lista de waypoints
            try:
                patrol.execute() # se ejecuta la maquina de estados
            except:
                print("Patrol execution failed")

        # exit when ctrl+c is pressed
        if rospy.is_shutdown(): 
            break
