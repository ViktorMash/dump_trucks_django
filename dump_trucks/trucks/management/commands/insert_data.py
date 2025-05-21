from django.core.management.base import BaseCommand

# noinspection PyUnresolvedReferences
from trucks.models import Truck, TruckModel


class Command(BaseCommand):
    help = "Добавляет тестовые данные о самосвалах"

    def handle(self, *args, **options):
        try:
            # Создание моделей самосвалов
            belaz = TruckModel.objects.create(name="БЕЛАЗ", max_capacity=120)
            komatsu = TruckModel.objects.create(
                name="Komatsu", max_capacity=110
            )

            # Создание самосвалов
            Truck.objects.create(
                board_number="101", model=belaz, current_load=100
            )
            Truck.objects.create(
                board_number="102", model=belaz, current_load=125
            )
            Truck.objects.create(
                board_number="K103", model=komatsu, current_load=120
            )

            self.stdout.write(self.style.SUCCESS("Данные успешно добавлены!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {e}"))
