# Transform a Lexicon.xml file into an interactive HTML lexicon, optionally saving it in the calling folder.
#
#
# Security threats:
# Only the slightest sanitising of inputs is carried out so the arguments passed will be used to read in and output whatever filename is given.
#
# Sensible sanitisation of output would probably include:
# 1. No / allowed in first character of output filename.
# 2. No .. allowed anywhere.
# 3. Output filename must end in html (either xhtml or html).
#
# Thanks to
# https://stackoverflow.com/questions/16698935/how-to-transform-an-xml-file-using-xslt-in-python
#
# Version history
#

#######
# 0. Imported libraries
import lxml.etree as ET
import os
import sys


#######
# 1. defaults
mpp = "/Users/Shared/VMs/WinMacShare/My Paratext 8 Projects/"
mpp_fallbacks = ["C:\\My Paratext 8 Projects\\","C:\\My Paratext 9 Projects\\"]	# not yet used.
mpp_possibilities = ["C:\\My Paratext 8 Projects\\","C:\\My Paratext 9 Projects\\","/Users/Shared/VMs/WinMacShare/My Paratext 8 Projects/","Z:\\WinMacShare\\My Paratext 8 Projects\\"]
project = "AHS"

xml_filename_suffix = "Lexicon.xml" # "Lexicon.xml" #
xsl_filename = os.path.dirname(os.path.realpath(__file__)) + "/glossy9.xsl"
interlinear_path_suffix = "/AHS/Interlinear_en/"
output_filename = "Lexicons/AHS_Lexicon.xhtml"

#######
# 2. Helper utilities
def sanitise_output(filename):
	if filename=="-":
		return "-"
	elif len(filename)<2:
		return ""
	elif filename[0]=="/":
		return ""

	if filename[-4:]=="html":
		return filename
	else:
		return filename+".xhtml"
	return filename

def walk_projects_dir(my_paratext_projects,outpath):
	for dirpath, dirnames, filenames in os.walk(my_paratext_projects):
		for filename in filenames:
			if filename.endswith(('Lexicon.xml', '.txt')):
				dom = ET.parse(dirpath + filename)
				xslt = ET.parse(xsltfile)
				transform = ET.XSLT(xslt)
				newdom = transform(dom)
				transformed_file = unicode(ET.tostring(newdom, pretty_print=True))
				outfile = open(outpath + filename, 'a')
				print("dirpath:"+dirpath+"  filename:"+filename)
				#outfile.write(transformed_file)

def find_mpp(folder_list):
	for a_folder in folder_list:
		if (os.path.exists(a_folder)):
			return a_folder
	return "";

def get_xml_filename():
	return mpp+project+"/"+xml_filename_suffix

#######
# 3. sanity checks
if sys.version_info[0]<3:
	print("\n\nError:\nIt seems we are running in an old version of python.")
	print("\tVersion: "+str(sys.version_info[0])+"."+str(sys.version_info[1])+"."+str(sys.version_info[2]))
	print("I need Python 3 or more to run. Try running me with \n\tpython3 glossy9.py [input] [output].\n\n")
	exit(1)

if not(os.path.exists(xsl_filename)):
	print("\n\nThe required file "+xsl_filename+" doesn't exist. Stopping.")
	exit(1)

mpp = find_mpp(mpp_possibilities)

# check arguments
# 1: project code, eg AHS
# 2: output file
# 3: my-paratext-projects
if (len(sys.argv)>1):
	if (sys.argv[1]=="-?" or sys.argv[1]=="--help"):
		print("\nGlossy:\tTransform a Paratext Lexicon.xml file into an interactive \n\tHTML lexicon, optionally saving it in the calling folder.\n")
		print("Syntax: glossy9.py [ALL | project [output-filename [my-paratext-projects-folder]]]")
		print("\tALL means produce lexicons for all the projects we find.")
		print("\tIf no arguments are given then we use \n\t\t"+get_xml_filename())
		print("\tIf output-filename is - then output is to stdout")
		print("\tOtherwise default output-filename is \n\t\t"+output_filename)
		print("\n\tCurrently the My Paratext Projects folder I find is: \n\t\t"+mpp)
		exit(0)
	else:
		if sys.argv[1][0]!="-":
			project = sys.argv[1]
		if len(sys.argv)>2:
			output_filename = sanitise_output(sys.argv[2])
		if len(sys.argv)>3:
			mpp = sanitise_output(sys.argv[3])
		if sys.argv[1]=="ALL":
			walk_projects_dir(mpp)
		if output_filename!="-":
			print("Args: "+str(len(sys.argv)))
			print("\t1.Project: \t"+project)
			print("\t2.Output: \t"+output_filename)
			print("\t3.My Paratext Projects: "+mpp)

# check input exists
if not(os.path.exists(get_xml_filename())):
	print("\n\nThe input file "+get_xml_filename()+" doesn't exist. Stopping.")
	exit(2)

#######
# 4. Main transform and output
def transform_xml(input_xml_filename,transform_xsl_filename,output_filename):
	# parse and transform
	dom = ET.parse(input_xml_filename)
	xslt = ET.parse(transform_xsl_filename)
	transform = ET.XSLT(xslt)
	newdom = transform(dom)

	# output appropriately
	if output_filename=="" or output_filename=="-":
		print((ET.tostring(newdom, pretty_print=True)))
	else:
		# also check output dir exists
		print("Directory for output: "+os.path.dirname(output_filename))
		if not(os.path.exists(os.path.dirname(output_filename))):
			print("\n\nThe output directory "+os.path.dirname(output_filename)+" doesn't exist. Stopping.")
			exit(2)

		transformed_html = str(ET.tostring(newdom, pretty_print=True),'UTF-8','ignore')
		outfile = open(output_filename, 'w')
		outfile.write(transformed_html)


########
# 5. MAIN PROGRAM STARTS HERE

transform_xml(get_xml_filename(),xsl_filename,output_filename)

# Things to check
# - how are directory names handled in Windows? is / OK?
