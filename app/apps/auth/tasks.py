import time
from app.core.celery_app import celery_app
from loguru import logger

@celery_app.task(name="auth.send_welcome_email")
def send_welcome_email_task(user_email: str, username: str):
    """
    Simulates sending a welcome email in the background.
    """
    logger.info(f"Starting to send welcome email to {user_email}...")
    
    # Simulate a network delay (e.g., talking to an Email API like SendGrid)
    time.sleep(5)
    
    logger.info(f"Welcome email successfully sent to {username} ({user_email})")
    return {"status": "sent", "recipient": user_email}
