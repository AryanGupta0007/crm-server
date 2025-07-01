from django.apps import AppConfig
import threading

class AdminApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "admin_api"
    
    # def ready(self):
    #     from . import startup  # Import your function module here

    #     # Run in a new thread so it doesn't block server startup
    #     threading.Thread(target=startup.run_on_startup, daemon=True).start()
