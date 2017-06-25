## Email Handler


This project provides the basic functionality to access contents of a mailbox
and use the features of IMAP and SMTP in a intuitive fashion. This project has
been tested with gmail. The project can act as a backeend to build a fully
functional mailbox.

Following actions can be performed with the email handler:

1. Retrieve emails from inbox including attachments
2. Get email's based on index(newest , oldest, specific index etc)
3. Fetching emails between dates
4. Fetching emails from a specific folder.
5. Fetching all unread mails.
6. Sending mail's with/without attachments
7. Move mails between mailbox folders(i.e inbox, spam etc)


The email handler consists of four files:

1. email_handler.py
2. email_container.py
3. config.py
4. email_handler_test.py



**1. email_handler.py **

Hosts the emailHandler class. This class is designed to take care of all tasks related to the mail box. The class provides API's to 

1. Fetch mails on different filters
2. Send mail with attachments 
3. Retrieve the list of mailbox folders present.

**2. email_container.py**

Hosts a class that is used to encapsulte all the information in an email. 
This is used in the email_container.py. This also needs to be used if we 
want to sent an email.

**3. config.py**

This is used to store the configuration parameters for the module.


**4. email_handler_test.py**

Shows sample usage of the module. Information about each test is commented.


**Usage Instructions**

Configure the downloads folder in config.py. The API's are documented
and the docstrings explain the functionality. For further understanding
of usage refer email_handler_test.py.



**Note**

To access a mailbox one has to enable the imap configuration on the email
settings of ones mail server. Also there is no support for secure sign in,
This means "access by less secure apps" needs to be enabled in gmail settings.
The secure login will be added in the future.

The source code of the project can be accessed from
[git hub](https://github.com/dheeptuck/email_handler)