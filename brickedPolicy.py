#!/bin/python3
from os.path import join as joinpath
from os.path import exists as doesPathExists
from shutil import copytree, rmtree
import yaml, sys


mainPolicyFilename = sys.argv[1]
print("opening and parsing main policy file '{}' ...".format(mainPolicyFilename))
sfile = open(mainPolicyFilename, "r")
mainPolicy = yaml.safe_load(sfile.read())
sfile.close()


subpolicyHeadingCollection = []
subpolicyBodyCollection = []
themeDir = joinpath(mainPolicy["themesDir"], mainPolicy["theme"])
outputDir = "out"
outputFilename = joinpath(outputDir, mainPolicy["out"])


print("loading theme '{}' ...".format(mainPolicy["theme"]))
sfile = open(joinpath(themeDir, "template"), "r")
template = sfile.read()
sfile.close()

sfile = open(joinpath(themeDir, "policy-heading-list"), "r")
policyHeadingListTemplate = sfile.read()
sfile.close()

sfile = open(joinpath(themeDir, "policy-body"), "r")
policyBodyTemplate = sfile.read()
sfile.close()

sfile = open(joinpath(themeDir, "policy-body-list"), "r")
policyBodyListTemplate = sfile.read()
sfile.close()


for policyName in mainPolicy["policies"]:
	print("applying sub policy '{}' ...".format(policyName))
	subpolicyHeadingCollection.append(policyHeadingListTemplate
		.replace("${title}", mainPolicy["policies"][policyName]["title"])
		.replace("${description}", mainPolicy["policies"][policyName]["description"])
		.replace("${id}", policyName)
	)

	subpolicyBrickets = []

	for bricketName in mainPolicy["policies"][policyName]["brickets"]:
		print("  applying bricket '{}' ...".format(bricketName))
		sfile = open(joinpath(mainPolicy["bricketsDir"], bricketName), "r")
		subpolicyBrickets.append(
			policyBodyListTemplate
				.replace("${content}", sfile.read())
				.replace("${id}", policyName + "." + bricketName)
				.replace("${class}", policyName + " " + bricketName)
		)
		sfile.close()
	
	subpolicyBodyCollection.append(
		policyBodyTemplate
			.replace("${content}", "\n".join(subpolicyBrickets))
			.replace("${title}", mainPolicy["policies"][policyName]["title"])
			.replace("${description}", mainPolicy["policies"][policyName]["description"])
			.replace("${id}", policyName)
	)

print("save output to '{}' ...".format(outputFilename))
if doesPathExists(joinpath(outputDir, "assets")):
	rmtree(joinpath(outputDir, "assets"))
copytree(joinpath(themeDir, "assets"), joinpath(outputDir, "assets"))

sfile = open(outputFilename, "w")
sfile.write(
	template
		.replace("${policyHeadings}", "\n".join(subpolicyHeadingCollection))
		.replace("${policyBodies}", "\n".join(subpolicyBodyCollection))
)
sfile.close()