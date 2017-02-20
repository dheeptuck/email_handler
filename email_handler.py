import imaplib
import email
import re
import time
import datetime
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

from email_container import emailContainer



class emailHandler:
	"""
	This class is designed to handle all functionality with respect
	to a mailbox.
	"""
	def __init__(self, email_id, password, SSL_address, smtp_server_address,\
	            smtp_port):
		"""
		@param1: email_id
		@param2: password
		@param3: SSL_address
		"""
		self.email_id = email_id
		self.password = password
		self.SSL_address = SSL_address
		self.smtp_server_address = smtp_server_address
		self.smtp_port = smtp_port
		self.mail = imaplib.IMAP4_SSL(self.SSL_address)
		self.mail.login(email_id, password)
		self.mail.list()
		#The regex for the folder patten string
		self.mail_list_pattern = re.compile(
			r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')


	def get_mailbox_folders(self):
		"""
		Returns a list of mailbox folders This can be used to do
		search queries in specific mail folders
		"""
		mailbox_folders = []
		lst = self.mail.list()
		for line in lst[1]:
			mailbox_folders.append(self.parse_list_response(line)[2])
		return mailbox_folders



	def parse_list_response(self, line):
		"""
		Helper function for get_mailbox_folders to parse the utf-8
		encoded mail.list parse_list_response
		@param1: line to be parsed
		"""
		match = self.mail_list_pattern.match(line.decode('utf-8'))
		flags, delimiter, mailbox_name = match.groups()
		mailbox_name = mailbox_name.strip('"')
		return (flags, delimiter, mailbox_name)


	def get_first_text_block(self, email_message_instance):
		"""
		Parses and returns a string containing the content of email.
		@param1: Instance of email
		"""
		maintype = email_message_instance.get_content_maintype()
		if maintype == 'multipart':
			for part in email_message_instance.get_payload():
				if part.get_content_maintype() == 'text':
					return part.get_payload()
		elif maintype == 'text':
			return email_message_instance.get_payload()


	def get_mail_by_id(self, mailbox_folder, id):
		"""
		Returns the Nth mail in the specified mailbox folder.
		@param1: Mailbox folder from which the message needs to
		         be retrieved in string.
		@param2: The index of the message(1 denotes the oldest message
			and -1 denotes the newest message)
		@return: Returns a email contianer

		"""
		return_dict = {}
		self.mail.select(mailbox_folder)
		result, data = self.mail.uid('search', None, "ALL")
		latest_email_uid = data[0].split()[id] # data is a list.
		return self.get_email_by_uid(latest_email_uid)

	def get_all_mail_uid(self, mailbox_folder):
		return_dict = {}
		self.mail.select(mailbox_folder)
		result, data = self.mail.uid('search', None, "ALL")
		return data[0].split()


	def get_email_by_uid(self, email_uid):
		"""
		@param1: the uid for the email that we want to fetch
		@return: Returns a email container
		"""
		return_container = emailContainer()
		result, data = self.mail.uid('fetch', email_uid, '(RFC822)')# fetch the email body (RFC822) for the given ID
		raw_email = data[0][1]
		email_message = email.message_from_string(raw_email)
		utc_ts = time.mktime((email.utils.parsedate(email_message['Date'])))
		dt = datetime.datetime.fromtimestamp(utc_ts)
		return_container.from_address = email.utils.parseaddr(email_message['From'])
		return_container.to_address = email.utils.parseaddr(email_message['To'])
		return_container.date = dt 
		return_container.message_id = email_message['Message-ID']
		return_container.content_type = email_message['Content-Type']
		return_container.mime_version = email_message['MIME-Version']
		return_container.content = self.get_first_text_block(email_message)
		return_container.subject = email_message['Subject']
		return return_container

	def get_latest_email(self, mailbox_folder):
		"""
		Retrieves the latest mail in a given folder
		@param: Mailbox folder
		"""
		self.get_mail_by_id(mailbox_folder,-1)



	def get_emails_since_yesterday(self):
		"""
		Returns mail sent since yeterday.
		@param: None
		@return: List of reply dicts
		"""
		date = (datetime.date.today() - datetime.timedelta(1)).\
		        strftime("%d-%b-%Y")
		result, data = self.mail.uid('search', None, '(SENTSINCE {date})'.\
			     format(date=date))
		reply_list = []
		for uid in data[0].split():
			reply_list.append(self.get_email_by_uid(uid))
		return reply_list

	def get_uid_between_dates(self, start_date=None, end_date=None):
		"""
		Retrieves the uid between the dates.
		@param1: start date from which retrieval needs to start
		@param2: end date for the retrieval
		@return: List of uid's
		"""
		reply_list = []
		start_date = datetime.datetime.strptime(start_date, "%d-%m-%Y")
		start_date = start_date.strftime("%d-%b-%Y")
		end_date = datetime.datetime.strptime(end_date, "%d-%m-%Y")
		end_date = end_date.strftime("%d-%b-%Y")
		result, data = self.mail.uid('search', '(SINCE {date})'\
			.format(date=start_date),'(BEFORE {end_date})'\
			.format(end_date=end_date))
		for uid in data[0].split():
			reply_list.append(uid)
		return reply_list

	def get_emails_between_dates(self, start_date=None, end_date=None):
		"""
		Retrieves all mails between two dates. This is not a optimized
		retrieval because it retrieves the entire email between the
		given dates. For optimized retrieval use get_uid_between_dates
		and then use the uid to retrieve the email using get_email_by_uid(uid).
		This is a wrapper over get_uid_between_dates.
		@param1: start date from which retrieval needs to start
		@param2: end date for the retrieval
		@return: List of email dict
		"""
		reply_list = []
		uid_list = self.get_uid_between_dates(start_date, end_date)
		for uid in uid_list:
			reply_list.append(self.get_email_by_uid(uid))
		return reply_list

	def get_uid_unread_emails(self, mailbox_folder):
		"""
		Gets the  UID of all unread emails.
		@param 1: mailbox folder name
		@return: list of UID's
		"""
		reply_list = []
		self.mail.select(mailbox_folder)
		result, data = self.mail.uid('search', None,"UNSEEN")
		for uid in data[0].split():
			reply_list.append(uid)
		return reply_list

	def get_unread_emails(self, mailbox_folder):
		"""
		Wrapper over get_uid_unread_emails to return a list
		of email_containers having unread emails
		@param 1: mailbox folder name
		@return: list off email containers
		"""
		reply_list = []
		for uid in self.get_uid_unread_emails(mailbox_folder):
			reply_list.append(self.get_email_by_uid(uid))
		return reply_list

	def get_uid_read_emails(self, mailbox_folder):
		"""
		Gets the  UID of all read emails.
		@param 1: mailbox folder name
		@return: list of UID's
		"""
		reply_list = []
		all_uid_list = self.get_all_mail_uid(mailbox_folder)
		unread_uid_list =  self.get_uid_unread_emails(mailbox_folder)
		for uid in all_uid_list:
			reply_list.append(uid)
		#remove all read UID's from the list
		for uid in unread_uid_list:
			reply_list.remove(uid)
		return reply_list

	def get_read_emails(self, mailbox_folder):
		"""
		Wrapper over get_uid_read_emails to return a list
		of email_containers having read emails
		@param 1: mailbox folder name
		@return: list off email containers
		"""
		reply_list = []
		for uid in self.get_uid_read_emails(mailbox_folder):
			reply_list.append(self.get_email_by_uid(uid))
		return reply_list



	def send_mail(self, email_container):
		"""
		Send mail to the specified address
		TODO: add support for multiple attachments
		@param1: The email container
		"""
		msg = MIMEMultipart()
		msg['From'] = self.email_id
		msg['To'] = email_container.to_address
		msg['Subject'] = email_container.subject
		body = email_container.content
		msg.attach(MIMEText(body, 'plain'))

		#copy attachment if present
		if email_container.attachment is not None:
			filename = email_container.attachment_name
			attachment = email_container.attachment
			part = MIMEBase('application', 'octet-stream')
			part.set_payload((attachment).read())
			encoders.encode_base64(part)
			part.add_header('Content-Disposition', "attachment; \
				            filename= %s" % filename)
			msg.attach(part)

		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(msg['From'], self.password)
		text = msg.as_string()
		server.sendmail(msg['From'], msg['To'], text)
		server.quit()



	

