Summary: Kaltura Open Source Video Platform - Analytics 
Name: kaltura-dwh
Version: 9.7.0
Release: 2 
License: AGPLv3+
Group: Server/Platform 
URL: http://kaltura.org
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: kaltura-base,kaltura-pentaho,java-1.7.0-openjdk, kaltura-postinst 
BuildArch: noarch

%description
Kaltura is the world's first Open Source Online Video Platform, transforming the way people work, 
learn, and entertain using online video. 
The Kaltura platform empowers media applications with advanced video management, publishing, 
and monetization tools that increase their reach and monetization and simplify their video operations. 
Kaltura improves productivity and interaction among millions of employees by providing enterprises 
powerful online video tools for boosting internal knowledge sharing, training, and collaboration, 
and for more effective marketing. Kaltura offers next generation learning for millions of students and 
teachers by providing educational institutions disruptive online video solutions for improved teaching,
learning, and increased engagement across campuses and beyond. 
For more information visit: http://corp.kaltura.com, http://www.kaltura.org and http://www.html5video.org.


The Kaltura platform enables video management, publishing, syndication and monetization, 
as well as providing a robust framework for managing rich-media applications, 
and developing a variety of online workflows for video. 

This package configures the Data Warehouse [DWH] analytics component. 

%prep

%build

%install
#@DWH_DIR@/etlsource/execute/etl_daily.sh -p @DWH_DIR@
#@DWH_DIR@/etlsource/execute/etl_hourly.sh -p @DWH_DIR@
#@DWH_DIR@/etlsource/execute/etl_perform_retention_policy.sh -p @DWH_DIR@
#@DWH_DIR@/etlsource/execute/etl_update_dims.sh -p @DWH_DIR@

%clean
rm -rf %{buildroot}

%post
if [ "$1" = 1 ];then
	echo"#####################################################################################################################################
	Installation of %{name} %{version} completed
	Please run: 
	# %{prefix}/bin/%{name}-config.sh [/path/to/answer/file]
	To finalize the setup.
	#####################################################################################################################################
"
fi
%files
#cron/dwh.template
#.kettle/kettle.template.properties

%changelog
* Mon Dec  23 2013 Jess Portnoy <jess.portnoy@kaltura.com> - 9.7.0-1
- First package
