Email Handler
=============

This project provides the basic functionality to access contents of a mailbox
and use the features of IMAP and SMTP in a intutive fashion. This project has
been tested with gmail.

The emailer handler consists of two files:

1. email_handler.py
2. email_container.py
3. config.py
4. email_handler_test.py

###1. email_handler.py 
Hosts the emailHandler class. This class is supposed to take care of all tasks related to the mail box. The class provides API's to fetch mails on different filters, send mail with attachments and retrieve the list of mailbox folders present.

###2. email_container.py
Hosts a class that is used to encapsulte all the information in an email. 
This is used in the email_container.py. This also needs to be used if we 
want to sent an email.


####3. config.py
This is used to store the configuration parameters for the module.


###4. email_handler_test.py
Shows sample usage of the module. Information about each test is commented.


Usage Instructions
------------------
Configure the downloads folder in config.py. The API's are documented
and the docstrings explaint the functionality. For further understanding
of usage refer email_handler_test.py.



Note:
----
To acces a mailbox one has to enable the imap configuration on the email
settings of your mail server. Also this corrently doesn't support secure
authentication and sign in, This means if you are working with gmail please
enable access by less secure apps settings in gmail. The secure login will
be added in the future.
