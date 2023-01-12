# Keeps inserting the appropriate xsl line into the live dictionary tool so it keeps working even when lexicon.xml is written to
# David Rowbory: www.rowbory.co.uk
#
# Run from a batch file
# Takes 1 argument: the My Paratext Projects folder, with trailing slash (which tells glossy what the path separator is)
# unless you want it to default to look in C:\My Paratext Projects\

# Probably would be good to put all the helper files in a folder 'glossy' in the My Paratext Projects folder
# Then run everything from there

import os
import time
from datetime import date
import sys

def copy_and_prep_lexicon(project):
	this_lexicon_file = myParatextProjects+project+path_sep+lexicon_file
	print "Opening ",this_lexicon_file
	f_pt = open(this_lexicon_file,"rb")
	f_glossy = open(project+glossy_lexicon,"wb")
	line = f_pt.readline()
	line_count = 0
	if (line != ""):
		f_glossy.write(line)
		f_glossy.write(xsl_line)
		line = f_pt.readline()
		while(line != ""):
			f_glossy.write(line)
			line = f_pt.readline()
			line_count += 1
	else:
		print this_lexicon_file,"is empty"
	f_pt.close()
	f_glossy.close()

def write_nav_bar(nav_links):
	# Write out the navigation bar
	
	f_list_template = open(glossy_index_t,"rb")
	list_template = f_list_template.read()
	f_list_template.close()
	list_template = list_template % nav_links	# more modern code 2.6+ should use .format('lex_links',lex_list_links)
	
	f_list = open(glossy_index,"w+b")
	f_list.write(list_template)
	f_list.close()
	
# 1. Starting values

available_lexicons = {}
xsl_line 	= '<?xml-stylesheet type="text/xsl" href="../glossy/glossy_no_highlight.xsl"?><!-- Added for transformation '+str(date.today())+'-->'
lexicon_file 	= "Lexicon.xml"	#The original file
glossy_lexicon	= "_Lexicon.xml"	# The suffix added to the project name as name of the copied lexicon.
glossy_index	= "lex_list.html"
glossy_index_t	= "lex_list_template.html"
glossy_index_rep= "______"

path_sep 	= "\\"
myParatextProjects = 'C:\\My Paratext Projects\\'

if len(sys.argv)>1:	# command line arguments
	if sys.argv[1]=="--help":
		print "Pass the My Paratext Projects folder, with trailing slash unless you want it to default to look in "+myParatextProjects
		quit()
	myParatextProjects = sys.argv[1]
	if str(sys.argv[1])[:1]=="/":
		path_sep = "/"

# 2. Look through whole My Paratext Projects folder

for project in os.listdir(myParatextProjects):
	if project[0:1] == ".":
		print "Ignore hidden folder "+project
	else:
		if os.path.isdir(myParatextProjects+project):
			if os.path.exists(myParatextProjects+project+path_sep+lexicon_file):
				print "Found Lexicon: " + project
				available_lexicons[project] = os.path.getmtime(myParatextProjects+project+path_sep+lexicon_file)
		else:
			print "I can't find the folder "+(myParatextProjects+project)

# 3. Build the navigation bar

lex_list_links = ""
for project, l in available_lexicons.iteritems():
	copy_and_prep_lexicon(project)
	lex_list_links += '<a href="'+project+glossy_lexicon+'" target="main">'+project+'</a> &bull; '

write_nav_bar(lex_list_links)

# 4. Perpetual watch for 
while 1:
	time.sleep(30) # Poll every 30s
	# Todo: Find a way to work out whether Pt still running and if not, then quit.
	
	for project in os.listdir(myParatextProjects):
		if project[0:1] != ".":
			if os.path.isdir(myParatextProjects+project):
				this_lexicon_file = myParatextProjects + project + path_sep + lexicon_file
				if os.path.exists(this_lexicon_file):
					if not(project in available_lexicons):
						print "New Lexicon available: " + project
						available_lexicons[project] = 0
						lex_list_links += '<a href="'+project+glossy_lexicon+'" target="main">'+project+'</a> &bull; '
						write_nav_bar(lex_list_links)
					if (available_lexicons[project] < os.path.getmtime(this_lexicon_file)):
						print "Changed Lexicon: " + project, " Before: ",str(available_lexicons[project]) , " After: "+ str(os.path.getmtime(this_lexicon_file))
						copy_and_prep_lexicon(project)