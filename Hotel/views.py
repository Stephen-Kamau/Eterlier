from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utilsFile import (auth as authentication,  passwordHash as password_hasher, sms,
                        stringGen as string_generator, mainChecker as validator, sendMail)
from eterlier import settings
from .serielizers import BranchSerializer

import datetime
import jwt
from .models import Eatery, Branch
# Create your views here.

@api_view(['GET'])
def homePageView(request):
    return Response({"message": "Hotels homePageView"})


@api_view(['POST'])
def create_Eterly(request):
    try:
        eterly_name = request.data.get('name',None)
        email = request.data.get('email',None)
        password = request.data.get('password',None)
        description = request.data.get('description',None)

        image = request.FILES.get('image', None)
        if not image:
            return Response({"error": "Please provide an image."}, status=400)

        if validator.checkmail(email) == False:
            return_data = {
                "error": "1",
                "message": "Email number is Invalid"
            }
            return Response(return_data, status=400)

        if Eatery.objects.filter(email = email).exists():
            return Response({"error": "Email Already Taken. Please use your email address.", "message":"Unable to create eterly"}, status=400)
        #sill be used to know who is registering the branchs
        encryped_password = password_hasher.generate_password_hash(password)
        random_id = string_generator.alphanumeric(20)
        code = string_generator.numeric(4)
        eterly = Eatery.objects.create(
            eatery_id = random_id,
            name=eterly_name,
            email=email,
            password=encryped_password,
            description=description,
            image=image,
            is_verified=False,
            verification_code=code
        )

        title = "Verification Code"
        body = f"Your verification code is: {code}"
        print(f"""

        {title}
        {body}
        """)
        timeLimit= datetime.datetime.now() + datetime.timedelta(minutes=1440) #set duration for token 1day
        payload = {"user_id": f"{random_id}",
                   "role": f"IS VERIEFIED :  {eterly.is_verified}",
                   "validated": eterly.is_verified,
                   "exp":timeLimit}

        #get totken
        token = jwt.encode(payload,settings.SECRET_KEY)
        # SendMail.send_email(title, email, body)

        return Response({"token":token, "success": "Eterly created successfully.", "message":"Please Verify the account and then Login with your email {email} to register branch"}, status=201)
    except Exception as e:
        return Response({"error": f"An Error OCcurred  {str(e)}"}, status=500)



#User verfication of the otp send through msg
@api_view(["POST"])
@authentication.token_required
def eterly_verification(request, decrypedToken):
    #get the token from headers
    try:
        otp_entered = request.data.get("code",None)
        if otp_entered != None and otp_entered != "":
            if Eatery.objects.filter(eatery_id=decrypedToken['user_id']).exists():
                curr_eterly = Eatery.objects.get(eatery_id=decrypedToken['user_id'])
            else:
                return Response({"error": "No such Eterly You login with", "message":"Wrong details presented"}, status=400)

            coded_added = str(curr_eterly.verification_code)
            if otp_entered == coded_added:
                #validate user
                curr_eterly.is_verified = True
                curr_eterly.save()

                return Response({"success": "Eterly Verified successfully.", "message":"You can create your branches now"}, status=201)
            elif otp_entered != coded_added:
                return Response({"error": "Code is Incorrect", "message":"Wrong details presented"}, status=400)
            else:
                return Response({"error": "An error occured", "message":"Wrong details presented"}, status=400)
        else:
            return Response({"error": "Invalid Parameters", "message":"Check your code format again, Must not be Blank"}, status=400)

    except Exception as e:
        return Response({"error": "An Exception was raised", "message":f"Error OCcurred  {e}"}, status=400)



# to create branch, the eterly must be VERIEFIED
@api_view(['POST'])
@authentication.token_required
def create_branch(request , decrypedToken):
    try:
        if Eatery.objects.filter(eatery_id=decrypedToken["user_id"]).exists() == False:
            return Response({"error": "No such Eterly Present", "message":f"Create an Eterly to connue with this"}, status=400)

        else:
            eterly_ref = Eatery.objects.get(eatery_id=decrypedToken["user_id"])
            name = request.data.get('name',None)
            city = request.data.get('city','')
            phone = request.data.get('phone',None)
            address = request.data.get('address',"")
            state = request.data.get('state',"")
            branch_id = string_generator.alphanumeric(20)

            #field that are must
            branch_fields = [eterly_ref , name , phone]
            if not None in branch_fields and "" not in branch_fields:
                if Branch.objects.filter(name= name, branch_ref=eterly_ref).exists():
                    return Response({"error": "You already have existing branch with such name", "message":f"Please update the name and other details"}, status=400)
                branch_object = Branch(
                    branch_id = branch_id,
                    branch_ref = eterly_ref,
                    name = name,
                    city=city,
                    phone = phone,
                    address = address,
                    state = state,
                )

                branch_object.save()
                return Response(
                {
                    "success": f"A bracnh  {name} for {eterly_ref.name} created successfully.",
                    "message":" Create Managers to allow access to the eterly",
                    "details": {"name":branch_object.name, "city":branch_object.city, "phone":branch_object.phone, "eterly":branch_object.branch_ref.name}
                    }, status=201)

            else:
                return Response({"error": "Invalid details provied. You must provided name and phone", "message":f"Correct the errors"}, status=400)


    except Exception as e:
        return Response({"error": "Erorr OCcurred", "message":f"An error occured    {e}"}, status=400)



@api_view(['GET'])
@authentication.token_required
def get_all_my_branches(request, decrypedToken):
    try:
        if Eatery.objects.filter(eatery_id=decrypedToken["user_id"]).exists() == False:
            return Response({"error": "No such Eterly Present", "message":f"Create an Eterly to connue with this"}, status=400)
        else:
            eterly_ref = Eatery.objects.get(eatery_id=decrypedToken['user_id'])
            return Response(
            {
                "success": f" Brachs for  {eterly_ref.name} .",
                "message":" Brachs Retrived well",
                "details": BranchSerializer(Branch.objects.filter(branch_ref = eterly_ref), many=True).data
                }, status=201)


    except Exception as e:
        return Response({"error": "Erorr OCcurred", "message":f"An error occured    {e}"}, status=400)

@api_view(['GET'])
def signup(request):
    return Response({"message": "signup"})

@api_view(['GET'])
def uploadProduct(request):
    return Response({"message": "uploadProduct"})

@api_view(['GET'])
def viewProduct(request):
    return Response({"message": "viewProduct"})

@api_view(['GET'])
def orderProduct(request):
    return Response({"message": "orderProduct"})
