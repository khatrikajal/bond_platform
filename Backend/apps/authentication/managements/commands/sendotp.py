# management/commands/sendotp.py
from django.core.management.base import BaseCommand
from otp_helpers import OtpHelperMixin

class Command(BaseCommand, OtpHelperMixin):
    help = "Send OTP to a phone number"

    def add_arguments(self, parser):
        parser.add_argument("phone_number", type=str, help="Phone number with country code")
        parser.add_argument("--otp", type=str, help="OTP to send (optional)")

    def handle(self, *args, **options):
        phone_number = options["phone_number"]
        otp = options.get("otp")
        result = self.send_otp(phone_number, otp)
        if result.get("success"):
            self.stdout.write(self.style.SUCCESS(f"OTP sent to {phone_number}"))
            if self.USE_STATIC_OTP:
                self.stdout.write(f"Use OTP: {self.STATIC_OTP}")
        else:
            self.stderr.write(self.style.ERROR(f"Failed to send OTP: {result.get('error')}"))
