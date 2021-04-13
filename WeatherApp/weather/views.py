import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


def index(request):
    appid = 'b932d4d71767381c1b0aa1222558060b'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid
    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all().order_by('id')
    all_cities = []
    for city in cities:
        res = requests.get(url.format(city.name)).json()
        city_info = {
            'city': city.name,
            'temp': res['main']['temp'],
            'icon': res['weather'][0]['icon']
        }
        all_cities.insert(0, city_info)
        if len(all_cities) >= 7:
            all_cities.pop()

    context = {'all_info': all_cities, 'form': form}
    return render(request, 'weather/index.html', context)
