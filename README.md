
CSV PARSER.

A script, written in python that parses the content of a CSV immediately they are posted in an AWS s3 bucket and writes same into an SQLite database. 


- Create an s3 bucket within the availability zone we intend to create our lambda function. The name of our s3 bucket should be unique across the board. The default configurations by AWS would be just fine. 

- Create an AWS VPC. We can also use the default VPC in the region. All region comes with a default VPC, ensure that there are associated subnets attached to the VPC.
For new VPCs, create the subnets. 

- Create a security group. Go to the EC2 dashboard(or using the CLI) and navigate to the security group. Give the SG a name and attach it to our VPC created above. A description is also mandatory to create a Security Group.  Click `Edit inbound rules`. Add a rule to open port 2049 for our EFS. Type should be Custom TCP, Port range 2049, source: Anywhere. 
    
    Click `save rules`.

- On AWS Console, choose VPC service and then Endpoints. Create a new endpoint, associate it to the s3 service and then select the VPC and route table. Select access level: full.  This is so our traffic does not leave the AWS Network. 

- Create an EFS. The EFS is needed because we'll be creating an SQLite DB to store our values and EFS is the way to do it when using lambda. 

- In the network access pop up when creating our EFS, there's a column called `"mount target"`. Attach the security group we've just created in the earlier step to the availability zones below. You can add tags if desired.

- Also go to the `"Access points"` column, still in the EFS dashboard and click on `create access point`. For the file system, choose the EFS we've created earlier. For the `POSIX user entry`, `User ID` should be provided as `1000`, `Group ID` also as `1000`. Set the `directory path` to `/access`. 

    Set `Owner User ID` to `1000`, `Owner Group ID` to `1000` and `Permissions` to `777`. 

    This would create an individual network interface for each of the availability zones. 

- Create an IAM role for the lambda function. Head over to the Identity and Access Management console, click on Roles and create a role for the AWS service, lambda. 
Attach the following AWS managed policy.
     -   `AmazonS3ReadOnlyAccess `
     -   `AWSLambdaExecute `
     -   `AmazonS3readOnlyAccess` 
     -   `AWSLambdaVPCAccessExecutionRole`  
     -   `AmazonElasticFileSystemClientFullAccess` 

- Create the Lambda Function. Move over to the lambda console, and select author from scratch, provide a name and select python 3.8 as runtime. 

Within permissions, select `use an existing role` and select the role that we've just created. Click on `create` to create the function. 

- Navigate to configuration and select VPC. Click on edit, select the VPC created above or the default VPC if that's what we're using, select at least 2 subnets(the more the better) and also select the security group we created earlier. Save the changes. This would take a while to update the function.

- Navigate to the select File system. Click on the EFS we created earlier. Also, select the Access point for the file system. Should be the same Access point we created above. describe the local mount path as "/mnt/access".

Save the changes. 

- Add a trigger. Select s3 and the bucket name. EventType should be ObjectCreatedByPut. And suffix .csv

- Upload the lambda function either through s3 or as a zip file or even just copy and paste the content into the default lambda file.

- Add an AWS lambda test event. For the first run, please uncomment line 19 to initialize the database. Subsequent runs should be commented. # aws-csvparser
