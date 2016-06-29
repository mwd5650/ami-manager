#!/usr/bin/env python
import boto3
import datetime
import dateutil.parser as dp
import sys
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",  help="Filename containing the ImageIds", default="NONE")
    parser.add_argument("-t", "--time",  default=1, help="Number of Days to keep, Images in Filename older than this will be deleted", type=int)
    parser.add_argument("-i", "--imageid", nargs='+', help="Imageid, or list of ImageIds to delete")
    args = parser.parse_args()

    if (args.file == "NONE"):
        print "Filename required please use --file or -f and specify a file to process."
        exit()


    #need to do some time adjustment to get this in seconds since epoc
    #isoformat is needed because AWS uses iso formated datetimes
    today = datetime.datetime.now().isoformat()
    #Parse the datetime to get it to seconds since epoch.
    seconds_to_keep = args.time * 86400
    today_parsed = dp.parse(today)
    today_seconds = today_parsed.strftime('%s')
    print seconds_to_keep

    ec2 = boto3.resource('ec2')

    #images = ec2.images.limit(50)

    #for image in images:
    #    print image.id

    #Open up the "backup log" or file list file.
    try:
        #backup_log = open(str(sys.argv[1]),"rw")
        backup_log = open(args.file,"rw")
    except:
        print "Error: Unable to open file " + args.file
        exit()

    for line in backup_log.readlines():
      if "ImageId" in line:
        tag, imageidraw = line.split(':')
        imageid = imageidraw[2:-2]
        image = ec2.Image(imageid)
        # I don't cleanup my backup_log files (mainly so I have historical reference)
        # Because of that I just skip the ImageId if it doesn't exist.
        try:
          image_date_parsed = dp.parse(image.creation_date)
        except:
          continue #skip it it doesn't exist.
        image_seconds = image_date_parsed.strftime('%s')
        if (int(today_seconds) - seconds_to_keep) > int(image_seconds):
          print image.creation_date
          block_list = image.block_device_mappings
          response = image.deregister()
          print "Image: " + image.image_id + " Deleted"
          for items in block_list:
            if items.has_key('Ebs'):
              snapshot = ec2.Snapshot(items['Ebs']['SnapshotId'])
              response = snapshot.delete()
              #print "Snapshot Delete Response: " + str(response)
              print "SnapshotID: " + items['Ebs']['SnapshotId'] + " Deleted"

    backup_log.close()

if __name__ == "__main__":
    main()
