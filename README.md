# wagtail_newsletter
This app implements newsletters, subscriptions and email-notifications in Wagtail CMS.
It allows you to manage all your organizations newsletters in the Wagtail CMS backend. Newsletters can be created, collected and curated and are sent to the subscribers as an editor wishes. 

This app also handles subscription, validation and unsubscribing.
It is also translatable.

# Installation

Clone this repository and copy the ```newsletter``` directory into your Wagtail CMS project. 

Enable the application by adding it to your ```INSTALLED_APPS``` list like so:

```python
INSTALLED_APPS = [
	...,
	'newsletter',
	...
]
```

Since this app uses email notifications, please also make sure you have your project configured so it can send emails.

After applying the necessary customizations (see below), run ```python manage.py makemigrations``` to generate the necessary migrations and ```python manage.py migrate``` to apply them to your database.

# Customization

This Wagtail application comes with all needed templates. However, some parts of the source code and templates need to be customized to your organization.

## Email Subject

The file ```newsletter/signals.py``` contains a hardcoded email-heading that needs to be customized to your organization.
```python
subject = 'New newsletter from YOUR ORGANIZATION'
```
Change this to your liking.

## Twitter and Facebook Icons

The templates used during the subscription process use Twitter and Facebook buttons. Their links need to be set, or the icons need to be removed.

The templates in question are:

- validate_success.html
- validate_fail.html
- unsubscribe.html
- unsubscribe_success.html
- subscribe.html
- subscribe_fail.html
- subscribe_success.html

## Message template

This app includes a html email-template that you can use to create a nicer looking notification email. Change ```templates/newsletter/email_template.html``` accordingly.

# Usage

Newsletters are created akin to a blog page. Each newsletter is a seperate Wagtail page. You can add new content blocks to the newsletter and send it out when it is ready. The editor has a simple checkbox that needs to be checked if you wish a notification email to be sent.

Each content block consists of a heading, a subheading an image and a text block. Not all need to be populated. Once your newsletter is finished, simply check the checkbox "notify subscribers" and Wagtail CMS will send out an email to your subscribers.
Leaving the checkbox unchecked when translating a newsletter avoids spam, since sending our emails is triggered each time a page is saved.

# Privacy

Since subscribers leave their name and email address, privacy needed to be addressed. All email-addresses and names a stored in encrypted database fields, using the [Django-Cryptography](https://pypi.org/project/django-cryptography/) library. The during the validation process, a verification email is sent out to a subscriber with a link that needs to be clicked or copied into the browser. This ensures that only people that have access to the email account they are impersonating can subscribe.

Subscribers are furthermore curatable by hand. So even if the automated unsubscription fails, an editor (or somebody with the right privileges) can remove (or add) any given subscriber.

# Dependencies
- [Django-Cryptography](https://pypi.org/project/django-cryptography/)

# Environment

This app is tested with:
- Python 3.8, 3.9, 3.10
- Wagtail 2.13, 2.14, 2.15
- Django 3.1, 3.2
- Django-Cryptography 1.0