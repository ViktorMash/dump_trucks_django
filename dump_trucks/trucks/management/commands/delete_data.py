from django.core.management.base import BaseCommand

# noinspection PyUnresolvedReferences
from trucks.models import Truck, TruckModel


class Command(BaseCommand):
    help = "Удаление данных из БД"

    def handle(self, **args):
        """Интерактивное меню для удаления данных"""
        self.stdout.write(
            self.style.NOTICE("=== Управление удалением данных ===")
        )
        self.stdout.write(
            "\n1. Удалить все модели самосвалов (и экземпляры самосвалов)"
            "\n2. Удаление всех самосвалов без удаления моделей"
            "\n3. Удаление самосвала по бортовому номеру"
            "\n4. Удаление самосвала по модели"
            "\n5. Выход"
        )
        while True:
            choice = input("\nВыберите опцию (1-5): ")

            if choice == "1":
                self._delete_models()
                break
            elif choice == "2":
                self._delete_trucks()
                break
            elif choice == "3":
                board_number = input(
                    "Введите бортовой номер самосвала для удаления: "
                )
                # todo реализовать валидацию введенных данных
                self._delete_specific_truck(board_number)
                break
            elif choice == "4":
                model_name = input(
                    "Введите название модели самосвала для удаления: "
                )
                # todo реализовать валидацию введенных данных
                self._delete_specific_model(model_name)
                break
            elif choice == "5":
                self.stdout.write("Выход из программы.")
                break
            else:
                self.stdout.write(
                    self.style.ERROR("Неверный выбор, попробуйте еще раз")
                )

    def _delete_models(self, auto_confirm=False):
        """1. Удалить все модели самосвалов (и экземпляры самосвалов)"""
        if not auto_confirm:
            self.stdout.write(
                self.style.WARNING(
                    "ВНИМАНИЕ: Будут удалены все модели самосвалов "
                    "и связанные с ними экземпляры самосвалы!"
                )
            )
            confirm = input("Подтвердите удаление (y/n): ")
            if confirm.lower() != "y":
                self.stdout.write(self.style.ERROR("Операция отменена."))
                return

        models_count = TruckModel.objects.count()
        trucks_count = Truck.objects.count()

        TruckModel.objects.all().delete()  # Каскадное удаление затронет и самосвалы

        self.stdout.write(
            self.style.SUCCESS(
                f"Удалено: {models_count} моделей самосвалов и {trucks_count} связанных самосвалов."
            )
        )

    def _delete_trucks(self, auto_confirm=False):
        """2. Удаление всех самосвалов без удаления моделей"""
        if not auto_confirm:
            self.stdout.write(
                self.style.WARNING(
                    "ВНИМАНИЕ: Будут удалены все экземпляры самосвалов с бортовыми номерами "
                    "(модели самосвалов останутся в базе)!"
                )
            )
            confirm = input("Подтвердите удаление (y/n): ")
            if confirm.lower() != "y":
                self.stdout.write(self.style.ERROR("Операция отменена."))
                return

        trucks_count = Truck.objects.count()
        Truck.objects.all().delete()

        self.stdout.write(
            self.style.SUCCESS(f"Удалено: {trucks_count} самосвалов.")
        )

    def _delete_specific_truck(self, board_number):
        """3. Удаление самосвала по бортовому номеру"""
        try:
            truck = Truck.objects.get(board_number=board_number)
            truck_info = f"{truck.board_number} ({truck.model.name})"
            truck.delete()
            self.stdout.write(
                self.style.SUCCESS(f"Самосвал {truck_info} успешно удален.")
            )
        except Truck.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f"Самосвал с бортовым номером {board_number} не найден."
                )
            )

    def _delete_specific_model(self, model_name, auto_confirm=False):
        """4. Удаление самосвала по модели"""
        try:
            model = TruckModel.objects.get(name=model_name)
            trucks_count = model.trucks.count()

            if not auto_confirm:
                self.stdout.write(
                    self.style.WARNING(
                        f"ВНИМАНИЕ: Будет удалена модель {model.name}. Всего {trucks_count} записей"
                    )
                )
                confirm = input("Подтвердите удаление (y/n): ")
                if confirm.lower() != "y":
                    self.stdout.write(self.style.ERROR("Операция отменена."))
                    return

            model_info = f"{model.name}"
            model.delete()  # Каскадное удаление
            self.stdout.write(
                self.style.SUCCESS(
                    f"Модель {model_info} и {trucks_count} связанных самосвалов успешно удалены."
                )
            )
        except TruckModel.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(
                    f"Модель с названием {model_name} не найдена."
                )
            )
