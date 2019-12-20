'''
This script converts the CLIF truth from sqlite3 to csv files.

The LEFT JOIN keyword returns all records from the left table (table1),
and the matched records from the right table (table2). The result is NULL from
the right side, if there is no match.

In order to verify the count of the table use the command:
    select count(track.id) from track;

'''
import sqlite3
import argparse
import csv
from os import listdir
from os.path import isfile, join


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--db_file_name",
                        help="name of the sqlite3 database file with .db extension",
                        action="store", required=True)
    parser.add_argument("-c", "--csv_file_name",
                        help="name of the csf file to create",
                        action="store", required=True)
    args = parser.parse_args()

    with open(args.csv_file_name, 'w') as csv_file:
        # don't put spaces in field names
        csv_file.write("track_point.fileId,track_point.time,track_point.frame,track.id,track_point.id,target_type.name,color.color,track.length,track.width,track_point.x,track_point.y,track_point.latitude,track_point.longitude\n")
        csv_writer = csv.writer(csv_file, delimiter=',')

        print("processing sqlite3 file named: %s" % args.db_file_name)
        conn = sqlite3.connect(args.db_file_name)
        c = conn.cursor()
        SQL_statement = ("SELECT track_point.fileId,track_point.time,track_point.frame,track.id,track_point.id,target_type.name,color.color,track.length,track.width,track_point.x,track_point.y,track_point.latitude,track_point.longitude from track_point "
                 + "  LEFT JOIN track on track_point.trackId = track.id"
                 + "  LEFT JOIN target_type ON track.targetTypeId=target_type.id"
                 + "  LEFT JOIN color on track.colorId=color.id" 
                 + " ORDER BY track.id, track_point.frame")
            
        record_count = 0
        for row in c.execute(SQL_statement):
            # print row
            csv_writer.writerow(row)
            record_count += 1

        print("total record count: %d" % record_count)
        conn.close()
