# import boto3
# import os
# import cv2
# from PIL import Image
# from io import BytesIO
# from pymongo import MongoClient
# from collector_setting import *
# from selenium.common.exceptions import WebDriverException

# # s3 = boto3.client('s3')
# # S3_BUCKET_NAME = os.environ['S3_BUCKET']



# # img = open(os.path.join(os.getcwd(), "kakao_image", "{}.png".format()))
# # s3.put_object(
# #     Body=img,
# #     Bucket=S3_BUCKET_NAME,
# #     Key=str(),
# # )

# url = 'https://kr-a.kakaopagecdn.com/P/C/2320/c1a/78363bcd-eec2-4d43-8045-c1f732ad87a1.webm'
# url = 'https://kr-a.kakaopagecdn.com/P/C/2690/c1a/6d207528-1893-4efb-b2d9-5119018abeb1.webm'
# url = 'https://kr-a.kakaopagecdn.com/P/C/2511/c1a/59c77f26-a29e-4be0-b49f-4abecb220b51.webm'
# name = "gg"

# def wheel_element(element, deltaY = 120, offsetX = 0, offsetY = 0):
#   error = element._parent.execute_script("""
#     var element = arguments[0];
#     var deltaY = arguments[1];
#     var box = element.getBoundingClientRect();
#     var clientX = box.left + (arguments[2] || box.width / 2);
#     var clientY = box.top + (arguments[3] || box.height / 2);
#     var target = element.ownerDocument.elementFromPoint(clientX, clientY);

#     for (var e = target; e; e = e.parentElement) {
#       if (e === element) {
#         target.dispatchEvent(new MouseEvent('mouseover', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
#         target.dispatchEvent(new MouseEvent('mousemove', {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY}));
#         target.dispatchEvent(new WheelEvent('wheel',     {view: window, bubbles: true, cancelable: true, clientX: clientX, clientY: clientY, deltaY: deltaY}));
#         return;
#       }
#     }    
#     return "Element is not interactable";
#     """, element, deltaY, offsetX, offsetY)
#   if error:
#     raise WebDriverException(error)

# driver = driver_set()
# url = 'https://page.kakao.com/home?seriesId=56310553'
# get_url_untill_done(driver, url)

# item_artist = driver.find_elements(By.XPATH, "//div[@class='text-ellipsis css-7a7cma']")[1].text.split(',')
# print(item_artist)

a = ' 123'

a = a.strip()

print(a)