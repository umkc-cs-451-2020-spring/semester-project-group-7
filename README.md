# Semester-Project-Group-7
# CS-451R


# Our Team:

>Mariam Habib- Project Manager
>Scott Howard- Developer
>Irem Atik- Developer
>Grant Jenkins-Developer
>Maryam Albakhiet-Developer





# High Level Overview
>A web application that pulls in transaction details and allows the user to set triggers for notification rules and receive notifications around them.  The system should also save data to a database so recurring reports can be created.


# Requirements
>1.	Must be a web application (not a desktop application) built in a “newer” web development framework
>> a.	.Net preferably – if you choose another framework, support from us will be limited
>2.	Make the application responsive and aesthetically pleasing. Client side framework/libraries are up to you but must be included in project (aka no external resources), but you must use at least one CSS framework such as Bootstrap (unless you want to make all the styles yourself).
>3.	Database should preferably be in SQL server 2012 or above – if you choose another database option, support from us will be limited. 
>4.	Home Page 
>>a.	Dashboard:
>>>i.	Number of times each notification rule has been triggered over the past month and year
>>>>1.	Daily screen should be easy to read, easy to use, and provide a snapshot of data
>>>ii.	Ability to hide notification rules where the times tripped is zero
>>b.	Ability to pull/compare notification rule different timeframes
>>c.	Ability to export to spreadsheet
>5.	Login Page
>>a.	Simple login and passwords fields.
>>>i.	Mask the password field.
>>>ii.	Password requirements:
>>>>1.	8 characters minimum
>>>>2.	1 upper case letter
>>>>3.	1 symbol
>>>>4.	1 number
>>b.	Login button
>6.	Dashboard
>>a.	Summary for triggered notification rules
>7.	Transaction Summary
>>a.	Transaction list sorted by date
>>>i.	Don’t need to worry about searching/filtering
>>b.	Users should have the ability to add transactions here, which should automatically trigger any associated notification rules
>8.	Triggers - Tool should allow for configurable notification rules to be created to notify user when transactions fit into a set of criteria.
>>a.	Users should be able to Add/Edit/Delete notification rules without technical assistance.
>>b.	These are examples (you have the liberty of coming up with what types of notification rules there are and how they are implemented): 
>>>i.	Minimum of 3 notification rules added to system
>>>>1.	Ex: Out of state transactions
>>>>2.	Ex: Timeframe usage
>>>>3.	Ex: Categories
>9.	Notifications based on Notification Rules
>>a.	Main Requirement: Notification when the user logs in
>>>i.	Ex: Transaction in Alaska
>>>ii.	Ex: Transaction at 2AM
>>>iii.	Ex: Transaction from Spa
>10.	Unit testing
>a.	10% code coverage for unit tests. xUnit is a good framework for .NET.

# Stretch Goals (Two are required)
>1.	Deploy the project into a windows server/cloud instance
>>a.	Practice configuration properties for different environments
>2.	Create a Web API layer for backend interactions. 
>3.	Use an open source reporting tool/business intelligence suite for all the reporting and its data visualization
>4.	Use version control throughout the project
>5.	Security scan your application and fix Critical issues at a minimum. OWASP ZAP is a good open source option
>6.	Use Commerce Bank color scheme in styling
>7.	Session for remembering user if they close their browser and then log in again
>8.	Options for user if they forgot their username or password
>9.	Notifications via messaging center in the app
>10.	Notifications via email or text 
