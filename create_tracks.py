num_tracks = 1
track_length = 10

def createTracks(n, length, goal_blocks):
	''' Creates n number of tracks/obstacles with minecarts for the agent to get through'''
	drawTracks = ""
	for i in range(n):
		goal = goal_blocks[i]
		trackPos = (i*3)+1
		if i == 0:
			trackPos = i+1
		safePos = trackPos+1
		emptyPos = safePos+1
		goal_block = "emerald_block"
		if i == n-1:
			goal_block = "diamond_block"
		currTrack = '''	    
							<DrawCuboid x1="''' + str(0-(length//2)) + '''" y1="4" z1="''' + str(trackPos) + '''" x2="''' + str((length//2)-1) + '''" y2="4" z2="''' + str(trackPos) + '''" type="redstone_block"/>
							<DrawCuboid x1="''' + str(0-(length//2)-1) + '''" y1="5" z1="''' + str(trackPos) + '''" x2="''' + str(0-(length//2)-1) + '''" y2="5" z2="''' + str(trackPos) + '''" type="obsidian"/>
							<DrawCuboid x1="''' + str((length//2)) + '''" y1="5" z1="''' + str(trackPos) + '''" x2="''' + str((length//2)) + '''" y2="5" z2="''' + str(trackPos) + '''" type="obsidian"/>
							<DrawLine x1="''' + str(0-(length//2)) + '''" y1="5" z1="''' + str(trackPos) + '''" x2="''' + str((length//2)-1) + '''" y2="5" z2="''' + str(trackPos) + '''" type="golden_rail"/>
							<DrawCuboid x1="''' + str(0-(length//2)) + '''" y1="4" z1="''' + str(safePos) + '''" x2="''' + str((length//2)-1) + '''" y2="4" z2="''' + str(safePos) + '''" type="netherrack"/>
							<DrawCuboid x1="''' + str(0-(length//2)-1) + '''" y1="5" z1="''' + str(safePos) + '''" x2="''' + str(goal-1) + '''" y2="5" z2="''' + str(safePos) + '''" type="fire"/>
							<DrawCuboid x1="''' + str(goal+1) + '''" y1="5" z1="''' + str(safePos) + '''" x2="''' + str(length//2) + '''" y2="5" z2="''' + str(safePos) + '''" type="fire"/>
							<DrawCuboid x1="''' + str(goal) + '''" y1="4" z1="''' + str(safePos) + '''" x2="''' + str(goal) + '''" y2="4" z2="''' + str(safePos) + '''" type="''' + goal_block + '''"/>
					'''
		drawTracks += currTrack
		if i % 2 == 0:
			drawTracks += '''<DrawEntity x="''' + str(0-(length//2)) + '''" y="5" z="''' + str(trackPos+0.5) + '''" type="MinecartRideable"/>'''
		else:
			drawTracks += '''<DrawEntity x="''' + str((length//2)-1) + '''" y="5" z="''' + str(trackPos+0.5) + '''" type="MinecartRideable"/>'''
	return '''<DrawingDecorator>
						''' + drawTracks + '''
			  </DrawingDecorator>'''



def GetMissionXML(n_tracks, length, goal_blocks):
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
				  ''' + createTracks(n_tracks, length, goal_blocks) + '''
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
      agent_host.startMission(my_mission, my_client_pool, my_mission_record, 0, "AI")
      break
    except RuntimeError as e:
      if retry == max_retries - 1:
        print("Error starting", (i+1), ":",e)
        exit(1)
      else:
        time.sleep(2)
