import boto3
import datetime
import dateutil.parser as dp
import sys

#check to make sure we got the parameters we need to run.
if len(sys.argv) < 3:
  print "Not enough arguments given"
  print "USAGE: ami_manager.py <file_with_imageids> <days_to_keep>"
  exit()

#need to do some time adjustment to get this in seconds since epoc
#isoformat is needed because AWS uses iso formated datetimes
today = datetime.datetime.now().isoformat()
#Parse the datetime to get it to seconds since epoch.
seconds_to_keep = int(sys.argv[2]) * 86400
today_parsed = dp.parse(today)
today_seconds = today_parsed.strftime('%s')

ec2 = boto3.resource('ec2')

#images = ec2.images.limit(50)

#for image in images:
#    print image.id

#Open up the "backup log" or file list file.
# This needs to be error checked and trapped so when an in correct
# file is passed we can be nice and tell you instead of dropping
# you on your head.
backup_log = open(str(sys.argv[1]),"rw")

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

