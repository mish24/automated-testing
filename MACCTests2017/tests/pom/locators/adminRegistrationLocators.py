class AdminRegistrationPageLocators(object):

	USERNAME = 'id_username'
	PASSWORD = 'id_password'
	FIRST_NAME = 'id_first_name'
	LAST_NAME = 'id_last_name'
	EMAIL = 'id_email'
	ADDRESS = 'id_address'
	

	USERNAME_ERROR = "id('div_id_username')/div/p/strong"
	FIRST_NAME_ERROR = "id('div_id_first_name')/div/p/strong"
	LAST_NAME_ERROR = "id('div_id_last_name')/div/p/strong"
	EMAIL_ERROR = "id('div_id_email')/div/p/strong"
	ADDRESS_ERROR = "id('div_id_address')/div/p/strong"
	

	HELP_BLOCK = 'help-block'
	MESSAGES = 'messages'
	SUBMIT_PATH = '//form[1]'