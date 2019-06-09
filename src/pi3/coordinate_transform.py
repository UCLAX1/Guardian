import numpy as np

# Same as translatedAnimation, but directly changes the coordinates given
def translate(coordinates, x, y, z):
    v = np.array([x,y,z])
    s = coordinates.shape
    num_rows = s[0]
    for ind in range(num_rows):
        coordinates[ind,:] = coordinates[ind,:] + v

# Same as scaledAnimation, but directly changes the coordinates given
def scale(coordinates, scalingFactor):
    coordinates = coordinates * scalingFactor

# Same as rotatedAnimation, but directly changes the coordinates given
def rotate(coordinates, rotateAngle):
    R_matrix = [np.cos(rotateAngle),np.sin(rotateAngle),0],[-1*np.sin(rotateAngle),np.cos(rotateAngle),0],[0,0,1]
    coordinates[:,:] = np.matmul(coordinates,R_matrix)
    #print("Post rotate")
    #print(coordinates)

