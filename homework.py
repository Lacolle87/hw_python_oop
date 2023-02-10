class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {"{:.3f}".format(self.duration)} ч.; '
            f'Дистанция: {"{:.3f}".format(self.distance)} км; '
            f'Ср. скорость: {"{:.3f}".format(self.speed)} км/ч; '
            f'Потрачено ккал: {"{:.3f}".format(self.calories)}.'
        )


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return (
            ((((self.CALORIES_MEAN_SPEED_MULTIPLIER * super().get_mean_speed())
               + self.CALORIES_MEAN_SPEED_SHIFT))
             * self.weight / self.M_IN_KM * (self.duration * self.MIN_IN_H))
        )


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    MULT = 2
    CM_IN_M = 100
    KMH_IN_MSEC = 0.278

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return super().get_mean_speed()

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed() * self.KMH_IN_MSEC
        training_time_in_minutes = self.duration * self.MIN_IN_H
        height_cm = self.height / self.CM_IN_M
        return ((self.CALORIES_WEIGHT_MULTIPLIER
                 * self.weight + (mean_speed ** self.MULT / height_cm)
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight
                 ) * training_time_in_minutes)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SWIMMING_MEAN_SPEED_MULTIPLIER = 2
    SWIMMING_MEAN_SPEED_SHIFT = 1.1

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return ((self.length_pool * self.count_pool)
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return (((self.get_mean_speed() + self.SWIMMING_MEAN_SPEED_SHIFT)
                 * self.SWIMMING_MEAN_SPEED_MULTIPLIER)
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_codes = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    return workout_codes[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1.5, 80, 25, 40]),
        ('RUN', [15000, 1.5, 75]),
        ('WLK', [9000, 1.5, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
