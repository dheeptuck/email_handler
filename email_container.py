


class emailContainer:
	"""
	A continer to store all the attribute related to an email.
	"""

	def __init__(self):
		"""
		1. From
		2. To
		3. Date
		4. Message-ID
		5. Content-Type
		6. MIME-Version
		7. Content
		8. Subject
		"""
		self.from_address = None
		self.to_address = None
		self.date = None
		self.message_id = None
		self.content_type = None
		self.mime_version = None
		self.content = None
		self.subject = None
		self.attachment_name = None
		self.attachment = None
		self.container = {}


	def __str__(self):
		return ("From: {}\n"
			    "To: {}\n"
			    "Date: {}\n"
			    "Subject: {}\n"
			    #"Content: {}\n"
			    "attachment_name: {}\n").format(
													self.from_address,
													self.to_address,
													self.date,
													self.subject,
													#self.content,
													self.attachment_name)