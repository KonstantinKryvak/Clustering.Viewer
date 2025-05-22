

from .CodeWalker import Algorithms as algorithms, DistanceMetrics as metrics
from .           import Display


try:

    if not algorithms:
        raise RuntimeError('Не знайдено жодного алгоритму для тестування!')
    if not metrics:
        print(f'\n\033[38;5;220mНе знайдено жодної метрики в теці! Застосовується "Евклідова відстань" за замовчуванням.\033[0m')


    Display.Init()
    Display.SetupInitialLayout(metrics, algorithms)
    Display.StartWindowPayload()


except Exception as error:
    print(f'\033[38;5;196m{type(error).__name__} exception raised: {str(error)}.\033[0m')
    raise error


finally:
    Display.Finalize()



