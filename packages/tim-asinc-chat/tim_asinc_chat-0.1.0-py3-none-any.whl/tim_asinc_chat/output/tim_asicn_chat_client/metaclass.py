import dis
from weakref import WeakKeyDictionary


class ClassVerifier(type):

    def __new__(cls, name, bases, clsdict):
        methods = []
        attrs = []
        if name not in ['Server', 'Client']:
            print(f'Class {name} not supported! Created without check!')
            return type.__new__(cls, name, bases, clsdict)

        for item in clsdict:
            try:
                ret = dis.get_instructions(clsdict[item])
            except TypeError:
                pass
            else:
                for i in ret:

                    if i.opname == 'LOAD_METHOD':
                        if i.argval not in methods:
                            methods.append(i.argval)
                    elif i.opname == 'LOAD_GLOBAL':
                        if i.argval not in attrs:
                            attrs.append(i.argval)

        if not ('SOCK_STREAM' in attrs and 'AF_INET' in attrs):
            raise TypeError('Некорректная инициализация сокета.')
        if name == 'Server':
            if 'connect' in methods:
                raise TypeError(
                    'Использование метода connect недопустимо в серверном классе')

        if name == 'Client':
            for command in ('accept', 'listen', 'socket'):
                if command in methods:
                    raise TypeError(
                        'В классе обнаружено использование запрещённого метода')

        print(f'Class {name} checked!')
        return type.__new__(cls, name, bases, clsdict)


class PortChecker:
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instanse, instanse_type):
        if instanse is None:
            return self
        return self._values.get(instanse, 0)

    def __set__(self, instance, value):
        if 0 <= value <= 65535 and type(value) == int:
            print(f"Port {value} checked!")
            self._values[instance] = value
        else:
            raise ValueError("Wrong por number!")
