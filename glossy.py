# Keeps inserting the appropriate xsl line into the live dictionary tool so it keeps working even when lexicon.xml is written to
# David Rowbory: www.rowbory.co.uk
#
# Version: 1.6
#
#	Requires accompanying files:
#		display_glossies.html
#		lex_list_template.html
#		glossy.xsl
#		glossy.css
#
# Assumptions that may break:
#	There's a folder called %LOCALAPPDATA%\Paratext7.... with the log file in it.
#		You can edit this. It being missing will stop it keeping looking for changes.
#		(Broken on Win XP)
# 	Projects are stored in C:\My Paratext Projects\
#		You can edit this or supply the actual My Paratext Projects as the sole argument.
#		If path is wrong it just won't work.
#	This script must be in the glossy folder along with other helper files.
#
# Run from a batch file
# Takes 1 argument: the My Paratext Projects folder, with trailing slash (which tells glossy what the path separator is)
# unless you want it to default to look in C:\My Paratext Projects\

# Probably would be good to put all the helper files in a folder 'glossy' in the My Paratext Projects folder
# Then run everything from there.
#
# 1.5.2 workaround: look to see if we begin with ?xml
# if the first line begins <?xml then we need to just add our line in the 2nd line.

import os
import time
from datetime import date
import sys

def copy_and_prep_lexicon(project):
	'''Copy the lexicon file for the mentioned project into the glossy directory, attaching XSL on the way.'''
	this_lexicon_file = myParatextProjects+project+path_sep+lexicon_file
	print "Opening ",this_lexicon_file
	f_pt = open(this_lexicon_file,"rb")
	f_glossy = open(project+glossy_lexicon,"wb")
	line = f_pt.readline()
	line_count = 0
	if (line == ""):
		print this_lexicon_file,"is empty"
	else:
		if (line[:8] == "<Lexicon"):
			print "  First line begins with <Lexicon..."
			#if (line[:1]== "\xFE"):
			f_glossy.write("\xFE\xFF")
			#	line = line[2:]
			print "   Assuming a BOM here."
			f_glossy.write('<?xml version="1.0" encoding="utf-8"?>')
			f_glossy.write(xsl_line)	# but occasionally esp with old lexicon files, the XML statement isn't there at the start of the file (naughty!)
			f_glossy.write(line)
		else:
			f_glossy.write(line)		# if first line begins with <?xml then we need to insert our style info on the 2nd line
			f_glossy.write(xsl_line)
		line = f_pt.readline()	# now echo out the rest of the lines again
		while(line != ""):
			f_glossy.write(line)
			line = f_pt.readline()
			line_count += 1

	f_pt.close()
	f_glossy.close()

def write_nav_bar(nav_links):
	'''Write out the navigation bar.'''

	f_list_template = open(glossy_index_t,"rb")	# read the source file (template)
	list_template = f_list_template.read()
	f_list_template.close()
	# this plonks the nav_links into the place in the template file that has %s
	list_template = list_template % nav_links	# NOTE more modern code python 2.6+ should use .format('lex_links',lex_list_links)

	f_list = open(glossy_index,"w+b")	# with write access
	f_list.write(list_template)
	f_list.close()

def get_pt_logfile():
	'''Returns the full path of the pt log file or "" if it doesn't exist.'''
	pt_log = ""
	if os.path.exists(os.environ["LOCALAPPDATA"]):
		for folder in os.listdir(os.environ["LOCALAPPDATA"]):
			if folder[0:9] == "Paratext7":
				if os.path.isdir(os.environ["LOCALAPPDATA"]+path_sep+folder):
					pt_log = os.environ["LOCALAPPDATA"]+path_sep+folder+path_sep+"ParatextLog.log"
		return pt_log
	else:
		return ""

def is_pt_used_recently():
	'''Return true if we think Paratext is still open and false if not.'''
	recent_timeout_mins = 120
	if os.path.exists(pt_logfile):
		print "Log file "+pt_logfile+" changed "+str(os.path.getmtime(pt_logfile))
		return os.path.getmtime(pt_logfile)>time.time()-(60*recent_timeout_mins)
	return 1
##################################### Program starts here #####################################

# 1. Starting values

available_lexicons = {}
xsl_line 	= '<?xml-stylesheet type="text/xsl" href="glossy.xsl"?><!-- Added for transformation '+str(date.today())+'-->'
lexicon_file 	= "Lexicon.xml"	#The original file
glossy_lexicon	= "_Lexicon.xml"	# The suffix added to the project name as name of the copied lexicon.
glossy_index	= "lex_list.html"
glossy_index_t	= "lex_list_template.html"
glossy_index_rep= "______"

path_sep 	= "\\"
myParatextProjects = 'C:\\My Paratext Projects\\'

pt_logfile = get_pt_logfile()
recent_timeout_mins = 120

if len(sys.argv)>1:	# command line arguments
	if sys.argv[1]=="--help":
		print "Pass the My Paratext Projects folder, with trailing slash unless you want it to default to look in __"+myParatextProjects+"__"
		quit()
	myParatextProjects = sys.argv[1]
	if str(sys.argv[1])[:1]=="/":
		path_sep = "/"

# 2. Look through whole My Paratext Projects folder
print "Looking for project folders in folder '" + myParatextProjects + "'"

for project in os.listdir(myParatextProjects):
	if project[0:1] == ".":
		None #print "Ignoring hidden folder "+project
	else:
		if os.path.isdir(myParatextProjects+project):
			this_lex = myParatextProjects+project+path_sep+lexicon_file
			if os.path.exists(this_lex):
				if os.path.getsize(this_lex)>500:
					print "Found Lexicon: " + project
					available_lexicons[project] = os.path.getmtime(this_lex)
				else:
					print "Ignoring almost empty Lexicon: " + project

# 3. Build the navigation bar

lex_list_links = ""
for project, l in available_lexicons.iteritems():
	copy_and_prep_lexicon(project)
	lex_list_links += '<a href="'+project+glossy_lexicon+'" target="main">'+project+'</a> &bull; '

write_nav_bar(lex_list_links)
print "Now watching for changes. Close this window or hold down ctrl then tap C to stop this."

# 4. Perpetual watch for
pt_log_file = get_pt_logfile();
keep_watching = 1
while keep_watching:
	time.sleep(30) # Poll every 30s
	# Todo: Find a way to work out whether Pt still running and if not, then quit.

	for project in os.listdir(myParatextProjects):
		if project[0:1] != "." and os.path.isdir(myParatextProjects+project):
			this_lexicon_file = myParatextProjects + project + path_sep + lexicon_file
			if os.path.exists(this_lexicon_file):
				if not(project in available_lexicons):
					if os.path.getsize(this_lexicon_file)>500:
						print "New Lexicon available: " + project
						available_lexicons[project] = 0
						lex_list_links += '<a href="'+project+glossy_lexicon+'" target="main">'+project+'</a> &bull; '
						write_nav_bar(lex_list_links)
					# ignore if a new lexicon is very small
				else:
					if (available_lexicons[project] < os.path.getmtime(this_lexicon_file)):
						print "Changed Lexicon: " + project #, " Before: ",str(available_lexicons[project]) , " After: "+ str(os.path.getmtime(this_lexicon_file))
						copy_and_prep_lexicon(project)
	keep_watching = is_pt_used_recently()
