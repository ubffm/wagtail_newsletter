from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from newsletter.models import Subscriber, Newsletter


class NewsletterSubscriberAdmin(ModelAdmin):

    model = Subscriber
    menu_label = 'Subscribers'
    menu_icon = 'group'
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('email', 'full_name',)
    seach_fields = ('email', 'full_name',)


class NewsletterAdmin(ModelAdmin):
    model = Newsletter
    menu_label = 'Newsletters'
    menu_icon = 'doc-empty'
    list_display = ('date', 'teaser',)


class RegisterGroup(ModelAdminGroup):
    menu_label = 'Newsletter'
    menu_icon = 'mail'  # change as required
    menu_order = 300  # will put in 5th place (000 being 1st, 100 2nd)
    items = (NewsletterSubscriberAdmin, NewsletterAdmin,)


# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(RegisterGroup)
