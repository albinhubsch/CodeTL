# 
# CodeTL
# 
# CodeTL automatically logs all your coding hours in Sublime
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
from os.path import expanduser, dirname, realpath, join

# 
# CONSTANTS
# 
ST_VERSION = int(sublime.version())

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

# Get the project directory to create the logging folder
def getProjectDir():
	window = sublime.active_window()
	try:
		project_dir = window.project_data()['folders'][0]['path']
	except Exception as err:
		raise err
	
	return project_dir

# Prepare folder for logging
def createTimeLoggingFolder(dir):
	if not os.path.exists(dir+'/'+SETTINGS.get('CodeTL_folder')):
		os.makedirs(dir+'/'+SETTINGS.get('CodeTL_folder'))

# 
# CodeTL
# Description goes here
# 
class CodeTL(sublime_plugin.EventListener):

	def on_post_save(self, view):
		print('Herrrororrororooooo')
		global PLUGIN_DIR
		print(getProjectName())
		
		print(getProjectDir())

	def on_activated(self, view):
		print('\n')
		print(getProjectName())

		# createTimeLoggingFolder(getProjectDir())

	def on_modified(self, view):
		pass
		# Check if file exists
			# if not create dir and file