from rest_framework import generics, status
from rest_framework.response import Response

from utils.city import cities

from ..models import Contact, Rate
# from ..models import AboutUs, Contact, Rules, Privacy,Rate
from .serializers import ContactSerializer, RateSerializer

# from .serializers import AboutUsSerializer, ContactSerializer, RulesSerializer, PrivacySerializer,RateSerializer


# class PrivacyApiView(generics.GenericAPIView):
#     serializer_class = PrivacySerializer
#     queryset = Privacy.load()

#     def get(self, request, *args, **kwargs):
#         serializer = self.serializer_class(self.queryset)
#         context = {"is_done": True, "message": "متن حریم خصوصی ", "data": serializer.data}
#         return Response(data=context, status=status.HTTP_200_OK)


# class AboutUsApiView(generics.GenericAPIView):
#     serializer_class = AboutUsSerializer
#     queryset = AboutUs.load()

#     def get(self, request, *args, **kwargs):
#         serializer = self.serializer_class(self.queryset)
#         context = {"is_done": True, "message": "متن درباره ما", "data": serializer.data}
#         return Response(data=context, status=status.HTTP_200_OK)


#
#
# class RuleApiView(generics.GenericAPIView):
#     serializer_class = RulesSerializer
#     queryset = Rules.load()

#     def get(self, request, *args, **kwargs):
#         serializer = self.serializer_class(self.queryset)
#         context = {"is_done": True, "message": "متن قوانین", "data": serializer.data}
#         return Response(data=context, status=status.HTTP_200_OK)


# class RuleApiView(ListAPIView):
#     serializer_class = RulesSerializer
#     queryset = Rules.load()
#
#     def list(self, request, *args, **kwargs):
#         response = super().list(request, *args, **kwargs)
#         return response({
#             "is_done": True
#         })
#
#
# class AboutUsApiView(ListAPIView):
#     queryset = AboutUs.load()
#     serializer_class = AboutUsSerializer
#
#     def list(self, request, *args, **kwargs):
#         response = super().list(request, *args, **kwargs)
#         return response({
#             'is_done': True
#         })


class CityListApiView(generics.GenericAPIView):
    """
    this view is for getting the city of province;
    query params as province passed in views urls and filter down base on that
    """

    def get(self, request, *args, **kwargs):
        province = self.request.query_params.get("province")
        city_list = [item for item in cities if item["state"] == province]
        context = {
            "is_done": True,
            "message": f"لیست شهرهای {province}",
            "city": city_list,
        }
        return Response(data=context, status=status.HTTP_200_OK)


class ContactUsCreateAPiView(generics.CreateAPIView):
    """
    this view is for creating contact;
    """

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response(
            {
                "is_done": True,
                "message": "پیام با موفقیت ارسال شد",
                "data": response.data,
            }
        )
    
class RateApiView(generics.GenericAPIView):
    serializer_class = RateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            obj, created = Rate.objects.update_or_create(
                user=request.user,
                defaults={'number': serializer.validated_data['number']},
            )
            context = {
                'is_done': True,
                'message': 'rate submitted'
            }
            return Response(data=context, status=status.HTTP_200_OK)
        context = {
            'is_done': True,
            'message': serializer.errors
        }
        return Response(data=context, status=status.HTTP_400_BAD_REQUEST)    
