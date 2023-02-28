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

import lxml.etree as ET
import os
import sys

# defaults
mpp = "/VMs/WinMacShare/My Paratext 8 Projects/"
project = "AHS"
xml_filename = mpp+"AHS/Lexicon.xml" # "Lexicon.xml" #
xsl_filename = os.path.dirname(os.path.realpath(__file__)) + "/glossy9.xsl"
interlinear_path = "/VMs/WinMacShare/My Paratext 8 Projects/AHS/Interlinear_en/"
output_filename = "Lexicons/LexiconLDB.xhtml"

def main():
	# analyse arguments
	if (len(sys.argv)>1):
		if (sys.argv[1]=="-?" or sys.argv[1]=="--help"):
			print("\nGlossy:\n\tTransform a Paratext Lexicon.xml file into an interactive \n\tHTML lexicon, optionally saving it in the calling folder.\n")
			print("Syntax: glossy9.py [source-filename [output-filename]]")
			print("\tIf no input filename is given then default input filename is\n\t\t"+xml_filename)
			print("\tIf [output-filename] is - then output is to stdout")
			print("\tOtherwise default output filename is \n\t\t"+output_filename)
		else:
			print("Args: "+str(len(sys.argv)))
			if sys.argv[1]!="-":
				xml_filename = sys.argv[1]
				print("Input: "+xml_filename)
			if len(sys.argv)>2 and sys.argv[2]!="-":
				output_filename = sanitise_output(sys.argv[2])
				print("Output: "+output_filename)

	dom = ET.parse(xml_filename)
	xslt = ET.parse(xsl_filename)
	transform = ET.XSLT(xslt)
	newdom = transform(dom)

	if output_filename=="" or output_filename=="-":
		print((ET.tostring(newdom, pretty_print=True)))
	else:
		transformed_file = ET.tostring(newdom, encoding="unicode") #pretty_print=True)
		outfile = open(output_filename, 'w')
		outfile.write(transformed_file)

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

def walk_projects_dir(my_paratext_projects):
	for dirpath, dirnames, filenames in os.walk(my_paratext_projects):
		for filename in filenames:
			if filename.endswith(('Lexicon.xml', '.txt')):
				dom = ET.parse(inputpath + filename)
				xslt = ET.parse(xsltfile)
				transform = ET.XSLT(xslt)
				newdom = transform(dom)
				infile = unicode(ET.tostring(newdom, pretty_print=True))
				outfile = open(outpath + "\\" + filename, 'a')
				outfile.write(infile)

# MAIN PROGRAM STARTS HERE

main()

# Things to check
# - how are directory names handled in Windows? is / OK?
