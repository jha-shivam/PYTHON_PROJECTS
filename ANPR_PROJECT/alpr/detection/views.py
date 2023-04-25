from django.shortcuts import render, HttpResponseRedirect
from .form import ImageForm
from .models import Images,Contact
from django.contrib import messages
import cv2
import numpy as np
import imutils
import easyocr
from matplotlib import pyplot as plt
import pytesseract
import os
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.


def index(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            image_1 = request.FILES['photo']
            image = str(image_1)
            url_1 = "/view_pic/?output={}".format(image)
            return HttpResponseRedirect(url_1)
            # return render(request,'HTML/view_pic.html',{'output':image})
    else:
        form = ImageForm()
    return render(request, 'HTML/index.html', {'form': form})


def usecase(request):
    return render(request, 'HTML/usecase.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        return render(request,'HTML/contact.html')
    return render(request, 'HTML/contact.html')


def about(request):
    return render(request, 'HTML/about.html')


def view_pic(request):
    if request.method == "GET":
        output = request.GET.get('output')
        folder = "C:/Users/shiva/OneDrive/Desktop/PROJECT/alpr/media/images"
        path = str(output)
        pic_url = os.path.join(folder,path) 
        pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        image = cv2.imread(pic_url)
        image = imutils.resize(image, width=500)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        plt.imshow(cv2.cvtColor(gray, cv2.COLOR_BGR2RGB))
        edged = cv2.Canny(gray, 170, 200)
        plt.imshow(cv2.cvtColor(edged, cv2.COLOR_BGR2RGB))
        cnts, new = cv2.findContours(
            edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        image1 = image.copy()
        cv2.drawContours(image1, cnts, -1, (0, 255, 0), 3)
        plt.imshow(cv2.cvtColor(image1, cv2.COLOR_BGR2RGB))
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:30]
        NumberPlateCount = None
        image2 = image.copy()
        cv2.drawContours(image2, cnts, -1, (0, 255, 0), 3)
        plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
        count = 0
        name = 1
        for i in cnts:
            perimeter = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * perimeter, True)
            if (len(approx) == 4):
                NumberPlateCount = approx
                x, y, w, h = cv2.boundingRect(i)
                crp_img = image[y:y + h, x:x + w]
                cv2.imwrite(str(name) + '.png', crp_img)
                name += 1
                break
        cv2.drawContours(image, [NumberPlateCount], -1, (0, 255, 0), 3)
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        crop_img_loc = cv2.imread('1.png')
        plt.imshow(cv2.cvtColor(crop_img_loc, cv2.COLOR_BGR2RGB))
        text = pytesseract.image_to_string(crop_img_loc, config='--psm 6')
        t1 = ""
        for i in text:
            if i.isalnum():
                t1 += i
        
        
    return render(request, 'HTML/view_pic.html', {'output': output,'number':t1})
