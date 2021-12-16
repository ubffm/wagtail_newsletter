from django.apps import AppConfig

class NewsletterConfig(AppConfig):
	name = 'newsletter'

	def ready(self):

		import newsletter.signals