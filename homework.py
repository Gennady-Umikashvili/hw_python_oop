from dataclasses import dataclass, asdict
from typing import ClassVar


@dataclass(init=True, repr=False, eq=False, order=False, unsafe_hash=False,
           frozen=False)
class InfoMessage:
    """Информационное сообщение о тренировке."""
    MESSAGE: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Сообщение о результатах."""
        return self.MESSAGE.format(**asdict(self))


@dataclass(init=True, repr=False, eq=False, order=False, unsafe_hash=False,
           frozen=False)
class Training:
    """Базовый класс тренировки."""
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[float] = 1000
    MIN_IN_H: ClassVar[float] = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.action * self.LEN_STEP / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("Требуется расчитать get_spent_calories()")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass(init=True, repr=False, eq=False, order=False, unsafe_hash=False,
           frozen=False)
class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        """Потраченные колории при беге."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_H)


@dataclass(init=True, repr=False, eq=False, order=False, unsafe_hash=False,
           frozen=False)
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: ClassVar[float] = 0.029
    KMH_IN_MSEC: ClassVar[float] = 0.278
    CM_IN_M: ClassVar[float] = 100

    height: float

    def get_spent_calories(self) -> float:
        """Потраченные колории при спортивной ходьбе."""
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * self.KMH_IN_MSEC)**2
                 / (self.height / self.CM_IN_M))
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                 * self.weight) * self.duration * self.MIN_IN_H)


@dataclass(init=True, repr=False, eq=False, order=False, unsafe_hash=False,
           frozen=False)
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 1.1
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 2.0

    length_pool: float
    count_pool: int

    def get_mean_speed(self) -> float:
        """Средняя скорость плавца."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Потраченные колории плавца."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_MULTIPLIER)
                * self.CALORIES_MEAN_SPEED_SHIFT * self.weight
                * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_type: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    type_workout: Training = training_type[workout_type](*data)
    return type_workout


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
