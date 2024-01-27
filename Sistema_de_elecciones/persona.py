class Persona:
    def __init__(self, ci, nombre, fechaN, genero):
        self.__ci = ci
        self.__nombre = nombre
        self.__fechaN = fechaN
        self.__genero = genero
    
    def get_ci(self):
        return self.__ci
    def get_nombre(self):
        return self.__nombre

    def get_fecha_nacimiento(self):
        return self.__fechaN
    def get_genero(self):
        return self.__genero
    
    def set_ci(self, ci):
        self.__ci = ci
    def set_nombre(self, nombre):
        self.__nombre = nombre

    def set_fecha_nacimiento(self, fechaN):
        self.__fechaN = fechaN 
    def set__genero(self, genero):
        self.__genero = genero