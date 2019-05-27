from django.shortcuts import render
import pyrebase
from django.contrib import auth
import cv2

config = {
    "apiKey": "AIzaSyCG-EbfcPM8GBUyFWIcuR5azrHlVG53ado",
    "authDomain": "cholocheck-54b2d.firebaseapp.com",
    "databaseURL": "https://cholocheck-54b2d.firebaseio.com",
    "projectId": "cholocheck-54b2d",
    "storageBucket": "cholocheck-54b2d.appspot.com",
    "messagingSenderId": "504827221145"
  }
firebase = pyrebase.initialize_app(config)
u = ''

authe = firebase.auth()
database = firebase.database()
def signIn(request):
    return render(request,"signIn.html")
def postsign(request):
    email = request.POST.get("email")
    passw = request.POST.get("pass")
    try:
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message = "invalid credentials"
        return render(request,"signIn.html",{"messg":message})
    user = authe.refresh(user['refreshToken'])
    print(user)
    session_id = user['idToken']
    request.session['uid'] = str(session_id)
    return render(request,"welcome.html",{"e":email})
def logout(request):
    auth.logout(request)
    return render(request,"signIn.html")
def signUp(request):
    return render(request,"signup.html")
def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')
    try:
        user = authe.create_user_with_email_and_password(email,passw)
    except:
        message = "Unable to create account.TRY AGAIN."
        return render(request,"signup.html",{"messg":message})
    uid =  user['localId']
    data = {"name":name,"status":"1"}
    database.child("users").child(uid).child("details").set(data)
    return render(request,"signIn.html")
def create(request):                     #create is for upload image
    return render(request,"create.html")
def post_create(request):
    import time
    from datetime import datetime, timezone
    import pytz
    tz = pytz.timezone('Asia/Kolkata')
    time_now = datetime.now(timezone.utc).astimezone(tz)
    millis = int(time.mktime(time_now.timetuple()))
    print("mili"+str(millis))
    url = request.POST.get('url')
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("info"+str(a))
    global u
    u = url

    data = {
        "url":url
    }
    database.child("users").child(a).child("reports").child(millis).set(data)
    name = database.child("users").child(a).child("details").child("name").get().val()
    return render(request,"welcome.html",{"e":name,"u":u})
def click(request):


    cap = cv2.VideoCapture(0)

    # Check if the webcam is opened correctly
    if not cap.isOpened():
        raise IOError("Cannot open webcam")

    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        cv2.imshow('Input', frame)

        c = cv2.waitKey(1)
        if c == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return render(request,'create.html')
def result(request):
    return render(request,'result.html')
