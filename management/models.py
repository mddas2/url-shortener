# models.py in url_shortener app

from django.db import models
from account.models import CustomUser
from django.utils import timezone
import qrcode
from PIL import Image
import os
from django.conf import settings

class ShortenedURL(models.Model):
    user = models.ForeignKey(CustomUser,related_name = "urls", on_delete=models.CASCADE)
    long_url = models.URLField()
    short_key = models.CharField(max_length=10, unique=True,null=True)
    click_count = models.PositiveIntegerField(default=0)
    expired_date = models.DateField(default=timezone.now() + timezone.timedelta(days=30))
    created_at = models.DateTimeField(auto_now_add=True)

    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.long_url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Print the current working directory
        print("Current Working Directory:", os.getcwd())

        img_path = os.path.join('qr_codes', f'{self.short_key}.png')

        # Save QR code image to MEDIA_ROOT
        full_path = os.path.join(settings.MEDIA_ROOT, img_path)
        img.save(full_path)

        # Use os.path.normpath to ensure consistent path format
        full_path = os.path.normpath(full_path)

        # Print the full path where the image is saved
        print("Full Path:", full_path)

        # Save QR code image path to qr_code field
        self.qr_code = img_path
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.short_key} - {self.long_url}"
