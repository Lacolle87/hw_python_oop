from dataclasses import asdict, dataclass
import dataclasses
from typing import Dict, Type, List


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите get_spent_calories в %s.'
            % self.__class__.__name__)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


@dataclass
class Running(Training):
    """Тренировка: бег."""

    action: int
    duration: float
    weight: float

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return (self.CALORIES_MEAN_SPEED_MULTIPLIER
                * super().get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
                ) * self.weight / self.M_IN_KM * (
                    self.duration * self.MIN_IN_H)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    action: int
    duration: float
    weight: float
    height: float

    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    MULT = 2
    CM_IN_M = 100
    SEC_IN_HOUR = 3600
    KMH_IN_MSEC = round(Training.M_IN_KM / SEC_IN_HOUR, 3)

    def get_spent_calories(self) -> float:
        return (self.CALORIES_WEIGHT_MULTIPLIER * self.weight + (
                (self.get_mean_speed() * self.KMH_IN_MSEC
                 ) ** self.MULT / (self.height / self.CM_IN_M)
                ) * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight) * (self.duration * self.MIN_IN_H)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    action: int
    duration: float
    weight: float
    length_pool: int
    count_pool: int

    LEN_STEP = 1.38
    SWIMMING_MEAN_SPEED_MULTIPLIER = 2
    SWIMMING_MEAN_SPEED_SHIFT = 1.1

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                ) / self.M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                 + self.SWIMMING_MEAN_SPEED_SHIFT)
                * self.SWIMMING_MEAN_SPEED_MULTIPLIER
                * self.weight * self.duration)


WORKOUT_TYPES: Dict[str, Type[Training]] = {
    'SWM': Swimming,
    'RUN': Running,
    'WLK': SportsWalking
}


def read_package(workout_type: str, data: List) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type not in WORKOUT_TYPES:
        raise ValueError(f'Wrong workout_type: {workout_type}. '
                         f'Available types: '
                         f'{", ".join(list(WORKOUT_TYPES.keys()))}')
    elif len(dataclasses.fields(WORKOUT_TYPES[workout_type])) != len(data):
        raise ValueError("Input data doesn't match")
    else:
        return WORKOUT_TYPES[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1.5, 80, 25, 40]),
        ('RUN', [15000, 1.5, 75]),
        ('WLK', [9000, 1.5, 75, 180]),
    ]
    try:
        for workout_type, data in packages:
            main(read_package(workout_type, data))
    except Exception as err:
        print(f"{type(err).__name__} was raised: {err}")
