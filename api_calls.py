from PIL import Image
import requests
from io import BytesIO
import cv2
import numpy as np

base_url="https://hexam.eu-gb.mybluemix.net/"

def get_test_details(test_id):
    path="api/test/"
    try:
        print("making call: ",base_url+path+test_id)
        r = requests.get(url=base_url+path+test_id)
        return r.json()
    except:
        return None

def get_student_details(email):
    path = "api/student/"
    try:
        print("making call: ",base_url+path+email)

        r = requests.get(url=base_url + path + email)
        return r.json()
    except:
        return None

def get_student_img(email):
    student_details=get_student_details(email)
    try:
        print("making call: ",student_details['imgpath'])

        response = requests.get(student_details['imgpath'])
        print("got img")
        img = Image.open(BytesIO(response.content))
        img = np.array(img)

        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    except :
        return None
def put_reports(test_id,student_email,tab_switches,face_suspicion,eye_suspicion):
    try :
        path = "api/student/report/"

        # Making a PUT request
        r = requests.put(base_url+path+test_id, data={'studentEmail': student_email,'faceSuspicion': face_suspicion,'eyeSuspicion': eye_suspicion,'tabSwitches': tab_switches})

        # check status code for response recieved
        # success code - 200
        print(r)

        # print content of request
        print(r.content)
        return True
    except:
        return False


# put_reports("d7689f6c-edde-4d06-ad14-","lk@gmail",31,30,30)

# print(get_test_details("c6c76b4a-bf53-4a9e-9c33-b86e11c53371"))
#
# from PIL import Image
# import requests
# from io import BytesIO
# import cv2
# import numpy as np
# response = requests.get("https://hexam.eu-gb.mybluemix.net/uploads/1590492232629banner-test.jpg")
#
# img = Image.open(BytesIO(response.content))
# img = np.array(img)
#
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#
# cv2.imshow("img",np.array(img) )
# while(True):
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break