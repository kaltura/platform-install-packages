### Setup Amazon S3 Remote storage

  To Setup a Remote Storage Following link has the Reference Contents 

  Reference URL : [kalturaCE Amazon s3 storage cloudfront cdn setup](http://www.panda-os.com/2012/11/kaltura-ce-amazon-s3-storage-cloudfront-cdn-setup/#.Uy_7KHUW3h_)

######Setting up Amazon S3 and getting security credentials

* To get your Amazon security credentials (assuming you have an account with amazon AWS), go to this link
  (https://portal.aws.amazon.com/gp/aws/securityCredentials)

* To set up your amazon S3 bucket, go to (https://console.aws.amazon.com/s3/home) , create a new bucket, and name it.

* Inside this bucket, create a folder called **kaltura**

* Select your new bucket on the left side, click Actions and select **Properties**

* Add more permissions – **Authenticated Users** – check all boxes.

* Select the kaltura folder, click **properties**, go to **Permissions**.

* Add more permissions – Everyone – read and download (you can also right click the folder and select **Make Public**)

  In the Above 6th and 7th Step there is no Permission available, So Just Right click on kaltura Directory and choose     **Make Public**

  Then we need to add a bucket Policy for your bucket, Granting Object get Permission to any Anonymous User in Amazon S3   Bucket for reading the file.

```
{
  "Version":"2012-10-17",
  "Statement":[{
	"Sid":"AddPerm",
        "Effect":"Allow",
	  "Principal": {
            "AWS": "*"
         },
      "Action":["s3:GetObject"],
      "Resource":["arn:aws:s3:::Bucket-name/*"
      ]
    }
  ]
}
```

![selection_014](https://raw.githubusercontent.com/blackyboy/Centos-Linux-Stuffs/master/setup-images/setup_amazon_s3_remote_storage.png)


  If this Policy was not added, We will face clip not found error when ever uploading a new video to kaltura.
