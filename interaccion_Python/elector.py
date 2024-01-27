from persona import Persona
class Elector(Persona):
    def __init__(self, ci, nombre, fechaN, genero,estado):
        super().__init__(ci, nombre, fechaN, genero)
        self.__estado = estado

    def get_estado(self):
        if self.__estado==True:
            self.__estado = "Habilitado"
        else:
            self.__estado= "Inabilitado"
        return self.__estado

    def set_estado(self, estado):
        self.__estado = estado

    def votar(self):
        self.__estado = 'Inactivo'