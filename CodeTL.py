# 
# CodeTL
# 
# CodeTL automatically logs all your coding hours in Sublime
# 
# This plugin is developed for Sublime Text 3. And will probably
# not work properly under this version.
# 
# version: 0.0.1
# 
# Author: Albin Hubsch - albin.hubsch@gmail.com
# Github: 
# 

__version__ = '0.0.1'

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
# ST_VERSION = int(sublime.version())

PLUGIN_DIR = dirname(realpath(__file__))

SETTINGS_FILE = 'CodeTL.sublime-settings'

SETTINGS = {}

# 
# plugin_loaded
# 
def plugin_loaded():
	global SETTINGS
	SETTINGS = sublime.load_settings(SETTINGS_FILE)


# Get the project name
def getProjectName():
	window = sublime.active_window()
	projectName = window.project_file_name()
	return projectName.split(os.sep)[-1].replace('.sublime-project', '')

def getCurrentView():
	pass


# Get the project directory to create the logging folder
def getProjectDir():
	window = sublime.active_window()
	try:
		project_dir = window.project_data()['folders'][0]['path']
	except Exception as e:
		raise e

	return project_dir

# Get the logging dir + user folder
def getLoggingDir():
	return getProjectDir()+'/'+SETTINGS.get('CodeTL_folder')+'/'+SETTINGS.get('user')


# Prepare folders for logging
def createFolderStructure():
	# Try create the user folder
	try:
		if not os.path.exists(getLoggingDir()):
			os.makedirs(getLoggingDir())
			# Create logging file
			f = open(getLoggingDir()+'/timelog.json', 'w')
			f.write('[]')
			f.close()
	except Exception as e:
		pass


# 
def writeToJson(section):

	# Prepare data
	newSection = section
	
	try:
		# Open timelog file
		f = open(getLoggingDir()+'/timelog.json', 'r+')

		# Load json and time sections
		sections = json.load(f)

		# Append sections with the new section
		sections.append(newSection)

		# Reset file pointer and write to file, first 
		# one use in deploy mode, second one for debug mode
		f.seek(0)
		# f.write(json.dumps(x))
		json.dump(sections, f, indent=4)

	except ValueError as ve:
		print(ve)

	except Exception as e:
		print('e: ', e)
		raise e

	# Close file
	f.close()


# 
def writeToConclusion():
	pass


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
# CodeTL
# Description goes here
# 
class CodeTL(sublime_plugin.EventListener):

	def on_post_save(self, view):
		# print('Herrrororrororooooo')
		global PLUGIN_DIR
		# print(getProjectName())
		# 
		# writeToJson()
		
		print(ignoreFilter(view))
		
		# print(getProjectDir())

	def on_activated(self, view):
		createFolderStructure()

	def on_modified_async(self, view):
		self.lastCheck = time.time()
		# print(self.lastCheck)
		# createFolderStructure()
		
		# Check if file exists
			# if not create dir and file