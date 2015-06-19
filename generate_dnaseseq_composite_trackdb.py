import argparse
import xml.dom.minidom

def bigwig_defaults( trackhub_defaults ):
	defaults = dict();
	for e in trackhub_defaults:
		defaults[e.tag] = e.text

	return defaults 

def writeCompositeBigWigTrack(dnase_seq_datasets, trackhub_defaults):
	bigwig_range_min = trackhub_defaults.getElementsByTagName("range_min").item(0).firstChild.nodeValue
	bigwig_range_max = trackhub_defaults.getElementsByTagName("range_max").item(0).firstChild.nodeValue
	bigwig_options   = trackhub_defaults.getElementsByTagName("option");

	replicates = set()
	time_points = set()
	bigwig_files = dict()

	for d in dnase_seq_datasets.getElementsByTagName("Dataset"):
		time_point = None
		replicate = None
		a = d.attributes
		for i in range(0, a.length):
			if(a.item(i).name == "timePoint"):
				time_point = a.item(i).value
			elif(a.item(i).name == "replicate"):
				replicate = a.item(i).value

		replicates.add(replicate)
		time_points.add(time_point)
		bigwig_files[(time_point, replicate)] = d.getElementsByTagName("BigWig").item(0).firstChild.nodeValue

	print "track GGR_DNase_seq_composite"
	print "compositeTrack on"
	print "shortLabel GGR_DNase_seq_Composite"
	print "longLabel GGR_DNase_seq_Composite"
	print "type bigWig",bigwig_range_min,bigwig_range_max

	for e in bigwig_options:
		a = e.attributes
		for i in range(0, a.length):
			print a.item(i).name,a.item(i).value

	time_points_seq = []
	for t in time_points:
		time_points_seq.append(t+"="+t+"_hr")

	str = " "
	time_points_seq = []
	for t in time_points:
		time_points_seq.append(t+"="+t+"_hr")
	print "subGroup1 timePoint Time_Point "+str.join(time_points_seq)

	replicates_seq = []
	for r in replicates:
		replicates_seq.append(r+"=Rep"+r)
	print "subGroup2 replicate Replicate "+str.join(replicates_seq)

	print "dimensions dimX=replicate dimY=timePoint"
	print "sortOrder replicate=+ timePoint=+"
        print ""

	for t,e in bigwig_files.iteritems():
		timepoint=t[0]
		replicate=t[1]
		print "\ttrack DNase_"+timepoint+"hr_Rep"+replicate
		print "\ttype bigWig"
		print "\tshortLabel DNase_"+timepoint+"hr_Rep"+replicate
		print "\tlongLabel DNase_"+timepoint+"hr_Rep"+replicate
		print "\tparent GGR_DNase_seq_composite"
		print "\tsubGroups replicate="+replicate+" timePoint="+timepoint
		print "\tbigDataUrl",e
		print ""

	return

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--defaults', type=argparse.FileType('r'), required=True, metavar='defaultTrackSettings.xml')
parser.add_argument('-c', '--config', type=argparse.FileType('r'), required=True, metavar='configuration.xml')
args = parser.parse_args()

trackhub_defaults_root = xml.dom.minidom.parse(args.defaults)
dnase_seq_dataset_root = xml.dom.minidom.parse(args.config)
	
writeCompositeBigWigTrack(dnase_seq_dataset_root, trackhub_defaults_root)

