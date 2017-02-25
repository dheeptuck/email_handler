Email Handler
=============

This project provides the basic functionality to access contents of a mailbox
and use the features of IMAP and SMTP in a intutive fashion. This project has
been tested with gmail.

The emailer handler consists of two files:

1. email_handler.py
2. email_container.py

email_handler.py 
----------------
Hosts the emailHandler class. This class is supposed to take care of all tasks related to the mail box. The class provides API's to fetch mails on different filters, send mail with attachments and retrieve the list of mailbox folders present.

email_container.py
------------------
Hosts a class that is used to encapsulte all the information in an email. This is used in the
email_container.py. This also needs to be used if we want to sent an email.


For the usage of the module refer email_handler_test.py.

Note:
----
To acces a mailbox one has to enable the imap configuration on the email
settings of your mail server. Also this corrently doesn't support secure
authentication and sign in, This means if you are working with gmail please
enable access by less secure apps settings in gmail. The secure login will
be added in the future.
