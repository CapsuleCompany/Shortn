from django.db import models

class QRCode(models.Model):
    url = models.URLField()
    qr_code_image = models.ImageField(upload_to="qr_codes/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url