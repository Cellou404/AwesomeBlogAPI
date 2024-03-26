from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        import users.signals


"""
    This is called when Django starts, it imports the signals module 
    so that any signal handlers are registered with Django's internal signals framework. 
"""
