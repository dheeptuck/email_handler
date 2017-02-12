from email_handler import emailHandler      #Handler for all mailbox relates tasks
from email_container import emailContainer  #Contains all info in an email






if __name__ == "__main__":
	mailer = emailHandler('verduremail@gmail.com', 'Dabangg!', 'imap.gmail.com',\
							'smtp.gmail.com',587)
	

	#Print all available mail folders
	lst = mailer.get_mailbox_folders()
	print "List of mailbox folders"
	for info in lst:
		print info

	#Get email by order (-2 refers second newest)
	message = mailer.get_mail_by_id("Inbox",-2)
	print "Latest email in the mail box"
	print message

	#Fetch emails between dates
	y_mails = mailer.get_emails_between_dates(start_date = "10-02-2017", end_date="11-02-2017")
	print "fetching email between dates"
	for message in y_mails:
		print "*******************************************"
		print message

	#get the newest email from the specified email folder
	mailer.get_latest_email("Inbox")


	#send mail without an attachment
	print "sending mail without attachment"
	mail_to_send = emailContainer()
	mail_to_send.to_address = "dheeptuck@gmail.com"
	mail_to_send.subject = "TEST MAIL without attachment"
	mail_to_send.content = "Chutiya kuch kaam kar le \nemail container"
	mailer.send_mail(mail_to_send)


	#send mail with an attachment
	print "sending mail with attachment"
	mail_to_send = emailContainer()
	mail_to_send = emailContainer()
	mail_to_send.to_address = "dheeptuck@gmail.com"
	mail_to_send.subject = "TEST MAIL with attachment"
	mail_to_send.content = "Chutiya kuch kaam kar le \nemail container"
	mail_to_send.attachment = open("test_attachment.txt","rb") #Attach a opened file object 
	mail_to_send.attachment_name = "out.txt"
	mailer.send_mail(mail_to_send)