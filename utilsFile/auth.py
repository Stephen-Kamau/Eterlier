from rest_framework.response import Response
from rest_framework import status
import jwt
from eterlier import settings

def token_required(something):
    def wrap(request):
        # I will user Bearer Token Instead of Get
        token_bearer = request.headers.get('Authorization')
        try:
            #if request.GET.get('token') != '' and request.GET.get('token') != None:
            if token_bearer !="" and token_bearer !=None and "bearer" in token_bearer:
                token_passed = token_bearer.split(" ")[-1]
                try:
                    data = jwt.decode(token_passed,settings.SECRET_KEY, algorithms=['HS256'])
                    return something(request,data)
                except jwt.exceptions.ExpiredSignatureError:
                    return_data = {
                        "error": "1",
                        "message": "Token has expired"
                        }
                    return Response(return_data, status=status.HTTP_401_UNAUTHORIZED)
                except Exception as e:
                    return_data = {
                        "e":f"{e}",
                        "error": "1",
                        "message": "Invalid Token"
                    }
                    return Response(return_data, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return_data = {
                    "error" : "2",
                    "message" : "Token required",
                    }
                return Response(return_data, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return_data = {
                "error" : "3",
                "message" : "An error occured check verification of token"
                }
            return Response(return_data, status=status.HTTP_401_UNAUTHORIZED)
    return wrap
