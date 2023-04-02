import cv2
from pyzbar.pyzbar import decode

#https://qr.io/?gclid=Cj0KCQjw8e-gBhD0ARIsAJiDsaVcIiGPicFv24csL6VdrTmjN8io0ppPIaom2kV66Y4h_WuUlNHtE7gaAiLdEALw_wcB
def QRReader():
    cam = cv2.VideoCapture(0)
    cam.set(5,640)
    cam.set(6,480)
    camera = True
    while camera == True:
        suceess,frame = cam.read()
        
        for i in decode(frame):
          
            decodeItem =i.data.decode('utf-8')
            print(decodeItem)
            print(type(decodeItem))
            #convert the string to list 
            my_list = eval(decodeItem)
            print(my_list[0])
            #load json object
            # json_object = json.loads(decodeItem)
            # print(json_object['Item_Name'])  # Output: 'Food'
            # print(json_object['Item_No'])  # Output: 1
            # print(json_object['Item_Price'])  # Output: 100
            # print(json_object['Discount'])  # Output: 0.1
            return my_list
            


# # Access the Item_Name field of the first element in the array
# first_item_name = json_array[0]['Item_Name']

# # Print the result
# print(first_item_name)
# QRReader()

# my_list = ["ItemName","ItemNo","ItemPrice","ItemCount","TotalPrice"]
# first_item = my_list[0]
# print(first_item)
