# Transform a Lexicon.xml file into an interactive HTML lexicon, optionally saving it in the calling folder.
#
#
# Security threats:
# Absolutely no sanitising of inputs is carried out so the arguments passed will be used to read in and output whatever filename is given.
#
# Sensible sanitisation of output would probably include:
# 1. No / allowed in first character of output filename.
# 2. No .. allowed anywhere.
# 3. Output filename must end in html (either xhtml or html).
#
# Thanks to
# https://stackoverflow.com/questions/16698935/how-to-transform-an-xml-file-using-xslt-in-python

#######
# 0. Imported libraries
import lxml.etree as ET
import os
import sys


#######
# 1. defaults
mpp = "/VMs/WinMacShare/My Paratext 8 Projects/"
mpp_fallbacks = ["C:\\My Paratext 8 Projects\\","C:\\My Paratext 9 Projects\\"]	# not yet used.
project = "AHS"
xml_filename = mpp+project+"/Lexicon.xml" # "Lexicon.xml" #
xsl_filename = os.path.dirname(os.path.realpath(__file__)) + "/glossy9.xsl"
interlinear_path = "/VMs/WinMacShare/My Paratext 8 Projects/AHS/Interlinear_en/"
output_filename = "Lexicons/AHS_Lexicon.xhtml"


#######
# 2. Helper utilities
def sanitise_output(filename):
	if len(filename)<2:
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

#######
# 3. sanity checks
if not(os.path.exists(xsl_filename)):
	print("\n\nThe required file "+xsl_filename+" doesn't exist. Stopping.")
	exit(1)

# check arguments
if (len(sys.argv)>1):
	if (sys.argv[1]=="-?" or sys.argv[1]=="--help"):
		print("\nGlossy:\n\tTransform a Paratext Lexicon.xml file into an interactive \n\tHTML lexicon, optionally saving it in the calling folder.\n")
		print("Syntax: glossy9.py [source-filename [output-filename]]")
		print("\tIf no source-filename is given then we use \n\t\t"+xml_filename)
		print("\tIf [output-filename] is - then output is to stdout")
		print("\tOtherwise default output-filename is \n\t\t"+output_filename)
	else:
		print("Args: "+str(len(sys.argv)))
		if sys.argv[1]=="ALL":
			walk_projects_dir()
		if sys.argv[1][0]!="-":
			xml_filename = sys.argv[1]
		if len(sys.argv)>2 and sys.argv[2]!="-":
			output_filename = sanitise_output(sys.argv[2])
		print("Input: "+xml_filename)
		print("Output: "+output_filename)

# check input exists
if not(os.path.exists(xml_filename)):
	print("\n\nThe input file "+xml_filename+" doesn't exist. Stopping.")
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
		if not(os.path.exists(os.path.dirname(output_filename))):
			print("\n\nThe output directory "+os.path.dirname(output_filename)+" doesn't exist. Stopping.")
			exit(2)

		transformed_html = ET.tostring(newdom, encoding="unicode") #pretty_print=True)
		outfile = open(output_filename, 'w')
		outfile.write(transformed_html)


########
# 5. MAIN PROGRAM STARTS HERE

transform_xml(xml_filename,xsl_filename,output_filename)

# Things to check
# - how are directory names handled in Windows? is / OK?
