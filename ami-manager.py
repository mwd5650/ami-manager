#!/usr/bin/env python
import boto3
import datetime
import dateutil.parser as dp
import sys
import argparse


ec2 = boto3.resource('ec2')

def image_deregister(imageid):
    try:
        image = ec2.Image(imageid)
        image_date =  image.creation_date
    except:
        print "ImageId not found, or you do not have permission to deregister that ImageId"
        exit()

    try:
        block_list = image.block_device_mappings
        response = image.deregister()
        print "Image: " + image.image_id + " Deleted"
        for items in block_list:
            if items.has_key('Ebs'):
                snapshot = ec2.Snapshot(items['Ebs']['SnapshotId'])
                response = snapshot.delete()
                print "SnapshotID: " + items['Ebs']['SnapshotId'] + " Deleted"

    except:
        print "no EBS snapshots associated with imageid %s" % imageid
        print "Deregistered ImageID: %s" % imageid
        exit()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file",  help="Filename containing the ImageIds", default="NONE")
    parser.add_argument("-t", "--time",  default=1, help="Number of Days to keep, Images in Filename older than this will be deleted, default is to keep 1 day.", type=int)
    parser.add_argument("-i", "--imageid", help="Imageid, or list of ImageIds to delete", default="NONE")
    args = parser.parse_args()

    if (args.imageid == "NONE" and args.file == "NONE"):
        print "Filename or ImageId required, please see usage / help -h"
        exit()
    elif (args.imageid != "NONE"):
        image_deregister(args.imageid)
        exit()

    #need to do some time adjustment to get this in seconds since epoc
    #isoformat is needed because AWS uses iso formated datetimes
    today = datetime.datetime.now().isoformat()
    #Parse the datetime to get it to seconds since epoch.
    seconds_to_keep = args.time * 86400
    today_parsed = dp.parse(today)
    today_seconds = today_parsed.strftime('%s')

    try:
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
          continue #skip if it doesn't exist.
        image_seconds = image_date_parsed.strftime('%s')
        if (int(today_seconds) - seconds_to_keep) > int(image_seconds):
          image_deregister(imageid)

    backup_log.close()

if __name__ == "__main__":
    main()
