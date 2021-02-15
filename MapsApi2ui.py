import sys
import requests
import pygame
import os

# Этот класс поможет нам сделать картинку из потока байт
from api_utils import get_degree_size, get_toponim, get_coords, show_map_pygame, show_map
from PyQt5 import QtWidgets
from PyQt5 import uic

Form, Window = uic.loadUiType("MapsApi1.ui")


class Ui(QtWidgets.QDialog, Form):
    def __init__(self):
        super(Ui, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.clickedbutton)
        self.setWindowTitle('Параметры для отображения карты')
                            
    def clickedbutton(self):
        self.params = all((self.lineEdit.text(), self.lineEdit_2.text()))
        
        running = True
        
        pygame.init()
        screen = pygame.display.set_mode((600, 450))
        
        k = 1.0
        
        func = True
        
        if self.params:
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            if k < 4.0:
                                k += 0.1
                                func = True
                        if event.key == pygame.K_DOWN:
                            if k > 1.0:
                                k -= 0.1
                                func = True
                # Пусть наше приложение предполагает запуск:
                # python search.py Москва, ул. Ак. Королева, 12
                # Тогда запрос к геокодеру формируется следующим образом:
                if func:
                    toponym_to_find = self.lineEdit.text()
                    
                    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
                    
                    geocoder_params = {
                        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
                        "geocode": toponym_to_find,
                        "format": "json"}
                    
                    response = requests.get(geocoder_api_server, params=geocoder_params)
                    
                    if not response:
                        # обработка ошибочной ситуации
                        pass
                    # Координаты центра топонима:
                    toponym_coodrinates = get_coords(toponym_to_find)
                    # Долгота и широта:
                    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
                    
                    # Собираем параметры для запроса к StaticMapsAPI:
                    map_params = {
                        "ll": ",".join([toponym_longitude, toponym_lattitude]),
                        'spn': ",".join([self.lineEdit_2.text(), self.lineEdit_2.text()]),
                        "scale": k,
                        "l": "map"
                    }
                    api_server = "http://static-maps.yandex.ru/1.x/"
                    response = requests.get(api_server, params=map_params)
                
                    if not response:
                        print("Ошибка выполнения запроса:")
                        sys.exit(1)
                
                    # Запишем полученное изображение в файл.
                    map_file = "map.png"
                    with open(map_file, "wb") as file:
                        file.write(response.content)
                    
                    screen.blit(pygame.image.load(map_file), (0, 0))
                    pygame.display.flip()
                    func = False
            pygame.quit()
            os.remove()
            self.lineEdit.clear()
            self.lineEdit_2.clear()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui()
    ex.show()
    sys.exit(app.exec())