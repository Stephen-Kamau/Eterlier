
import datetime

import jwt
from .models import User ,otp, Manager, Customer, Staff

from utilsFile import (auth as authentication,  passwordHash as password_hasher, sms,
                        stringGen as string_generator, mainChecker as validator, sendMail)
from django.db.models import Sum
from rest_framework.decorators import api_view
from rest_framework.response import Response
from eterlier import settings
from django.shortcuts import render


# Create your views here.


@api_view(['GET'])
def index_page(request):
    return Response({"message": "AccountshomePageView"})


# THIS IS CUSTOMER REGISTRATION... OTHER WILL BE COPIED FROM THIS FUNCTION I>E FOR MANAGER AND OTHERS...
@api_view(["POST"])
def user_registration(request):
    try:
        user_name = request.data.get('username',None)
        email = request.data.get('email',None)
        phoneNumber = request.data.get('phonenumber',None)
        gender = request.data.get('gender',None)
        password = request.data.get('password',None)
        address = request.data.get('address',None)
        state = request.data.get('state',None)
        country = request.data.get('country',None)

        #get all registration fields together
        reg_field = [user_name,phoneNumber,email, gender,password,address,state,country]
        if not None in reg_field and not "" in reg_field:
            if  User.objects.filter(user_phone =phoneNumber).exists() or  User.objects.filter(email =email).exists():
                return_data = {
                    "error": "1",
                    "message": "User Exists",
                    # "user":User.objects.filter(email =email)[0].email,
                    # "pass":User.objects.filter(email =email)[0].user_password
                }
                # or validator.checkphone(phoneNumber)== False
            elif validator.checkmail(email) == False :
                return_data = {
                    "error": "1",
                    "message": "Email or Phone number is Invalid"
                }
            else:
                #generate user_id
                userRandomId = string_generator.alphanumeric(20)
                #encrypt password
                encryped_password = password_hasher.generate_password_hash(password)
                #Save user_data
                # THIS IS CUSTOMER DATA, HENCE CUSTOMER IS TRUE
                new_userData = User(user_id=userRandomId,user_name=user_name,
                                email=email,user_phone=phoneNumber,user_gender=gender,
                                user_password=encryped_password,user_address=address,
                                user_state=state,user_country=country, is_customer=True)
                new_userData.save()
                #create customer Object to save him as customer..
                new_customer = Customer(customer_id= string_generator.alphanumeric(20), user= new_userData)
                new_customer.save()

                #Generate OTP
                code = string_generator.numeric(4)
                #Save OTP
                user_OTP =otp(user=new_userData,otp_code=code)
                user_OTP.save()


                validated = otp.objects.get(user__user_id=userRandomId).validated
                #Generate token
                timeLimit= datetime.datetime.now() + datetime.timedelta(minutes=1440) #set duration for token 1day
                payload = {"user_id": f"{userRandomId}",
                           "role": f"IS_CUSTOMER :  {new_userData.is_customer}",
                           "validated": validated,
                           "exp":timeLimit}

                #get totken
                token = jwt.encode(payload,settings.SECRET_KEY)
                message = f"Welcome to Eterlier, your verification code is {code} The code expires in the next 24hrs"
                # sms.sendsms(phoneNumber[1:],message)
                print(f"""
                {message}
                {token}
                """)

                return_data = {
                    "error": "0",
                    "message": "The registration was successful, A verrification SMS has been sent",
                    "token": f"{token}",#.decode('UTF-8')
                    "elapsed_time": f"{timeLimit}",
                    }
        else:
            return_data = {
                "error":"2",
                "message": "Invalid Parrameter"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": f"An error occured    {e}"
        }
    return Response(return_data)

#User verfication of the otp send through msg
@api_view(["POST"])
@authentication.token_required
def user_verification(request,decrypedToken):
    try:
        otp_entered = request.data.get("otp",None)
        if otp_entered != None and otp_entered != "":
            if User.objects.filter(user_id=decrypedToken['user_id']).exists():
                curr_user = User.objects.get(user_id=decrypedToken['user_id'])
            else:
                curr_user = None
            user_data = otp.objects.get(user = curr_user)
            otpCode,date_added = user_data.otp_code,user_data.date_added
            date_now = datetime.datetime.now()
            #print(date_now, date_added)
            duration = float((date_now.replace(tzinfo=None)  - date_added.replace(tzinfo=None) ).total_seconds())

            #WILL CHANGE THIS
            timeLimit = 3600.0 #60 mins interval
            if otp_entered == otpCode and duration < timeLimit:
                #validate user
                user_data.validated = True
                user_data.save()
                return_data = {
                    "error": "0",
                    "message":"User Verified"
                }
            elif otp_entered != otpCode and duration < timeLimit:
                return_data = {
                    "error": "1",
                    "message": "Incorrect OTP"
                }
            elif otp_entered == otpCode and duration > timeLimit:
                return_data = {
                    "error": "1",
                    "message": "OTP has expired"
                }
        else:
            return_data = {
                "error": "2",
                "message": "Invalid Parameters"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": f"An error occured  {e}"
        }
    return Response(return_data)

#resend OTP
@api_view(["POST"])
def resend_otp(request):
    try:
        phone_number = request.data.get('phone_number',None)
        if phone_number != None and phone_number != "":
            if User.objects.filter(user_phone =phone_number).exists() == False:
                    return_data = {
                        "error": "1",
                        "message": "User does not exist"
                    }
            else:
                user_data = otp.objects.get(user__user_phone=phone_number)
                user = User.objects.get(user_phone=phone_number)
                #generate new otp
                code = string_generator.numeric(4)
                user_data.otp_code = code
                user_data.save()
                message = f"Welcome to Eterlier, your verification code is {code}"
                print(f"""
                {message}
                """)
                # sms.sendsms(phone_number[1:],message)
                timeLimit= datetime.datetime.now() + datetime.timedelta(minutes=1440) #set limit for user
                payload = {"user_id": f'{user.user_id}',
                           "role": f"IS_CUSTOMER :  {new_userData.is_customer}"  ,
                           "validated": user_data.validated,
                           "exp":timeLimit}
                token = jwt.encode(payload,settings.SECRET_KEY)
                return_data = {
                    "error": "0",
                    "message": "OTP sent to phone number",
                    "token": token#.decode('UTF-8')
                }
        else:
            return_data = {
                "error": "2",
                "message": "Invalid Parameters"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": f"An error occured  {e}"
        }
    return Response(return_data)


#User login
@api_view(["POST"])
def user_login(request):
    try:
        email_phone = request.data.get("email_phone",None)
        password = request.data.get("password",None)
        field = [email_phone,password]
        if not None in field and not '' in field:
            validate_mail = validator.checkmail(email_phone)
            # validate_phone = validator.checkphone(email_phone)
            validate_phone = True
            if validate_mail == True:
                if User.objects.filter(email =email_phone).exists() == False:
                    return_data = {
                        "error": "1",
                        "message": "User does not exist"
                    }
                else:
                    user_data = User.objects.get(email=email_phone)
                    is_valid_password = password_hasher.check_password_match(password,user_data.user_password)
                    if otp.objects.filter(user__user_phone=user_data.user_phone).exists():
                        is_verified = otp.objects.get(user__user_phone=user_data.user_phone).validated
                    else:
                        is_verified = False
                    #print("IT IS VALIDAD ", is_verified)
                    #Generate token
                    timeLimit= datetime.datetime.now() + datetime.timedelta(minutes=1440) #set limit for user
                    payload = {"user_id": f'{user_data.user_id}',
                               "role": f"IS_CUSTOMER :  {user_data.is_customer}",
                               "validated": is_verified,
                               "exp":timeLimit}
                    token = jwt.encode(payload,settings.SECRET_KEY)
                    if is_valid_password and is_verified:
                        return_data = {
                            "error": "0",
                            "message": "Successfull",
                            "token": token,#.decode('UTF-8'),
                            "token-expiration": f"{timeLimit}",
                            "user_details": [
                                {
                                    "username": f"{user_data.user_name}",
                                    "email": f"{user_data.email}",
                                    "phone_number": f"{user_data.user_phone}",
                                    "gender": f"{user_data.user_gender}",
                                    "address": f"{user_data.user_address}",
                                    "state": f"{user_data.user_state}",
                                    "country": f"{user_data.user_country}"

                                }
                            ]

                        }
                    elif is_verified == False:
                        return_data = {
                            "error" : "1",
                            "message": "User is not verified",
                            "token": token#.decode('UTF-8')
                        }
                    else:
                        return_data = {
                            "error" : "1",
                            "message" : "Wrong Password"
                        }
            elif validate_phone == True:
                if User.objects.filter(user_phone =email_phone).exists() == False:
                    return_data = {
                        "error": "1",
                        "message": "User does not exist"
                    }
                else:
                    user_data = User.objects.get(user_phone=email_phone)
                    if otp.objects.filter(user__user_phone=user_data.user_phone).exists():
                        is_verified = otp.objects.get(user__user_phone=user_data.user_phone).validated
                    else:
                        is_verified = False
                    is_valid_password = password_functions.check_password_match(password,user_data.user_password)
                    #Generate token
                    timeLimit= datetime.datetime.now() + datetime.timedelta(minutes=1440) #set limit for user
                    payload = {"user_id": f'{user_data.user_id}',
                               "validated": is_verified,
                               "role": f"IS_CUSTOMER :  {user_data.is_customer}",
                               "exp":timeLimit}
                    token = jwt.encode(payload,settings.SECRET_KEY)
                    if is_valid_password and is_verified:
                        return_data = {
                            "error": "0",
                            "message": "Successfull",
                            "token": token.decode('UTF-8'),
                            "token-expiration": f"{timeLimit}",
                            "user_details": [
                                {
                                    "firstname": f"{user_data.user_name}",
                                    "email": f"{user_data.email}",
                                    "phone_number": f"{user_data.user_phone}",
                                    "gender": f"{user_data.user_gender}",
                                    "address": f"{user_data.user_address}",
                                    "state": f"{user_data.user_state}",
                                    "country": f"{user_data.user_country}"

                                }
                            ]

                        }
                    elif is_verified == False:
                        return_data = {
                            "error" : "1",
                            "message": "User is not verified",
                            "token": token.decode('UTF-8')
                        }
                    else:
                        return_data = {
                            "error" : "1",
                            "message" : "Wrong Password"
                        }
            else:
                return_data = {
                    "error": "2",
                    "message": "Email or Phone Number is Invalid"
                }
        else:
            return_data = {
                "error" : "2",
                "message" : "Invalid Parameters"
                }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": f"An error occured      {e}"
        }
    return Response(return_data)


@api_view(["POST"])
def password_reset(request):
    try:
        phone_number = request.data.get('phone_number',None)
        if phone_number != None and phone_number != "":
            if User.objects.filter(user_phone =phone_number).exists() == False:
                return_data = {
                    "error": "1",
                    "message": "User does not exist"
                }
            else:
                user_data = otp.objects.get(user__user_phone=phone_number)
                user = User.objects.get(user_phone=phone_number)
                generate_pin = string_generator.alphanumeric(15)
                user_data.password_reset_code = generate_pin
                user_data.save()
                message = f"Welcome to Eterlier, your password reset code is {generate_pin}"
                print(f"""
                {message}
                """)
                # sms.sendsms(phone_number[1:],message)
                timeLimit= datetime.datetime.now() + datetime.timedelta(minutes=1440) #set limit for user
                payload = {"user_id": f'{user.user_id}',
                           "role": f"IS_CUSTOMER :  {user_data.is_customer}",
                           "validated": user_data.validated,
                           "exp":timeLimit}
                token = jwt.encode(payload,settings.SECRET_KEY)
                return_data = {
                    "error": "0",
                    "message": "Successful, reset code sent to Phone Number",
                    "token": token#.decode('UTF-8')
                }
        else:
            return_data = {
                "error": "2",
                "message": "Invalid Parameter"
            }
    except Exception:
        return_data = {
            "error": "3",
            "message": "An error occured"
        }
    return Response(return_data)

#Change password
@api_view(["POST"])
@authentication.token_required
def password_reset_change(request,decrypedToken):
    try:
        reset_code = request.data.get("reset_code",None)
        new_password = request.data.get("new_password",None)
        fields = [reset_code,new_password]
        #print("This is the fielsss    ",fields , "\n\n\n\n")
        if not None in fields and not "" in fields:
            #get user info
            user_data = User.objects.get(user_id=decrypedToken["user_id"])
            otp_reset_code = otp.objects.get(user__user_id=decrypedToken["user_id"]).password_reset_code
            #print(otp_reset_code)
            if reset_code == otp_reset_code:
                #encrypt password
                encryptpassword = password_hasher.generate_password_hash(new_password)
                user_data.user_password = encryptpassword
                user_data.save()
                return_data = {
                    "error": "0",
                    "message": "Successfull, Password Changed"
                }
            elif reset_code != otp_reset_code:
                return_data = {
                    "error": "1",
                    "message": "Code does not Match"
                }
        else:
            return_data = {
                "error": "2",
                "message": "Invalid Parameters"
            }
    except Exception as e:
        return_data = {
            "error": "3",
            "message": f"An error occured  {e}"
        }
    return Response(return_data)
