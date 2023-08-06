import requests
import importlib
import os

def bing():
    while True:
        prompt = input("Enter the prompt: ").strip()
        if prompt == "bye":
            break
        url = "http://144.91.83.35:5500/"
        params = {"text": prompt}
        response = requests.get(url, params=params)
        print(response.text)

def installopenai():
    try:
        importlib.import_module('openai')
        print("openai is already installed")
    except ImportError:
        print("openai is not installed, installing now...")
        import subprocess
        subprocess.check_call(["pip", "install", "openai"])
        print("openai has been installed successfully!")

def bingfile():
    while True:
        message = input("User: ")
        if message.strip() == "":
            file_path = input("Enter path of text file (leave blank for default 'a.txt' file): ")
            if file_path.strip() == "":
                file_path = os.path.join(os.path.dirname(__file__), "a.txt")
            try:
                with open(file_path, "r") as file:
                    prompt = file.read()
            except FileNotFoundError:
                print(f"Error: File '{file_path}' not found.")
                continue
        elif message == "bye":
            break
        else:
            prompt = message.strip()
        url = "http://144.91.83.35:5500/"
        params = {"text": prompt}
        response = requests.get(url, params=params)
        print(response.text)

def openaiml(api_key=None):
    try:
        importlib.import_module('openai')
    except ImportError:
        installopenai()
    import openai
    if api_key:
        openai.api_key = api_key
    else:
        openai.api_key = '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'
    messages = [{"role": "system", "content": "You are a kind helpful assistant."}]
    while True:
        message = input("User: ").strip()
        if message == "bye":
            break
        else:
            messages.append({"role": "user", "content": message})
        try:
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        except Exception as e:
            print("An error occurred:", str(e))
            break
        reply = chat.choices[0].message.content
        print(f"Bot: {reply}")
        messages.append({"role": "assistant", "content": reply})

def openaifile(api_key=None):
    try:
        importlib.import_module('openai')
    except ImportError:
        installopenai()
    import openai
    if api_key:
        openai.api_key = api_key
    else:
        openai.api_key = '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'
    messages = [{"role": "system", "content": "You are a kind helpful assistant."}]
    while True:
        message = input("User: ")
        if message.strip() == "":
            file_path = input("Enter path of text file (leave blank for default 'a.txt' file): ")
            if file_path.strip() == "":
                file_path = os.path.join(os.path.dirname(__file__), "a.txt")
            try:
                with open(file_path, "r") as file:
                    text = file.read()
            except FileNotFoundError:
                print(f"Error: File '{file_path}' not found.")
                continue
            messages.append({"role": "user", "content": text})
        elif message == "bye":
            break
        elif len(message) > 2048:
            print("Message is too long. Please keep it under 2048 characters.")
            continue
        else:
            messages.append({"role": "user", "content": message})
            text = None
        try:
            chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        except Exception as e:
            print("An error occurred:", str(e))
            break
        reply = chat.choices[0].message.content
        print(f"Bot: {reply}")
        messages.append({"role": "assistant", "content": reply})
        
def installgpt4free():
    try:
        importlib.import_module('gpt4free')
        print("gpt4free is already installed")
    except ImportError:
        print("gpt4free is not installed, installing now...")
        import subprocess
        subprocess.check_call(["pip", "install", "gpt4free"])
        print("gpt4free has been installed successfully!")

def you():
    try:
        importlib.import_module('gpt4free')
    except ImportError:
        installgpt4free()
    import gpt4free
    from gpt4free import Provider
    prompt = input("Enter the prompt: ").strip()
    response = gpt4free.Completion.create(Provider.You, prompt=prompt)
    print(response)

def theb():
    try:
        importlib.import_module('gpt4free')
    except ImportError:
        installgpt4free()
    import gpt4free
    from gpt4free import Provider
    prompt = input("Enter the prompt: ").strip()
    response = gpt4free.Completion.create(Provider.Theb, prompt)
    print(response)

def useless():
    try:
        importlib.import_module('gpt4free')
    except ImportError:
        installgpt4free()
    from gpt4free import usesless
    message_id = ""
    while True:
        prompt = input("User: ")
        if prompt == 'bye':
            break
        req = usesless.Completion.create(prompt=prompt, parentMessageId=message_id)
        message_id = req["id"]
        print(req['text'])

def uselessadv():
    try:
        importlib.import_module('gpt4free')
    except ImportError:
        installgpt4free()
    from gpt4free import usesless
    import os
    message_id = ""
    while True:
        message = input("User: ")
        if message == 'bye':
            break
        if message.strip() == "":
            file_path = input("Enter path of text file (leave blank for default 'a.txt' file): ")
            if file_path.strip() == "":
                file_path = os.path.join(os.path.dirname(__file__), "a.txt")
            try:
                with open(file_path, "r") as file:
                    message = file.read()
            except FileNotFoundError:
                print(f"Error: File '{file_path}' not found.")
                continue
        req = usesless.Completion.create(prompt=message, parentMessageId=message_id)
        message_id = req["id"]
        print(req['text'])

def whileyou():
    try:
        importlib.import_module('gpt4free')
    except ImportError:
        installgpt4free()
    import gpt4free
    from gpt4free import Provider
    while True:
        prompt = input("User: ").strip()
        if prompt == "bye":
            break
        response = gpt4free.Completion.create(Provider.You, prompt=prompt)
        print(response)
    
def whiletheb():
    try:
        importlib.import_module('gpt4free')
    except ImportError:
        installgpt4free()
    import gpt4free
    from gpt4free import Provider
    while True:
        prompt = input("User: ").strip()
        if prompt == "bye":
            break
        try:
            response = gpt4free.Completion.create(Provider.Theb, prompt)
            print(response)
        except:
            print('some error')
    
def youadv():
    try:
        importlib.import_module('gpt4free')
    except ImportError:
        installgpt4free()
    import gpt4free
    from gpt4free import Provider
    safe_search = input("Do you want to turn on safe search? (1/0): ")
    include_links = input("Do you want to include links in the response? (1/0): ")
    detailed = input("Do you want a detailed response? (1/0): ")
    prompt = input("User: ").strip()
    if not safe_search:
        safe_search = False
    else:
        safe_search = True if safe_search.lower() == '1' else False
    if not include_links:
        include_links = False
    else:
        include_links = True if include_links.lower() == '1' else False
    if not detailed:
        detailed = False
    else:
        detailed = True if detailed.lower() == '1' else False    
    response = gpt4free.Completion.create(Provider.You,safe_search=False,include_links=False,detailed=False,prompt=prompt)
    print(response)
    print('\n')
    
def whileyouadv():
    while True:
        youadv()
        exit_choice = input("Do you want to exit? (y/n): ")
        if exit_choice.lower() == 'y' or 1 or 'yes':
            break

def generateemail():
    url = "https://disposable-gmail.p.rapidapi.com/generate"
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "b0d08f556cmshf9843920db7fe8bp1dfa21jsn6f16e1b1de9a",
        "X-RapidAPI-Host": "disposable-gmail.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers)
    print(response.json())

def getemail():
    url = "https://disposable-gmail.p.rapidapi.com/inbox"
    email = input("Enter the email: ")
    payload = {
        "email": email,
        "limit": 20
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "b0d08f556cmshf9843920db7fe8bp1dfa21jsn6f16e1b1de9a",
        "X-RapidAPI-Host": "disposable-gmail.p.rapidapi.com"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.json())

def bingrapidapi():
    url = "https://chatgpt-4-bing-ai-chat-api.p.rapidapi.com/chatgpt-4-bing-ai-chat-api/0.2/send-message/"
    prompt = input("Enter the prompt: ")
    payload = {
        "bing_u_cookie": "1qCR_WN-8qUYqWeyR5b0l2JFh8sZbYLrnyrLvMrje_XQQ_MCKFRSlKq2iF5DgklUbQHuP8niKq9G8if_7jwVxYnDHPyHRL5K08AHYV3i8sa7FsXoAAijc_Ct86oBPPyZFXBBV1CuumYL77xqdECk5ONljXJ-ytKVgyDKDLe4KiA_9OWiC5fyFrg-YfyVjT7C3N6kszzfzj1ojRdZ97oDXcg",
        "question": prompt
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "b0d08f556cmshf9843920db7fe8bp1dfa21jsn6f16e1b1de9a",
        "X-RapidAPI-Host": "chatgpt-4-bing-ai-chat-api.p.rapidapi.com"
    }
    response = requests.post(url, data=payload, headers=headers)
    print(response.json()[0]['text_response'])
    
def shortenurl():
    url = "https://url-shortener-service.p.rapidapi.com/shorten"
    data = input("Enter the long url: ")
    payload = { "url": data }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "b0d08f556cmshf9843920db7fe8bp1dfa21jsn6f16e1b1de9a",
        "X-RapidAPI-Host": "url-shortener-service.p.rapidapi.com"
    }
    response = requests.post(url, data=payload, headers=headers)
    print(response.json())
    
def websearch():
    url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPI"
    query = input("Enter the search string: ")
    pgnos = input("Enter the page Number (put 1): ")
    pgsize = input("Enter the page Size (put 10):")
    querystring = {"q": query ,"pageNumber":pgnos,"pageSize":pgsize,"autoCorrect":"true"}
    headers = {
        "X-RapidAPI-Key": "b0d08f556cmshf9843920db7fe8bp1dfa21jsn6f16e1b1de9a",
        "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    print(response.json())
   
def ocrapiimg1():
    url = "https://pen-to-print-handwriting-ocr.p.rapidapi.com/recognize/"
    img = input("Enter the image path: ")
    with open(img,'rb') as f:
        files = { "srcImg": f }
        payload = { "Session": "string" }
        headers = {
            "X-RapidAPI-Key": "b0d08f556cmshf9843920db7fe8bp1dfa21jsn6f16e1b1de9a",
            "X-RapidAPI-Host": "pen-to-print-handwriting-ocr.p.rapidapi.com"
        }
        response = requests.post(url, data=payload, files=files, headers=headers)
        print(response.json())
        
       
def ocrapiimg2():
    url = "https://ocr43.p.rapidapi.com/v1/results"
    img = input("Enter the image path: ")
    with open(img,'rb') as f:
        files = { "image": f }
        headers = {
            "X-RapidAPI-Key": "b0d08f556cmshf9843920db7fe8bp1dfa21jsn6f16e1b1de9a",
            "X-RapidAPI-Host": "ocr43.p.rapidapi.com"
        }
        response = requests.post(url, files=files, headers=headers)
        print(response.json())
        
def convertpdf2text():
    url = "https://pdf-to-text-converter.p.rapidapi.com/api/pdf-to-text/convert"
    pdf = input("Enter the pdf path: ")
    page = input("Enter the nos of pages: ")
    with open(pdf,'rb') as f:
        files = { "file": f }
        payload = { "page": page }
        headers = {
            "X-RapidAPI-Key": "b0d08f556cmshf9843920db7fe8bp1dfa21jsn6f16e1b1de9a",
            "X-RapidAPI-Host": "pdf-to-text-converter.p.rapidapi.com"
        }
        response = requests.post(url, data=payload, files=files, headers=headers)
        print(response.content)
        
def ocrapiurl():
    url = "https://ocr43.p.rapidapi.com/v1/results"
    data = input("Enter the URL: ")
    payload = { "url": data }
    headers = {
        "X-RapidAPI-Key": "b0d08f556cmshf9843920db7fe8bp1dfa21jsn6f16e1b1de9a",
        "X-RapidAPI-Host": "ocr43.p.rapidapi.com"
    }
    response = requests.post(url, data=payload, headers=headers)
    print(response.json())
     

def bitotodownload():          
    import platform
    import os
    system = platform.system()
    if system == "Windows":
        os.system('wget -P "{}" https://aiml6thsem.repl.co/bitoai/bito.exe'.format(os.path.join(os.path.expanduser("~"), "Downloads")))
    elif system == "Linux":
        machine = platform.machine()
        if machine == "x86_64":
            os.system('wget -P "{}" https://aiml6thsem.repl.co/bitoai/bito-linux-x86'.format(os.path.join(os.path.expanduser("~"), "Downloads")))
        elif machine == "armv7l" or machine == "aarch64":
            os.system('wget -P "{}" https://aiml6thsem.repl.co/bitoai/bito-linux-arm'.format(os.path.join(os.path.expanduser("~"), "Downloads")))
                     
def bito():
    import platform
    import os
    system = platform.system()
    if system == "Windows":
        os.system('wget https://aiml6thsem.repl.co/bitoai/bito.exe')
    elif system == "Linux":
        machine = platform.machine()
        if machine == "x86_64":
            os.system('wget https://aiml6thsem.repl.co/bitoai/bito-linux-x86')
            os.system('chmod +x bito-linux-x86')
        elif machine == "armv7l" or machine == "aarch64":
            os.system('wget https://aiml6thsem.repl.co/bitoai/bito-linux-arm')
            os.system('chmod +x bito-linux-arm')

def bitofast():
    import os
    os.system('wget https://aiml6thsem.repl.co/bito')
    os.system('chmod +x bito')
    
def helpdir():
    print(r"""
import sklearn.datasets as a
l = dir(a)
s = "ir"
r = [x for x in l if s in x]
print(r)
    """)

class dip:
    """
    import sb6 as s 
    s.dip.pg1()
    pg1() - Write a Program to read a digital image. Split and display image into 4 quadrants, up, down, right and left
    pg2() - Write a program to showrotation, scaling, and translation of an image.
    pg3() - Read an image, first apply erosion to the image and then subtract the result from the original. Demonstrate the difference in the edge image if you use dilation instead of erosion.
    pg4() - Read an image and extract and display low-level features such as edges, textures using filtering techniques
    pg5() - Demonstrate enhancing and segmenting low contrast 2D images
    """
    def pg1():
        print(r"""
import cv2
from PIL import Image, ImageDraw, ImageFont

img = cv2.imread('lena.tiff')
h,w = img.shape[:2]

# Define matrix size of image
left_top = img[0:h//2,0:w//2]
right_top = img[0:h//2,w//2:w]
left_bottom = img[h//2:h,0:w//2,]
right_bottom = img[h//2:h,w//2:w]

left = img[0:h,0:w//2]
right = img[0:h,w//2:w]
top = img[0:h//2,0:w]
bottom = img[h//2:h,0:w]

# show the images
cv2.imshow("left_top",left_top)
cv2.imshow("right_top",right_top)
cv2.imshow("left_bottom",left_bottom)
cv2.imshow("right_bottom",right_bottom)

cv2.imshow("left",left)
cv2.imshow("right",right)
cv2.imshow("top",top)
cv2.imshow("bottom",bottom)

# save the images
cv2.imwrite("left_top.tiff",left_top)
cv2.imwrite("right_top.tiff",right_top)
cv2.imwrite("left_bottom.tiff",left_bottom)
cv2.imwrite("right_bottom.tiff",right_bottom)

cv2.imwrite("left.tiff",left)
cv2.imwrite("right.tiff",right)
cv2.imwrite("top.tiff",top)
cv2.imwrite("bottom.tiff",bottom)

'''
# give names to images
img = Image.open('left_top.tiff')
draw = ImageDraw.Draw(img)
font = ImageFont.truetype('arial.ttf', 25)
text = '1st Quadrent'
draw.text((10, 10), text, fill=(255,0,0), font=font)
img.save('left_top.tiff')
'''

def writename(imgname,text):
    img = Image.open(imgname)
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('arial.ttf',25)
    draw.text((10,10),text,fill=(255,0,0),font=font)
    img.save(imgname)
    
writename("left_top.tiff",'1st quadrent')
writename("right_top.tiff",'2nd quadrent')
writename("left_bottom.tiff",'3rd quadrent')
writename("right_bottom.tiff",'4th quadrent')

writename("left.tiff",'left')
writename("right.tiff",'right')
writename("top.tiff",'top')
writename("bottom.tiff",'bottom')

# close on any key press
cv2.waitKey(0)
cv2.destroyAllWindows()
        """)

    def pg2():
        print(r"""
# USING CV2

# 1. Rotation
import cv2
img = cv2.imread('camaraman.png')
rows, cols = img.shape[:2]

rotation = cv2.warpAffine(img, cv2.getRotationMatrix2D((cols/2, rows/2), 45, 1), (cols, rows))
cv2.imshow('rotation', rotation)
cv2.imwrite('rotation.png', rotation)

cv2.waitKey()


# 2. scaling
import cv2
img = cv2.imread('camaraman.png')
(height,width)=img.shape[:2]

img_scaled = cv2.resize(img,None,fx=1.2,fy=1.2,interpolation = cv2.INTER_LINEAR)
cv2.imshow('Scaling - linear interpolation',img_scaled)
cv2.imwrite('Scaling - linear interpolation.png',img_scaled)

img_scaled = cv2.resize(img,None,fx=1.2,fy=1.2,interpolation = cv2.INTER_CUBIC)
cv2.imshow('Scaling - Cubic interpolation',img_scaled)
cv2.imwrite('Scaling - Cubic interpolation.png',img_scaled)

img_scaled = cv2.resize(img,(600,600),interpolation = cv2.INTER_AREA)
cv2.imshow('Scaling - Skewed Size',img_scaled)
cv2.imwrite('Scaling - Skewed Size.png',img_scaled)

cv2.waitKey()


# 3. translation (left and right side making black by moving image some down & right)
import cv2
import numpy as np

M = np.float32([[1, 0, 100], [0, 1, 50]])

img = cv2.imread('camaraman.png')
rows, cols = img.shape[:2]

img_translation = cv2.warpAffine(img, M, (cols, rows))
cv2.imshow('translation', img_translation)
cv2.imwrite('translation.png', img_translation)
cv2.waitKey()
        """)

    def pg3():
        print(r"""
import cv2
import numpy as np
img = cv2.imread('lena.png')

kernel = np.ones((5,5),np.uint8)
img_erosion = cv2.erode(img, kernel, iterations=1)
img_dilation = cv2.dilate(img, kernel, iterations=1)

edges = cv2.Canny(img,100,200)          # (img,threshold_lower = 100 ,threshold_upper = 200)
erosion_edges = cv2.erode(edges, kernel, iterations=1)
dilation_edge = cv2.dilate(edges, kernel, iterations=1)

result = cv2.subtract(img,img_erosion)

cv2.imshow('Image',img)
cv2.imshow('Erosion',img_erosion)
cv2.imshow('Dilation',img_dilation)
cv2.imshow('Edge image using Erosion',erosion_edges)
cv2.imshow('Edge image using Dilation',dilation_edge)
cv2.imshow('result after subtraction',result)

cv2.imwrite('Image.png',img)
cv2.imwrite('Erosion.png',img_erosion)
cv2.imwrite('Dilation.png',img_dilation)
cv2.imwrite('Edge image using Erosion.png',erosion_edges)
cv2.imwrite('Edge image using Dilation.png',dilation_edge)
cv2.imwrite('result after subtraction.png',result)

cv2.waitKey(0)
cv2.destroyAllWindows()
        """)

    def pg4():
        print(r"""
import cv2
import numpy as np
img = cv2.imread('lena.png',0)      # 0 for gray image #img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(img, (5,5), cv2.BORDER_DEFAULT)
blur_median = cv2.medianBlur(img,5)

sobelx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=5)
sobely = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=5)
sobel_edges = cv2.addWeighted(sobelx,0.5,sobely,0.5,0)

laplacian = cv2.Laplacian(blur, cv2.CV_64F) 

canny_edges = cv2.Canny(blur, 100, 200) 

bilateral = cv2.bilateralFilter(img,15,75,75)

kernel = cv2.getGaborKernel((31,31),5,0,10,0.5,0,ktype=cv2.CV_32F)
gabor = cv2.filter2D(img,cv2.CV_8UC3,kernel)

cv2.imshow('gray scale image',img)
cv2.imshow('Filtered output',blur)
cv2.imshow('Sobel Edges',sobel_edges)
cv2.imshow('laplacian',laplacian)
cv2.imshow('Canny Edge detection',canny_edges)
cv2.imshow('Blur Median',blur_median)
cv2.imshow('Bilateral Filter',bilateral)
cv2.imshow('Gabor Filter',gabor)

cv2.waitKey(0)
cv2.destroyAllWindows()
        """)

    def pg5():
        print(r"""
import cv2
import numpy as np

img = cv2.imread('lena.png',0)   # img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # for enhancing convert color to gray scale image

img_equalize = cv2.equalizeHist(img)

result = np.hstack((img,img_equalize))      # combine both

ret,img_thresh = cv2.threshold(img_equalize,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

cv2.imshow('Original Image Converted to grayscale',img)
cv2.imshow('Enhanced Image',img_equalize)
cv2.imshow('Original Image & Enhanced Image',result)
cv2.imshow('Segmented Image',img_thresh)

cv2.imwrite('Original Image.png',img)
cv2.imwrite('Original Image Converted to grayscale.png',img)
cv2.imwrite('Enhanced Image.png',img_equalize)
cv2.imwrite('Original Image & Enhanced Image.png',result)
cv2.imwrite('Segmented Image.png',img_thresh)

cv2.waitKey(0)
cv2.destroyAllWindows()
        """)

class shortdip:
    """
import sb6 as s 
s.dip.pg1()
pg1() - Write a Program to read a digital image. Split and display image into 4 quadrants, up, down, right and left
pg2() - Write a program to showrotation, scaling, and translation of an image.
pg3() - Read an image, first apply erosion to the image and then subtract the result from the original. Demonstrate the difference in the edge image if you use dilation instead of erosion.
pg4() - Read an image and extract and display low-level features such as edges, textures using filtering techniques
pg5() - Demonstrate enhancing and segmenting low contrast 2D images
    """
    def pg1():
        print(r"""
import cv2
img = cv2.imread('lena.tiff')
height, width = img.shape[:2]

top_left = img[0:height//2, 0:width//2]
top_right = img[0:height//2, width//2:width]
bottom_left = img[height//2:height, 0:width//2]
bottom_right = img[height//2:height, width//2:width]

top_section = img[0:height//2, :]
bottom_section = img[height//2:height, :]

left_section = img[:, 0:width//2]
right_section = img[:, width//2:width]

cv2.imshow('Top Left', top_left)
cv2.imshow('Top Right', top_right)
cv2.imshow('Bottom Left', bottom_left)
cv2.imshow('Bottom Right', bottom_right)

cv2.imshow('Top Section', top_section)
cv2.imshow('Bottom Section', bottom_section)

cv2.imshow('Left Section', left_section)
cv2.imshow('Right Section', right_section)

cv2.waitKey(0)
cv2.destroyAllWindows()
        """)

    def pg2():
        print(r"""
# USING PIL

# 1. Rotation
from PIL import Image
image = Image.open('camaraman.png')
rotated_image = image.rotate(45)
rotated_image.save('rotated.png')
rotated_image.show()

# 2. scaling
from PIL import Image
img = Image.open('camaraman.png')

# Linear interpolation
img_linear = img.resize((int(img.width*1.2), int(img.height*1.2)), resample=Image.BILINEAR)
img_linear.save('linear scaling.png')
img_linear.show()

# Cubic interpolation
img_cubic = img.resize((int(img.width*1.2), int(img.height*1.2)), resample=Image.BICUBIC)
img_cubic.save('cubic scaling.png')
img_cubic.show()

# Skewed size
img_skewed = img.resize((600, 600), resample=Image.LANCZOS)
img_skewed.save('skewed scaling.png')
img_skewed.show()

# 3. translation (left and right side making black by moving image some down & right)
from PIL import Image
image = Image.open('camaraman.png')
x = 100 ; y=50                                       # Translate the image by (x, y) pixels
translated_image = image.transform(image.size, Image.AFFINE, (1, 0, x, 0, 1, y))
translated_image.save('translated.png')
translated_image.show()
        """)

    def pg3():
        print(r"""
import cv2
import numpy as np
img = cv2.imread('lena.png')

edges = cv2.Canny(img,100,200)
kernel = np.ones((5,5),np.uint8)

img_erosion = cv2.erode(img, kernel, iterations=1)
img_dilation = cv2.dilate(img, kernel, iterations=1)

erosion_edges = cv2.erode(edges, kernel, iterations=1)
dilation_edge = cv2.dilate(edges, kernel, iterations=1)

result = cv2.subtract(img,img_erosion)

cv2.imshow('Image',img)
cv2.imshow('Erosion',img_erosion)
cv2.imshow('Dilation',img_dilation)
cv2.imshow('Edge image using Erosion',erosion_edges)
cv2.imshow('Edge image using Dilation',dilation_edge)
cv2.imshow('result after subtraction',result)

cv2.waitKey(0)
cv2.destroyAllWindows()
        """)

    def pg4():
        print(r"""
import cv2
import numpy as np
img = cv2.imread('lena.png',0)

blur = cv2.GaussianBlur(img, (5,5), cv2.BORDER_DEFAULT)
blur_median = cv2.medianBlur(img,5)

sobelx = cv2.Sobel(blur, cv2.CV_64F, 1, 0, ksize=5)
sobely = cv2.Sobel(blur, cv2.CV_64F, 0, 1, ksize=5)
sobel_edges = cv2.addWeighted(sobelx,0.5,sobely,0.5,0)

laplacian = cv2.Laplacian(blur, cv2.CV_64F) 
canny_edges = cv2.Canny(blur, 100, 200) 
bilateral = cv2.bilateralFilter(img,15,75,75)
kernel = cv2.getGaborKernel((31,31),5,0,10,0.5,0,ktype=cv2.CV_32F)
gabor = cv2.filter2D(img,cv2.CV_8UC3,kernel)

cv2.imshow('gray scale image',img)
cv2.imshow('Filtered output',blur)
cv2.imshow('Sobel Edges',sobel_edges)
cv2.imshow('laplacian',laplacian)
cv2.imshow('Canny Edge detection',canny_edges)
cv2.imshow('Blur Median',blur_median)
cv2.imshow('Bilateral Filter',bilateral)
cv2.imshow('Gabor Filter',gabor)

cv2.waitKey(0)
cv2.destroyAllWindows()
        """)

    def pg5():
        print(r"""
import cv2
import numpy as np

img = cv2.imread('lena.png',0)
img_equalize = cv2.equalizeHist(img)
result = np.hstack((img,img_equalize))
ret,img_thresh = cv2.threshold(img_equalize,0,255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)

cv2.imshow('Original Image Converted to grayscale',img)
cv2.imshow('Enhanced Image',img_equalize)
cv2.imshow('Original Image & Enhanced Image',result)
cv2.imshow('Segmented Image',img_thresh)
        """)

class ml():
    """
import sb6 as s 
s.ml.fs()
enjoysportdataset()   - for find s and candidate elimination
fs() - Find S algorithm 
ce() - Candidate Elimination 
nbnos() - Naive Bayesian Classifier for numbers automatic: Compute the accuracy of the classifier, considering few test data sets
nbother() - Naive Bayesian Classifier for numbers manual 
nbtext() - Naive Bayesian Classifier for text :Assuming a set of documents that need to be classified : Calculate the accuracy, precision, and recall for your data set.
svm() - Demonstrate the working of SVM classifier for a suitable data set
    """
    def enjoysportdataset():
        print(r"""
enjoysport.csv
        
sky,airtemp,humidity,wind,water,forcast,enjoysport
sunny,warm,normal,strong,warm,same,yes
sunny,warm,high,strong,warm,same,yes
rainy,cold,high,strong,warm,change,no
sunny,warm,high,strong,cool,change,yes
        """)
    def fs():
        """
    FIND-S: FINDING A MAXIMALLY SPECIFIC HYPOTHESIS
    1. Initialize h to the most specific hypothesis in H
    2. For each positive training instance x
            For each attribute constraint a, in h
                If the constraint a, is satisfied by x
                    Then do nothing
                Else replace a, in h by the next more general constraint that is satisfied by x
    3. Output hypothesis h
    
    The LIST-THEN-ELIMINATE
    1. VersionSpace c a list containing every hypothesis in H
    2. For each training example, (x, c(x))
            remove from VersionSpace any hypothesis h for which h(x) != c(x)
    3. Output the list of hypotheses in VersionSpace
        """
        print(r"""
import pandas as pd
import numpy as np
fulldata = pd.read_csv('enjoysport.csv')  

data = np.array(fulldata.iloc[:,:-1])    
target = np.array(fulldata.iloc[:,-1])   # iloc[start heigth : end height , start width : end width]

sp = ['0']*len(data[0])
for i, instance in enumerate(data):
    if target[i].lower() == 'yes':
        for j, attribute in enumerate(instance):
            if sp[j] == '0':
                sp[j] = attribute
            elif sp[j] != attribute:
                sp[j] = '?'
                
print("Specific hypothesis: ",sp)
        """)
    
    def ce():
        print(r"""
import pandas as pd
import numpy as np
fulldata = pd.read_csv('enjoysport.csv')

data = np.array(fulldata.iloc[:,:-1])    
target = np.array(fulldata.iloc[:,-1])   # iloc[start heigth : end height , start width : end width]

sp = ['0']*len(data[0])
gn = [["?" for i in range(len(sp))] for i in range(len(sp))]

for i, instance in enumerate(data):
    if target[i].lower() == 'yes':
        for j, attribute in enumerate(instance):
            if sp[j] == '0':
                sp[j] = attribute
            elif sp[j] != attribute:
                sp[j] = '?'
                gn[j][j] = sp[j]

    if target[i].lower() == 'no':
        for j, attribute in enumerate(instance):
            if sp[j] != attribute:
                gn[j][j] = sp[j]

gn = [x for x in gn if not all(val == '?' for val in x)]

print("Specific hypothesis: ",sp)
print("General hypothesis: ",gn)
        """)
        
    def nbnos():
        print(r"""
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
fulldata = load_iris()
data = fulldata.data
target = fulldata.target
xtrain,xtest,ytrain,ytest = train_test_split(data,target,test_size=0.3,random_state=42)

from sklearn.preprocessing import LabelEncoder
target = LabelEncoder().fit_transform(target)       # automatic text to numbers 

from sklearn.naive_bayes import GaussianNB
bclassifier = GaussianNB().fit(xtrain,ytrain)
bpredict = bclassifier.predict(xtest)       # predict for testing

from sklearn.metrics import accuracy_score,confusion_matrix
print(confusion_matrix(bpredict,ytest))          # if only diagonal no error
print(accuracy_score(bpredict,ytest))       # only get accurecy
        """)
        
    def nbnosothers():
        print(r"""
import pandas as pd
fulldata = pd.read_csv('Iris.csv')
data = fulldata.iloc[:,1:-1].values
target = fulldata.iloc[:,-1].values

'''
# OR 
import numpy as np
import pandas as pd
fulldata = pd.read_csv('Iris.csv')
data = np.array(fulldata.iloc[:,1:-1])
target = np.array(fulldata.iloc[:,-1])
'''

from sklearn.preprocessing import LabelEncoder
target = LabelEncoder().fit_transform(target)
'''
# OR maually
for i,h in enumerate(target):
    if target[i]=='Iris-setosa':
        target[i]='0'
    elif target[i]=="Iris-versicolor":
        target[i]='1'
    else:
        target[i]='2'
'''  

from sklearn.model_selection import train_test_split
Xtrain,Xtest,ytrain,ytest = train_test_split(data,target,test_size=0.3,random_state=42)

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
classifier=GaussianNB().fit(Xtrain,ytrain)
y_pred=classifier.predict(Xtest)
print("Accuracy=",accuracy_score(ytest, y_pred)*100)

'''
# OR manually
from sklearn.naive_bayes import GaussianNB
classifier=GaussianNB().fit(Xtrain,ytrain)
y_pred=classifier.predict(Xtest)
pc=0
nc=0
for i,h in enumerate(y_pred):
    if ytest[i]==y_pred[i]:
        pc+=1
    else:
        nc+=1
tot=len(y_pred)
pc=(pc/tot)*100
nc=(nc/tot)*100
if pc>nc:
    print("Accuracy=",pc," which is positive")
else:
    print("Accuracy=",nc," which is negative")
'''
        """)
        
    def nbtext():
        """
        Assuming a set of documents that need to be classified, use the naive Bayesian Classifier model to perform this task. 
        Calculate the accuracy, precision, and recall for your data set.
        """
        print(r"""
import pandas as pd
msg = pd.read_csv('dataset_text.csv', names=['message', 'label'])

print("Total Instances of Dataset: ", msg.shape[0])

msg['labelnum'] = msg.label.map({'pos': 1, 'neg': 0})
X = msg.message
y = msg.labelnum

from sklearn.model_selection import train_test_split
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y)

# required to convert string sentence to float
from sklearn.feature_extraction.text import CountVectorizer
count_v = CountVectorizer()
Xtrain_dm = count_v.fit_transform(Xtrain)
Xtest_dm = count_v.transform(Xtest)

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB()
clf.fit(Xtrain_dm, ytrain)
pred = clf.predict(Xtest_dm)

from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score
print('\nAccuracy Metrics: ')
print('Accuracy: ', accuracy_score(ytest, pred))
print('Recall: ', recall_score(ytest, pred))
print('Precision: ', precision_score(ytest, pred))
print('Confusion Matrix: \n', confusion_matrix(ytest, pred))

'''
#dataset_text.csv

I love this sandwich,pos
This is an amazing place,pos
I feel very good about these beers,pos
This is my best work,pos
What an awesome view,pos
I do not like this restaurant,neg
I am tired of this stuff,neg
'''
        """)
        
    def svm():
        """
    The fit_transform method is used to fit the scaler to the training data and transform the training data at the same time. 
    However, for the test data, we only need to transform it based on the scaler that was fit to the training data. 
    Therefore, we only need to use the transform method on the test data after fitting the scaler to the training data.
        """
        print(r"""
import pandas as pd
data = pd.read_csv('SocialNetworkAds.csv')
X = data.iloc[:,:-1].values
y = data.iloc[:,-1].values

from sklearn.model_selection import train_test_split
Xtrain,Xtest,ytrain,ytest = train_test_split(X,y,test_size=0.3,random_state=42)
        
from sklearn.preprocessing import StandardScaler
s = StandardScaler()
Xtrain = s.fit_transform(Xtrain)
Xtest = s.transform(Xtest)

from sklearn.svm import SVC
sc = SVC(kernel='rbf',random_state=0).fit(Xtrain,ytrain)
ypred = sc.predict(Xtest)

from sklearn.metrics import accuracy_score,confusion_matrix
print(accuracy_score(ytest,ypred))
print(confusion_matrix(ytest,ypred))

'''
SocialNetworkAds.csv

Age,EstimatedSalary,Purchased
19,19000,0
35,20000,0
26,43000,0
27,57000,0
19,76000,0
27,58000,0
27,84000,0
32,150000,1
25,33000,0
35,65000,0
'''
        """)
    def id3():
        """
    building decision trees

    - load_csv(filename): reads in a CSV file and returns the dataset and headers as a tuple.
    - subtables(data, col, delete): creates subtables for a given column in the dataset.
    - entropy(S): calculates the entropy of a set of data.
    - compute_gain(data, col): calculates the information gain for a given column in the dataset.
    - build_tree(data, features): builds a decision tree using the ID3 algorithm.
    - print_tree(node, level): prints the decision tree to the console.
    - classify(node, x_test, features): classifies a test instance using the decision tree.
        """
        print(r"""
import math 
import csv

def load_csv(filename):
	lines=csv.reader(open(filename,"r"))
	dataset=list(lines)
	headers=dataset.pop(0)
	return dataset,headers

class Node:
	def __init__(self,attribute):
		self.attribute=attribute
		self.children=[]
		self.answer=""

def subtables(data,col,delete):
	dic={}
	coldata=[row[col] for row in data]
	attr=list(set(coldata))
	counts=[0]*len(attr)
	r=len(data)
	c=len(data[0])
	for x in range(len(attr)):
		for y in range(r):
			if data[y][col]==attr[x]:
				counts[x]+=1
	for x in range(len(attr)):
		dic[attr[x]]=[[0 for i in range(c)]for j in range(counts[x])]
		pos=0
		for y in range(r):
			if data[y][col]==attr[x]:
				if delete:
					del data[y][col]
				dic[attr[x]][pos]=data[y]
				pos+=1
	return attr,dic
	
def entropy(S):
	attr=list(set(S))
	if len(attr)==1:
		return 0
	counts=[0,0]
	for i in range(2):
		counts[i]=sum([1 for x in S if attr[i]==x])/(len(S)*1.0)
	sums=0
	for cnt in counts:
		sums+=-1*cnt*math.log(cnt,2)
	return sums

def compute_gain(data,col):
	attr,dic=subtables(data,col,delete=False)
	total_size=len(data)
	entropies=[0]*len(attr)
	ratio=[0]*len(attr)
	total_entropy=entropy([row[-1] for row in data])
	for x in range(len(attr)):
		ratio[x]=len(dic[attr[x]])/(total_size*1.0)
		entropies[x]=entropy([row[-1] for row in dic[attr[x]]])
		total_entropy-=ratio[x]*entropies[x]
	return total_entropy

def build_tree(data,features):
	lastcol=[row[-1] for row in data]
	if(len(set(lastcol)))==1:
		node=Node("")
		node.answer=lastcol[0]
		return node
	n=len(data[0])-1
	gains=[0]*n
	for col in range(n):
		gains[col]=compute_gain(data,col)
	split=gains.index(max(gains))
	node=Node(features[split])
	fea=features[:split]+features[split+1:]
	attr,dic=subtables(data,split,delete=True)
	for x in range(len(attr)):
		child=build_tree(dic[attr[x]],fea)
		node.children.append((attr[x],child))
	return node
	
def print_tree(node,level):
	if node.answer!="":
		print(" "*level,node.answer)
		return
	print(" "*level,node.attribute)
	for value,n in node.children:
		print(" "*(level+1),value)
		print_tree(n,level+2)
		
def classify(node,x_test,features):
	if node.answer!="":
		print(node.answer)
		return
	pos=features.index(node.attribute)
	for value,n in node.children:
		if x_test[pos]==value:
			classify(n,x_test,features)
			
'''Main program'''
dataset,features=load_csv("id3.csv")
node1=build_tree(dataset,features)
print("The decision tree for the dataset using ID3 algorithm is ")
print_tree(node1,0)
testdata,features=load_csv("id3_test_1.csv")
for xtest in testdata:
	print("The test instance: ",xtest)
	print("The label for test instance: ",end=" ")
	classify(node1,xtest,features)
        """)
        
    def rf():
        """
      Demonstrate the working of the Random forest algorithm. Use an appropriate data set for building and apply this knowledge to classify a new sample.
      Random Forest is a popular machine learning algorithm that belongs to the category of ensemble learning methods. 
      It is widely used for both classification and regression tasks.

    In Random Forest, multiple decision trees are trained on different subsets of the training data, using a technique called "bootstrap aggregating" or "bagging." 
    Each tree is trained independently, and the final prediction is obtained by aggregating the predictions of all the individual trees.
        """
        print(r"""
from sklearn.datasets import load_iris
iris = load_iris()
X = iris.data
y = iris.target

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100,max_leaf_nodes=16,n_jobs=-1)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

from sklearn.tree import export_graphviz
export_graphviz(model.estimators_[99], out_file="iris_tree.dot", feature_names=iris.feature_names, class_names=iris.target_names, filled=True, rounded=True)

import numpy as np
new_sample = np.array([[5.1, 3.5, 1.4, 0.2]])
new_sample_class = model.predict(new_sample)
print(f"Predicted class for the new sample: {iris.target_names[new_sample_class[0]]}")

''' manual 
import pandas as pd
import numpy as np
data = pd.read_csv('Iris.csv',index_col=0)
data.reset_index(drop=True,inplace=True)
X = np.array(data.iloc[:,:-1])
y = np.array(data.iloc[:,-1])
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
from sklearn.ensemble import RandomForestClassifier
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
# Create a new sample for classification
new_sample = np.array([[3, 3, 2, 2]])
y_pred = clf.predict(new_sample)
print(y_pred)

from sklearn.tree import export_graphviz
for i, tree_in_forest in enumerate(clf.estimators_):
    if i<1:         # to print only 1st tree
        export_graphviz(tree_in_forest, out_file=f"tree_{i+1}.dot", feature_names=['SepalLength', 'SepalWidth', 'PetalLength', 'PetalWidth'])
        print(f"dot -Tpng tree_{i+1}.dot -o tree_{i+1}.png")
'''
        """)
        
    def knn():
        """
      k-Nearest Neighbors (k-NN) is a supervised machine learning algorithm used for both classification and regression tasks. 
      It is a non-parametric algorithm that makes predictions based on the similarity between a new data point and its k nearest neighbors in the feature space.
      When a new data point is given, the algorithm calculates the distance between that point and all the data points in the training set. 
      The distance metric used is typically Euclidean distance, although other metrics can also be used.
      For classification, the predicted class label for the new data point is determined by majority voting among its k nearest neighbors
        """
        print(r"""
import pandas as pd
data = pd.read_csv('Iris.csv')
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

from sklearn.neighbors import KNeighborsClassifier
knn_classifier = KNeighborsClassifier(n_neighbors=3)
knn_classifier.fit(X_train, y_train)
y_pred = knn_classifier.predict(X_test)

from sklearn.metrics import accuracy_score,confusion_matrix
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
print(f"Accuracy: \n",confusion_matrix(y_test, y_pred))

'''
from sklearn.datasets import load_iris
iris = load_iris()
X = iris.data
y = iris.target
'''
        """)
        
    def em():
        """
     A DataFrame is a two-dimensional labeled data structure in pandas, which is a popular library for data manipulation and analysis in Python. 
    It organizes data into rows and columns, similar to a table or spreadsheet, and provides various methods and operations for data manipulation.
    GaussianMixture is a class in scikit-learn, a popular machine learning library in Python. It is used to model data using a Gaussian Mixture Model (GMM). 
    GMM is a probabilistic model that assumes the data points are generated from a mixture of Gaussian distributions. 
    It is commonly used for clustering tasks where the goal is to assign data points to different clusters based on their statistical properties.
    EM algorithm, short for Expectation-Maximization algorithm, is an iterative algorithm used to estimate the parameters of statistical models when there are hidden or unobserved variables involved. 
    It is commonly used in unsupervised learning tasks such as clustering, where the goal is to find latent patterns or groupings in the data.
        """
        print(r"""
from sklearn.datasets import load_iris
import pandas as pd
dataset = load_iris()
x = pd.DataFrame(dataset.data, columns=['sepal_length', 'sepal_width', 'petal_length', 'petal_width'])
y = pd.DataFrame(dataset.target, columns=['Targets'])

import numpy as np
colormap = np.array(['red', 'lime', 'black'])    # Create a colormap for visualization

import matplotlib.pyplot as plt
fig = plt.figure(figsize=(14, 7))           # Plot the original data
plt.subplot(1, 3, 1)
plt.scatter(x['petal_length'], x['petal_width'], c=colormap[y['Targets']], s=40)
plt.title('Real')

from sklearn import preprocessing
scaler = preprocessing.StandardScaler()
x_scaled = scaler.fit_transform(x)
x_scaled = pd.DataFrame(x_scaled, columns=x.columns)

from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=3)
gmm.fit(x_scaled)
y_cluster_gmm = gmm.predict(x_scaled)

import sklearn.metrics as sm
print("The accuracy score of EM:", sm.accuracy_score(y['Targets'], y_cluster_gmm))

plt.subplot(1, 3, 3)        # Plot the clusters predicted by GMM
plt.scatter(x['petal_length'], x['petal_width'], c=colormap[y_cluster_gmm], s=40)
plt.title('GMM Clusters')
plt.show()


'''
from sklearn.mixture import GaussianMixture
from sklearn.datasets import load_iris
import sklearn.metrics as sm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

dataset = load_iris()
X = pd.DataFrame(dataset.data)
X.columns = ['Sepal_Length','Sepal_Width','Petal_Length','Petal_Width']
y = pd.DataFrame(dataset.target)
y.columns=['Targets']

plt.figure(figsize=(14,7))
colormap = np.array(['red','lime','black'])

plt.subplot(1,3,1)
plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[y.Targets],s=40)
plt.title("Real")

scaler=preprocessing.StandardScaler()
scaler.fit(X)
xsa = scaler.transform(X)
xs=pd.DataFrame(xsa,columns=X.columns)
gmm=GaussianMixture(n_components=3)
gmm.fit(xs)
y_cluster_gmm=gmm.predict(xs)
print('The accuracy score of EM: ',sm.accuracy_score(y,y_cluster_gmm))
plt.subplot(1,3,3)
plt.scatter(X.Petal_Length,X.Petal_Width,c=colormap[y_cluster_gmm],s=40)
plt.title("GMM Classification")
'''
        """)
        
    def pp():
        """
        Data Cleaning - Identifying and Deleting Duplicate Rows:
            The program removes duplicate rows from the housing DataFrame using the drop_duplicates() function.
            The resulting DataFrame with duplicates removed is stored in the housing_cleaned variable.
        Data Integration - Identifying and Deleting Columns with a Single Value:
            The program identifies columns in the housing_cleaned DataFrame that have only one unique value.
            It appends these columns to the columns_to_drop list.
            The identified columns are then dropped from the DataFrame using the drop() function.
            DataFrame that have only one unique value means finding columns where all the values are the same throughout the entire column. 
            In other words, these columns provide no meaningful variation or information because they have only one distinct value.
        Data Transformation - Preprocessing Pipeline:
            First, the program creates two lists: num_attribs to store the names of numerical columns and cat_attribs to store the names of categorical columns.
            Next, two separate pipelines are created. The num_pipeline is responsible for handling numerical data, while the cat_pipeline handles categorical data.
            In the num_pipeline, missing values in numerical columns are filled using the median strategy. Then, the features in the numerical columns are scaled using a technique called standardization, which makes them easier to compare and interpret.
            In the cat_pipeline, categorical features are encoded. First, ordinal encoding is applied, which assigns numeric labels to the categories while preserving any order or hierarchy that may exist. Then, one-hot encoding is performed,
            creating binary columns for each category to represent their presence or absence in each sample.
            To apply these pipelines to the respective columns, a ColumnTransformer called full_pipeline is created. 
            It takes the num_pipeline for numerical columns and the cat_pipeline for categorical columns.
        """
        print(r"""
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OrdinalEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
housing = pd.read_csv('housing.csv')

# Data Cleaning - Identifying and Deleting Duplicate Rows
housing_cleaned = housing.drop_duplicates()
print("Number of rows after removing duplicates:", len(housing_cleaned))

# Data Integration - Identifying and Deleting Columns with a Single Value
columns_to_drop = []
for column in housing_cleaned.columns:
    if housing_cleaned[column].nunique() == 1:
        columns_to_drop.append(column)
housing_integrated = housing_cleaned.drop(columns=columns_to_drop)
print("Columns after removing single-valued columns:")
print(housing_integrated.columns)

# Data Transformation - Preprocessing Pipeline
num_attribs = list(housing_integrated.select_dtypes(include=['float64', 'int64']))
cat_attribs = list(housing_integrated.select_dtypes(include=['object']))
num_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy="median")),
    ('std_scaler', StandardScaler()),
])
cat_pipeline = Pipeline([
    ('ordinal_encoder', OrdinalEncoder()),
    ('one_hot_encoder', OneHotEncoder()),
])
full_pipeline = ColumnTransformer([
    ("num", num_pipeline, num_attribs),
    ("cat", cat_pipeline, cat_attribs),
])
housing_preprocessed = full_pipeline.fit_transform(housing_integrated)
print("Preprocessed data shape:", housing_preprocessed.shape)
        """)
        
    def ec():
        """
        Ensemble learning is a machine learning technique that combines the predictions of multiple individual models, known as base models or weak 
        learners, to make more accurate and robust predictions.  
        Voting: Each base classifier gets one vote, and the class with the majority of votes is chosen as the final prediction. This can be further classified into majority voting (simple voting)
        Averaging: The predictions of each base classifier are averaged to produce the final prediction.
        Stacking: In this approach, the predictions of base classifiers are used as input features for a meta-classifier. The meta-classifier learns to combine these predictions and make the final decision.
        """
        print(r"""
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
X, y = make_moons(n_samples=100, noise=0.15)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
log_clf = LogisticRegression()
rnd_clf = RandomForestClassifier()
svm_clf = SVC()
voting_clf = VotingClassifier(estimators=[('lr', log_clf), ('rf', rnd_clf), ('svm', svm_clf)], voting='hard')
voting_clf.fit(X_train, y_train)
y_pred_voting = voting_clf.predict(X_test)
print("Voting Classifier Accuracy:", accuracy_score(y_test, y_pred_voting))


'''
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris['data'], iris['target'], test_size=0.3, random_state=42)

log_clf = LogisticRegression()
rnd_clf = RandomForestClassifier()
svm_clf = SVC()

voting_clf = VotingClassifier(estimators=[('lr', log_clf), ('rf', rnd_clf), ('svm', svm_clf)], voting='hard')
voting_clf.fit(X_train, y_train)
y_pred_voting = voting_clf.predict(X_test)
print("Voting Classifier Accuracy:", accuracy_score(y_test, y_pred_voting))


tree_clf = DecisionTreeClassifier()
knn_clf = KNeighborsClassifier()
svm_clf = SVC()
'''
        """)
        
    def bn():
        """
        A Bayesian network is a graphical model that represents the relationships between variables using nodes and arrows. 
        Each node represents a variable, and the arrows show how the variables influence each other. 
        It helps us understand how the variables are connected and allows us to make predictions or decisions by using probabilities and updating our beliefs based on new evidence. 
        Overall, it's a way to visually represent and analyze complex systems using probabilities and logical connections.
        
        """
        print(r"""
import numpy as np
import pandas as pd
from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination

heart_disease = pd.read_csv('heart.csv')
heart_disease = heart_disease.replace('?', np.nan)

# Define the Bayesian network structure
model = BayesianModel([
    ('age', 'trestbps'), ('age', 'fbs'), ('sex', 'trestbps'), ('exang', 'trestbps'),
    ('trestbps', 'heartdisease'), ('fbs', 'heartdisease'), ('heartdisease', 'restecg'),
    ('heartdisease', 'thalach'), ('heartdisease', 'chol')
]) 
model.fit(heart_disease, estimator=MaximumLikelihoodEstimator)

# Perform inference with Bayesian Network
heart_disease_infer = VariableElimination(model)  

# Calculate probability of Heart Disease given Age=63
q = heart_disease_infer.query(variables=['heartdisease'], evidence={'age': 63})
print(q)

q = heart_disease_infer.query(variables=['heartdisease'], evidence={'chol': 233})  # cholesterol
print(q)

q = heart_disease_infer.query(variables=['heartdisease'], evidence={'age': 63, 'sex' :1,'trestbps':130})
print(q)
        """)

class mlfull():
    """
pg1() : FIND-S : Finding a Maximally Specific (0) Hypothesis  
    Implement and demonstrate the FIND-S algorithm for finding the most specific hypothesis based on a given set of training data samples. 
    Read the training data from a .CSV file and show the output for test cases. 
    Develop an interactive program by Compareing the result by implementing LIST THEN ELIMINATE algorithm. 
    
pg2() : CE : Candidate-Elimination
    For a given set of training data examples stored in a .CSV file, implement and demonstrate the Candidate-Elimination algorithm. 
    Output a description of the set of all hypotheses consistent with the training examples.
    
pg3() : Demonstrate Pre processing (Data Cleaning, Integration and Transformation) activity on suitable data:
    For example:
        Identify and Delete Rows that Contain Duplicate Data by considering an appropriate dataset.
        Identify and Delete Columns That Contain a Single Value by considering an appropriate dataset.
        
pg4() :  Demonstrate the working of the decision tree based ID3 algorithm. 
    Use an appropriate data set for building the decision tree and apply this knowledge toclassify a new sample.
        
pg5() :  Demonstrate the working of the Random forest algorithm. Use an appropriate data set for building and apply this knowledge toclassify a new sample.

pg6() : Implement the naïve Bayesian classifier for a sample training data set stored as a .CSV file. 
    Compute the accuracy of the classifier, considering few test data sets.
    
pg7() : Assuming a set of documents that need to be classified, use the naive Bayesian Classifier model to perform this task. 
    Calculate the accuracy, precision, and recall for your data set.
    
pg8() : Construct aBayesian network considering medical data. 
    Use this model to demonstrate the diagnosis of heart patients using standard Heart Disease Data Set.
    
pg9() : Demonstrate the working of EM algorithm to cluster a set of data stored in a .CSV file.

pg10() : Demonstrate the working of SVM classifier for a suitable data set

pg11() :  Write a program to implement k-Nearest Neighbour algorithm to classify the iris data set. 
    Print both correct and wrong predictions. Java/Python ML library classes can be used for this problem.
    
pg12() : Write a program Ensembling of Classifiers for moon or iris dataset 
    """
    def pg1():
        """
    FIND-S: FINDING A MAXIMALLY SPECIFIC HYPOTHESIS
    1. Initialize h to the most specific hypothesis in H
    2. For each positive training instance x
            For each attribute constraint a, in h
                If the constraint a, is satisfied by x
                    Then do nothing
                Else replace a, in h by the next more general constraint that is satisfied by x
    3. Output hypothesis h
    
    The LIST-THEN-ELIMINATE
    1. VersionSpace c a list containing every hypothesis in H
    2. For each training example, (x, c(x))
            remove from VersionSpace any hypothesis h for which h(x) != c(x)
    3. Output the list of hypotheses in VersionSpace
        """
        print(r"""
import csv

def read_data(filename):
    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile, delimiter=',')
        traindata = []
        for row in datareader:
            traindata.append(row)
    return traindata

attributes = ['Sky','Temp','Humidity','Wind','Water','Forecast']
num_attributes = len(attributes)

dataset=read_data('enjoysport.csv')

hypothesis=['0'] * num_attributes

for j in range(0,num_attributes):
    hypothesis[j] = dataset[0][j];
    
#  Find S: Finding a Maximally Specific Hypothesis
for i in range(0,len(dataset)):
    if dataset[i][num_attributes]=='Yes':
        for j in range(0,num_attributes):
            if dataset[i][j]!=hypothesis[j]:
                hypothesis[j]='?'
                
print("The Maximally Specific Hypothesis for a given Training Examples :")
print(hypothesis)
        """)
        
    def pg2():
        """
    Candidate-Elimination algorithm
    
    Initialize G to the set of maximally general hypotheses in H
    Initialize S to the set of maximally specific hypotheses in H
    For each training example d, do
        If d is a positive example
            Remove from G any hypothesis inconsistent with d
            For each hypothesis s in S that is not consistent with d
                Remove s from S
                Add to S all minimal generalizations h of s such that
                    h is consistent with d, and some member of G is more general than h
                Remove from S any hypothesis that is more general than another hypothesis in S
        If d is a negative example
            Remove from S any hypothesis inconsistent with d
            For each hypothesis g in G that is not consistent with d
                Remove g from G
                Add to G all minimal specializations h of g such that
                    h is consistent with d, and some member of S is more specific than h
                Remove from G any hypothesis that is less general than another hypothesis in G
        """
        print(r"""
import csv
a = []
print("\n The Given Training Data Set")
with open('enjoysport.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    for row in reader:
        a.append (row)
num_attributes = len(a[0])-1

S = ['0'] * num_attributes
G = ['?'] * num_attributes

for j in range(0,num_attributes):
    S[j]=a[0][j];
    
print("\n Candidate Elimination algorithm Hypotheses Version Space Computation\n")
temp=[]
for i in range(0,len(a)):
    if a[i][num_attributes]=='Yes':
        for j in range(0,num_attributes):
            if a[i][j]!=S[j]:
                S[j]='?'
        for j in range(0,num_attributes):
            for k in range(1,len(temp)):
                if temp[k][j]!='?' and temp[k][j]!=S[j]:
                    del temp[k]
        print("----------------------------------------------------------------------------- ")
        print(" For Training Example No :{0} the hypothesis is S{0} ".format(i+1),S)
        if (len(temp)==0):
            print(" For Training Example No :{0} the hypothesis is G{0} ".format(i+1),G)
        else:
            print(" For  Positive Training Example No :{0} the hypothesis is G{0}".format(i+1),temp)
    if a[i][num_attributes]=='No':
        for j in range(0,num_attributes):
            if S[j] != a[i][j] and S[j]!= '?':
                G[j]=S[j]
                temp.append(G)
                G = ['?'] * num_attributes
        print("----------------------------------------------------------------------------- ")
        print(" For Training Example No :{0} the hypothesis is S{0} ".format(i+1),S)
        print(" For Training Example No :{0} the hypothesis is G{0}".format(i+1),temp)
        """)
        
    def pg3():
        """
    Demonstrate Pre processing (Data Cleaning, Integration and Transformation) activity on suitable data:
    For example: 
    Identify and Delete Rows that Contain Duplicate Data by considering an appropriate dataset.
    Identify and Delete Columns That Contain a Single Value by considering an appropriate dataset.
    
    In this program, we first load the customer orders dataset using the pandas library. We then print the original dataset to see what it looks like.
    Next, we use the drop_duplicates() method to remove any duplicate rows in the dataset. This ensures that we are only working with unique data. 
    We then print the new dataset without duplicates.
    Finally, we loop through each column in the dataset and check if it only contains a single value using the unique() method. 
    If it does, we use the drop() method to remove that column from the dataset. We then print the final dataset without any columns that only contain a single value.
        """
        print(r"""
import pandas as pd

# Load the dataset
df = pd.read_csv("customer_orders.csv")

# Print the original dataset
print("Original Dataset:")
print(df)

# Remove duplicate rows
df = df.drop_duplicates()

# Print the dataset without duplicates
print("\nDataset without duplicates:")
print(df)

# Remove columns with a single value
for col in df.columns:
    if len(df[col].unique()) == 1:
        df.drop(col, axis=1, inplace=True)

# Print the dataset without columns with a single value
print("\nDataset without columns with a single value:")
print(df)

'''
name,age,gender,country,city
John,25,Male,USA,New York
Emily,31,Female,Canada,Toronto
Alex,19,Male,UK,London
Samantha,42,Female,USA,Los Angeles
Bob,28,Male,Canada,Montreal
'''
        """)
        
    def pg4():
        """
    Write a program to demonstrate the working of the decision tree based on ID3 algorithm. 
    Use an appropriate data set for building the decision tree and apply this knowledge to classify a new sample
        """
        print(r"""
import pandas as pd
import numpy as np
df_tennis = pd.read_csv('tennis.csv')

from collections import Counter
def entropy_list(a_list):
    cnt = Counter(x for x in a_list)
    num_instance = len(a_list)*1.0
    probs = [x/num_instance for x in cnt.values()]
    return entropy(probs)
    
import math
def entropy(probs):
    return sum([-prob*math.log(prob,2) for prob in probs])
    
def info_gain(df,split,target,trace=0):
    df_split = df.groupby(split)
    nobs = len(df.index)*1.0
    df_agg_ent = df_split.agg({ target:[entropy_list, lambda x: len(x)/nobs] })
    #print(df_agg_ent)
    df_agg_ent.columns = ['Entropy','PropObserved']
    new_entropy = sum( df_agg_ent['Entropy'] * df_agg_ent["PropObserved"])
    old_entropy = entropy_list(df[target])
    return old_entropy - new_entropy
    
def id3(df,target,attribute_name,default_class = None):
    cnt = Counter(x for x in df[target])
    if len(cnt)==1:
        return next(iter(cnt))
    elif df.empty or (not attribute_name):
        return default_class
    else:
        default_class = max(cnt.keys())
        gains = [info_gain(df,attr,target) for attr in attribute_name]
        index_max = gains.index(max(gains))
        best_attr = attribute_name[index_max]
        tree = { best_attr:{ } }
        remaining_attr = [x for x in attribute_name if x!=best_attr]
        for attr_val, data_subset in df.groupby(best_attr):
            subtree = id3(data_subset,target,remaining_attr,default_class)
            tree[best_attr][attr_val] = subtree
        return tree
        
def classify(instance,tree,default = None):
    attribute = next(iter(tree))
    if instance[attribute] in tree[attribute].keys():
        result = tree[attribute][instance[attribute]]
        if isinstance(result,dict):
            return classify(instance,result)
        else:
            return result
    else:
        return default
        
attribute_names = list(df_tennis.columns)
attribute_names.remove('PlayTennis') #Remove the class attribute
tree = id3(df_tennis,'PlayTennis',attribute_names)
print("The Resultant Decision Tree is :\n")
print(tree)

training_data = df_tennis.iloc[1:-4]    # all but last thousand instances
test_data = df_tennis.iloc[-4:]          # just the last thousand
train_tree = id3(training_data, 'PlayTennis', attribute_names)
print("The Resultant Decision train_tree is :\n")
print(train_tree)

test_data['predicted2'] = test_data.apply(classify,axis=1,args=(train_tree,'Yes') )

#print ('\nTraining the model for a few samples, and again predicting \'Playtennis\' for remaining attribute')

print('The Accuracy for new trained data is : ' + str( sum(test_data['PlayTennis']==test_data['predicted2'] ) / (1.0*len(test_data.index)) ))
        """)
        
    def pg5():
        """
        Demonstrate the working of the Random forest algorithm. 
        Use an appropriate data set for building and apply this knowledge toclassify a new sample
        
        In this program, we first load the iris dataset from sklearn and convert it into a pandas dataframe. 
        We then split the dataset into a training set and a test set using the train_test_split function from sklearn.
        We create a Random Forest classifier with 100 trees and fit the classifier to the training data using the fit method. 
        We then use the classifier to make predictions on the test data and calculate the accuracy of the classifier using the accuracy_score function from sklearn. 
        Finally, we demonstrate how to classify a new sample using the predict method of the Random Forest classifier.
        """
        print(r"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the iris dataset from sklearn
from sklearn.datasets import load_iris
iris = load_iris()

# Convert dataset into a dataframe
iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
iris_df['target'] = iris.target

# Split dataset into train and test sets
X_train, X_test, y_train, y_test = train_test_split(iris_df.drop(['target'], axis=1), iris_df['target'], test_size=0.2, random_state=42)

# Create a Random Forest classifier with 100 trees
rf = RandomForestClassifier(n_estimators=100)

# Fit the classifier to the training data
rf.fit(X_train, y_train)

# Use the classifier to make predictions on the test data
y_pred = rf.predict(X_test)

# Calculate the accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred)

# Print the accuracy of the classifier
print("Accuracy:", accuracy)

# Demonstrate how to classify a new sample
new_sample = [[5.1, 3.5, 1.4, 0.2]]  # new sample with feature values for sepal length, sepal width, petal length and petal width
new_prediction = rf.predict(new_sample)
print("New sample prediction:", new_prediction)
        """)
        
    def pg6():
        """
        Implement the naïve Bayesian classifier for a sample training data set stored as a .CSV file. 
        Compute the accuracy of the classifier, considering few test data sets.
        """
        print(r"""
import numpy as np
import math
import csv

def read_data(filename):
    with open(filename, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        metadata = next(datareader)
        traindata=[]
        for row in datareader:
            traindata.append(row)
    return (metadata, traindata)
    
def splitDataset(dataset, splitRatio): 
    trainSize = int(len(dataset) * splitRatio)
    trainSet = []
    testset = list(dataset)
    i=0
    while len(trainSet) < trainSize:
        trainSet.append(testset.pop(i))
    return [trainSet, testset]
    
def classify(data,test):
    total_size = data.shape[0]
    print("training data size=",total_size)
    print("test data size=",test.shape[0])
    target=np.unique(data[:,-1])
    count = np.zeros((target.shape[0]), dtype=np.int32)
    prob = np.zeros((target.shape[0]), dtype=np.float32)
    
    print("target count probability")
    
    for y in range(target.shape[0]):
        for x in range(data.shape[0]):
            if data[x,data.shape[1]-1] == target[y]:
                count[y] += 1
        prob[y]=count[y]/total_size # comptes the probability of target
        print(target[y],"\t",count[y],"\t",prob[y])
        
    prob0 = np.zeros((test.shape[1]-1), dtype=np.float32)
    prob1 = np.zeros((test.shape[1]-1), dtype=np.float32)
    accuracy=0
    print("Instance prediction target")
    for t in range(test.shape[0]):
        for k in range(test.shape[1]-1): 
            count1=count0=0
            for j in range(data.shape[0]):
                if test[t,k]== data[j,k] and data[j,data.shape[1]-1]== target[0]:
                    count0+=1
                elif test[t,k]== data[j,k] and data[j,data.shape[1]-1]== target[1]:
                    count1+=1
            prob0[k]= count0/count[0] 
            prob1[k]= count1/count[1]
    
        probno=prob[0]
        probyes=prob[1]
        for i in range(test.shape[1]-1):
            probno=probno*prob0[i]
            probyes=probyes*prob1[i]
    
        if probno>probyes: 
            predict='no'
        else:
            predict='yes'
        print(t+1,"\t",predict,"\t ",test[t,test.shape[1]-1])
    
        if predict== test[t,test.shape[1]-1]:
            accuracy+=1
        final_accuracy=(accuracy/test.shape[0])*100
        print("accuracy",final_accuracy,"%")
    return
    
metadata, traindata = read_data("tennis.csv")
splitRatio = 0.6
trainingset, testset = splitDataset(traindata, splitRatio)
training=np.array(trainingset)
testing=np.array(testset)

classify(training,testing)
        """)
        
    def pg7():
        """
        Assuming a set of documents that need to be classified, use the naive Bayesian Classifier model to perform this task. 
        Calculate the accuracy, precision, and recall for your data set.
        """
        print(r"""
import pandas as pd
import warnings 
warnings.filterwarnings('ignore')
msg=pd.read_csv('naivetext1.csv',names=['message','label']) #Tabular form dta
print('Total instances in the dataset:',msg.shape[0])

msg['labelnum']=msg.label.map({'pos':1,'neg':0})
X=msg.message
Y=msg.label

'''
print('\nThe message and its label of first 5 instances are listed below')
X5, Y5 = X[0:5], msg.label[0:5]
for x, y in zip(X5,Y5):
  print(x,',',y)
'''

from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest=train_test_split(X,Y)
print('\nDataset is split into Training and Testing samples')
print('Total training instances :', xtrain.shape[0])
print('Total testing instances :', xtest.shape[0])

from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
xtrain_dtm = count_vect.fit_transform(xtrain) #Sparse matrix
xtest_dtm = count_vect.transform(xtest)
print('\nTotal features extracted using CountVectorizer:',xtrain_dtm.shape[1])

print('\nFeatures for first 5 training instances are listed below')
df=pd.DataFrame(xtrain_dtm.toarray(),columns=count_vect.get_feature_names())
print(df[0:5])

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(xtrain_dtm,ytrain)
predicted = clf.predict(xtest_dtm)

'''
print('\nClassstification results of testing samples are given below')
for doc, p in zip(xtest, predicted):
    pred = 'pos' if p==1 else 'neg'
    print('%s -> %s ' % (doc, pred))
'''

from sklearn.metrics import accuracy_score,recall_score,precision_score,confusion_matrix
print('\nAccuracy metrics')
print('Accuracy of the classifer is',accuracy_score(ytest,predicted))
print('Recall:{0}\n Precison:{1}'.format(recall_score(ytest,predicted, pos_label='positive',average='micro'),precision_score(ytest,predicted,pos_label='positive',average='micro')))
print('Confusion matrix')
print(confusion_matrix(ytest,predicted)) 
        """)
        
    def pg8():
        """
        Construct aBayesian network considering medical data. Use this model to demonstrate the diagnosis of heart patients using standard Heart Disease Data Set.
        """
        print(r"""
'''
pip install bayespy
pip install pgmpy
'''
import pandas as pd
import numpy as np
# import bayespy as bp
import warnings 
warnings.filterwarnings('ignore')

heart_disease=pd.read_csv("heart.csv")
# print(heart_disease)
print('Columns in the dataset')
for col in heart_disease.columns: 
    print(col) 
    
from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator
model=BayesianModel([('age','trestbps'), ('age', 'fbs'), ('sex', 'trestbps'), ('exang',
'trestbps'),('trestbps','heartdisease'),('fbs','heartdisease'),('heartdisease','restecg'),
('heartdisease','thalach'), ('heartdisease','chol')])
model.fit(heart_disease, estimator=MaximumLikelihoodEstimator)

from pgmpy.inference import VariableElimination
HeartDisease_infer = VariableElimination(model)
q = HeartDisease_infer.query(variables=['heartdisease'], evidence={'age': 63, 'sex' :1,'trestbps':130})
print(q)
        """)
        
    def pg9():
        """
        Demonstrate the working of EM algorithm to cluster a set of data stored in a .CSV file.
        """
        print(r"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

data=pd.read_csv("clusterdata.csv")
df1=pd.DataFrame(data)
print(df1)
f1 = df1['Distance_Feature'].values
f2 = df1['Speeding_Feature'].values

fig = plt.figure()
fig.subplots_adjust(hspace=0.4, wspace=0.4)
for i in range(1, 7):
    plt.subplot(2, 3,i)
    plt.text(0.5, 0.5, str((2, 3, i)),
             fontsize=18, ha='center')
             
X=np.matrix(list(zip(f1,f2)))
# plt.subplot(511)
plt.xlim([0, 100])
plt.ylim([0, 50])
plt.title('Dataset')
plt.ylabel('speeding_feature')
plt.xlabel('distance_feature')
plt.scatter(f1,f2)

colors = ['b', 'g', 'r']
markers = ['o', 'v', 's']

# ax=plt.subplot(513)
plt.xlim([0, 100])
plt.ylim([0, 50])
plt.title('K- Means')
plt.ylabel('speeding_feature')
plt.xlabel('distance_feature')

kmeans_model = KMeans(n_clusters=3).fit(X)
for i, l in enumerate(kmeans_model.labels_):
    plt.plot(f1[i], f2[i], color=colors[l],marker=markers[l])

plt.plot(3)
plt.subplot(515)
plt.xlim([0, 100])
plt.ylim([0, 50])
plt.title('Gaussian Mixture')
plt.ylabel('speeding_feature')
plt.xlabel('distance_feature')
gmm=GaussianMixture(n_components=3).fit(X)
labels= gmm.predict(X)
for i, l in enumerate(labels):
    plt.plot(f1[i], f2[i], color=colors[l], marker=markers[l])
        """)
        
    def pg10():
        """
        Demonstrate the working of SVM classifier for a suitable data set.
        """
        print(r"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score

data = pd.read_csv('dataset.csv')
X = data.iloc[:, :-1].values
y = data.iloc[:, -1].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

classifier = SVC(kernel='rbf', random_state=0)
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)
print("Confusion matrix: ", confusion_matrix(y_test, y_pred))
print("Accuracy: ", accuracy_score(y_test, y_pred))

'''
Age,EstimatedSalary,Purchased
19,19000,0
35,20000,0
26,43000,0
27,57000,0
19,76000,0
27,58000,0
27,84000,0
32,150000,1
25,33000,0
35,65000,0
'''


# For Iris dataset 
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# Load dataset
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Train the SVM classifier
clf = SVC(kernel='linear')
clf.fit(X_train, y_train)

# Make predictions on the testing set
y_pred = clf.predict(X_test)

# Calculate accuracy of the classifier
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
        """)
        
    def pg11():
        print(r"""
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report,confusion_matrix
from sklearn import datasets

iris=datasets.load_iris()
iris_data=iris.data
iris_labels=iris.target
x_train,x_test,y_train,y_test=train_test_split(iris_data,iris_labels,test_size=0.30)

classifier=KNeighborsClassifier(n_neighbors=5).fit(x_train,y_train)
y_pred=classifier.predict(x_test)

print('Confusion matrix is as follows')
print(confusion_matrix(y_test,y_pred))
print('Accuracy Matrics')
print(classification_report(y_test,y_pred))
        """)
    
    def pg12():
        print(r"""
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
X, y = make_moons(n_samples=100, noise=0.15)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
log_clf = LogisticRegression()
rnd_clf = RandomForestClassifier()
svm_clf = SVC()
voting_clf = VotingClassifier(estimators=[('lr', log_clf), ('rf', rnd_clf), ('svm', svm_clf)], voting='hard')
voting_clf.fit(X_train, y_train)
y_pred_voting = voting_clf.predict(X_test)
print("Voting Classifier Accuracy:", accuracy_score(y_test, y_pred_voting))
        """)
        
class mad:
    """
visitingcard() :
    Create an application to design aVisiting Card. The Visiting card should have a company logo at the top right corner. 
    The company name should be displayed in Capital letters, aligned to the center.
    Information like the name of the employee, job title, phone number, address, email, fax and the website address isto be displayed. 
    Insert a horizontal line between the job title and the phone number.

calculator():
    Develop an Android application using controls like Button, TextView, EditText for designing a calculator having basic functionality like Addition, 
    Subtraction, Multiplication,andDivision

signup_signin():
    Create a SIGN Up activity with Username and Password. Validation of password should happen based on the following rules:
     Password should contain uppercase and lowercaseletters.
     Password should contain letters andnumbers.
     Password should contain specialcharacters.
     Minimum length of the password (the default value is 8).
    On successful SIGN UP proceed to the next Login activity. Here the user should SIGN IN using  the Username and Password created during signup activity. If the Username and Password are
    matched then navigate to the next activity whichdisplays a message saying “Successful Login” or else display a toast message saying “Login Failed”.The user is given only two attempts and after
    thatdisplay a toast message saying “Failed Login Attempts” and disable the SIGN IN button. 
    Use Bundle to transfer information from one activity to another.

wallpaper():
    Develop an application to set an image as wallpaper. On click of a button, the wallpaper image should start to change randomly every 30 seconds.

counter():
    Write a program to create an activity with two buttons START and STOP. On pressing of the START button, the activity must start the counter by displaying the numbers from One and the
    counter must keep on counting until the STOP button is pressed. Display the counter value in a TextViewcontrol.

parse_xml_json_files():
    Create two files of XML and JSON type with values for City_Name, Latitude, Longitude, Temperature, and Humidity. 
    Develop an application to create an activity with two buttons to parse the XML and JSON files which when clicked 
    should display the data in their respective layouts side by side.

texttospeech():
    Develop a simple application with one Edit Text so that the user can write some text in it. Create a
    button called “Convert Text to Speech” that converts the user input text into voice.

phone():
    Create an activity like a phone dialer with CALL and SAVE buttons. On pressing the CALL
    button, it must call the phone number and on pressing the SAVE button it must save the number to the phonecontacts.
    """
    def visitingcard():
        """
        Create an application to design a Visiting Card
        """
        print(r"""
// MainActivity.java
package com.example.project1;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }
}


//strings.xml
<resources>
    <string name="app_name">project1</string>
    <string name="company">UNIVERSAL POLYMER</string>
    <string name="name">Shreesha B</string>
    <string name="job">Manager</string>
    <string name="phone">9620522347</string>
    <string name="Address">Badanaje,Vital,DK 574243</string>
    <string name="emailweb">shreeshapilinja@gmail.com\n\nhttps://aiml.eu5.org</string>
</resources>


//activity_main.java
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:background="#E7EDDF"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView6"
        android:layout_width="357dp"
        android:layout_height="104dp"
        android:gravity="center"
        android:text="@string/emailweb"
        android:textColor="#F1940C"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.92" />

    <TextView
        android:id="@+id/textView5"
        android:layout_width="312dp"
        android:layout_height="68dp"
        android:gravity="center"
        android:text="@string/Address"
        android:textColor="#0BDD14"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.494"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.72" />

    <TextView
        android:id="@+id/textView4"
        android:layout_width="197dp"
        android:layout_height="36dp"
        android:gravity="center"
        android:text="@string/phone"
        android:textColor="#380342"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.528"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.594" />

    <TextView
        android:id="@+id/textView3"
        android:layout_width="195dp"
        android:layout_height="38dp"
        android:gravity="center"
        android:text="@string/name"
        android:textColor="#0B7BD5"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.523"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.392" />

    <TextView
        android:id="@+id/textView"
        android:layout_width="212dp"
        android:layout_height="88dp"
        android:gravity="center"
        android:text="@string/company"
        android:textColor="#EC0B0B"
        android:textSize="30sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.08"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.071" />

    <ImageView
        android:id="@+id/imageView"
        android:layout_width="153dp"
        android:layout_height="156dp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.937"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.027"
        app:srcCompat="@drawable/icon" />

    <TextView
        android:id="@+id/textView2"
        android:layout_width="195dp"
        android:layout_height="42dp"
        android:gravity="center"
        android:text="@string/job"
        android:textColor="#EF1616"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.523"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.499" />

    <View
        android:id="@+id/view"
        android:layout_width="wrap_content"
        android:layout_height="12dp"
        android:background="#CF09F1"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.0"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.305" />
</androidx.constraintlayout.widget.ConstraintLayout>
        """)
    
    def calculator():
        """
    Develop an Android application using controls like Button, TextView, EditText for designing a calculator having basic functionality like Addition, Subtraction, Multiplication,and Division.    
        """
        print(r"""
// MainActivity.java
package com.example.project2;

import androidx.appcompat.app.AppCompatActivity;
import android.annotation.SuppressLint;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    Button b0,b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,b11,b12,b13,b14,b15,b16;            // button objects
    EditText result;
    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        b0 = (Button) findViewById(R.id.zero);
        b0.setOnClickListener((View.OnClickListener)this);

        b1 = (Button) findViewById(R.id.one);
        b1.setOnClickListener((View.OnClickListener)this);

        b2 = (Button) findViewById(R.id.two);
        b2.setOnClickListener((View.OnClickListener)this);

        b3 = (Button) findViewById(R.id.three);
        b3.setOnClickListener((View.OnClickListener)this);

        b4 = (Button) findViewById(R.id.four);
        b4.setOnClickListener((View.OnClickListener)this);

        b5 = (Button) findViewById(R.id.five);
        b5.setOnClickListener((View.OnClickListener)this);

        b6 = (Button) findViewById(R.id.six);
        b6.setOnClickListener((View.OnClickListener)this);

        b7 = (Button) findViewById(R.id.seven);
        b7.setOnClickListener((View.OnClickListener)this);

        b8 = (Button) findViewById(R.id.eight);
        b8.setOnClickListener((View.OnClickListener)this);

        b9 = (Button) findViewById(R.id.nine);
        b9.setOnClickListener((View.OnClickListener)this);

        b10 = (Button) findViewById(R.id.add);
        b10.setOnClickListener((View.OnClickListener)this);

        b11 = (Button) findViewById(R.id.sub);
        b11.setOnClickListener((View.OnClickListener)this);

        b12 = (Button) findViewById(R.id.mul);
        b12.setOnClickListener((View.OnClickListener)this);

        b13= (Button) findViewById(R.id.div);
        b13.setOnClickListener((View.OnClickListener)this);

        b14 = (Button) findViewById(R.id.dot);
        b14.setOnClickListener((View.OnClickListener)this);

        b15 = (Button) findViewById(R.id.clear);
        b15.setOnClickListener((View.OnClickListener)this);

        b16 = (Button) findViewById(R.id.equal);
        b16.setOnClickListener((View.OnClickListener)this);

        result = findViewById(R.id.res);
        result.setText("");
    }

    @Override
    public void onClick(View view) {
        if(view.equals(b0))
            result.append("0");

        if(view.equals(b1))
            result.append("1");

        if(view.equals(b2))
            result.append("2");

        if(view.equals(b3))
            result.append("3");

        if(view.equals(b4))
            result.append("4");

        if(view.equals(b5))
            result.append("5");

        if(view.equals(b6))
            result.append("6");

        if(view.equals(b7))
            result.append("7");

        if(view.equals(b8))
            result.append("8");

        if(view.equals(b9))
            result.append("9");

        if(view.equals(b10))
            result.append("+");

        if(view.equals(b11))
            result.append("-");

        if(view.equals(b12))
            result.append("*");

        if(view.equals(b13))
            result.append("/");

        if(view.equals(b14))
            result.append(".");

        if(view.equals(b15))
            result.setText("");

        if(view.equals(b16)){
            String data = result.getText().toString();
            if(data.contains("+")){
                String[] op = data.split("\\+");
                if(op.length==2){
                    double op1 = Double.parseDouble(op[0]);
                    double op2 = Double.parseDouble(op[1]);
                    double ans = op1+op2;
                    result.setText(""+ans);
                }
            }
            if(data.contains("-")){
                String[] op = data.split("-");
                if(op.length==2){
                    double op1 = Double.parseDouble(op[0]);
                    double op2 = Double.parseDouble(op[1]);
                    double ans = op1-op2;
                    result.setText(""+ans);
                }
            }
            if(data.contains("*")){
                String[] op = data.split("\\*");
                if(op.length==2){
                    double op1 = Double.parseDouble(op[0]);
                    double op2 = Double.parseDouble(op[1]);
                    double ans = op1*op2;
                    result.setText(""+ans);
                }
            }
            if(data.contains("/")){
                String[] op = data.split("/");
                if(op.length==2){
                    double op1 = Double.parseDouble(op[0]);
                    double op2 = Double.parseDouble(op[1]);
                    double ans = op1/op2;
                    result.setText(""+ans);
                }
            }
        }
    }
}

//strings.xml
<resources>
    <string name="app_name">project2</string>
    <string name="head">CALCULATOR</string>
    <string name="zero">0</string>
    <string name="one">1</string>
    <string name="two">2</string>
    <string name="three">3</string>
    <string name="four">4</string>
    <string name="five">5</string>
    <string name="six">6</string>
    <string name="seven">7</string>
    <string name="eight">8</string>
    <string name="nine">9</string>
    <string name="add">+</string>
    <string name="sub">-</string>
    <string name="mul">x</string>
    <string name="div">/</string>
    <string name="dot">.</string>
    <string name="equals">=</string>
    <string name="clear">CLEAR</string>
</resources>


// activity_main.xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <Button
        android:id="@+id/seven"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginStart="20dp"
        android:layout_marginLeft="20dp"
        android:layout_marginTop="60dp"
        android:gravity="center"
        android:text="@string/seven"
        android:textSize="20sp"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/res" />

    <Button
        android:id="@+id/zero"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginStart="16dp"
        android:layout_marginLeft="16dp"
        android:layout_marginTop="16dp"
        android:gravity="center"
        android:text="@string/zero"
        android:textSize="20sp"
        app:layout_constraintStart_toEndOf="@+id/dot"
        app:layout_constraintTop_toBottomOf="@+id/two" />

    <Button
        android:id="@+id/six"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginStart="24dp"
        android:layout_marginLeft="24dp"
        android:layout_marginTop="16dp"
        android:gravity="center"
        android:text="@string/six"
        android:textSize="20sp"
        app:layout_constraintStart_toEndOf="@+id/five"
        app:layout_constraintTop_toBottomOf="@+id/nine" />

    <Button
        android:id="@+id/four"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginStart="20dp"
        android:layout_marginLeft="20dp"
        android:layout_marginTop="16dp"
        android:gravity="center"
        android:text="@string/four"
        android:textSize="20sp"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/seven" />

    <Button
        android:id="@+id/div"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginTop="60dp"
        android:gravity="center"
        android:text="@string/div"
        android:textSize="20sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.313"
        app:layout_constraintStart_toEndOf="@+id/nine"
        app:layout_constraintTop_toBottomOf="@+id/res" />

    <Button
        android:id="@+id/eight"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginStart="16dp"
        android:layout_marginLeft="16dp"
        android:layout_marginTop="60dp"
        android:gravity="center"
        android:text="@string/eight"
        android:textSize="20sp"
        app:layout_constraintStart_toEndOf="@+id/seven"
        app:layout_constraintTop_toBottomOf="@+id/res" />

    <Button
        android:id="@+id/two"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginStart="16dp"
        android:layout_marginLeft="16dp"
        android:layout_marginTop="12dp"
        android:gravity="center"
        android:text="@string/two"
        android:textSize="20sp"
        app:layout_constraintStart_toEndOf="@+id/one"
        app:layout_constraintTop_toBottomOf="@+id/five" />

    <Button
        android:id="@+id/five"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginStart="16dp"
        android:layout_marginLeft="16dp"
        android:layout_marginTop="16dp"
        android:gravity="center"
        android:text="@string/five"
        android:textSize="20sp"
        app:layout_constraintStart_toEndOf="@+id/four"
        app:layout_constraintTop_toBottomOf="@+id/eight" />

    <Button
        android:id="@+id/three"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginStart="24dp"
        android:layout_marginLeft="24dp"
        android:layout_marginTop="12dp"
        android:gravity="center"
        android:text="@string/three"
        android:textSize="20sp"
        app:layout_constraintStart_toEndOf="@+id/two"
        app:layout_constraintTop_toBottomOf="@+id/six" />

    <Button
        android:id="@+id/equal"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginStart="24dp"
        android:layout_marginLeft="24dp"
        android:layout_marginTop="16dp"
        android:gravity="center"
        android:text="@string/equals"
        android:textSize="20sp"
        app:layout_constraintStart_toEndOf="@+id/zero"
        app:layout_constraintTop_toBottomOf="@+id/three" />

    <Button
        android:id="@+id/one"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginStart="20dp"
        android:layout_marginLeft="20dp"
        android:layout_marginTop="12dp"
        android:gravity="center"
        android:text="@string/one"
        android:textSize="20sp"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/four" />

    <Button
        android:id="@+id/mul"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginTop="16dp"
        android:gravity="center"
        android:text="@string/mul"
        android:textSize="20sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.313"
        app:layout_constraintStart_toEndOf="@+id/six"
        app:layout_constraintTop_toBottomOf="@+id/div" />

    <Button
        android:id="@+id/clear"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:gravity="center"
        android:text="@string/clear"
        android:textSize="20sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.464"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/equal"
        app:layout_constraintVertical_bias="0.234" />

    <Button
        android:id="@+id/dot"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginStart="20dp"
        android:layout_marginLeft="20dp"
        android:layout_marginTop="16dp"
        android:gravity="center"
        android:text="@string/dot"
        android:textSize="20sp"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/one" />

    <Button
        android:id="@+id/add"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginTop="16dp"
        android:gravity="center"
        android:text="@string/add"
        android:textSize="20sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.313"
        app:layout_constraintStart_toEndOf="@+id/equal"
        app:layout_constraintTop_toBottomOf="@+id/sub" />

    <Button
        android:id="@+id/sub"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginTop="12dp"
        android:gravity="center"
        android:text="@string/sub"
        android:textSize="20sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.313"
        app:layout_constraintStart_toEndOf="@+id/three"
        app:layout_constraintTop_toBottomOf="@+id/mul" />

    <Button
        android:id="@+id/nine"
        android:layout_width="67dp"
        android:layout_height="53dp"
        android:layout_marginStart="24dp"
        android:layout_marginLeft="24dp"
        android:layout_marginTop="60dp"
        android:gravity="center"
        android:text="@string/nine"
        android:textSize="20sp"
        app:layout_constraintStart_toEndOf="@+id/eight"
        app:layout_constraintTop_toBottomOf="@+id/res" />

    <TextView
        android:id="@+id/textView"
        android:layout_width="225dp"
        android:layout_height="43dp"
        android:gravity="center"
        android:text="@string/head"
        android:textColor="#EC0808"
        android:textSize="30sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.046" />

    <EditText
        android:id="@+id/res"
        android:layout_width="368dp"
        android:layout_height="47dp"
        android:ems="10"
        android:gravity="center"
        android:hint="RESULT"
        android:inputType="textPersonName"
        android:textColorHint="#06DC0E"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.372"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.156" />

</androidx.constraintlayout.widget.ConstraintLayout>
        """)
        
    def counter():
        """
    Write a program to create an activity with two buttons START and STOP. 
    On pressing of the START button, the activity must start the counter by displaying the numbers from One and the counter must keep on 
    counting until the STOP button is pressed. Display the counter value in a TextViewcontrol.
        """
        print(r"""
 // MainActivity.java
package com.example.project3;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
public class MainActivity extends AppCompatActivity {
    Button b1,b2;
    TextView t1;
    int i=1;
    Handler hd = new Handler();
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        b1 = findViewById(R.id.bstart);
        b2 = findViewById(R.id.bstop);
		//b3 = findViewById(R.id.clear);
        t1 = findViewById(R.id.displaycount);

        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                hd.postDelayed(updatetimer,1000);
            }
        });
        b2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                hd.removeCallbacks(updatetimer);
            }
        });
	
	// For Clear Button
//        b3.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View view) {
//                hd.removeCallbacks(updatetimer);
//                t1.setText("");
//                i=1;
//            }
//        });

    }
    private final Runnable updatetimer = new Runnable() {
        @Override
        public void run() {
            t1.setText(""+i);
            hd.postDelayed(this,1000);
            i++;
        }
    };
}

// strings.xml
<resources>
    <string name="app_name">project3</string>
    <string name="start">START</string>
    <string name="stop">STOP</string>
    <string name="heading">COUNTER APPLICATION</string>
    <string name="count">COUNT</string>
</resources>


// activity_main.xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <Button
        android:id="@+id/bstop"
        android:layout_width="317dp"
        android:layout_height="77dp"
        android:gravity="center"
        android:text="@string/stop"
        android:textSize="34sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/bstart"
        app:layout_constraintVertical_bias="0.338" />

    <TextView
        android:id="@+id/displaycount"
        android:layout_width="364dp"
        android:layout_height="104dp"
        android:gravity="center"
        android:hint="@string/count"
        android:textColor="@color/purple_700"
        android:textSize="48sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.489"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.277" />

    <Button
        android:id="@+id/bstart"
        android:layout_width="317dp"
        android:layout_height="77dp"
        android:layout_marginTop="84dp"
        android:gravity="center"
        android:text="@string/start"
        android:textSize="34sp"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/displaycount" />

    <TextView
        android:id="@+id/textView2"
        android:layout_width="381dp"
        android:layout_height="65dp"
        android:gravity="center"
        android:text="@string/heading"
        android:textColor="@android:color/holo_red_dark"
        android:textSize="34sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.533"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.043" />
</androidx.constraintlayout.widget.ConstraintLayout>
        """)
        
    def signup_signin():
        """
Create a SIGN Up activity with Username and Password. Validation of password should happen based on the following rules:
 Password should contain uppercase and lowercaseletters.
 Password should contain letters andnumbers.
 Password should contain specialcharacters.
 Minimum length of the password (the default value is8).
On successful SIGN UP proceed to the next Login activity. Here the user should SIGN IN using
the Username and Password created during signup activity. If the Username and Password are
matched then navigate to the next activity whichdisplays a message saying “Successful Login” or
else display a toast message saying “Login Failed”.The user is given only two attempts and after
thatdisplay a toast message saying “Failed Login Attempts” and disable the SIGN IN button. Use
Bundle to transfer information from one activity to another.
        """
        print(r"""
 // MainActivity.java
package com.example.project4;
import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
public class MainActivity extends AppCompatActivity {
    EditText ed1,ed2;
    Button b1;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ed1 = findViewById(R.id.txt1);
        ed2 = findViewById(R.id.txt2);
        b1 = (Button) findViewById(R.id.button1);
        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String username = ed1.getText().toString();
                String password = ed2.getText().toString();
                if(validate(password)){
                    Toast.makeText(MainActivity.this, "Signup Successful !", Toast.LENGTH_SHORT).show();
                    Intent intlogin = new Intent(MainActivity.this,login.class);
                    intlogin.putExtra("pword",password);
                    intlogin.putExtra("uname",username);
                    startActivity(intlogin);
                }
                else {
                    Toast.makeText(MainActivity.this, "Signup Unsuccessful !", Toast.LENGTH_LONG).show();
                }
            }
        });
    }
    private Boolean validate(String pw){
        Pattern ptrn;
        Matcher mtch;
        String pwd = "^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@$%^&()_]).{8,}$";
        ptrn = Pattern.compile(pwd);
        mtch = ptrn.matcher(pw);
        return mtch.matches();
    }
}

 // login.java
package com.example.project4;
import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;
public class login extends AppCompatActivity {
    EditText ed3,ed4;
    Button b2;
    int Counter=2;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        ed3 = findViewById(R.id.txt3);
        ed4 = findViewById(R.id.txt4);
        b2 = (Button) findViewById(R.id.button2);
        String reguser,redpwd;
        reguser = getIntent().getStringExtra("uname");
        redpwd = getIntent().getStringExtra("pword");
        b2.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                String username = ed3.getText().toString();
                String password = ed4.getText().toString();
                if(username.equals(reguser) && password.equals(redpwd)){
                    Toast.makeText(login.this, "Successful Login", Toast.LENGTH_SHORT).show();
                    Intent in = new Intent(login.this,Success.class);
                    startActivity(in);
                }
                else {
                    Counter--;
                    Toast.makeText(login.this, "Incorrect Credentials", Toast.LENGTH_SHORT).show();
                    if(Counter==0){
                        Toast.makeText(login.this, "Max Attepmts you are Blocked", Toast.LENGTH_SHORT).show();
                        b2.setEnabled(false);
                    }
                }
            }
        });
    }
}

//Success.java
package com.example.project4;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
public class Success extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_success);
    }
}


// activity_main.xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <EditText
        android:id="@+id/txt1"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:ems="10"
        android:hint="Username"
        android:inputType="textPersonName"
        android:textColorHint="@color/design_default_color_primary_dark"
        android:textSize="30sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.497"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.24" />

    <EditText
        android:id="@+id/txt2"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:ems="10"
        android:hint="Password"
        android:inputType="textPassword"
        android:textColor="@color/black"
        android:textColorHint="@color/purple_700"
        android:textSize="30sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.491"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/txt1"
        app:layout_constraintVertical_bias="0.14" />

    <Button
        android:id="@+id/button1"
        android:layout_width="174dp"
        android:layout_height="74dp"
        android:text="Sign up"
        android:textSize="30sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.497"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/txt2"
        app:layout_constraintVertical_bias="0.263" />
</androidx.constraintlayout.widget.ConstraintLayout>


// activity_login.xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".login">

    <EditText
        android:id="@+id/txt3"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:ems="10"
        android:hint="Username"
        android:inputType="textPersonName"
        android:textColorHint="@color/design_default_color_primary_dark"
        android:textSize="30sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.497"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.24" />

    <EditText
        android:id="@+id/txt4"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:ems="10"
        android:hint="Password"
        android:inputType="textPassword"
        android:textColor="@color/black"
        android:textColorHint="@color/purple_700"
        android:textSize="30sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.491"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/txt3"
        app:layout_constraintVertical_bias="0.14" />

    <Button
        android:id="@+id/button2"
        android:layout_width="174dp"
        android:layout_height="74dp"
        android:text="Login"
        android:textSize="30sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.497"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/txt4"
        app:layout_constraintVertical_bias="0.263" />
</androidx.constraintlayout.widget.ConstraintLayout>

//activity_success.xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".Success">

    <TextView
        android:id="@+id/textView"
        android:layout_width="393dp"
        android:layout_height="99dp"
        android:gravity="center"
        android:text="Login is Successfull !"
        android:textColor="@android:color/holo_red_dark"
        android:textColorHighlight="@color/purple_500"
        android:textSize="40sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent" />
</androidx.constraintlayout.widget.ConstraintLayout>
        """)
        
    def wallpaper():
        """
    Develop an application to set an image as wallpaper. On click of a button, the wallpaper image should start to change randomly every 30 seconds.
        """
        print(r"""
  //MainActivity.java
package com.example.project7;
import androidx.appcompat.app.AppCompatActivity;
import android.app.WallpaperManager;
import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import java.io.IOException;
import java.util.Timer;
import java.util.TimerTask;
public class MainActivity extends AppCompatActivity {
    Button b1;
    Timer Mytimer;
    WallpaperManager Mywall;
    Drawable Mydraw;
    int nextpaper = 1;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        b1 = findViewById(R.id.click);
        Mytimer = new Timer();
        Mywall = WallpaperManager.getInstance(this);
        b1.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                changewallpaper();
            }
        });
    }
    private void changewallpaper() {
        Mytimer.schedule(new TimerTask() {
            @Override
            public void run() {
                if (nextpaper == 1) {
                    Mydraw = getResources().getDrawable(R.drawable.a);
                    nextpaper = 2;
                } else if (nextpaper == 2) {
                    Mydraw = getResources().getDrawable(R.drawable.b);
                    nextpaper = 3;
                } else if (nextpaper == 3) {
                    Mydraw = getResources().getDrawable(R.drawable.c);
                    nextpaper = 4;
                } else if (nextpaper == 4) {
                    Mydraw = getResources().getDrawable(R.drawable.d);
                    nextpaper = 5;
                } else if (nextpaper == 5)
                    System.exit(0);
                Bitmap wallpaper = ((BitmapDrawable) Mydraw).getBitmap();
                try {
                    Mywall.setBitmap(wallpaper);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }, 0, 3000);
    }
}


    // activity_main.xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="409dp"
        android:layout_height="wrap_content"
        android:gravity="center"
        android:text="CHANGING WALLPAPER APPLICATION"
        android:textColor="@color/black"
        android:textSize="34sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.292" />

    <Button
        android:id="@+id/click"
        android:layout_width="346dp"
        android:layout_height="84dp"
        android:text="CLICK HERE TO CHANGE WALLPAPER"
        android:textSize="20sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.492"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toBottomOf="@+id/textView"
        app:layout_constraintVertical_bias="0.254" />

</androidx.constraintlayout.widget.ConstraintLayout>
        """)
        
    def parse_xml_json():
        """
        parse xml json files
        
        advice
        - create assets  folder in app 
        - create city.json file in assets folder
        - create city.xml file in assets folder
        """
        print(r"""
 advice
- create assets  folder in app 
- create city.json file in assets folder
- create city.xml file in assets folder


    //MainActivity.java
package com.example.project8;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;
import org.json.JSONArray;
import org.json.JSONObject;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
public class MainActivity extends AppCompatActivity {
    TextView tv1,tv2;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        tv1=findViewById(R.id.tv1);
        tv2=findViewById(R.id.tv2);
    }
    public void parsexml(View view){
        try{
            InputStream is=getAssets().open("city.xml");
            DocumentBuilderFactory documentfact=DocumentBuilderFactory.newInstance();
            DocumentBuilder documentBuil=documentfact.newDocumentBuilder();
            Document docu=documentBuil.parse(is);
            StringBuilder stringbuild=new StringBuilder();
            stringbuild.append("XML DATA");
            stringbuild.append("\n...........\n");
            NodeList nodeList=docu.getElementsByTagName("place");
            for(int i=0;i<nodeList.getLength();i++){
                Node node=nodeList.item(i);
                if(node.getNodeType()==Node.ELEMENT_NODE){
                    Element element=(Element) node;
                    stringbuild.append("\n city name :").append(getvalue("city",element));
                    stringbuild.append("\n latitude :").append(getvalue("lat",element));
                    stringbuild.append("\n longitude :").append(getvalue("long",element));
                    stringbuild.append("\n temperature :").append(getvalue("temp",element));
                    stringbuild.append("\n humidity :").append(getvalue("hum",element));
                    stringbuild.append("\n .........\n");
                }
            }
            tv1.setText(stringbuild.toString());
        }catch (Exception e){
            e.printStackTrace();
            Toast.makeText(this, "Error", Toast.LENGTH_SHORT).show();
        }
    }
    public void parsejson(View view){
        String json;
        StringBuilder stringbuild=new StringBuilder();
        try{
            InputStream is =getAssets().open("city.json");
            int size=is.available();
            byte[] buffer=new byte[size];
            is.read(buffer);
            json=new String(buffer, StandardCharsets.UTF_8);
            JSONArray jsonarry=new JSONArray(json);
            stringbuild.append("JSON DATA");
            stringbuild.append("\n..........\n");
            for(int i=0;i<jsonarry.length();i++){
                JSONObject jsonObject=jsonarry.getJSONObject(i);
                stringbuild.append("\n city name : " ).append(jsonObject.getString("city"));
                stringbuild.append("\n latitude : ").append(jsonObject.getString("lat"));
                stringbuild.append("\n longitude : ").append(jsonObject.getString("long"));
                stringbuild.append("\n temperature : ").append(jsonObject.getString("temp"));
                stringbuild.append("\n humidity : ").append(jsonObject.getString("hum"));
                stringbuild.append("\n..........\n");
            }
            tv2.setText(stringbuild.toString());
        }catch (Exception e){
            e.printStackTrace();
            Toast.makeText(this, "error", Toast.LENGTH_SHORT).show();
        }
    }
    private String getvalue(String tag,Element element){
        return element.getElementsByTagName(tag).item(0).getChildNodes().item(0).getNodeValue();
    }
}


//assets/city.xml
<record>
    <place>
        <city>Mysore</city>
        <lat>75.55</lat>
        <long>76.639</long>
        <temp>22</temp>
        <hum>90</hum>
    </place>
    <place>
        <city>puttur</city>
        <lat>12.2</lat>
        <long>16.539</long>
        <temp>25</temp>
        <hum>70</hum>
    </place>
</record>


//assets/city.json

[
  {
    "city": "mysore",
    "lat": "75.55",
    "long": "76.639",
    "temp": "22",
    "hum": "90"
  },
  {
    "city": "puttur",
    "lat": "12.2",
    "long": "16.539",
    "temp": "25",
    "hum": "70"
  }
]


 // activity_main.xml
 <?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/tv2"
        android:layout_width="185dp"
        android:layout_height="444dp"
        android:gravity="center"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.964"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.867" />

    <Button
        android:id="@+id/bt2"
        android:layout_width="177dp"
        android:layout_height="52dp"
        android:onClick="parsejson"
        android:text="PARSING JSON DATA"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.931"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.262" />

    <TextView
        android:layout_width="360dp"
        android:layout_height="75dp"
        android:gravity="center"
        android:text="PARSING XML AND JSON DATA"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.49"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.077" />

    <Button
        android:id="@+id/bt1"
        android:layout_width="177dp"
        android:layout_height="52dp"
        android:onClick="parsexml"
        android:text="PARSING XML DATA"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.05"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.262" />

    <TextView
        android:id="@+id/tv1"
        android:layout_width="185dp"
        android:layout_height="444dp"
        android:gravity="center"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.017"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.867" />

</androidx.constraintlayout.widget.ConstraintLayout>
        """)
    
    def texttospeech():
        """
    Develop a simple application “convert text to speech” that converts the user input text into voice.
        """
        print(r"""
 // MainActivity.java
package com.example.project5;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.speech.tts.TextToSpeech;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import java.util.Locale;
public class MainActivity extends AppCompatActivity {
    Button b1;
    EditText et1;
    TextToSpeech t1;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        et1 = findViewById(R.id.ed1);
        b1 = findViewById(R.id.bt1);
        t1 = new TextToSpeech(getApplicationContext(),status -> {
            if(status!=TextToSpeech.ERROR){
                t1.setLanguage(Locale.ENGLISH);
            }
        });
    }
    public void convert(View view){
        String tospeak = et1.getText().toString();
        t1.speak(tospeak,TextToSpeech.QUEUE_FLUSH,null);
    }
}

//activity_main.xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:onClick="convert"
    tools:context=".MainActivity">

    <TextView
        android:id="@+id/textView"
        android:layout_width="368dp"
        android:layout_height="59dp"
        android:gravity="center"
        android:text="TTS Application"
        android:textColor="@color/design_default_color_error"
        android:textSize="38sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.4"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.037" />

    <EditText
        android:id="@+id/ed1"
        android:layout_width="370dp"
        android:layout_height="165dp"
        android:ems="10"
        android:gravity="center"
        android:hint="Enter your text here"
        android:inputType="textPersonName"
        android:textSize="24sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.487"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.353" />

    <Button
        android:id="@+id/bt1"
        android:layout_width="297dp"
        android:layout_height="70dp"
        android:text="CONVERT TTS"
        android:textSize="34sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.662" />
</androidx.constraintlayout.widget.ConstraintLayout>
        """)
        
    def phone():
        """
        Create an activity like a phone dialer with CALL and SAVE options
        """
        print(r"""
// MainActivity.java
package com.example.project6;

import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.ContactsContract;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
public class MainActivity extends AppCompatActivity {
    Button call,save,clear;
    EditText et1;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        et1 = findViewById(R.id.ed1);
        clear = findViewById(R.id.clrbtn);
        call = findViewById(R.id.clbtn);
        save = findViewById(R.id.svbtn);
        clear.setOnClickListener(view -> et1.setText(""));
        call.setOnClickListener(view -> {
            String number = et1.getText().toString();
            Intent intent = new Intent(Intent.ACTION_DIAL);
            intent.setData(Uri.parse("tel:"+number));
            startActivity(intent);
        });
        save.setOnClickListener(view -> {
            String number = et1.getText().toString();
            Intent intent = new Intent(Intent.ACTION_INSERT, ContactsContract.Contacts.CONTENT_URI);
            intent.putExtra(ContactsContract.Intents.Insert.PHONE,number);
            startActivity(intent);
        });
    }
    public void inputnumber(View view){
        Button btn=(Button) view;
        String digit = btn.getText().toString();
        String phonenumber = et1.getText().toString();
        et1.setText(phonenumber+digit);
    }
}

//activity_main.xml
<?xml version="1.0" encoding="utf-8"?>
<androidx.constraintlayout.widget.ConstraintLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    tools:context=".MainActivity">

    <Button
        android:id="@+id/clrbtn"
        android:layout_width="157dp"
        android:layout_height="71dp"
        android:text="CLEAR"
        android:textSize="34sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.498"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.808" />

    <Button
        android:id="@+id/svbtn"
        android:layout_width="177dp"
        android:layout_height="65dp"
        android:text="SAVE"
        android:textSize="34sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.651" />

    <TextView
        android:id="@+id/textView"
        android:layout_width="311dp"
        android:layout_height="86dp"
        android:gravity="center"
        android:text="CALLER"
        android:textColor="@color/design_default_color_error"
        android:textSize="48sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.496"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.07" />

    <EditText
        android:id="@+id/ed1"
        android:layout_width="405dp"
        android:layout_height="74dp"
        android:ems="10"
        android:gravity="center"
        android:hint="Enter Phone Number"
        android:inputType="textPersonName"
        android:textSize="34sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.432"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.275" />

    <Button
        android:id="@+id/clbtn"
        android:layout_width="146dp"
        android:layout_height="66dp"
        android:text="CALL"
        android:textSize="34sp"
        app:layout_constraintBottom_toBottomOf="parent"
        app:layout_constraintEnd_toEndOf="parent"
        app:layout_constraintHorizontal_bias="0.498"
        app:layout_constraintStart_toStartOf="parent"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintVertical_bias="0.491" />
</androidx.constraintlayout.widget.ConstraintLayout>
        """)
        
        
class general:
    """
sb6.general.read_csv_file()  :-  read csv files and getting the data
sb6.general.load_iris_dataset() :- Load the iris dataset 
sb6.general.preprocessing_text_to_numbers() :- both manual and automatic preprocessing for iris target
sb6.general.split_the_data_to_test_train()  :- import data and splitting the data to test and train 

sb6.general.some_classifiers() :- 
    classifiers like :-  GaussianNB , MultinomialNB , KNeighborsClassifier (knn) , RandomForestClassifier
        RandomForestRegressor , SGDClassifier , SGDRegressor , LogisticRegression , LinearRegression , SVM (Support Vector Machine) Classification 
        SVR - SVM (Support Vector Machine) Regression , DecisionTreeClassifier , DecisionTreeRegressor,  GradientBoostingClassifier , GradientBoostingRegressor 
        AdaBoostClassifier , AdaBoostRegressor  , Bagging Classifier  , Bagging Regressor , Extra Trees Classifier , Extra Trees Regressor 
        Ridge Classifier, Ridge Regressor 
        

    """
    def read_csv_file():
        print(r"""
import csv
fulldata = []
with open('enjoysport.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        fulldata.append(row)
fulldata.pop(0)   # pop heading
   
# OR 

import csv
with open('enjoysport.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    fulldata = [row for row in reader]
fulldata.pop(0)       # pop heading

# OR 

import pandas as pd
import numpy as np
fulldata = pd.read_csv('enjoysport.csv')   # can write next line in this only
fulldata = np.array(fulldata)    # already removed heading by numpy

# OR

import pandas as pd
import numpy as np
fulldata = pd.read_csv('enjoysport.csv')
data = np.array(fulldata.iloc[:,:-1])    # iloc[start heigth : end height , start width : end width]
target = np.array(fulldata.iloc[:,-1])   # np removes the heading by default

# OR

import pandas as pd
fulldata = pd.read_csv('enjoysport.csv')
data = fulldata.iloc[:,:-1].values
target = fulldata.iloc[:,-1].values
        """)
        
    def load_iris_dataset():
        print(r"""
from sklearn.datasets import load_iris
fulldata = load_iris()
data = fulldata.data
target = fulldata.target
        """)
        
    def preprocessing_text_to_numbers():
        print(r"""
from sklearn.preprocessing import LabelEncoder
target = LabelEncoder().fit_transform(target)

# OR maually

for i,h in enumerate(target):
    if target[i]=='Iris-setosa':
        target[i]='0'
    elif target[i]=="Iris-versicolor":
        target[i]='1'
    else:
        target[i]='2'
        """)
        
    def split_the_data_to_test_train():
        print(r"""
import numpy as np,import pandas as pd
fulldata = pd.read_csv('Iris.csv')

data = np.array(fulldata.iloc[:,1:-1])
target = np.array(fulldata.iloc[:,-1])

from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest = train_test_split(data,target,test_size=0.3,random_state=42)

#OR
from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest = train_test_split(fulldata.iloc[:,1:-1],fulldata.iloc[:,-1],test_size=0.3,random_state=42)
        """)
        
    def some_classifiers():
        print(r"""
from sklearn.datasets import load_iris
import numpy as np
fulldata = load_iris()
data = np.array(fulldata.data)
target = np.array(fulldata.target)

from sklearn.preprocessing import LabelEncoder
target = LabelEncoder().fit_transform(target)

from sklearn.model_selection import train_test_split
xtrain, xtest, ytrain, ytest = train_test_split(data, target, test_size=0.3, random_state=42)


from sklearn.metrics import accuracy_score, confusion_matrix , mean_squared_error , r2_score


print("GaussianNB")
from sklearn.naive_bayes import GaussianNB
gaussianmodel = GaussianNB().fit(xtrain, ytrain)
gaussianmodelpred = gaussianmodel.predict(xtest)
print(accuracy_score(ytest, gaussianmodelpred))

print("MultinomialNB")
from sklearn.naive_bayes import MultinomialNB
multinomialmodel = MultinomialNB().fit(xtrain, ytrain)
multinomialmodelpred = multinomialmodel.predict(xtest)
print(accuracy_score(ytest, multinomialmodelpred))

print("KNeighborsClassifier")
from sklearn.neighbors import KNeighborsClassifier
kclassifier = KNeighborsClassifier(n_neighbors=3).fit(xtrain, ytrain)
kpredict = kclassifier.predict(xtest)
print(accuracy_score(ytest, kpredict))

print("RandomForestClassifier")
from sklearn.ensemble import RandomForestClassifier
randomforestclassifier = RandomForestClassifier().fit(xtrain, ytrain)
rfcpred = randomforestclassifier.predict(xtest)
print(accuracy_score(ytest, rfcpred))

print("RandomForestRegressor")
from sklearn.ensemble import RandomForestRegressor
randomforestregressor = RandomForestRegressor().fit(xtrain, ytrain)
rfgpred = randomforestregressor.predict(xtest)
# Confusion matrix cannot be calculated for a regression problem
print(accuracy_score(ytest, rfgpred))

print("SGDClassifier")
from sklearn.linear_model import SGDClassifier
sgdclassifier = SGDClassifier().fit(xtrain, ytrain)
sgdcpred = sgdclassifier.predict(xtest)
print(accuracy_score(ytest, sgdcpred))

print("SGDRegressor")
from sklearn.linear_model import SGDRegressor
sgdregressor = SGDRegressor().fit(xtrain, ytrain)
sgdrpred = sgdregressor.predict(xtest)
# Confusion matrix cannot be calculated for a regression problem
print(accuracy_score(ytest, sgdrpred))

print("LogisticRegression")
from sklearn.linear_model import LogisticRegression
logisticregression = LogisticRegression().fit(xtrain, ytrain)
logisticregressionpred = logisticregression.predict(xtest)
print(accuracy_score(ytest, logisticregressionpred))

print("LinearRegression")
from sklearn.linear_model import LinearRegression
linearregression = LinearRegression().fit(xtrain, ytrain)
linearregressionpred = linearregression.predict(xtest)
# Confusion matrix cannot be calculated for a regression problem
print(accuracy_score(ytest, linearregressionpred))

print("SVM - SVM (Support Vector Machine) Classification")
from sklearn.svm import SVC
svmclassifier = SVC(kernel='linear').fit(xtrain,ytrain)
svmpred = svmclassifier.predict(xtest)
print(confusion_matrix(svmpred,ytest))  
print(accuracy_score(svmpred,ytest))

print("SVR - SVM (Support Vector Machine) Regression")
from sklearn.svm import SVR
svmregressor = SVR(kernel='linear').fit(xtrain,ytrain)
svrpred = svmregressor.predict(xtest)
print(mean_squared_error(svrpred,ytest))  
print(r2_score(svrpred,ytest))

print("DecisionTreeClassifier")
from sklearn.tree import DecisionTreeClassifier
dtclassifier = DecisionTreeClassifier().fit(xtrain,ytrain)
dtpred = dtclassifier.predict(xtest)
print(confusion_matrix(dtpred,ytest))  
print(accuracy_score(dtpred,ytest))

print("DecisionTreeRegressor")
from sklearn.tree import DecisionTreeRegressor
dtregressor = DecisionTreeRegressor().fit(xtrain,ytrain)
dtrpred = dtregressor.predict(xtest)
print(mean_squared_error(dtrpred,ytest))  
print(r2_score(dtrpred,ytest))

print("GradientBoostingClassifier")
from sklearn.ensemble import GradientBoostingClassifier
gbclassifier = GradientBoostingClassifier().fit(xtrain,ytrain)
gbpred = gbclassifier.predict(xtest)
print(confusion_matrix(gbpred,ytest))  
print(accuracy_score(gbpred,ytest))

print("GradientBoostingRegressor")
from sklearn.ensemble import GradientBoostingRegressor
gbregressor = GradientBoostingRegressor().fit(xtrain,ytrain)
gbrpred = gbregressor.predict(xtest)
print(mean_squared_error(gbrpred,ytest))  
print(r2_score(gbrpred,ytest))

print("AdaBoostClassifier")
from sklearn.ensemble import AdaBoostClassifier
adaclassifier = AdaBoostClassifier().fit(xtrain,ytrain)
adapred = adaclassifier.predict(xtest)
print(confusion_matrix(adapred,ytest))  
print(accuracy_score(adapred,ytest))

print("AdaBoostRegressor")
from sklearn.ensemble import AdaBoostRegressor
adaregressor = AdaBoostRegressor().fit(xtrain,ytrain)
adarpred = adaregressor.predict(xtest)
print(mean_squared_error(adarpred,ytest))  
print(r2_score(adarpred,ytest))

print("Bagging Classifier")
from sklearn.ensemble import BaggingClassifier
bg_classifier = BaggingClassifier().fit(xtrain, ytrain)
bg_classifier_pred = bg_classifier.predict(xtest)
print(confusion_matrix(bg_classifier_pred, ytest))
print(accuracy_score(bg_classifier_pred, ytest))

print("Bagging Regressor")
from sklearn.ensemble import BaggingRegressor
bg_regressor = BaggingRegressor().fit(xtrain, ytrain)
bg_regressor_pred = bg_regressor.predict(xtest)
print(mean_squared_error(bg_regressor_pred, ytest))

print("Extra Trees Classifier")
from sklearn.ensemble import ExtraTreesClassifier
et_classifier = ExtraTreesClassifier().fit(xtrain, ytrain)
et_classifier_pred = et_classifier.predict(xtest)
print(confusion_matrix(et_classifier_pred, ytest))
print(accuracy_score(et_classifier_pred, ytest))

print("Extra Trees Regressor")
from sklearn.ensemble import ExtraTreesRegressor
et_regressor = ExtraTreesRegressor().fit(xtrain, ytrain)
et_regressor_pred = et_regressor.predict(xtest)
print(mean_squared_error(et_regressor_pred, ytest))

print("Ridge Classifier")
from sklearn.linear_model import RidgeClassifier
ridge_classifier = RidgeClassifier().fit(xtrain, ytrain)
ridge_classifier_pred = ridge_classifier.predict(xtest)
print(confusion_matrix(ridge_classifier_pred, ytest))
print(accuracy_score(ridge_classifier_pred, ytest))

print("Ridge Regressor")
from sklearn.linear_model import Ridge
ridge_regressor = Ridge().fit(xtrain, ytrain)
ridge_regressor_pred = ridge_regressor.predict(xtest)
print(mean_squared_error(ridge_regressor_pred, ytest))
        """)
        
class mlothers:
    def pg1():
        print(r"""
import csv
a = []
with open('enjoysport.csv', 'r') as c:
    rea = csv.reader(c)
    next(rea)
    a = [row for row in rea]
n = len(a[0]) - 1
hyp = ['0'] * n
for i in range(0, n):
    hyp[i] = a[0][i]
for i in range(0, len(a)):
    if a[i][n] == 'yes':
        for j in range(0, n):
            if a[i][j] != hyp[j]:
                hyp[j] = '?'
print('\n', hyp)
        """)

    def pg2():
        print(r"""
import numpy as np
import pandas as pd

# load .csv
data = pd.read_csv('enjoysport.csv')
concepts = np.array(data.iloc[:,0:-1])
target = np.array(data.iloc[:,-1])

def learn(concepts, target):
    specific_h = concepts[0].copy()
    print("\nInitialization of specific_h and generic_h")
    print("\nSpecific Boundary:", specific_h)
    general_h = [["?" for i in range(len(specific_h))] for i in range(len(specific_h))]
    print("\nGeneric Boundary:", general_h)
    
    for i, h in enumerate(concepts):
        print("\nInstance", i+1, "is", h)
        if target[i] == "yes":
            print("Instance is Positive")
            for x in range(len(specific_h)):
                if h[x] != specific_h[x]:
                    specific_h[x] = '?'
                    general_h[x][x] = '?'
        if target[i] == "no":
            print("Instance is Negative")
            for x in range(len(specific_h)):
                if h[x] != specific_h[x]:
                    general_h[x][x] = specific_h[x]
                else:
                    general_h[x][x] = '?'
        print("Specific Bundary after", i+1, "Instance is", specific_h)
        print("Generic Boundary after", i+1, "Instance is", general_h)
        print("\n")
        
    indices = [i for i, val in enumerate(general_h) if val == ['?', '?', '?', '?', '?', '?']]
    for i in indices:
        general_h.remove(['?', '?', '?', '?', '?', '?'])
        
    return specific_h, general_h

s_final, g_final = learn(concepts, target)
print("Final Specific_h:", s_final)
print("Final General_h:", g_final)
        """)

    def pg3():
        print(r"""

import pandas as pd

# Load the dataset
iris_df = pd.read_csv('iris.csv')

# Identify and delete rows with duplicate data
iris_df.drop_duplicates(inplace=True)

# Identify and delete columns with a single value
columns_to_delete = []
for column in iris_df.columns:
    if len(iris_df[column].unique()) == 1:
        columns_to_delete.append(column)

iris_df.drop(columns=columns_to_delete, inplace=True)

# Print the preprocessed dataset
print(iris_df)

# IT's not my program its someone else's program; mine is still not ready 
        """)

    def pg4():
        print(r"""

import numpy as np

class Node:
    def __init__(self, feature=None, label=None):
        self.feature = feature
        self.label = label
        self.children = {}

def id3(X, y, features):
    # Create a new node
    node = Node()
    
    # If all labels are the same, return the label
    if len(np.unique(y)) == 1:
        node.label = y[0]
        return node
    
    # If no more features are left, return the majority label
    if len(features) == 0:
        node.label = np.bincount(y).argmax()
        return node
    
    # Find the best feature to split the data
    best_feature = None
    best_gain = -1
    for feature in features:
        gain = information_gain(X[:, feature], y)
        if gain > best_gain:
            best_gain = gain
            best_feature = feature
    
    node.feature = best_feature
    
    # Split the data based on the best feature
    unique_values = np.unique(X[:, best_feature])
    for value in unique_values:
        idx = X[:, best_feature] == value
        child_features = [f for f in features if f != best_feature]
        child_node = id3(X[idx], y[idx], child_features)
        node.children[value] = child_node
    
    return node

def information_gain(feature, labels):
    entropy_parent = entropy(labels)
    unique_values = np.unique(feature)
    entropy_children = 0
    for value in unique_values:
        idx = feature == value
        child_labels = labels[idx]
        entropy_children += len(child_labels) / len(labels) * entropy(child_labels)
    
    return entropy_parent - entropy_children

def entropy(labels):
    unique_labels, counts = np.unique(labels, return_counts=True)
    probabilities = counts / len(labels)
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return entropy

# Example usage
X = np.array([
    [1, 0, 1],
    [1, 1, 0],
    [0, 1, 1],
    [1, 0, 0],
    [0, 1, 0]
])
y = np.array([1, 0, 0, 1, 0])
features = [0, 1, 2]

root = id3(X, y, features)

# Classify a new sample
sample = np.array([1, 1, 1])  # Modify with your own sample
current_node = root
while current_node.label is None:
    feature_value = sample[current_node.feature]
    current_node = current_node.children[feature_value]

predicted_label = current_node.label
print("Predicted label:", predicted_label)
        """)

    def pg5():
        print(r"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import export_graphviz
from sklearn import tree

data = pd.read_csv("Iris.csv", index_col=0)
data.reset_index(drop=True, inplace=True)
x = np.array(data.iloc[:, :-1])
y = np.array(data.iloc[:, -1])

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.30, random_state=42)

clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

y_pred = clf.predict(X_test)
print()
print("ACCURACY OF THE MODEL: ", metrics.accuracy_score(y_test, y_pred))

y = clf.predict([[3, 3, 2, 2]])
print(y)

i_tree = 0
for tree_in_forest in clf.estimators_:
    if i_tree < 1:
        tree.export_graphviz(tree_in_forest, out_file='tree.dot', feature_names=['sepalLength', 'sepalWidth', 'petalLength', 'petalWidth'])
        i_tree = i_tree + 1

# IT's not my program its someone else's program mine is still not ready 
        """)

    def pg6():
        print(r"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import OneHotEncoder

data = pd.read_csv('iris.csv')
x = np.array(data.iloc[:, :-1])
y = np.array(data.iloc[:, -1])

encoder = OneHotEncoder()
# ye = encoder.fit_transform(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=.4, random_state=42)

cl = GaussianNB()
mul = MultinomialNB()

mul.fit(x_train, y_train)
cl.fit(x_train, y_train)

y_predmul = mul.predict(x_test)
y_pred = cl.predict(x_test)

accuracy1 = accuracy_score(y_test, y_pred)
accuracy2 = accuracy_score(y_test, y_predmul)

print("Accuracy gaussian:", accuracy1, "\nconfusion matrix:\n", confusion_matrix(y_test, y_pred))
print("Accuracy mutinomial", accuracy2, "\nconfusion matrix:\n", confusion_matrix(y_test, y_predmul))

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(x_train, y_train)
y_pred = knn.predict(x_test)
accuracy = knn.score(x_test, y_test)
print("Accuracy knn", accuracy, "\nconfusion matrix:\n", confusion_matrix(y_test, y_pred))
        """)

    def pg7():
        print(r"""
import pandas as pd
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score

df = pd.read_csv('/home/pranav/Documents/work/iris.csv')
X = np.array(df.iloc[:, :-1])
y = np.array(df.iloc[:, -1])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

model = GaussianNB()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='macro')

print("Accuracy:", accuracy)
print("Precision:", precision)
        """)

    def pg8():
        print(r"""
import numpy as np
import csv
import pandas as pd
from pgmpy.models import BayesianModel
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination

heartDisease = pd.read_csv('heart.csv')
heartDisease = heartDisease.replace('?', np.nan)

print('Few examples from the dataset are given below')
print(heartDisease.head())

model = BayesianModel([
    ('age', 'trestbps'), ('age', 'fbs'),
    ('sex', 'trestbps'), ('exang', 'trestbps'),
    ('trestbps', 'heartdisease'), ('fbs', 'heartdisease'),
    ('heartdisease', 'restecg'), ('heartdisease', 'thalach'),
    ('heartdisease', 'chol')
])

print('\nLearning CPD using Maximum likelihood estimators')
model.fit(heartDisease, estimator=MaximumLikelihoodEstimator)

print('\nInferencing with Bayesian Network:')
HeartDisease_infer = VariableElimination(model)

print('\n1. Probability of HeartDisease given Age=30')
q = HeartDisease_infer.query(variables=['heartdisease'], evidence={'age': 67})
print(q)

print('\n2. Probability of HeartDisease given cholesterol=100')
q = HeartDisease_infer.query(variables=['heartdisease'], evidence={'chol': 233})
print(q)
        """)

    def pg9():
        print(r"""
import numpy as np
import pandas as pd
from sklearn.mixture import GaussianMixture

data = pd.read_csv('your_data_file.csv')
X = data.iloc[:, :-1].values

em = GaussianMixture(n_components=3, random_state=42)
em.fit(X)

y_pred = em.predict(X)

data['Cluster'] = y_pred
print(data['Cluster'])
        """)

    def pg10():
        print(r"""
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

iris = datasets.load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

svm = SVC(kernel='linear')
svm.fit(X_train_scaled, y_train)

y_pred = svm.predict(X_test_scaled)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
        """)

    def pg11():
        print(r"""
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix

data = pd.read_csv('SocialNetworkAds.csv')
x = np.array(data.iloc[:, :-1])
y = np.array(data.iloc[:, -1])

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.5, random_state=42)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)
print(y_pred)

accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_pred, y_test)

print("Accuracy:", accuracy)
print("Confusion Matrix:\n", cm)
        """)

    def pg12():
        print(r"""
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

iris = pd.read_csv('iris.csv')
X = iris.drop('species', axis=1)
y = iris['species']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
rf_classifier.fit(X_train, y_train)

y_pred = rf_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

new_sample = [[5.1, 3.5, 1.4, 0.2]] # Modify with your own sample
predicted_class = rf_classifier.predict(new_sample)
print("Predicted class:", predicted_class)
        """)
