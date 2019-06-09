import numpy as np

# path is a Nx3 numpy array
def scale_path(path,a=1,b=1,c=1,x=1,y_scale=1/2,z_scale=1/2,y_offset=0,z_offset=0):

	# Zero out the x coordinate
	zero_out_mat = [[0,0,0],
					[0,1,0],
					[0,0,1]]
	path = np.matmul(path,zero_out_mat)

	tot_len = a+b+c
	sec_thr_len = b+c
	theta = np.arccos((x*tot_len-a)/(sec_thr_len))
	radius = (sec_thr_len)*np.cos(theta)

	#print("Raw path",path)

	path = path*radius;

	#print("Path adjusted for radius",path)

	N = path.shape[0]

	x_pos = x*tot_len
	y_off = y_offset*tot_len
	z_off = z_offset*tot_len


	scaling_matrix = [[0,       0,       0       ],
					  [0,       y_scale, 0       ],
					  [0,       0,       z_scale]]
	#print("Scaling matrix: ",scaling_matrix)
	path = np.matmul(path,scaling_matrix)
	#print("Path after multiplication",path)

	path = path + np.concatenate((x_pos*np.ones((N,1)),y_off*np.ones((N,1)),z_off*np.ones((N,1))),1)
	#print("Path after offset",path)

	return path