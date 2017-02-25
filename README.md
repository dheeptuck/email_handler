Email Handler
=============

The emailer handler consists of two files:

1. email_handler.py
2. email_container.py

email_handler.py 
Hosts the emailHandler class. This class is supposed to take care of all tasks related to
the mail box. The class provides API's to fetch mails on different filters, send mail with
attachments and retrieve the list of mailbox folders present.

email_container.py
Hosts a class that is used to encapsulte all the information in an email. This is used in the
email_container.py. This also needs to be used if we want to sent an email.


For the usage of the module refer email_handler_test.py
