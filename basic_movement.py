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
                            <Placement x="0.5" y="2" z="0.5" yaw="0"/>
                            <Inventory>
                                <InventoryItem slot="0" type="diamond_sword"/>
                                <InventoryItem slot="1" type="diamond_pickaxe"/>
                                <InventoryItem slot="2" type="diamond_axe"/>
                                <InventoryItem slot="3" type="diamond_shovel"/>
                            </Inventory>
                        </AgentStart>
                        <AgentHandlers>
                            <AbsoluteMovementCommands/>
                            <ContinuousMovementCommands turnSpeedDegs="180"/>
                            <ObservationFromHotBar/>
                            <ObservationFromNearbyEntities>''' +\
                                "<Range name='Entities' xrange='{}' yrange='{}' zrange='{}'/>".format(self.size, self.size, self.size) + \
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
        # time.sleep(0.1)
        lastWorldState = self.agent_host.peekWorldState()
        observation = json.loads(lastWorldState.observations[-1].text)
        return observation[obs]

    def get_yaw(self):
        # time.sleep(0.1)
        lastWorldState = self.agent_host.peekWorldState()
        observation = json.loads(lastWorldState.observations[-1].text)
        yaw = observation.get(u'Yaw', 0)
        return yaw

    # checks if yaw is in the left side of the agent
    def in_range(self, minYaw, maxYaw, yaw):
        if minYaw < 0:
            return minYaw <= yaw <= maxYaw
        else: # minYaw > 0
            return minYaw <= yaw <= 180 or -180 < yaw <= maxYaw

    #helper function for find_entity
    def get_entityList(self, entity):
        entities = self.get_worldstate('Entities')
        agent = entities[0]

        targetEntities = []
        for ent in entities:
            if ent['name'].lower() == entity:
                targetEntities.append(ent)
        entityList = []
        for ent in targetEntities:
            entityList.append( (ent, (math.sqrt(abs((abs(agent['x'] - ent['x']) ** 2) + (abs(agent['z'] - ent['z']) ** 2))))) )

        entityList.sort(key = lambda x: x[1])
        return entityList # list of tuples where first item is ent

    def get_leftEntityList(self, entity):
        entities = self.get_worldstate('Entities')
        agent = entities[0]
        playerYaw = self.get_yaw()
        minYaw = playerYaw - 180
        if minYaw <= -180:
            minYaw += 360

        targetEntities = []
        for ent in entities:
            if ent['name'].lower() == entity:
                targetEntities.append(ent)
        entityList = []
        for ent in entities:
            if ent['name'].lower() == entity:
                targetEntities.append(ent)
        entityList = []
        for ent in targetEntities:

            diffX = ent['x'] - agent['x']
            diffZ = ent['z'] - agent['z']
            yaw = -180 * math.atan2(diffX, diffZ) / math.pi
            if self.in_range(minYaw, playerYaw, yaw):
                entityList.append( (ent, (math.sqrt(abs((abs(agent['x'] - ent['x']) ** 2) + (abs(agent['z'] - ent['z']) ** 2))))) )

        # there are no entities to the left of the player, so we find the nearest entity instead
        if len(entityList) == 0:
            return self.get_entityList(entity)
        entityList.sort(key = lambda x: x[1])
        return entityList # list of tuples where first item is ent

    def get_rightEntityList(self, entity):
        entities = self.get_worldstate('Entities')
        agent = entities[0]
        playerYaw = self.get_yaw()
        minYaw = playerYaw - 180
        if minYaw <= -180:
            minYaw += 360

        targetEntities = []
        for ent in entities:
            if ent['name'].lower() == entity:
                targetEntities.append(ent)
        entityList = []
        for ent in targetEntities:

            diffX = ent['x'] - agent['x']
            diffZ = ent['z'] - agent['z']
            yaw = -180 * math.atan2(diffX, diffZ) / math.pi
            if self.in_range(minYaw, playerYaw, yaw):
                pass
            else:
                entityList.append( (ent, (math.sqrt(abs((abs(agent['x'] - ent['x']) ** 2) + (abs(agent['z'] - ent['z']) ** 2))))) )

        # there are no entities to the right of the player, so we find the nearest entity instead
        if len(entityList) == 0:
            return self.get_entityList(entity)
        entityList.sort(key = lambda x: x[1])
        return entityList # list of tuples where first item is ent

    #FUTURE FEATURES
    #ADD cow to the right or cow to the left
    #to do this favor the cow with the lower x respective player (left)
    #favor the cow with the higher x respective to the player (right)
    #favor the cow with the lower z respective to the player (north)    
    #favor the cow with te higher z respective to the player (south)
    #based off chatbot steve project from 2020
    def find_entity(self, entity, time = 1, direction=None):
        count = time
        seenEntities = []
        entityList = self.get_entityList(entity)
        print(entityList[0])
        playerYaw = self.get_yaw()

        if direction == 'left':
            entitylist = self.get_leftEntityList(entity)
        elif direction == 'right':
            entitylist = self.get_rightEntityList(entity)

        while count > 0 and entityList:
            closestEntityID = entityList[0][0]['id']
            while True:
                entities = self.get_worldstate('Entities')
                agent = entities[0]
                for ent in self.get_entityList(entity):
                    if closestEntityID == ent[0]['id']:
                        closestEntity = ent[0]
                        break

                diffX = closestEntity['x'] - agent['x']
                diffZ = closestEntity['z'] - agent['z']

                distance = math.floor(math.sqrt(abs(diffX)**2 + abs(diffZ)**2))
                yaw = -180 * math.atan2(diffX, diffZ) / math.pi

                self.agent_host.sendCommand("setYaw {}".format(yaw))
                self.run_forward(math.ceil(distance/2))

                print(self.get_yaw())
                print(closestEntity)
                print(agent['x'])

                if distance <= 1:
                    count -=1
                    print("FOUND", time - count, "UNIQUE ENTITIES")
                    seenEntities.append(closestEntity['id'])
                    break
            if direction == None:
                entityList = [i for i in self.get_entityList(entity) if not i[0]['id'] in seenEntities] #get closest entity
            elif direction == 'left':
                entityList = [i for i in self.get_leftEntityList(entity) if not i[0]['id'] in seenEntities] #get closest entity
            elif direction == 'right':
                entityList = [i for i in self.get_rightEntityList(entity) if not i[0]['id'] in seenEntities] #get closest entity
        else:
            print('No nearby entites')
            
    # finds the nearest block to the agent
    def findBlock(self, block=None):
        time.sleep(1)
        lastWorldState = self.agent_host.peekWorldState()
        observation = json.loads(lastWorldState.observations[-1].text)
        agent_x = int(observation['XPos'])
        agent_z = int(observation['YPos'])

        # generates an array with all blocks in an 81x81 rectangle from the agent
        grid = observation.get('findBlock')

        # find the index in the array that represents the agent's position
        center = int(len(grid) / 2)
        counter = 0
        candidateBlocks = []
        print(len(grid))
        print(center)

        # finds all blocks in the environment that are the same type as the target block
        # so we can compare their distance from the agent and find the closest one
        for i in grid:
            if i == block:
                candidateBlocks.append(counter)
                print(i)
            counter += 1

        if block == None:
            return
        elif len(candidateBlocks) == 0:
            self.agent_host.sendCommand('chat No ' + block + ' found near me!')
        # find the closest target block to the agent
        else:
            target = candidateBlocks[0]
            distance = abs(target - center)
            for i in candidateBlocks:
                if abs(i - center) < distance:
                    target = i
                    distance = abs(i - center)

            # find out the position of the block in the 2D array
            blockRow = int(target / 81)
            blockColumn = target - (blockRow * 81)
            # agentRow = 40
            # agentColumn = 40

            # convert this to a coordinate using the agent's position
            differenceRow = agent_x + (blockRow - 40)
            differenceColumn = agent_z + (blockColumn - 40)
            if blockRow < 40:
                differenceRow = agent_x - (40 - blockRow)
            if blockColumn < 40:
                differenceColumn = agent_z - (40 - blockColumn)

            teleport = 'tp ' + str(differenceColumn) + ' 4 ' + str(differenceRow)
            self.agent_host.sendCommand(teleport)

            print(differenceRow)
            print(differenceColumn)

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
    test.find_entity('sheep', 1, 'left')
