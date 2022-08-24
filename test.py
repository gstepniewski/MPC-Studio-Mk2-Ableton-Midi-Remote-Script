from PIL import ImageDraw, Image
import io
import binascii

i = Image.new('RGB', (120,60), color=(255,0,0))
buf = io.BytesIO()
i.save(buf, format='JPEG')
byte_im = buf.getvalue()



print(binascii.hexlify(byte_im))