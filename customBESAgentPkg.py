#!/usr/bin/python
#--------------------------------------------------------------------------------------------------
#-- systemDivisions
#--------------------------------------------------------------------------------------------------
# Program    : systemDivisions
# To Complie : n/a
#
# Purpose    : 
#
# Called By  :
# Calls      :
#
# Author     : Rusty Myers <rzm102@psu.edu>
# Based Upon :
#
# Note       : 
#
# Revisions  : 
#           2016-01-25 <rzm102>   Initial Version
#
# Version    : 1.0
#--------------------------------------------------------------------------------------------------


import sys, glob, os, re, shutil, argparse
import urllib2 as url
import xml.etree.ElementTree as ET

# Names of packages to export
name = "CUSTOM"


# Function to remove 'relocate' tags
# This forces installer to place files in correct location on disk
def derelocatePacakge(distroPath):
    # Open Distribution file passed to function
    tree = ET.parse(distroPath)
    # Get the root of the tree
    root = tree.getroot()
    # Check each child
    for child in root:
        # If it's a pkg-ref
        if child.tag == "pkg-ref":
            # Check each subtag
            for subtag in child:
                # If it's a relocate tag
                if subtag.tag == "relocate":
                    # Remove the whole child
                    root.remove(child)
    # Remove old Distribution file
    os.remove(distroPath)
    # Write new Distribution file
    tree.write(distroPath)

# Function to load the latest BESAgent Installer
def loadPackages():
    # searches for BESAgent installer packages, returns latest version if 
    # multiple are found
    # Store packages in local folder
    besPkgs = []
    # Look in local folder
    source = "./"
    # check each file
    for filename in sorted(os.listdir(source)):
        # join path and filename
        p=os.path.join(source, filename)
        # check if it's a file
        if os.path.isfile(p):
            print("Found: " + str(filename))
            # Check if it matches BESAgent regex
            pattern = re.compile(r'^BESAgent-(\d+.\d+.\d+.\d+)-*.*pkg')
            match = pattern.search(filename)
            # If it matches, add it to the array of all packages
            if match:
                besPkgs.append(p)
    # If we have more than one package found, notify
    if len(besPkgs) > 1:
        print "Found more than one package, choosing latest version."
    # Return the last package found, which should be latest verison
    return besPkgs[-1]

# Clean out the modified files
def clean_up(oldfilepath):
    # We're done with the default folder, so we can remove it
    if os.path.isdir(oldfilepath):
        shutil.rmtree(oldfilepath)

# Touch a file - written by mah60
def touch(path):
    basedir = os.path.dirname(path)
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    open(path, 'a').close()

# Add command line arguments
parser = argparse.ArgumentParser(description='Build Custom BESAgent Installers.', conflict_handler='resolve')

# Add option for adding band
parser.add_argument('--brand','-b', dest='custom_brand', action="store_true",
                    help='add branding text to the BESAgent pacakge -b, --brand')

# Add option for adding custom settings
parser.add_argument('--settings','-s', dest='custom_settings', action="store_true",
                    help='add custom settings cfg to the BESAgent pacakge -s, --settings')

# Add option for specific package
parser.add_argument('--package','-p', dest='custom_package', action="append", type=str,
                    help='create a installer for a custom division -c, --custom <URN> <GUID>')

# Parse the arguments
args = parser.parse_args()

# Check that we're on OS X
if not sys.platform.startswith('darwin'):
     print "This script currently requires it be run on macOS"
     exit(2)

# run function to get packages
if args.custom_package:
    default_package = args.custom_package[0]
    print default_package[0:-4]
    default_folder = default_package[0:-4]
else:
    default_package = loadPackages()
    # remove .pkg from name
    default_folder = default_package[2:-4]

# Make sure our modified package folder exists
modifiedFolder = "ModifiedPackage"
if not os.path.isdir(modifiedFolder):
    # Make it if needed
    os.mkdir(modifiedFolder)

# Notify user of default package being used
print "Using Package: " + default_package


# Make the path for the modified package destination
modifiedDest = os.path.join(modifiedFolder, default_folder)

# Print path for modified folder
# print "Modified Dest: {0}".format(modifiedDest)
# Delete old files
clean_up(modifiedDest)

# Set path to distribution file
DistroFile = os.path.join(modifiedDest, "Distribution")

# If the default folder is missing
# Default folder is the BESAgent package expanded, 
# with the addition of our ModifiedFiles.
if not os.path.isdir(modifiedDest):
    # Expand default pacakge to create the default folder
    sys_cmd = "pkgutil --expand " + default_package + " " + modifiedDest
    os.system(sys_cmd)
    # Update Distribution file to remove relocate tags
    derelocatePacakge(DistroFile)
    # Set up paths to the Modified Files and their new destination in expanded package
    src = "./ModifiedFiles/"
    dest = os.path.join(modifiedDest, "besagent.pkg/Scripts/")
    # Create array of all of the modified files
    src_files = os.listdir(src)
    # For each file in the array of all modified files
    print "Dest {0}".format(dest)
    for file_name in src_files:
        # create path with source path and file name
        full_file_name = os.path.join(src, file_name)
        # if it's a file, copy it to the default folder
        if (os.path.isfile(full_file_name)):
            if "clientsettings.cfg" in full_file_name:
                if args.custom_settings:
                    shutil.copy(full_file_name, dest)
            else:
                shutil.copy(full_file_name, dest)

# Make dir for destination packages
finishedFolder = default_folder[0:-10] + "Finished"
if not os.path.isdir(finishedFolder):
    os.mkdir(finishedFolder)

# Print out the one we're doing
#print "{0:<40}".format(name)
# Name of temp unit folder
unit_folder = default_folder + "-" + name
# Name of unit package
unit_package = unit_folder + ".pkg"
# Copy modified package folder to temp unit folder
sys_cmd = "cp -R " + modifiedDest + " " + unit_folder
os.system(sys_cmd)
    
# Echo Unit Name into Brand file if requested
if args.custom_brand:
    sys_cmd = "echo \"" + name + "\" > " + os.path.join(unit_folder, "besagent.pkg/Scripts" ,"brand.txt")
    os.system(sys_cmd)

# Flatten customized unit folder into final package
sys_cmd = "pkgutil --flatten " + unit_folder + " " + finishedFolder + "/" + unit_package
os.system(sys_cmd)
# Clean out custom folder
clean_up(unit_folder)
                
# Clean ourselves up
clean_up(modifiedDest)

