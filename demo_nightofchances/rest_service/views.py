import requests

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from selenium import webdriver

from rest_service.models import Hotels
from rest_service.scrappers import HotelsScrapping
from rest_service.serializers import HotelsSerializer


def send_me_mail(body):
    data = {
        "from_email": "demo@intl.att.com",
        "subject": 'Hotels.com',
        "body": body,
        "to_email": "jp002f@intl.att.com",
    }
    r = requests.post(url='http://defragcs01.intl.att.com:8050/api/v1/email-send', data=data)

    return False if r.status_code == 500 else True


def test_required_params(data):
    req_params = ("city", "check_in", "check_out")
    for idx, param in enumerate(req_params):
        if param not in data:
            message = {
                "code": 4001,
                "text": "Required parameter {} was not provided".format(param),
                "hints": "Required params are, 'city', 'check_in', 'check_out'"
            }
            return False, message
    else:
        return True, None


class ScrappersView(APIView):

    def get(self, request, format=None):
        queryset = Hotels.objects.all()
        message = {
            "code": 5001,
            "text": "Table is empty",
            "hints": "Try execute post request on 'gbcdcgcs01.intl.att.com:8444/v1/hotels' endpoint first",
            "example": 'curl -X POST -H "Content-Type:application/json" gbcdcgcs01.intl.att.com:8444/v1/hotels -d '
                       '{"price_lt":"170","city":"Amsterdam","check_in":"06/10/2017","check_out":"08/10/2017"}'
        }
        if not queryset:
            return Response(data=message, status=status.HTTP_200_OK)
        else:
            serializer = HotelsSerializer(queryset, many=True)
            return Response(serializer.data)

    def post(self, request, format=None):
        city = request.data.get('city')
        check_in = request.data.get('check_in')
        check_out = request.data.get('check_out')

        test_pass, message = test_required_params(request.data)
        if not test_pass:
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        else:
            driver = webdriver.Firefox()
            scraper = HotelsScrapping(driver, city, check_in, check_out)
            cheapest_hotels = scraper.get_cheapest_hotels_detail()
            if cheapest_hotels:
                message = {
                    "code": 2000,
                    "text": "Successfully stored information about cheapest hotels in {}".format(city)
                }
                return Response(data=message)
            else:
                message = {
                    "code": 2000,
                    "text": "Service was not able to store data about cheapest hotels"
                }
                return Response(data=message, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class HotelsDetailView(APIView):

    def get(self, request, city, format=None):
        queryset = Hotels.objects.filter(city=city)
        message = {
            "code": 5001,
            "text": "Table is empty",
            "hints": "Try execute post request on 'gbcdcgcs01.intl.att.com:8444/v1/hotels' endpoint first",
            "example": 'curl -X POST -H "Content-Type:application/json" gbcdcgcs01.intl.att.com:8444/v1/hotels -d '
                       '{"price_lt":"170","city":"Amsterdam","check_in":"06/10/2017","check_out":"08/10/2017"}'
        }
        if not queryset:
            return Response(data=message, status=status.HTTP_200_OK)
        else:
            serializer = HotelsSerializer(queryset, many=True)
            return Response(serializer.data)


class TheCheapestHotelNotification(APIView):

    def post(self, request, format=None):
        price = request.data.get('price_lt')
        city = request.data.get('city')
        check_in = request.data.get('check_in')
        check_out = request.data.get('check_out')

        test_pass, message = test_required_params(request.data)
        if not test_pass:
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        else:
            driver = webdriver.Firefox()
            scraper = HotelsScrapping(driver, city, check_in, check_out)
            lowest_price = scraper.get_lowest_price()
            if lowest_price < int(price):
                message = 'Now is time to book hotel in {}, current lowest price is {} euro.'.format(city, lowest_price)
                send_me_mail(message)
                return Response(message)
            else:
                return Response('Hotels in {} are too expensive, current price is {} euro.'.format(city, lowest_price))
