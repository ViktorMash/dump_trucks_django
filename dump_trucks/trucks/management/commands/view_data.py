from django.core.management.base import BaseCommand

# noinspection PyUnresolvedReferences
from trucks.models import Truck, TruckModel


class Command(BaseCommand):
    help = "Отображает информацию о самосвалах и их моделях"

    def handle(self, *args, **options):
        # Просмотр всех моделей самосвалов
        truck_models = TruckModel.objects.all().order_by("name")
        self.stdout.write(self.style.NOTICE("\n=== Модели самосвалов ==="))

        if not truck_models:
            self.stdout.write(
                self.style.WARNING("Нет данных о моделях самосвалов")
            )
        else:
            table_format = "{:<4} {:<15} {:<10}"
            self.stdout.write(
                table_format.format("ID", "Название", "Макс. грузоподъемность")
            )
            self.stdout.write("-" * 30)

            for model in truck_models:
                self.stdout.write(
                    table_format.format(
                        model.id, model.name, f"{model.max_capacity} т"
                    )
                )

        # Просмотр всех самосвалов
        trucks = (
            Truck.objects.all()
            .select_related("model")
            .order_by("board_number")
        )
        self.stdout.write(self.style.NOTICE("\n=== Самосвалы ==="))

        if not trucks:
            self.stdout.write(self.style.WARNING("Нет данных о самосвалах"))
        else:
            table_format = "{:<10} {:<15} {:<15} {:<15}"
            self.stdout.write(
                table_format.format("Номер", "Модель", "Загрузка", "Перегруз")
            )
            self.stdout.write("-" * 55)

            for truck in trucks:
                overload = truck.overload_percentage
                overload_text = f"{overload}%"

                # Выделяем перегруз красным цветом
                if overload > 100:
                    overload_text = self.style.ERROR(
                        f"{overload}% (ПЕРЕГРУЗ!)"
                    )
                else:
                    overload_text = self.style.SUCCESS(f"{overload}% (норма)")

                self.stdout.write(
                    table_format.format(
                        truck.board_number,
                        truck.model.name,
                        f"{truck.current_load} т",
                        overload_text,
                    )
                )

        # Статистика
        total_models = truck_models.count()
        total_trucks = trucks.count()
        overloaded_trucks = sum(
            1 for truck in trucks if truck.overload_percentage > 100
        )

        self.stdout.write(self.style.NOTICE("\n=== Статистика ==="))
        self.stdout.write(f"Всего моделей самосвалов: {total_models}")
        self.stdout.write(f"Всего самосвалов: {total_trucks}")
        self.stdout.write(f"Самосвалов с перегрузом: {overloaded_trucks}")
