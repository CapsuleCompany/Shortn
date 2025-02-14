import qrcode
from io import BytesIO
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status
from PIL import Image

class GenerateQRCodeView(APIView):
    """
    API to generate a QR code for a given URL with an optional logo in the center.
    """
    parser_classes = [MultiPartParser, FormParser, JSONParser]  # Accept JSON and Form data

    def post(self, request):
        url = request.data.get("url")
        logo = request.FILES.get("logo")  # Optional logo

        if not url:
            return Response({"error": "URL is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        qr_img = qr.make_image(fill="black", back_color="white").convert("RGBA")

        # If a logo is provided, add it to the center
        if logo:
            try:
                logo_img = Image.open(logo)

                # Resize the logo
                logo_size = qr_img.size[0] // 4  # 1/4 of QR size
                logo_img = logo_img.resize((logo_size, logo_size), Image.Resampling.LANCZOS)  # ✅ Updated line

                # Calculate position to paste the logo
                pos = ((qr_img.size[0] - logo_size) // 2, (qr_img.size[1] - logo_size) // 2)
                qr_img.paste(logo_img, pos, mask=logo_img if logo_img.mode == "RGBA" else None)
            except Exception as e:
                return Response({"error": f"Invalid logo file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

        # Save QR code to a BytesIO buffer
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        buffer.seek(0)

        response = HttpResponse(buffer, content_type="image/png")
        response["Content-Disposition"] = 'inline; filename="qr_code.png"'
        return response