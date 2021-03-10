import math
import MalmoPython
import random
import time
import json
import os
import sys

# num_tracks = 1
track_length = 20 #number of blocks in the track


def createTracks():
	drawTracks = ""
	goal = random.randint(-5,5)
	goal_block = "diamond_block"
	drawTrack = '''	    
			<DrawCuboid x1="''' + '-10' + '''" y1="4" z1="''' + '1' + '''" x2="''' + '9' + '''" y2="4" z2="''' + '1' + '''" type="redstone_block"/>
			<DrawCuboid x1="''' + '-11' + '''" y1="5" z1="''' + '1'+ '''" x2="''' + '-11' + '''" y2="5" z2="''' + '1' + '''" type="obsidian"/>
			<DrawCuboid x1="''' + '10' + '''" y1="5" z1="''' + '1'+ '''" x2="''' + '10' + '''" y2="5" z2="''' + '1' + '''" type="obsidian"/>
			<DrawLine x1="''' + '-10' + '''" y1="5" z1="''' + '1' + '''" x2="''' + '9' + '''" y2="5" z2="''' + '1' + '''" type="golden_rail"/>
			<DrawCuboid x1="''' + '-10' + '''" y1="4" z1="''' + '2' + '''" x2="''' + '9' + '''" y2="4" z2="''' + '2' + '''" type="netherrack"/>
			<DrawCuboid x1="''' + '-11' + '''" y1="5" z1="''' + '2' + '''" x2="''' + str(goal-1) + '''" y2="5" z2="''' + '2' + '''" type="fire"/>
			<DrawCuboid x1="''' + str(goal+1) + '''" y1="5" z1="''' + '2' + '''" x2="''' + '10' + '''" y2="5" z2="''' + '2' + '''" type="fire"/>
			<DrawCuboid x1="''' + str(goal) + '''" y1="4" z1="''' + '2' + '''" x2="''' + str(goal) + '''" y2="4" z2="''' + '2' + '''" type="''' + goal_block + '''"/>
	'''
	drawTrack += '''<DrawEntity x="''' + str(-10) + '''" y="5" z="''' + '1.5' + '''" type="MinecartRideable"/>'''
	# set player position
	return '''<DrawingDecorator>
						''' + drawTracks + '''
			  </DrawingDecorator>'''



def GetMissionXML():
	return '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
			<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
			  <About>
				<Summary>CrossyCarts - Minecraft recreation of Frogger/CrossyRoad</Summary>
			  </About>
			<ServerSection>
			  <ServerInitialConditions>
				<Time>
					<StartTime>0</StartTime>
					<AllowPassageOfTime>false</AllowPassageOfTime>
				</Time>
				<Weather>clear</Weather>
			  </ServerInitialConditions>
			  <ServerHandlers>
				  <FlatWorldGenerator generatorString="biome_1" forceReset="true" />
				  ''' + createTracks() + '''
				  <ServerQuitWhenAnyAgentFinishes/>
				</ServerHandlers>
			  </ServerSection>
			  <AgentSection mode="Survival">
				<Name>CrossyCartsBot</Name>
				<AgentStart>
					<Placement x="0.5" y="5" z="0.5" yaw="0.5" pitch="-6"/>
				</AgentStart>
				<AgentHandlers>
					<ContinuousMovementCommands turnSpeedDegs="480"/>
					<ObservationFromNearbyEntities>
						<Range name="entities" xrange="20" yrange="2" zrange="2"/>
					</ObservationFromNearbyEntities>
					<ObservationFromGrid>
					  <Grid name="floorAhead">
						<min x="-4" y="0" z="1"/>
						<max x="4" y="0" z="1"/>
					  </Grid>
					  <Grid name="floorUnder">
						<min x="0" y="-1" z="0"/>
						<max x="0" y="0" z="0"/>
					  </Grid>
					</ObservationFromGrid>
					<AbsoluteMovementCommands/>
					<MissionQuitCommands/>
					<ChatCommands/>
				</AgentHandlers>
			  </AgentSection>
			</Mission>'''


if __name__ == '__main__':
  num_tracks = int(input("enter the number of tracks: "))
  agent_host = MalmoPython.AgentHost()
  goal_blocks = []
	for n in range(num_tracks):
		goal_blocks.append(random.randint((-track_length//2+1), (track_length//2)-2))
  my_mission = MalmoPython.MissionSpec(GetMissionXML(num_tracks, track_length, goal_blocks), True)
  my_mission_record = MalmoPython.MissionRecordSpec()
  my_mission.requestVideo(800, 500)
  my_mission.setViewpoint(1)

  # Attempt to start a mission:
  my_client_pool = MalmoPython.ClientPool()
  my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))
  max_retries = 3
  for retry in range(max_retries):
    try:
      agent_host.startMission(my_mission, my_client_pool, my_mission_record, 0, "cart_test")
      break
    except RuntimeError as e:
      if retry == max_retries - 1:
        print("Error starting", (i+1), ":",e)
        exit(1)
      else:
        time.sleep(2)
