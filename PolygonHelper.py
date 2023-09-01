from shapely.geometry import Polygon, Point, LineString
import math

# Given a list of coordinates (list of tuples) that form a polygon
# and a coordinate return true if coordinate lies within the polygon
def is_coordinate_in_polygon(polygon_coordinates, coordinate):
    polygon = Polygon(polygon_coordinates)
    point = Point(coordinate)
    return polygon.contains(point)

# Given 2 coordinates (tuple) return the midpoint coordinate
def calculate_midpoint(coordinate1, coordinate2):
    x1, y1 = coordinate1
    x2, y2 = coordinate2
    midpoint_x = (x1 + x2) / 2
    midpoint_y = (y1 + y2) / 2
    return (midpoint_x, midpoint_y)

# Given a list of coordinates (list of tuples) return a list 
# of side lengths
def calculate_side_lengths(vertices):
    n = len(vertices)
    side_lengths = []

    for i in range(n):
        if i < n - 1:
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1)]

            side_length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            side_lengths.append(round(side_length,3))

    return side_lengths

def calculate_side_length(coordinate_1, coordinate_2):
    x1,y1 = coordinate_1
    x2,y2 = coordinate_2
    return round(math.sqrt((x2 - x1)**2 + (y2 - y1)**2),3)

# Given 2 coordinates find the midpoint and return a point that lies
# a given distance on the perpendicular line at the midpoint
def calculate_perpendicular_point(line_point1, line_point2, distance):
    x1, y1 = line_point1
    x2, y2 = line_point2

    # Calculate the midpoint of the line
    mid_x = (x1 + x2) / 2
    mid_y = (y1 + y2) / 2

    # Calculate the slope of the line
    slope = (y2 - y1) / (x2 - x1) if x2 != x1 else float('inf')

    # Calculate the angle between the line and the x-axis
    if slope == 0:
        angle = math.pi / 2
    elif slope == float('inf'):
        angle = 0
    else:
        angle = math.atan(slope)

    # Calculate the coordinates of the endpoint of the perpendicular line
    if slope == 0:
        x_end = mid_x
        y_end = mid_y + distance
    elif slope == float('inf'):
        x_end = mid_x + distance
        y_end = mid_y
    else:
        x_end = mid_x + distance * math.cos(angle + math.pi / 2)
        y_end = mid_y + distance * math.sin(angle + math.pi / 2)

    # Return the coordinates of the perpendicular line segment
    return (x_end,y_end)

def check_line_intersection(line1, line2):
    line1 = LineString(line1)
    line2 = LineString(line2)
    return line1.intersects(line2)

def calculate_direction(coord1, coord2):
    x1, y1 = coord1
    x2, y2 = coord2

    # Calculate the angle in radians
    angle_rad = math.atan2(x2 - x1, y2 - y1)

    # Convert the angle to degrees and adjust the range to [0, 360)
    angle_deg = math.degrees(angle_rad) % 360

    # Convert the angle to the cardinal direction
    directions = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                  "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

    index = round(angle_deg / 22.5) % 16
    direction = directions[index]

    return direction

# Returns all directions of polygon sides pointing outwards
# if given specific coordinates in vertices, returns just the one direction of the specified
# Return none otherwise
def wall_direction(vertices, room_coordinates_1 = None, room_coordinates_2 = None):
    distance = 1
    list_of_directions = []
    for i in range(len(vertices)):
        if i < len(vertices) - 1:
            if (room_coordinates_1 == vertices[i] and room_coordinates_2 == vertices[i+1]) or (room_coordinates_1 == None and room_coordinates_2 == None):
                perpendicular_test_coordinate = calculate_perpendicular_point(vertices[i], vertices[i+1], distance)
                midpoint = calculate_midpoint(vertices[i], vertices[i+1])

                intersection_count = -1 # Since the midpoint counts as an intersection we start the intersection count at -1 so it goes back to zero
                for j in range(len(vertices)):
                    if j < len(vertices) - 1:
                        if check_line_intersection((midpoint, perpendicular_test_coordinate),(vertices[j],vertices[j+1])):
                            intersection_count = intersection_count + 1

                # Due to percision sometimes the midpoint doesn't get detected as an intersection so this just changes the intersections back to zero
                if intersection_count == -1:
                    intersection_count = 0

                if is_coordinate_in_polygon(vertices, perpendicular_test_coordinate) and intersection_count%2 == 0:
                    list_of_directions.append(calculate_direction(perpendicular_test_coordinate, midpoint))
                elif is_coordinate_in_polygon(vertices, perpendicular_test_coordinate) and intersection_count%2 != 0:
                    list_of_directions.append(calculate_direction(midpoint, perpendicular_test_coordinate))
                elif not is_coordinate_in_polygon(vertices, perpendicular_test_coordinate) and intersection_count%2 == 0:
                    list_of_directions.append(calculate_direction(midpoint, perpendicular_test_coordinate))
                elif not is_coordinate_in_polygon(vertices, perpendicular_test_coordinate) and intersection_count%2 != 0:
                    list_of_directions.append(calculate_direction(perpendicular_test_coordinate, midpoint))
    if len(list_of_directions) == 0:
        return None
    elif len(list_of_directions) == 1:
        return list_of_directions[0]
    else:
        return list_of_directions

# Given a set of coordinates (list of tuples) return the area
def calculate_enclosed_area(vertices):
    n = len(vertices)
    area = 0.0

    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]  # Wrap around for the last vertex

        area += (x1 * y2) - (x2 * y1)

    area = abs(area) / 2.0
    return area

def is_point_on_line(line_point1, line_point2, point):
    x1, y1 = line_point1
    x2, y2 = line_point2
    x, y = point

    # Calculate the range of x values covered by the line segment
    min_x = min(x1, x2)
    max_x = max(x1, x2)

    # Check if the point lies within the range of x values covered by the line segment
    if min_x <= x <= max_x:
        if x1 == x2:
            # For vertical lines, check if the point's y-coordinate lies between the line's y-coordinates
            return min(y1, y2) <= y <= max(y1, y2)
        else:
            # Calculate slope and y-intercept of the line
            slope = (y2 - y1) / (x2 - x1)
            y_intercept = y1 - slope * x1

            # Calculate the expected y value on the line at the given x
            expected_y = slope * x + y_intercept

            # Check if the point's y-coordinate is within a small tolerance of the expected y value
            tolerance = 1e-4  # Adjust tolerance as needed
            return abs(y - expected_y) <= tolerance
    else:
        return False
    
def is_point_on_polygon(polygon_coordinates, point):
    for i, coordinate in enumerate(polygon_coordinates):
        if i < len(polygon_coordinates) - 1:
            if is_point_on_line(polygon_coordinates[i], polygon_coordinates[i+1], point):
                return True
            else:
                continue
    return False

def get_polygon_center(coordinates):
    num_points = len(coordinates)
    
    x_sum = 0
    y_sum = 0
    
    for x, y in coordinates:
        x_sum += x
        y_sum += y
    
    centroid_x = x_sum / num_points
    centroid_y = y_sum / num_points
    
    return (centroid_x, centroid_y)