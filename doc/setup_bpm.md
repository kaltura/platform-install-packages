### Deploy BPM
* As super user run: 
```
/opt/kaltura/bin/deploy_bmp.sh
```
When prompted, please provide the Kaltura API host, the admin console partner mail and passwd and the activiti hostname [same as API host for an all in one install], its port [8080] and protocol [http], username [kermit], passwd [kermit].
*NOTE: these are all default values for the activiti app, you may want to modify them later*
*NOTE1: the script automates the steps described here: https://github.com/jessp01/server/blob/additions-to-bpmn-howto/release-notes.md#business-process-management-integration

* Obtain https://github.com/kaltura/platform-install-packages/blob/Jupiter-10.5.0/doc/flow.transcript.bpmn and request: $HOSTNAME:8080/activiti-explorer
* Login with user: kermit;passwd: kermit
* Swith to the 'Manage' tab and under the sub tab 'Deployments' hit 'Upload new'.
* Choose the flow.transcript.bpmn from your disk to upload
* Create a partner
* Under 'Profile' in the 'Publishers' tab for your partner, select 'Event Notifications'
* Select 'Start business-process' and 'Flavor status equal' in the select boxes and click 'Add from template'
* Check 'Automatic dispatch enabled:'
* Set key 'trigger_flavor_params_id' to 4
* Select your activiti server
* Select 'flow-transcript' as 'Business-Process'
* Leave the rest with default values and save
* Under 'Action' for the newly created profile set as enabled
* Get your profile ID and hit 'configure' under 'Actions'
* Set the profile ID for the 'templateId' key and save

* Select 'Signal business-process' and 'Entry Integration Job Finished' in the select boxes and click 'Add from template'
* Check 'Automatic dispatch enabled:'
* Select your activiti server
* Select 'kaltura-integrate' as 'Business-Process'
* Leave the rest with default values and save
* Under 'Action' for the newly created profile set as enabled

To test: 

* upload an entry and once ready go 'Batch process control' in Admin console. 
* Input your entry ID
* If the finished correctly then we are set up
* In activiti's web I/F, go to the 'Processes' tab and then 'My instances' where you should see the jobs run and their exec info.

