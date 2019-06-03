# This script renames the SAR files so the file names match closer to
# the EO names.
#
import argparse
import os
import sys

def get_date_file_name(source_file_name):
	'''
		reaches into the NITF file and carefully extracts out the date
		and time so we can reform the file name to match the EO.
	'''
	with open(source_file_name, 'rb') as f:
		first_lines = f.read(1000)
		#print(first_lines + '\n')
		index_utc = first_lines.find("UTC=")
		date_time_str = first_lines[index_utc:index_utc+27]
		#print(date_time_str)
		year_str = date_time_str[4:8]
		month_str = date_time_str[9:11]
		day_str = date_time_str[12:14]
		hour_str = date_time_str[15:17]
		minute_str = date_time_str[18:20]
		second_str = date_time_str[21:23]
		frame_str = os.path.basename(source_file_name)[1:6]
		date_file_name = (year_str + month_str + day_str + hour_str + minute_str 
			+ second_str + ("-020%s-SAR.ntf." % frame_str) + 
			source_file_name[-2:])
		#print("date_file_name: %s" % date_file_name)
		#sys.exit(200)
		# 27 characters exactly UTC=2008-08-16T14:34:05.175
		# EO file name: 20080816144142-01004704-VIS.ntf.r0


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--inputDirectory",
		help="name of the input directory of SAR files",
		action="store", required=True)
	parser.add_argument("-o", "--outputDirectory",
		help="name of the output directory to save the modified files",
		action="store", required=True)	
	args = parser.parse_args()
	for file in os.listdir(args.inputDirectory):
		if ".ntf.r" in file:
			source_file_name = args.inputDirectory + "/" + file
			date_file_name = get_date_file_name(source_file_name)			
			destination_file_name = args.outputDirectory + "/" + file
			print("source: %s destination: %s" % (source_file_name, destination_file_name))
		