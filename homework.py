class InfoMessage:
    """
    Создает объект класса сообщения.
    """

    def __init__(self,
                 training_type: str,
                 duration: int,
                 distance: float,
                 speed: int,
                 calories: int
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """
        Возвращает строку сообщения с детальной информацией о тренировке:
        """
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    '''
    Создает базовый класс тренировки.
    '''
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        self.training_type = None
        self.action = action
        self.duration = duration
        self.weight = weight
        self.distance = self.get_distance()
        self.speed = None
        self.calories = None

    def get_distance(self) -> float:
        '''
        Расчитывает дистанцию, которую пользователь преодолел во время тренировки.
        '''
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        '''
        Расчитывает среднюю скорость движения во время тренировки.
        '''
        return self.distance / self.duration

    def get_spent_calories(self) -> float:
        '''
        Расчитывает количество потраченных калорий во время тренировки.
        '''
        pass

    def show_training_info(self) -> InfoMessage:
        '''
        Создает объект сообщения о результатах тренировки:
        '''
        return InfoMessage(self.training_type,
                           self.duration,
                           self.distance,
                           self.speed,
                           self.calories)


class Running(Training):
    '''
    Создает объект Running для рассчета статистик по занятиям бегом.
    '''
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.distance = super().get_distance()
        self.speed = super().get_mean_speed()
        self.calories = self.get_spent_calories()
        self.training_type = 'Running'

    def get_spent_calories(self) -> float:
        speed = super().get_mean_speed()
        cof_kcal_1 = 18
        cof_kcal_2 = 20
        hour_to_min: int = 60
        self.calories = ((cof_kcal_1 * speed - cof_kcal_2)
                         * self.weight
                         / self.M_IN_KM
                         * self.duration
                         * hour_to_min)
        return self.calories


class SportsWalking(Training):
    '''
    Создает объект SportsWalking для рассчета статистик по занятиям спортивным шагом.
    '''
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.distance = super().get_distance()
        self.speed = super().get_mean_speed()
        self.calories = self.get_spent_calories()
        self.training_type = 'SportsWalking'

    def get_spent_calories(self) -> float:
        cof_kcal_1 = 0.035
        cof_kcal_2 = 0.029
        wt_weight = cof_kcal_1 * self.weight
        hour_to_min: int = 60

        self.calories = ((cof_kcal_1 * self.weight
                          + (self.speed**2 // self.height)
                          * cof_kcal_2 * self.weight)
                         * self.duration
                         * hour_to_min)
        return self.calories


class Swimming(Training):
    '''
    Создает объект Swimming для рассчета статистик по занятиям плаваньем.
    '''
    LEN_STEP: float = 1.38
    M_IN_KM: int = 1000

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
        self.distance = super().get_distance()
        self.speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()
        self.training_type = 'Swimming'

    def get_mean_speed(self) -> float:
        self.speed = (self.length_pool
                      * self.count_pool
                      / self.M_IN_KM
                      / self.duration)
        return self.speed

    def get_spent_calories(self) -> float:
        cof_kcal_1: float = 1.1
        cof_kcal_2: int = 2
        self.calories = ((self.speed + cof_kcal_1)
                         * cof_kcal_2
                         * self.weight)
        return self.calories


def read_package(workout_type: str,
                 data: list
                 ) -> Training:
    """Прочитать данные полученные от датчиков."""
    read_package = {'SWM': Swimming,
                    'RUN': Running,
                    'WLK': SportsWalking}
    return read_package[workout_type](*data)


def main(training: Training) -> InfoMessage:
    info = training.show_training_info()
    print(info.get_message())
    return info
