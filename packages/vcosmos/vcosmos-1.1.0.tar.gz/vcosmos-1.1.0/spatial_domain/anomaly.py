import numpy as np
import pandas as pd
import inspect
import seaborn as sns
import matplotlib.pyplot as plt

class O_Sieve:
	def __init__(self, data, column, tsf=1, bsf=1):

		if len(inspect.signature(O_Sieve.__init__).parameters)-1 !=4:
			raise TypeError('Invalid number of arguments')

		self.column=column # Name of the column
		self.data=data # Dataframe
		self.tsf=tsf # Top scaling factor.
		self.bsf=bsf # Bottom scaling factor.
		
		if not isinstance(self.column,str):
			raise TypeError('The variable \'column\' must be string.')
		
		if not isinstance(self.data,pd.DataFrame):
			raise TypeError('The variable \'data\' must be pandas dataframe.')
		
		self.xmin=self.data.index.min()
		self.xmax=self.data.index.max()
		self.ymin=self.data[self.column].min()
		self.ymax=self.data[self.column].max()
		self.zval=np.mean(np.square(self.data[self.column]))

		print('Filtering Initiated....')
	
	def hcps_plot(self):
		fig = plt.figure(figsize=(14,6))
		ax = fig.add_subplot(131,projection='3d')
		ax.scatter(self.data.index, self.data[self.column], np.square(self.data[self.column]), s=0.5,color='black')
		ax.scatter(np.mean(self.data.index),np.mean(self.data[self.column]),self.zval,color='orange',s=300)
		ax.plot_surface([[self.xmin, self.xmax], [self.xmin, self.xmax]], [[self.ymin, self.ymin], [self.ymax, self.ymax]], np.array([[self.zval, self.zval], [self.zval, self.zval]]), alpha=0.5,color='blue')
		ax.set_xlabel('X-axis')
		ax.set_ylabel('Y-axis')
		ax.set_zlabel('Z-axis')
		z_dist_plane1, z_dist_plane2=self.split_learning()
		ax.plot_surface([[self.xmin, self.xmax], [self.xmin, self.xmax]], [[self.ymin, self.ymin], [self.ymax, self.ymax]], np.array([[z_dist_plane1, z_dist_plane1], [z_dist_plane1, z_dist_plane1]]), alpha=0.5,color='red')
		ax.plot_surface([[self.xmin, self.xmax], [self.xmin, self.xmax]], [[self.ymin, self.ymin], [self.ymax, self.ymax]], np.array([[z_dist_plane2, z_dist_plane2], [z_dist_plane2, z_dist_plane2]]), alpha=0.5,color='red')
		
		ax1 = fig.add_subplot(132)
		sns.boxplot(self.data[self.column]).set_title('Pre-Cleaning')

		ax2 = fig.add_subplot(133)
		sns.boxplot(self.new_data[self.column]).set_title('Post-Cleaning')
		plt.tight_layout()
		return plt.show()

	def split_learning(self):
		centre = np.array([np.mean(self.data.index), np.mean(self.data[self.column]),self.zval])
		top_distances, bottom_distances =[],[]
		x=self.data.index
		y=self.data[self.column]
		z=np.square(self.data[self.column])
		
		for ind, val in enumerate(z):
			if val >= self.zval:
				top_distances.extend(np.linalg.norm(np.column_stack((x[ind], y[ind], z[ind])) - centre, axis=1).tolist())
			else:
				bottom_distances.extend(np.linalg.norm(np.column_stack((x[ind], y[ind], z[ind])) - centre, axis=1).tolist())
				
		def median_break(data):
			sorted_data=sorted(data)
			if len(sorted_data) % 2 !=0:
				return x[len(sorted_data)//2], y[len(sorted_data)//2], (z[len(sorted_data)//2], 0), sorted_data[len(sorted_data)//2]
			else:
				p1=sorted_data[len(sorted_data)//2]
				p2=sorted_data[len(sorted_data)//2+1]
				med=(p1+p2)/2
				return x[len(sorted_data)//2], y[len(sorted_data)//2], (z[len(sorted_data)//2],z[len(sorted_data)//2+1]), med
			
		u_x,u_y,u_z,up_med =median_break(top_distances)
		 
		if u_z[1]!=0:
			upper_point=np.array([u_x,u_y,(u_z[0]+u_z[1])/2])
		else:
			upper_point=np.array([u_x,u_y,u_z[0]])
			
		upper_distribution_length = np.linalg.norm(upper_point-centre)
		
		l_x, l_y, l_z, lo_med = median_break(bottom_distances) 
		
		if l_z[1]!=0:
			lower_point=np.array([l_x,l_y,(l_z[0]+l_z[1])/2])
		else:
			lower_point=np.array([l_x,l_y,l_z[0]])

		lower_distribution_length = np.linalg.norm(lower_point-centre)

		z_dist_plane1= self.zval + (upper_distribution_length*self.tsf) 
		z_dist_plane2= self.zval - (lower_distribution_length*self.bsf)

		return z_dist_plane1, z_dist_plane2

	def encompassing_points(self,z,d1,d2):
		if (z > d1)  or (z < d2):
			return 0 # OUTLIER
		else:
			return 1
		
	def filtered_data(self):
		z_dist_plane1, z_dist_plane2=self.split_learning()
		indices=[self.encompassing_points(n, z_dist_plane1, z_dist_plane2) for n in np.square(self.data[self.column])]
		self.data['Status']=indices
		self.new_data=self.data.loc[self.data['Status'] == 1].drop(columns='Status').reset_index(drop=True)
		print('Filtering Complete.')
		print('Ouliers Removed:',self.data.shape[0]-self.new_data.shape[0])
		return self.new_data 


