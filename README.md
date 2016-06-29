# ami-manager

###Disclaimer:
This is very raw, and while it works is not very rubust "yet". 
I've added some basice command line argument parsing, however I still have work to do, currently this still requires that you keep your imageids stored in a file in the "ImageId": "ami-2d8c6d4b" format.
I'll beworking on adding more commanline arguments to allow adding the ImageId directly on the command line, for one off deletes.

###ami-manager: 
aims to be a quick way to manage AWS AMIs and related snapshots. 
Currently it is only functional to deregister AMIs and delete the related snapshots.

It requires [boto3](https://github.com/boto/boto3) (AWS Python SDK).

USAGE: ami_manager.py -f file_with_imageids -t days_to_keep

days_to_keep parameter is the for telling ami_manager to delete AMIs in file_with_imageids older than the number of days given.
  
  usage: ami-manager.py [-h] [-f FILE] [-t TIME] [-i IMAGEID [IMAGEID ...]]

  optional arguments:
    -h, --help            show this help message and exit
    -f FILE, --file FILE  Filename containing the ImageIds
    -t TIME, --time TIME  Number of Days to keep, Images in Filename older than
                        this will be deleted
    -i IMAGEID [IMAGEID ...], --imageid IMAGEID [IMAGEID ...]
                        Imageid, or list of ImageIds to delete *****NOT IMPLIMENTED YET


The file_with_imageids can be formatted many ways, all that is really
required is that a separate line needs to be formated with:

"ImageId:" "ami-id"

my backup logs from the aws cli create image outputs to a format that
looks like the following:

    Fri Apr 29 14:31:44 UTC 2016 Backing up aws-am-app-33
    {
      "ImageId": "ami-2d8c6d4b"
    }

  the quotes are important around the ami-id and this is the default way
  that aws cli outputs them. so if you use aws cli to create your images
  using create-image then send the output to a file you'll be fine.
  
  Also describe-images outputs the ImageId in with the quotes also so if
  create a file to pass ami_manager.py it will also be fine.


  AWS Credentials: ami-manager.py uses [boto3](https://github.com/boto/boto3) so it uses the ~/.aws/credentials in the
  user environment.

