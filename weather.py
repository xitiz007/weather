from PyQt5.Qt import QWidget,QIcon,QApplication,QLabel,QLineEdit,QPushButton,QVBoxLayout,QHBoxLayout,Qt,QErrorMessage,QFileDialog
import requests
from datetime import datetime
import csv

weather_url = 'http://api.openweathermap.org/data/2.5/weather?appid=f58bec06b3c5a756d555011589fa63d3&units=metric&q='
class Weather(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Weather')
        self.setWindowIcon(QIcon('umbrella.png'))
        self.resize(300,120)
        self.ui()
        self.show()

    def ui(self):
        vbox = QVBoxLayout()
        title = QLabel()
        title.setText('Weather')
        title.setStyleSheet('font: 20pt')
        title.setAlignment(Qt.AlignCenter)
        vbox.addWidget(title)
        hbox = QHBoxLayout()
        label = QLabel()
        label.setText('City Name:')
        label.setStyleSheet('font: 15px')
        self.textLine = QLineEdit()
        self.textLine.setMinimumHeight(30)
        hbox.addWidget(label)
        hbox.addWidget(self.textLine)
        vbox.addItem(hbox)
        button = QPushButton()
        button.setText('Search')
        button.setStyleSheet('font: 15px')
        button.setMinimumHeight(30)
        button.clicked.connect(self.checkText)
        vbox.addWidget(button)
        self.setLayout(vbox)

    def checkText(self):
        if not self.textLine.text().isalpha():
            message = QErrorMessage(self)
            message.showMessage('Invalid Entry! Try Again.')
            message.setWindowTitle('Warning')
            message.setWindowIcon(QIcon('error.png'))
        else:
            location = self.textLine.text()
            url = weather_url + location
            global json
            json = requests.get(url).json()
            try:
                json['message']
            except Exception:
                self.obj = ShowWeather()
            else:
                message = QErrorMessage(self)
                message.showMessage('Invalid City Name! Try Again.')
                message.setWindowTitle('Warning')
                message.setWindowIcon(QIcon('error.png'))

class ShowWeather(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon('umbrella.png'))
        self.setWindowTitle('Weather')
        self.content()
        self.show()

    def content(self):
        main = json['weather'][0]['main']
        description = json['weather'][0]['description']
        current_temp = json['main']['temp']
        temp_min = json['main']['temp_min']
        temp_max = json['main']['temp_max']
        country = json['sys']['country']
        sunrise = json['sys']['sunrise']
        sunset = json['sys']['sunset']
        sunrise = datetime.fromtimestamp(sunrise).time().strftime('%I:%M %p')
        sunset = datetime.fromtimestamp(sunset).time().strftime('%I:%M %p')
        global fields
        fields = [{'main': main}, {'description': description}, {'current_temp': current_temp}, {'temp_min': temp_min},
                  {'temp_max': temp_max}, {'country': country}, {'sunrise': sunrise}, {'sunset': sunset}]

        vbox = QVBoxLayout()
        headinglabel = QLabel()
        headinglabel.setText('Weather')
        headinglabel.setStyleSheet('font: 20pt')
        headinglabel.setAlignment(Qt.AlignCenter)
        vbox.addWidget(headinglabel)

        mainLabel = QLabel()
        mainLabel.setText(f'Main: {main}')
        vbox.addWidget(mainLabel)

        descriptionLabel = QLabel()
        mainLabel.setText(f'Description: {description}')
        vbox.addWidget(descriptionLabel)

        current_tempLabel = QLabel()
        current_tempLabel.setText(f'Current Temperature: {current_temp}')
        vbox.addWidget(current_tempLabel)

        temp_minLabel = QLabel()
        temp_minLabel.setText(f'Minimum Temperature: {temp_min}')
        vbox.addWidget(temp_minLabel)

        temp_maxLabel = QLabel()
        temp_maxLabel.setText(f'Maximum Temperature: {temp_max}')
        vbox.addWidget(temp_maxLabel)

        sunriseLabel = QLabel()
        sunriseLabel.setText(f'Sunrise: {sunrise}')
        vbox.addWidget(sunriseLabel)

        sunsetLabel = QLabel()
        sunsetLabel.setText(f'Sunset: {sunset}')
        vbox.addWidget(sunsetLabel)

        countryLabel = QLabel()
        countryLabel.setText(f'Country: {country}')
        vbox.addWidget(countryLabel)

        button = QPushButton()
        button.setText('Save in Csv file')
        button.setStyleSheet('color:blue')
        button.clicked.connect(self.linked)
        vbox.addWidget(button)

        self.setLayout(vbox)

    def linked(self):
        filter = "CSV (*.csv)"
        fileName = QFileDialog.getSaveFileName(self, "Save Image", filter=filter)
        if fileName[0]:
            self.save(fileName[0])

    def save(self,path):
        with open(path, 'w',newline='') as file:
            writer = csv.writer(file, delimiter=',')
            for field in fields:
                for key in field.keys():
                    writer.writerow([key, field[key]])


app = QApplication([])
obj = Weather()
app.exec_()
