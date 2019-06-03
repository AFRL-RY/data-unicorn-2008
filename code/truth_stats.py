'''
    This script calculates the statistics on the truth data from the CSV file.
'''
import argparse
import csv

def update_dictionary_count(dictionary, key_to_count):
    '''
        This function looks for the object_name in the object_count dict. If not
        found then it is added otherwise increment by 1.
    '''
    if key_to_count in dictionary.keys():
        dictionary[key_to_count] = dictionary[key_to_count] + 1
    else:
        dictionary[key_to_count] = 1

def print_dictionary_count(dictionary):
    '''
        pretty print the object_count dictionary to copy/paste into markdown
    '''
    for key in sorted(dictionary.keys()):
        key_count_str = "{:,}".format(dictionary[key])
        print("      * %s: %s" % (key, key_count_str))

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv_file_name",
                        help="name of the csf file to read",
                        action="store", required=True)
    args = parser.parse_args()

    object_count = {}
    file_names_count = {}
    total_number_of_truth_points = 0
    with open(args.csv_file_name, 'r') as csv_file:
        # don't want to go through this file more than once becasue it is large
        reader = csv.DictReader(csv_file, delimiter=",")
        for row in reader:
            update_dictionary_count(object_count, row['target_type.name'])
            update_dictionary_count(file_names_count, row['track_point.fileId'])
            total_number_of_truth_points += 1

    print_dictionary_count(object_count)
    total_number_of_images_str = "{:,}".format(len(file_names_count))
    print("total number of images: %s" % total_number_of_images_str)
    total_number_of_truth_points_str = "{:,}".format(total_number_of_truth_points)
    print("total count of objects truthed: %s" % total_number_of_truth_points_str)