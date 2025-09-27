# otp_helpers.py
from twilio.rest import Client
import logging

class OtpHelperMixin:
    USE_STATIC_OTP = True  # Toggle this to False to use Twilio
    STATIC_OTP = "00000"

    # Twilio credentials - update when integrating Twilio
    TWILIO_ACCOUNT_SID = 'YOUR_ACCOUNT_SID'
    TWILIO_AUTH_TOKEN = 'YOUR_AUTH_TOKEN'
    TWILIO_PHONE_NUMBER = 'YOUR_TWILIO_PHONE_NUMBER'

    def __init__(self):
        if not self.USE_STATIC_OTP:
            self.twilio_client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
        else:
            self.twilio_client = None

    def send_otp(self, phone_number, otp=None):
        if self.USE_STATIC_OTP:
            otp = self.STATIC_OTP
            logging.info(f"[Static OTP] OTP for {phone_number} is {otp}")
            return {"success": True, "otp": otp}
        else:
            otp = otp or self.generate_otp()
            try:
                message = self.twilio_client.messages.create(
                    body=f"Your OTP code is {otp}",
                    from_=self.TWILIO_PHONE_NUMBER,
                    to=phone_number,
                )
                logging.info(f"[Twilio] Sent OTP to {phone_number}. SID: {message.sid}")
                return {"success": True, "sid": message.sid}
            except Exception as e:
                logging.error(f"Twilio send OTP error for {phone_number}: {e}")
                return {"success": False, "error": str(e)}

    def verify_otp(self, input_otp):
        if self.USE_STATIC_OTP:
            return input_otp == self.STATIC_OTP
        else:
            # Add real OTP verification logic here (e.g., DB/session check)
            raise NotImplementedError("Real OTP verification not implemented yet.")

    def generate_otp(self):
        import random
        return f"{random.randint(0, 99999):05d}"
