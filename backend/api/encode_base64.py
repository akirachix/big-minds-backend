from django.conf import settings
import base64

def generate_password(formatted_time):
    data_to_encode = settings.LIPANAMPESA_SHORTCODE + settings.LIPANAMPESA_PASSKEY + formatted_time
    encoded = base64.b64encode(data_to_encode.encode()).decode()
    return encoded