import streamlit as st
import pandas as pd
import numpy as np
import cv2 as cv
import dfply as df
from PIL import Image
#import matplotlib.pyplot as plt
from datetime import datetime



class trainingUI:
	def __init__(self):
		#load database
		self.database = pd.read_excel('mockDatabase.xlsx')

		#load logo
		self.logo = np.array(Image.open('standbic.jpg'))
		
		self.today = datetime.now()

	def build(self):
		st.title('Training Explorer')
		
		st.sidebar.text('Options')
		self.action_to_do = st.sidebar.selectbox('What would you like to do?', ('View Skills', 'Add New Skill', 'View Overall Performance'))
		self.a_number = st.sidebar.text_input('Enter employee number or name')
		#get input from user: view skills or add new skills
		if self.action_to_do == 'View Skills':
			self.view_skills = True
		elif self.action_to_do == 'Add New Skill':
			self.add_skill = True
		elif self.action_to_do == 'View Overall Performance':
			self.overall = True

		try:
			if self.view_skills and len(self.a_number) > 0:
				#process query
				try:
					q_ = (self.database >> df.mask(self.database.EmployeeNum==self.a_number))
					emp_name = q_['ResourceName'].unique()[0]
					a_number = q_['EmployeeNum'].unique()[0]
					bu = q_['Capability'].unique()[0]
					courses = q_[['CourseName', 'Status']]
					courses.index = np.arange(0, q_.shape[0])

					st.header('Employee Information')
					self.employee_im = np.array(Image.open('blank_profile.png'))
					st.image(cv.resize(self.employee_im, (150,150), cv.INTER_CUBIC), use_column_width=False)
					st.subheader('Name: {}'.format(emp_name))
					st.write('Employee Number: {}'.format(a_number))
					st.write('Capability: {}'.format(bu))
					st.write('Courses:')
					st.table(courses)
				
					#filter to get relevant information
					total_courses = len(q_['Status'])
					completed = len((q_ >> df.mask(q_.Status=='completed')))
					in_progress = (len((q_ >> df.mask(q_.Status=='in-progress'))))
					started = len((q_ >> df.mask(q_.Status=='registered-but-not-started')))
					
					#write information to user
					st.write('total courses: {}'.format(total_courses))
					st.write('completed: {}'.format(completed))
					st.write('in progress: {}'.format(in_progress))
					st.write('started: {}'.format(started))

					st.write('Have you finished any courses?')
					finished_courses = st.multi_select('',(''))


				except IndexError:
					st.write('Error: value entered not found in database')
		except AttributeError:
			pass

		try:
			if self.add_skill and len(self.a_number) > 0:
				st.write('Adding new skill for {}'.format(self.a_number))
				course_list = []
				for val in self.database['CourseName'].unique():
					course_list.append(val)
				self.courses_chosen = st.multiselect('The following are available', tuple(course_list))
				st.subheader('You have chosen the following courses')
				for course in self.courses_chosen:
					st.write(course)
				if st.button('Accept'):
					if len(self.courses_chosen) > 0:
						self.register_new_courses( self.a_number, self.courses_chosen)
				elif len(self.courses_chosen) == 0:
					st.write('Error: You did not select any courses')
		except AttributeError:
			pass

		try:
			if self.overall and len(self.a_number) > 0:
				st.write('Viewing Overall Perfomance')
				st.write(self.database)
		except AttributeError:
			pass

		st.sidebar.image(self.logo, use_column_width=True)
		st.sidebar.text(self.today)

	def register_new_courses(self, emp_num, courses):
		for x in courses:
			print('registering {0} for {1}'.format(emp_num, x))
	



if __name__ == '__main__':
	trainingUI().build()