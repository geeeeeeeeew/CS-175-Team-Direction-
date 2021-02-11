# Rllib docs: https://docs.ray.io/en/latest/rllib.html

try:
    from malmo import MalmoPython
except:
    import MalmoPython

import sys
import time
import json
import numpy as np
from numpy.random import randint

class BasicMovement():

    def __init__(self, env_config):  
        # Static Parameters
        self.size = 50

        # Malmo Parameters
        self.agent_host = MalmoPython.AgentHost()
        world_state = self.init_malmo()
        try:
            self.agent_host.parse( sys.argv )
        except RuntimeError as e:
            print('ERROR:', e)
            print(self.agent_host.getUsage())
            exit(1)

    def get_mission_xml(self):
    	return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
                <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

                    <About>
                        <Summary>Basic Movement</Summary>
                    </About>

                    <ServerSection>
                        <ServerInitialConditions>
                            <Time>
                                <StartTime>12000</StartTime>
                                <AllowPassageOfTime>false</AllowPassageOfTime>
                            </Time>
                            <Weather>clear</Weather>
                        </ServerInitialConditions>
                        <ServerHandlers>
                            <FlatWorldGenerator generatorString="3;7,2;1;"/>
                            <DrawingDecorator>''' + \
                                "<DrawCuboid x1='{}' x2='{}' y1='2' y2='2' z1='{}' z2='{}' type='air'/>".format(-self.size, self.size, -self.size, self.size) + \
                                "<DrawCuboid x1='{}' x2='{}' y1='1' y2='1' z1='{}' z2='{}' type='stone'/>".format(-self.size, self.size, -self.size, self.size) + \
                                '''<DrawBlock x='0'  y='2' z='0' type='air' />
                                <DrawBlock x='0'  y='1' z='0' type='melon_block' />
                            </DrawingDecorator>
                            <ServerQuitWhenAnyAgentFinishes/>
                        </ServerHandlers>
                    </ServerSection>

                    <AgentSection mode="Survival">
                        <Name>SpeechToSteve</Name>
                        <AgentStart>
                            <Placement x="0.5" y="2" z="0.5" pitch="45" yaw="0"/>
                            <Inventory>
                                <InventoryItem slot="0" type="diamond_pickaxe"/>
                            </Inventory>
                        </AgentStart>
                        <AgentHandlers>
                            <ContinuousMovementCommands/>
                            <ObservationFromFullStats/>
                            <ObservationFromRay/>
                            <ObservationFromGrid>
                                <Grid name="floorAll">
                                    <min x="-'''+str(int(5/2))+'''" y="-1" z="-'''+str(int(5/2))+'''"/>
                                    <max x="'''+str(int(5/2))+'''" y="0" z="'''+str(int(5/2))+'''"/>
                                </Grid>
                            </ObservationFromGrid>
                            <AgentQuitFromTouchingBlockType>
                                <Block type="bedrock" />
                            </AgentQuitFromTouchingBlockType>
                        </AgentHandlers>
                    </AgentSection>
                </Mission>'''

    def init_malmo(self):
        """
        Initialize new malmo mission.
        """
        my_mission = MalmoPython.MissionSpec(self.get_mission_xml(), True)
        my_mission_record = MalmoPython.MissionRecordSpec()
        my_mission.requestVideo(800, 500)
        my_mission.setViewpoint(1)

        max_retries = 3
        my_clients = MalmoPython.ClientPool()
        my_clients.add(MalmoPython.ClientInfo('127.0.0.1', 10000)) # add Minecraft machines here as available

        for retry in range(max_retries):
            try:
                self.agent_host.startMission( my_mission, my_clients, my_mission_record, 0, 'SpeechToSteve' )
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:", e)
                    exit(1)
                else:
                    time.sleep(2)

        world_state = self.agent_host.getWorldState()
        while not world_state.has_mission_begun:
            time.sleep(0.3)
            world_state = self.agent_host.getWorldState()
            for error in world_state.errors:
                print("\nError:", error.text)

        return world_state

    def walk_left(self, distance=1):
    	for i in range(distance):
    		self.agent_host.sendCommand("strafe -0.5")
    		time.sleep(0.45)
    		self.agent_host.sendCommand("strafe 0")

    def walk_right(self, distance=1):
    	for i in range(distance):
    		self.agent_host.sendCommand("strafe 0.5")
    		time.sleep(0.45)
    		self.agent_host.sendCommand("strafe 0")

    def walk_forward(self, distance=1):
    	for i in range(distance):
    		self.agent_host.sendCommand("move 0.5")
    		time.sleep(0.45)
    		self.agent_host.sendCommand("move 0")

    def walk_backward(self, distance=1):
    	for i in range(distance):
    		self.agent_host.sendCommand("move -0.5")
    		time.sleep(0.45)
    		self.agent_host.sendCommand("move 0")

    def run_left(self, distance=1):
    	for i in range(distance):
    		self.agent_host.sendCommand("strafe -1")
    		time.sleep(0.2)
    		self.agent_host.sendCommand("strafe 0")

    def run_right(self, distance=1):
    	for i in range(distance):
    		self.agent_host.sendCommand("strafe 1")
    		time.sleep(0.2)
    		self.agent_host.sendCommand("strafe 0")

    def run_forward(self, distance=1):
    	for i in range(distance):
    		self.agent_host.sendCommand("move 1")
    		time.sleep(0.2)
    		self.agent_host.sendCommand("move 0")

    def run_backward(self, distance=1):
    	for i in range(distance):
    		self.agent_host.sendCommand("move -1")
    		time.sleep(0.2)
    		self.agent_host.sendCommand("move 0")
    def jump(self, num_jumps=1):
    	for i in range(num_jumps):
    		self.agent_host.sendCommand("jump 1")
    		time.sleep(0.58)
    	self.agent_host.sendCommand("jump 0")

if __name__ == '__main__':
    test = BasicMovement({})
    #test.walk_left(5)
    #test.walk_right(5)
    #test.walk_forward(5)
    #test.walk_backward(5)
    #test.run_left(5)
    #test.run_right(5)
    #test.run_forward(5)
    #test.run_backward(5)
    test.jump(6)
