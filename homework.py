class InfoMessage:
    """Создает объект класса сообщения."""

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
        """Возвращает строку сообщения с детальной информацией о тренировке:
        """

        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Создает базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    HOURS_TO_MINUTES: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Расчитывает дистанцию, которую пользователь
        преодолел во время тренировки.
        """

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Расчитывает среднюю скорость движения во время тренировки.
        """

        distance = self.get_distance()
        return distance / self.duration

    def get_spent_calories(self) -> float:
        """Расчитывает количество потраченных калорий во время тренировки.
        """

        pass

    def show_training_info(self) -> InfoMessage:
        """Создает объект сообщения о результатах тренировки:"""

        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Создает объект Running для рассчета статистик по занятиям бегом.
    """

    CALORIES_MEAN_SPEED_MULTIPLIER_1: int = 18
    CALORIES_MEAN_SPEED_MULTIPLIER_2: int = 20

    def get_spent_calories(self) -> float:
        """Расчитывает количество потраченных калорий во время тренировки.
        """

        speed = self.get_mean_speed()
        calories = ((self.CALORIES_MEAN_SPEED_MULTIPLIER_1
                     * speed
                     - self.CALORIES_MEAN_SPEED_MULTIPLIER_2)
                     * self.weight
                     / self.M_IN_KM
                     * self.duration
                     * self.HOURS_TO_MINUTES)
        return calories


class SportsWalking(Training):
    """Создает объект SportsWalking для рассчета
    статистик по занятиям спортивным шагом.
    """

    WEIGHT_MULTIPLIER_1: float = 0.035
    WEIGHT_MULTIPLIER_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()

    def get_spent_calories(self) -> float:
        """Расчитывает количество потраченных калорий во время тренировки.
        """

        calories = ((self.WEIGHT_MULTIPLIER_1
                     * self.weight
                     + (self.speed**2 // self.height)
                     * self.WEIGHT_MULTIPLIER_2
                     * self.weight)
                    * self.duration
                    * self.HOURS_TO_MINUTES)
        return calories


class Swimming(Training):
    """Создает объект Swimming для рассчета статистик по занятиям плаваньем.
    """

    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_CONSTANT: float = 1.1
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_mean_speed(self) -> float:
        """Расчитывает среднюю скорость движения во время тренировки.
        """

        speed = (self.length_pool
                 * self.count_pool
                 / self.M_IN_KM
                 / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Расчитывает количество потраченных калорий во время тренировки.
        """

        calories = ((self.speed
                     + self.CALORIES_MEAN_SPEED_CONSTANT)
                    * self.CALORIES_MEAN_SPEED_MULTIPLIER
                    * self.weight)
        return calories


def read_package(workout_type: str,
                 data: list
                 ) -> Training:
    """Прочитать данные полученные от датчиков."""

    read_package = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking}
    return read_package[workout_type](*data)


def main(training: Training) -> InfoMessage:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
