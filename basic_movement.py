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
        self.size = 35
        self.mobCount = 5   #amount of mobs per mob type
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
                            <Placement x="0" y="2" z="0" yaw="0"/>
                            <Inventory>
                                <InventoryItem slot="0" type="diamond_sword"/>
                                <InventoryItem slot="1" type="diamond_pickaxe"/>
                                <InventoryItem slot="2" type="diamond_axe"/>
                                <InventoryItem slot="3" type="diamond_shovel"/>
                            </Inventory>
                        </AgentStart>
                        <AgentHandlers>
                            <AbsoluteMovementCommands/>
                            <InventoryCommands/>
                            <ContinuousMovementCommands turnSpeedDegs="180"/>
                            <ObservationFromHotBar/>
                            <ObservationFromNearbyEntities>''' +\
                                "<Range name='Entities' xrange='{}' yrange='{}' zrange='{}'/>".format(self.size*2, 5, self.size*2) + \
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
    
    #return list of items in hotbar
    def get_hotbarList(self):
        hotbarList = []
        for i in range(9):
            hotbar = 'Hotbar_{}_item'.format(i) 
            hotbarList.append(str(self.get_worldstate(hotbar)))
        return hotbarList

    #get item from hotbar
    def switch_item(self,item):
        for i in range(9):
            hotbar = 'Hotbar_{}_item'.format(i)
            if str(self.get_worldstate(hotbar)) == item:
                press = "hotbar.{} 1".format(i+1)
                release = "hotbar.{} 0".format(i+1)
                self.agent_host.sendCommand(press)
                self.agent_host.sendCommand(release)
                break
        else:
            print("item not found")

    #find block
    def find_block(self, block, num):
        pass

    #break block
    def break_block(self, block, num):
        pass

    #helper function for find_entity
    def get_entityList(self, entity, direction = None):
        entities = self.get_worldstate('Entities')
        agent = entities[0]

        targetEntities = []
        for ent in entities:
            if ent['name'].lower() == entity:
                targetEntities.append(ent)
        entityList = []     
        for ent in targetEntities:
            entityList.append( (ent, (math.sqrt(abs((abs(agent['x'] - ent['x']) ** 2) + (abs(agent['z'] - ent['z']) ** 2))))) )
        #create two lists left and right sort them then append to each other??
        if direction == None:
            entityList.sort(key = lambda x: x[1]) #sort by tuple second element which is the distance
        else:
            yaw = (agent['yaw'] + 90) * (math.pi / 180)
            pitch = (agent['pitch'] * -1) * (math.pi / 180)
            a = (agent['x'], agent['z'])
            b = (agent['x'] + self.size * math.cos(yaw) * math.cos(pitch), agent['z'] + self.size * math.sin(yaw) * math.cos(pitch) )
            print("A->", a)
            print("B->", b)
            leftEntityList = []
            rightEntityList = []

            for ent in entityList: 
                p = (ent[0]['x'], ent[0]['z'])
                isLeft = ((b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])) < 0
                if isLeft:
                    print("LEFT ENTITY FOUND")
                    leftEntityList.append(ent)
                else:
                    print("RIGHT ENTITY FOUND")
                    rightEntityList.append(ent)

            leftEntityList.sort(key = lambda x: x[1])
            rightEntityList.sort(key = lambda x: x[1])
            print("LEFT ENTITY LIST")
            for ent in leftEntityList:
                print( "({},{})".format(ent[0]['x'], ent[0]['z']))
            print("RIGHT ENTITY LIST")
            for ent in rightEntityList:
                print( "({},{})".format(ent[0]['x'], ent[0]['z']))
            if direction == 'left':
                if leftEntityList:
                    entityList = leftEntityList
                else:
                    entityList =  leftEntityList + rightEntityList
            else:
                if rightEntityList:
                    entityList = rightEntityList
                else:
                    entityList = rightEntityList + leftEntityList

        return entityList # list of tuples where first item is ent

    def find_entity(self, entity, num = 1, dis = 0, direction = None):
        count = num
        seenEntities = []
        entityList = self.get_entityList(entity, direction)
        if dis > len(entityList):
            dis = -1

        while count > 0 and entityList:
            targetEntityID = entityList[dis][0]['id']
            print("SELECTED ENTITY->", entityList[dis][0])
            while True:
                entities = self.get_worldstate('Entities')
                agent = entities[0]
                for ent in self.get_entityList(entity):
                    if targetEntityID == ent[0]['id']:
                        targetEntity = ent[0]
                        break
                
                #print("AGENT", agent)
                #print("TARGET", targetEntity)
                diffX = targetEntity['x'] - agent['x']
                diffZ = targetEntity['z'] - agent['z']

                distance = math.floor(math.sqrt(abs(diffX)**2 + abs(diffZ)**2))
                yaw = -180 * math.atan2(diffX, diffZ) / math.pi

                self.agent_host.sendCommand("setYaw {}".format(yaw))
                self.run_forward(math.ceil(distance/2))

                if distance <= 1:
                    count -=1
                    print("FOUND", num - count, "UNIQUE ENTITIES")
                    seenEntities.append(targetEntity['id'])
                    break
            entityList = [i for i in self.get_entityList(entity, direction) if not i[0]['id'] in seenEntities] #get sorted entity list
        else:
            print('No nearby entites')
    
    #kill specified entity
    def kill_entity(self, entity, num = 1, dis = 0, direction = None, item = None):
        count = num
        seenEntities = []
        entityList = self.get_entityList(entity, direction)
        
        if item != None:
            self.switch_item(item)
        if dis > len(entityList):
            dis = -1

        while count > 0 and entityList:
            targetEntityID = entityList[dis][0]['id']
            print("SELECTED ENTITY->", entityList[dis][0])
            while True:
                entities = self.get_worldstate('Entities')
                agent = entities[0]
                for ent in self.get_entityList(entity):
                    if targetEntityID == ent[0]['id']:
                        targetEntity = ent[0]
                        break
                else:
                    count -= 1
                    break
                
                diffX = targetEntity['x'] - agent['x']
                diffZ = targetEntity['z'] - agent['z']

                distance = math.floor(math.sqrt(abs(diffX)**2 + abs(diffZ)**2))
                yaw = -180 * math.atan2(diffX, diffZ) / math.pi

                self.agent_host.sendCommand("setYaw {}".format(yaw))
                self.run_forward(math.ceil(distance/2))

                if distance <= 1:
                    time.sleep(0.1)
                    self.agent_host.sendCommand('setPitch 50')
                    time.sleep(0.1)
                    self.agent_host.sendCommand("attack 1")
                    time.sleep(0.1)
                    self.agent_host.sendCommand('setPitch 0')
                    time.sleep(0.1)
                    self.agent_host.sendCommand("attack 0")
                    
            entityList = [i for i in self.get_entityList(entity, direction) if not i[0]['id'] in seenEntities] #get sorted entity list
        else:
            print('No nearby entites')

    def walk_left(self, distance=1):
        for i in range(distance):
            self.agent_host.sendCommand("strafe -0.5")
            time.sleep(0.4)
            self.agent_host.sendCommand("strafe 0")

    def walk_right(self, distance=1):
        for i in range(distance):
            self.agent_host.sendCommand("strafe 0.5")
            time.sleep(0.4)
            self.agent_host.sendCommand("strafe 0")

    def walk_forward(self, distance=1):
        for i in range(distance):
            self.agent_host.sendCommand("move 0.5")
            time.sleep(0.4)
            self.agent_host.sendCommand("move 0")

    def walk_backward(self, distance=1):
        for i in range(distance):
            self.agent_host.sendCommand("move -0.5")
            time.sleep(0.4)
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
    
    def turn_left(self, num = 1):
        for i in range(num):
            self.agent_host.sendCommand("turn -1")
            time.sleep(0.5)
            self.agent_host.sendCommand("turn 0")
    
    def turn_right(self, num = 1):
        for i in range(num):
            self.agent_host.sendCommand("turn 1")
            time.sleep(0.5)
            self.agent_host.sendCommand("turn 0")
    
if __name__ == "__main__":
    test = BasicMovement({})
    
    time.sleep(0.5)
    print(test.get_worldstate("floorAll"))
    test.turn_left()
    test.turn_right()
    test.kill_entity('cow', 3, -1, 'right','diamond_axe')