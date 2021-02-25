# Rllib docs: https://docs.ray.io/en/latest/rllib.html

try:
    from malmo import MalmoPython
except:
    import MalmoPython

import math
import sys
import time
import json
import numpy as np
from random import randint

spawnBlocks = "<DrawBlock x='8' y='2' z='3' type='log' variant='oak'/>" + \
            "<DrawBlock x='8' y='3' z='3' type='log' variant='oak'/>" + \
            "<DrawBlock x='8' y='4' z='3' type='log' variant='oak'/>" + \
            "<DrawBlock x='-7' y='2' z='14' type='lapis_ore'/>" + \
            "<DrawBlock x='12' y='2' z='-5' type='iron_ore'/>" + \
            "<DrawBlock x='-4' y='2' z='-9' type='coal_ore'/>"

class BasicMovement():

    def __init__(self, env_config):  
        # Static Parameters
        self.size = 25
        self.mobCount = 5   #amount of mobs per mob type
        self.block = 0.001
        # Malmo Parametersa
        self.agent_host = MalmoPython.AgentHost()
        world_state = self.init_malmo()
        try:
            self.agent_host.parse( sys.argv )
        except RuntimeError as e:
            print('ERROR:', e)
            print(self.agent_host.getUsage())
            exit(1)

    def spawn_mobs(self):
        spawnMobs = ''
        mobs = ['Llama', 'Cow', 'Sheep', 'Chicken', 'PolarBear', 'Pig']
        for mob in mobs:
            for i in range(self.mobCount):
                spawnMobs += "<DrawEntity x='{}' y='2' z='{}' type='{}'/>".format(randint(-self.size, self.size),randint(-self.size, self.size),mob)
        return spawnMobs

    def get_mission_xml(self):
        spawnMobs = self.spawn_mobs()
        return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
                <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                    <About>
                        <Summary>Speech-To-Steve</Summary>
                    </About>
                    <ServerSection>
                        <ServerInitialConditions>
                            <Time>
                                <StartTime>6000</StartTime>
                                <AllowPassageOfTime>false</AllowPassageOfTime>
                            </Time>
                            <Weather>clear</Weather>
                        </ServerInitialConditions>
                        <ServerHandlers>
                            <FlatWorldGenerator generatorString="3;7,2;1;"/>
                            <DrawingDecorator>''' + \
                                "<DrawCuboid x1='{}' x2='{}' y1='2' y2='2' z1='{}' z2='{}' type='air'/>".format(-self.size, self.size, -self.size, self.size) + \
                                "<DrawCuboid x1='{}' x2='{}' y1='1' y2='1' z1='{}' z2='{}' type='grass'/>".format(-self.size, self.size, -self.size, self.size) + \
                                spawnMobs + \
                                '''<DrawBlock x='0'  y='2' z='0' type='air' />
                                <DrawBlock x='0'  y='1' z='0' type='glowstone' />''' + \
                                spawnBlocks + \
                            '''</DrawingDecorator>
                            <ServerQuitWhenAnyAgentFinishes/>
                        </ServerHandlers>
                    </ServerSection>
                    <AgentSection mode="Survival">
                        <Name>SpeechToSteve</Name>
                        <AgentStart>
                            <Placement x="0.5" y="2" z="0.5" pitch="45" yaw="0"/>
                            <Inventory>
                                <InventoryItem slot="0" type="diamond_sword"/>
                                <InventoryItem slot="1" type="diamond_pickaxe"/>
                                <InventoryItem slot="2" type="diamond_axe"/>
                                <InventoryItem slot="3" type="diamond_shovel"/>
                            </Inventory>
                        </AgentStart>
                        <AgentHandlers>
                            <ContinuousMovementCommands/>
                            <ObservationFromHotBar/>
                            <ObservationFromNearbyEntities>''' +\
                                "<Range name='Entities' xrange='{}' yrange='{}' zrange='{}'/>".format(self.size/2, self.size/2, self.size/2) + \
                            '''</ObservationFromNearbyEntities>
                            <ObservationFromFullStats/>
                            <ObservationFromRay/>
                            <ObservationFromGrid>
                                <Grid name="floorAll">
                                    <min x="-'''+str(int(self.size/2))+'''" y="-1" z="-'''+str(int(self.size/2))+'''"/>
                                    <max x="'''+str(int(self.size/2))+'''" y="0" z="'''+str(int(self.size/2))+'''"/>
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

    #obs for observation
    #can be hotbar ie Hotbar_0_item, Hotbar_1_item, ... etc
    #Entites - return nearby mobs
    #floorall - grid
    #LineofSight
    #XPos, YPos, ZPos, Pitch, Yaw
    def get_worldstate(self, obs):
        lastWorldState = self.agent_host.peekWorldState()
        observation = json.loads(lastWorldState.observations[-1].text)
        return observation[obs]

    def find_entity(self, entity, num = 1):
        entities = self.get_worldstate('Entities')
        for ent in entities:
            print(ent['name'], '->', ent)
        #search for entity


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

    def crouch(self, length = 2):
        self.agent_host.sendCommand("crouch 1")
        time.sleep(length)
        self.agent_host.sendCommand("crouch 0")