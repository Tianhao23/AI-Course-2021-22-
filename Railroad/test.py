
from math import log, pi, acos, sin, cos, tan, log10, floor

# def draw_all_edges(Root, canvas):
#     Root.geometry("970x790") #sets the geometry of the tkinter
#     canvas.pack(fill=BOTH, expand =1)
#     for n in edges:
#         nbr = edges[n] # 
#         # lat1 = (stations[n][0]-9)/45 * 600
#         #     long1 = (stations[n][1]+134)/70*830
#         #     lat2 = (stations[n2][0]-9)/45 * 600
#         #     long2 = (stations[n2][1]+134)/70*830
#         for n2 in nbr:
#             lat1 = (stations[n][0])
#             long1 = (stations[n][1])
#             lat2 = (stations[n2][0])
#             long2 = (stations[n2][1])
#             drawLine(canvas, lat1, long1, lat2, long2, "black")
#             #drawLine(canvas, stations[n][0], stations[n][1], stations[n2][0], stations[n2][1], "black")
def gcd(lat1,long1, lat2,long2): #used to calculate great circle distance
    #
    # y1 = lat1, x1 = long1
    # y2 = lat2, x2 = long2
    # all assumed to be in decimal degrees

    # if (and only if) the input is strings
    # use the following conversions

    lat1  = float(lat1)
    long1  = float(long1)
    lat2  = float(lat2)
    long2 = float(long2)
    #
    R   = 3958.76 # miles = 6371 km
    #
    lat1 *= pi/180.0
    long1 *= pi/180.0
    lat2 *= pi/180.0
    long2 *= pi/180.0
    #
    # approximate great circle distance with law of cosines
    #
    return acos( sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(long2-long1)) * R
print(gcd('36.08742', '-115.19621', '36.08742', '-115.19621'))
