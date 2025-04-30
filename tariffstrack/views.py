from django.http import Http404
from django.shortcuts import render, get_list_or_404

from .models import Country, Tariff

# Change the rates into integer percentages
def make_integer(tariff_list):
     # multiply the rate to 100.00 and convert to integer
    for tariff in tariff_list:
        tariff.rate = int(tariff.rate * 100.00)
    return tariff_list

def index(request):
    # get the list of tariffs from the Model database
    tariff_list = Tariff.objects.order_by('country__name')
    # Change the rates into integers percentages
    integer_tariff_list = make_integer(tariff_list)
    # pass the list as a context variable named "tariff_list"
    context = { 
        "tariff_list": integer_tariff_list 
    }
    return render(request, "tariffs/index.html", context)

# def country(request, country_id):
    
#     tariff_list = get_list_or_404(Tariff, country_id__exact=country_id)

#     # Change the rates into integers percentages
#     integer_tariff_list = make_integer(tariff_list)

#     context = {
#             "tariff_list": integer_tariff_list,
#             "country_id": country_id,
#             "country_name": tariff_list[0].country.name,
#         }
#     # pass the list as a context variable named "tariff_list"
#     return render(request, "tariffs/country.html", context)    
