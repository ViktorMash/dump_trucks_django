from typing import cast

from django.db import models


class TruckModel(models.Model):
    """Модель самосвала"""

    name = models.CharField(max_length=50, verbose_name="Название модели")
    max_capacity = models.IntegerField(
        verbose_name="Максимальная грузоподъемность (тонн)"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Модель самосвала"
        verbose_name_plural = "Модели самосвалов"


class Truck(models.Model):
    """Параметры конкретного самосвала"""

    board_number = models.CharField(
        max_length=20, unique=True, verbose_name="Бортовой номер"
    )
    model = models.ForeignKey(
        TruckModel,
        on_delete=models.CASCADE,
        verbose_name="Модель",
        related_name="trucks",
    )
    current_load = models.IntegerField(
        default=0, verbose_name="Текущий вес груза (тонн)"
    )

    @property
    def overload_percentage(self) -> float:
        """Вычисляет процент перегруза"""

        # аннотации типов для IDE, чтобы избежать предупреждений о некорректном типе данных
        truck_model = cast(
            TruckModel, self.model
        )  # это не ForeignKey, а объект модели
        max_capacity = cast(int, truck_model.max_capacity)
        current_load = cast(int, self.current_load)

        if max_capacity > 0:
            return round((current_load / max_capacity) * 100, 2)
        return 0

    def __str__(self):
        return f"{self.board_number} ({self.model.name})"

    class Meta:
        verbose_name = "Самосвал"
        verbose_name_plural = "Самосвалы"
