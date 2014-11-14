---
layout: post
title: "Working with Amazon S3 from Rails:<br>A beginner's guide"
date: 2013-11-05 15:53:19 -0700
comments: true
categories:  rails, gems
---

Newcomers to Rails often want to use a convenient platform-as-a-service provider like Heroku to host their application.  This poses a problem as soon as they need to host large amounts of assets, or user-uploaded content, for their application to function properly.  To host this content, we need to integrate with a third-party storage provider.  For most people this will mean getting acquainted with Amazon S3, which stands for Simple Storage Service, and is the cloud storage infrastructure that backs most of the major services you use every day on the internet.  Using S3 is simple, but configuring it the first time can seem overwhelming.  In this post, I will walk you through the process.

I will assume the following are true about you:
	- You are writing a Ruby on Rails application
	- You are deploying your application to Heroku
	- You have never used Amazon Web Services


# Setup Amazon Web Services
This part is relatively easy, if tedious.  Although in the future you will probably want to explore command line utilities for managing your AWS resources, for this tutorial we'll be doing everything through their website.

1. Go to [http://aws.amazon.com/](http://aws.amazon.com/) and sign up for Amazon AWS. If you're not already a customer of Amazon, you'll have to enter your payment information. But if you already have an Amazon account this step should be relatively painless.

# Manage your AWS permissions
AWS permissions management is actually a large and important topic, and you should delve into the [official docs](http://docs.aws.amazon.com/IAM/latest/UserGuide/PermissionsOverview.html) as questions arise.  They have support for permissions Groups and Roles in addition to Users, but these only become significant if you are administrating AWS on behalf of many other people and applications in your company.  I'm going to assume that the type of folks reading this tutorial are probably just tinkering on a smallish personal project.

Even if you're just hacking on your own project, as your application grows or as you deploy more applications, you might find yourself using more and more of Amazon's cloud infrastructure offerings.  When setting up any of these services, it's considered best practice to create users (dubbed IAM Users in AWS jargon) that are scoped to the lowest level of permissions needed to get the necessary work done. Having separate IAM Users for each human or application accessing AWS on your behalf makes it easy to revoke or modify these permissions for one thing without interfering with others.

Keep in mind that an IAM "user" might represent either an actual human user or client credentials to be stored in your application.  Whether a human being or your application, an IAM User is anything that wants to access and use AWS resources on your behalf.

1. Navigate to the AWS Management Console.
2. Select IAM / Secure AWS Access Control. This should bring you to the "Identity and Access Management Dashboard"
3. On the dashboard sidebar, select "Users". 
4. Create a new user.
5. Make a note of the credentials. You will need them when configuring your Rails application in a later step.

# First steps with S3, Simple Storage Service 
Once S3 is set up, you will use it in a way that is similar to other forms of key/value store you are familiar with: Redis, Memcached, or even basic ruby Hash instances operate similarly.  If you've worked with Redis at all, you'll be familiar with the concept of namespaces, which bring some organization and sanity to your keys.  

Amazon S3 also has the idea of namespaces baked in, except instead of being called a "namespace" it is called a "bucket".  The metaphor is one of a physically separate container and might help you think about your AWS resources in a less abstract way.  Each bucket comes with its own configuration and has it's own resource permissions (aka "bucket policy") that must be set before we can get down to work.

Create a bucket, and set a bucket policy.
3. Create a bucket.
4. Set the bucket policy using the policy generator and paste it into your bucket permissions in the S3 console.
4. Install `figaro` and `aws-sdk` gems.
5. Put your IAM user credentials into config/application.yml to safely configure AWS.
6. Profit! Use the API provided by the Amazon Web Services gem (docs here) to do amazing things.

## The long version

Complete steps 1-4 above on amazonaws.com. After all that is set up, we can access S3 from our Ruby app using the official SDK provided by, `aws-sdk`, to access the S3 API. For something that seems simple, setting this up took a surprisingly long time. I’ll walk you through my process.

Add these gems to your Gemfile, and then run `bundle install` from the project directory to install the gems.

```ruby
gem 'aws-sdk', '~> 1.0'
gem 'figaro'
```

 Next we need to configure AWS with our credentials. The `aws-sdk` gem provides a top level AWS module namespace that can be manually configured, but the docs say it will automatically configure itself if we set the correct `ENV` variables. We can do this easily and securely using the `figaro` gem. After you’ve created your create an AWS IAM user you should copy the API credentials into your application.yml file.

```ruby
# config/application.yml
AWS_ACCESS_KEY_ID: "your_api_key"
AWS_SECRET_ACCESS_KEY: "your_secret_key"
AWS_DEFAULT_REGION: "us-standard"
```

This file is **not** checked into source control, and figaro will set these variables in the global ENV variable when the server is started. When we deploy our application to Heroku, we can set the environment variables with the `rake figaro:heroku` command.

If you didn’t do step 4 above already, go to Bucket > Properties > Permissions portion of the S3 console to set up a bucket policy. Bucket policies govern who can see or interact with the objects in your bucket. I needed to use the docs and the bucket policy generator tool to grant public read (s3:getObject) permissions along with other powers (s3:putObject, s3:deleteObject) for my authenticated application.

Now we’re ready to programmatically add files. Amazon S3 calls files objects, and they are referenced by key (the filename) and data (the file contents.) A simple example in the rails console would be

```
filename = "my_awesome_file.txt"
content = "Hello, World!"

s3 = AWS::S3.new
bucket = s3.buckets[:your_bucket_name]
bucket.objects[filename].write(content)
```

If you have set your bucket policy correctly to allow public read access you should now be able to see your content in the browser at `http://s3.amazonaws.com/your_bucket_name/my_awesome_file.txt`. Amazing!
