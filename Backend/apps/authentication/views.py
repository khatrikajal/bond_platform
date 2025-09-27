from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from otp_helpers import OtpHelperMixin

class SendOtpAPIView(APIView, OtpHelperMixin):
    def post(self, request):
        phone_number = request.data.get("phone_number")
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        result = self.send_otp(phone_number)
        if result.get("success"):
            return Response({"message": "OTP sent successfully", "static_otp": self.STATIC_OTP if self.USE_STATIC_OTP else None})
        else:
            return Response({"error": result.get("error", "Failed to send OTP")}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VerifyOtpAPIView(APIView, OtpHelperMixin):
    def post(self, request):
        input_otp = request.data.get("otp")
        if not input_otp:
            return Response({"error": "OTP is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if self.verify_otp(input_otp):
            return Response({"message": "OTP verification successful"})
        else:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
