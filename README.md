# ami-manager

###Disclaimer:
This is very raw, and while it works is not very rubust "yet". 
I'll be adding the command line option processingto make this much more robust. Moral of the store is I'mvery aware of how basic this code is.
My point was to get it function for my own purposes...I'll add spit and polish later, or if you want I'll be very grateful
or assistance.

###ami-manager: 
aims to be a quick way to manage AWS AMIs and related snapshots. 
Currently it is only functional to deregister AMIs and delete the related snapshots.

It requires [boto3](https://github.com/boto/boto3) (AWS Python SDK).

USAGE: ami_manager.py file_with_imageids days_to_keep

days_to_keep parameter is the for telling ami_manager to delete AMIs in file_with_imageids older than the number of days given.

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

