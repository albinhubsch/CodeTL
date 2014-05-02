# 
# CodeTL
# 
# CodeTL automatically logs all your coding hours in Sublime.
# 
# This plugin is developed for Sublime Text 3. And will probably
# not work properly under this version.
# 
# The plugin logs time spent in a specific Sublime project. So make sure
# you have your projects properly setup. Otherwise it wont work at all.
# 
# The plugin supprts multiple users, just make sure you use a unique username
# in the plugins settingsfile
# 
# version: 1.0.0
# 
# Author: Albin Hubsch - albin.hubsch@gmail.com
# Github: https://github.com/albinhubsch/CodeTL.git
# 

__version__ = '1.0.0'

# 
# IMPORTS
# 
import sublime, sublime_plugin

import os
import sys
import time
import threading
import json
import datetime
from os.path import expanduser, dirname, realpath, join

# 
# CONSTANTS
# 

PLUGIN_DIR = dirname(realpath(__file__))

SETTINGS_FILE = 'CodeTL.sublime-settings'

SETTINGS = {}

LAST_ACTION = {
	'time': time.time()
}

CURRENT_STREAK = {
	'start': 0,
	'end': 0,
	'duration': 0
}

# 
# plugin_loaded
# 
def plugin_loaded():
	global SETTINGS
	SETTINGS = sublime.load_settings(SETTINGS_FILE)


# 
# Get the project name
# 
def getProjectName():
	window = sublime.active_window()
	projectName = window.project_file_name()
	return projectName.split(os.sep)[-1].replace('.sublime-project', '')

# 
# Get the project directory to create the logging folder
# 
def getProjectDir():
	window = sublime.active_window()
	try:
		project_dir = window.project_data()['folders'][0]['path']
	except Exception as e:
		raise e

	return project_dir

# 
# Get the logging dir + user folder
# 
def getLoggingDir():
	return getProjectDir()+'/'+SETTINGS.get('CodeTL_folder')+'/'+SETTINGS.get('user')

# 
# Prepare folders for logging
# 
def createFolderStructure():
	# Try create the user folder
	try:
		if not os.path.exists(getLoggingDir()):
			os.makedirs(getLoggingDir())
			# Create logging file
			f = open(getLoggingDir()+'/timelog.json', 'w')
			f.close()
	except Exception as e:
		pass


#
# Write a full timelog section to json file
#
def writeLogToJson(sections):
	
	try:
		# Open timelog file
		f = open(getLoggingDir()+'/timelog.json', 'w')
		json.dump(sections, f, indent=4)

	except ValueError as ve:
		# Open timelog file
		f = open(getLoggingDir()+'/timelog.json', 'w')
		json.dump([sections], f, indent=4)

	except Exception as e:
		raise e

	f.close()

# 
# load json file and return list with all timelog sections
# 
def loadTimelog():

	try:
		f = open(getLoggingDir()+'/timelog.json', 'r+')
		sections = json.load(f)
		f.close()

		return sections

	except Exception as e:
		return []


# 
# This method checks the current streak and takes a decision what to do.
# If it should use the last updated streak or insert a new one.
# 
def saveCurrentStreak():
	global CURRENT_STREAK

	sections = loadTimelog()

	try:
		if time.time() - sections[-1]['end'] < SETTINGS.get('streak_treshold')*60:
			CURRENT_STREAK['start'] = sections[-1]['start']
			refreshStreak()
			sections[-1] = CURRENT_STREAK
		else:
			CURRENT_STREAK['start'] = 0
			refreshStreak()
			sections.append(CURRENT_STREAK)

	except IndexError as e:
		refreshStreak()
		sections.append(CURRENT_STREAK)

	writeLogToJson(sections)
	

# 
# ignoreFilter
# Function returns true if the file in the current view contains anything
# within the filter rules, false if no match
# 
def ignoreFilter(view):
	if any(x in view.file_name() for x in SETTINGS.get('ignore')):
		return True
	return False


# 
# Method that updates the current streak and calculates the duration
# 
def refreshStreak():
	global CURRENT_STREAK

	et = time.time()

	if CURRENT_STREAK['start'] is 0:
		CURRENT_STREAK['start'] = et

	CURRENT_STREAK['end'] = et
	m, s = divmod(et - CURRENT_STREAK['start'], 60)
	h, m = divmod(m, 60)
	CURRENT_STREAK['duration'] = '%d:%02d:%02d' % (h, m, s)


# 
# Function that check if still in streak mode or time to break and 
# write streak to json
# 
def updateStreak():
	global CURRENT_STREAK
	global LAST_ACTION

	if time.time() - LAST_ACTION['time'] > SETTINGS.get('refresh_rate')*60:
		print('inne för att skriva')
		saveCurrentStreak()
		LAST_ACTION['time'] = time.time()
	else:
		refreshStreak()


# 
# CodeTL
# The CodeTL class that extends the sublime eventlistener
# 
class CodeTL(sublime_plugin.EventListener):

	# 
	# When a view is activated, check if folder structure exists
	# 
	def on_activated(self, view):
		createFolderStructure()

	# 
	# When file is modified check if it is time to write streak to file
	# 
	def on_modified_async(self, view):

		if not ignoreFilter(view) and SETTINGS.get('active'):
			updateStreak()