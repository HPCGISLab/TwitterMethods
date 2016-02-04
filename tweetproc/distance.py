'''
Copyright (c) 2006-2010 Brian Beck
Copyright (c) 2010-2015 GeoPy Project and individual contributors

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# This method is based on the method from geopy.py under MIT license (listed above)
# See the following website for details
# https://pypi.python.org/pypi/geopy#downloads
# and the distance.py file for code
# Credit, other than mistakes, should be given to GeoPy project.

from math import *

def greatcircledistance(pt1, pt2):
    # Modified geopy code to meet expectations of my own code
    #a, b = Point(a), Point(b)

    #lat1, lng1 = radians(degrees=a.latitude), radians(degrees=a.longitude)
    #lat2, lng2 = radians(degrees=b.latitude), radians(degrees=b.longitude)

    lat1, lng1 = radians(pt1[0]), radians(pt1[1])
    lat2, lng2 = radians(pt2[0]), radians(pt2[1])

    sin_lat1, cos_lat1 = sin(lat1), cos(lat1)
    sin_lat2, cos_lat2 = sin(lat2), cos(lat2)

    delta_lng = lng2 - lng1
    cos_delta_lng, sin_delta_lng = cos(delta_lng), sin(delta_lng)

    d = atan2(sqrt((cos_lat2 * sin_delta_lng) ** 2 +
                   (cos_lat1 * sin_lat2 -
                    sin_lat1 * cos_lat2 * cos_delta_lng) ** 2),
              sin_lat1 * sin_lat2 + cos_lat1 * cos_lat2 * cos_delta_lng)

    return 6372.795 * d * 1000 # The 1000 multiplication is a modification of geopy.py code to return meters instead of kilometers
                               # The earth radius is also used from geopy (they pulled from Wikipedia)


