from django.shortcuts import render

from .models import Truck, TruckModel


def truck_list(request):
    # Получаем все модели самосвалов для выпадающего списка
    truck_models = TruckModel.objects.all()

    # Получаем выбранную модель из GET-параметра (если есть)
    selected_model = request.GET.get("model", "all")

    # Фильтруем самосвалы по выбранной модели
    if selected_model and selected_model != "all":
        trucks = Truck.objects.filter(model__id=selected_model)
    else:
        trucks = Truck.objects.all()

    # Добавляем расчет перегруза в процентах для каждого самосвала
    for truck in trucks:
        truck.overload_pct = truck.overload_percentage

    # Передаем данные в шаблон
    context = {
        "truck_models": truck_models,
        "trucks": trucks,
        "selected_model": selected_model,
    }

    return render(request, "trucks/trucks_list.html", context)
