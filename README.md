# kayak_tcp_transfer
REU code: publish kayak data from simulation to TCP

To be run with glider_kayak_sim.

Run roscore
Run launch file from glider_kayak_sim
Run kayak_tcp.py from this package
Use client to communicate with server started


class KayakReader requires a number input, the number should correspond to the kayak you want to subscribe to
In main, create new KayakReader as reader# = KayakReader(#) where # is the kayak # you want to subscribe to

Once a new kayak is created, create a dictionary for that kayak in the while not rospy.is_shutdown() loop in the style:
k# = dict(Temperature = reader#.temperature, Salinity = reader#.salinity, Latitude = reader#.latitude, Longitude = reader#.longitude, Depth = reader#.depth, x = reader#.x, y = reader#.y, z = reader#.z, w = reader#.w)

To add this as an option for a client to read add it to the tcp database:
tcp.database['kayak_#']=yaml.dump(k#)
