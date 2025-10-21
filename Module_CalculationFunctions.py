import math # used for stuff like square root, sine, cos
import numpy as np # needed to set axis for graph
import matplotlib.pyplot as plt # library used to plot trajectory



def quadratic_solver(a, b, c):
    """
    This function solves quadratic equations, which 
    are is needed when calculating time period when
    Height of target is lower than origin. (y < 0)
    
    Sample : 
    3x^2 + 5x + 2 = 0 
    a=3, b=5, c=2
    """

    discriminant = b**2-4*a*c 

    if discriminant < 0:
        print("This equation has no real solution")
    elif discriminant == 0:
        root_1 = (-b + math.sqrt(discriminant)) / (2 * a)
    
        return (root_1)
    else:
        root_1 = (-b + math.sqrt(discriminant)) / (2 * a)
        root_2 = (-b - math.sqrt(discriminant)) / (2 * a)

        # Choose the positive root if it exists
        if root_1 > 0:
            return root_1
        elif root_2 > 0:
            return root_2

        print("This equation has two solutions: ", root_1, " and", root_2)



def angle_formula(speed, gravity, distance_x, vector_y):
    """
    Calculates possible Pitch launch angles given its initial speed,
    gravitational acceleration (gravity), horizontal distance  to the target, and vertical (y)
    displacement from the origin. (Two possible angles)
    """

    angle_1 = math.degrees(
        math.atan((speed**2 + math.sqrt(speed**4 - gravity**2 * distance_x**2 - gravity * 2 * vector_y * speed**2)) / (gravity * distance_x)))
    print("p theta: ", angle_1)
    angle_2 = math.degrees(
        math.atan((speed**2 - math.sqrt(speed**4 - gravity**2 * distance_x**2 - gravity * 2 * vector_y * speed**2)) / (gravity * distance_x)))
    print("n theta: ", angle_2)

    return angle_1, angle_2


def calculate_angle_and_time(gravity, speed, vector_x, vector_y, vector_z):
    """
    Firtly, horizontal distance (hx) is found calculated
    Where its used in angle_formula() which calculates 
    pitch angles. Later corresponding times periods are calculated
    """
    # Make a variable for horizontal distance
    distance_x = 0

    # If target is directly infront, set hx to be x
    if vector_x > 0 and vector_z == 0:
        distance_x = vector_x
    
    # If target is directly behind, set it as -x 
    elif vector_x < 0 and vector_z == 0:
        distance_x = -vector_x

    # If target is left, set it as z
    elif vector_x == 0 and vector_z > 0:
        distance_x = vector_z

    # If target is right, set it as -z
    elif vector_x == 0 and vector_z < 0:
        distance_x = -vector_z

    # Target cannot be at origin
    elif vector_x == 0 and vector_z == 0:
        raise ZeroDivisionError()
    
    # Pythagoras theorem, sets hx to be the hypotenuse of x and z
    else:
        distance_x = math.sqrt(vector_x**2 + vector_z**2)

    # as distance_x is decided, we can now call the function to get angles
    angle_1, angle_2 = angle_formula(speed, gravity, distance_x, vector_y)

    
    if vector_y >= 0:
        time_1 = distance_x / (speed * math.cos(math.radians(angle_1)))
        print("p time: ", time_1)
        time_2 = distance_x / (speed * math.cos(math.radians(angle_2)))
        print("n time: ", time_2)
    elif vector_y < 0:
        time_1 = quadratic_solver(0.5 * -gravity, speed * math.sin(math.radians(angle_1)), -vector_y)
        print("p time: ", time_1)
        time_2 = quadratic_solver(0.5 * -gravity, speed * math.sin(math.radians(angle_2)), -vector_y)
        print("n time: ", time_2)

    return angle_1, angle_2, time_1, time_2



def calculate_direction(vector_x, vector_z):
    """
    Here, the yaw rotation is calculated using trigonometry
    vector_x -> forward
    vector_z -> left
    """

    if vector_x > 0 and vector_z > 0:
        direction = math.degrees(math.atan(vector_z/vector_x))
        return f"Rotate left by {direction}°"
        
    elif vector_x < 0 and vector_z > 0:
        direction = 180 - math.degrees(math.atan(vector_z/-vector_x))
        return f"Rotate left by {direction}°"
    
    elif vector_x == 0 and vector_z > 0:
        direction = 90
        return f"Rotate left by {direction}°"
        
    elif vector_x > 0 and vector_z < 0:
        direction = math.degrees(math.atan(-vector_z/vector_x))
        return f"Rotate right by {direction}°"
    
    elif vector_x < 0 and vector_z < 0:
        direction = 180 - math.degrees(math.atan(-vector_z/-vector_x))
        return f"Rotate right by {direction}°"
    
    elif vector_x == 0 and vector_z < 0:
        direction = 90
        return f"Rotate right by: {direction}°"
    
    elif vector_x < 0 and vector_z == 0:
        direction = 180
        return f"Rotate by {direction}°"

    elif vector_x > 0 and vector_z == 0:
        return "No need to rotate left or right."



def recommended_angle(time_1, time_2, angle_1, angle_2):
    """
    Here angle with quickest trajectory is decided and returned.
    """
    # fastest is the smallest value  out of the two times
    fastest = min(time_1, time_2)
    if fastest == time_1:
        return angle_1, time_1
    else:
        return angle_2, time_2    



def plot(sub_plot,canvas, speed, vector_y, graph_fastest_angle, graph_fastest_time):

    """
    Plot the trajectory of projectile using MatPlotLib

    """

    fastest_angle =  graph_fastest_angle
    fastest_time = graph_fastest_time

    sub_plot.clear()
    print(f"u:{speed} y:{vector_y} fastest_angle:{fastest_angle} fastest_time: {fastest_time}")    


    def f(x,a,b,c):
        return -a*x**2 + b*x + c

    # vertex equation for x and y coordinates
    def parabola_vertex(a, b, c):
        x_coordinate = (-b / (2 * a))
        y_coordinate = -(((4 * a * c) - (b * b)) / (4 * a))
        return x_coordinate, y_coordinate

    def max_hight(speed, fastest_angle, vector_y):
        def above_zero(speed, fastest_angle):
            height = (speed * math.sin(math.radians(fastest_angle)))**2 / (2*9.81)  
            return height
        
        def below_zero(vector_y):
            height = -vector_y
            return height

        if vector_y >= 0:
            max = above_zero(speed, fastest_angle)
        elif vector_y < 0:
            max = below_zero(vector_y)
        return max


    def horizontal_distance(speed, fastest_angle, fastest_time):
        distance_x = speed * math.cos(math.radians(fastest_angle)) * fastest_time
        return distance_x

    # horizontal distance
    distance_x = horizontal_distance(speed, fastest_angle, fastest_time)
    print(f"distance_x = {distance_x}")

    # Original parabola without compression
    if vector_y >= 0:
        a = 1 
        b = distance_x
        c = 0

        # set up the x axis
        xlist = np.linspace(0,b,num=1000)

    elif vector_y < 0:

        a = 1
        b = 0
        c = distance_x * -distance_x
        
        # set up the x axis
        xlist = np.linspace(0,distance_x,num=1000)


    # coordinates of parabola's vertex
    print(a, b, c)
    vertex_x, vertex_y = parabola_vertex(a, b, c)
    print(f"vertex_x = {vertex_x}")
    print(f"vertex_y = {vertex_y}")


    # max hight the actual projectile reaches
    max = max_hight(speed, fastest_angle, vector_y)
    print(f"max = {max}")


    # compressing the parabola to real values
    if vector_y >= 0:
        a = max/vertex_y 
        b = (b*max) / vertex_y
        c = 0
    elif vector_y < 0:
        a = max/vertex_y
        b = 0
        c = max


    ylist = f(xlist,a,b,c)


    plt.figure(num=0, dpi=120)
    
    sub_plot.plot(xlist,ylist)
    canvas.draw()

# ---------------------------------------