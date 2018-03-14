from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from rest_service import views

urlpatterns = [
    url(r'^v1/hotels$', views.ScrappersView.as_view()),
    url(r'^v1/hotels/(?P<city>[a-zA-Z]*)$$', views.HotelsDetailView.as_view()),
    url(r'^v1/cheapest-hotel$', views.TheCheapestHotelNotification.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
