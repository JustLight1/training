"""
Создайте декоратор access_control, который ограничивает доступ к функции на
основе переданных ролей пользователя. Декоратор должен принимать аргументы,
определяющие допустимые роли (например,
@access_control(roles=['admin', 'moderator'])).
Требования:
Если текущий пользователь имеет одну из допустимых ролей, функция выполняется.
Если нет, выбрасывается исключение PermissionError с соответствующим
сообщением.
Реализуйте механизм определения текущей роли пользователя. Для целей задания
можно использовать глобальную переменную или контекстный менеджер.
"""
from functools import wraps


current_user = 'user'


def access_control(roles: list[str]):

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if current_user in roles:
                    return func(*args, **kwargs)
                else:
                    raise PermissionError('Доступ запрещен!')
            except PermissionError as e:
                print(e)
        return wrapper
    return decorator


@access_control(roles=['admin', 'moderator'])
def delete_post(user):
    return 'Готово'


delete_post(current_user)
