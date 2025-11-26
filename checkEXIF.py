from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

img = Image.open('images/testimg.jpg')
exif = img._getexif()

if exif:
    print("EXIF data exists")
    for tag_id, value in exif.items():
        tag = TAGS.get(tag_id, tag_id)
        print(f"{tag}: {value}")
        
        if tag == 'GPSInfo':
            print("GPS DATA FOUND:")
            for gps_tag in value:
                gps_tag_name = GPSTAGS.get(gps_tag, gps_tag)
                print(f"  {gps_tag_name}: {value[gps_tag]}")
else:
    print("No EXIF data")