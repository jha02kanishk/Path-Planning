from dronekit import connect, VehicleMode, LocationGlobalRelative
import time, math

vehicle = connect('127.0.0.1:14550', wait_ready=True, baud=57600)

def arm_and_takeoff(aTargetAltitude):

  print("Basic pre-arm checks")
  # Don't let the user try to arm until autopilot is ready
  while not vehicle.is_armable:
    print(" Waiting for vehicle to initialise...")
    time.sleep(1)
        
  print("Arming motors")
  # Copter should arm in GUIDED mode
  vehicle.mode    = VehicleMode("GUIDED")
  vehicle.armed   = True

  while not vehicle.armed:
    print(" Waiting for arming...")
    time.sleep(1)

  print("Taking off!")
  vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

  # Check that vehicle has reached takeoff altitude
  while True:
    print(" Altitude: ", vehicle.location.global_relative_frame.alt) 
    #Break and return from function just below target altitude.        
    if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
      print("Reached target altitude")
      break
    time.sleep(1)
    
# Initialize the takeoff sequence to 15m
arm_and_takeoff(15)

print("Take off complete")


def haversine(lat1, lon1, lat2, lon2):
     
    # distance between latitudes
    # and longitudes
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0
 
    # convert to radians
    lat1 = (lat1) * math.pi / 180.0
    lat2 = (lat2) * math.pi / 180.0
 
    # apply formulae
    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
             math.cos(lat1) * math.cos(lat2));
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c

def go_to_waypoint(L):
  for i in L:
    #lat1 = vehicle.location.global_relative_frame.lat
    #lon1 = vehicle.location.global_relative_frame.lon
    #lat2 = i[0]
    #lon2 = i[1]
    vehicle.mode = VehicleMode("GUIDED")
    a_location = LocationGlobalRelative(i[0],i[1],i[2])
    vehicle.simple_goto(a_location)
    time.sleep(15)

    while True: 
      dist = haversine(vehicle.location.global_relative_frame.lat, vehicle.location.global_relative_frame.lon, i[0], i[1])
      if dist > 0.005:
        print("reaching waypoint")
        time.sleep(5)
      else:
        break  

go_to_waypoint([[-35.36054476,149.16980875,15.0],[-35.36084794,149.16845940,15.0]])


# Hover for 10 seconds
time.sleep(15)

print("Now let's land")
vehicle.mode = VehicleMode("LAND")

# Close vehicle object
vehicle.close()
