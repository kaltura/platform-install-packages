**[Track milestones progress](https://github.com/kaltura/platform-install-packages/issues/milestones)**.
   
#### 2014-02-17:
Cluster install passed successfully, Chef scripts created, many tests passed and bugs crushed.

+ Red5 package was added to kaltura-server and KCW webcam tested.
+ monit package was fully tested.
+ [Chef scripts were created](https://github.com/kaltura/platform-install-packages/tree/master/RPM/chef-repo) - now you can deploy a complete Kaltura cluster with the click of a button!
+ 18 packaging bugs crushed (thanks to @DBezemer, @mobcdi and @doubleshot)!
+ [7 fix patches submitted to core](https://github.com/kaltura/server/pull/871) by [@jessp01](https://github.com/jessp01).
+ [1 Admin Console view](https://github.com/kaltura/server/pull/872 ) contributed by  [@DBezemer](https://github.com/DBezemer).
+ New documents published: 1) [cluster deployment document](http://bit.ly/kipp-cluster-yum), 2) [configuring platform monitors](http://bit.ly/kipp-monit).
+ Local Drop folders passed tests.
+ Upgrade to 9.10 will be skipped. As 9.11 planned for release next week, nightly will progress straight to 9.11.
+ [Project announced on a blog post!](http://blog.kaltura.org/introducing-kipp-kaltura-install-made-simple)

#### 2014-02-03:
Single server installed passes successfully, including sanity of the following features:   

+ Partner creation
+ Content upload of various kinds
+ Convert
+ Thumbnail creation
+ Entry investigation
+ Entry embed
+ Partner config options via Admin Console
+ API v3 tests for the PHP5 and Java client libs
+ Cluster install is in final stages of testing and expected to finish sanity today
+ Monitoring suite is under way and is also expected to be released for testing today
      
#### 2014-01-27:
We are thrilled to share that we've reached public alpha testing phase of the RPM packages.
If you're running a RedHat based distro and would like to test, please review the RPM installation steps.
