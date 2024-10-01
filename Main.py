import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from requests import RequestException


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.cityLabel = QLabel("Enter city name: ", self)
        self.cityInput = QLineEdit(self)
        self.getWeatherButton = QPushButton("Get Weather", self)
        self.temperatureLabel = QLabel(self)
        self.emojiLabel = QLabel(self)
        self.descriptionLabel = QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")
        vbox = QVBoxLayout()

        vbox.addWidget(self.cityLabel)
        vbox.addWidget(self.cityInput)
        vbox.addWidget(self.getWeatherButton)
        vbox.addWidget(self.temperatureLabel)
        vbox.addWidget(self.emojiLabel)
        vbox.addWidget(self.descriptionLabel)

        self.setLayout(vbox)

        self.cityLabel.setAlignment(Qt.AlignCenter)
        self.cityInput.setAlignment(Qt.AlignCenter)
        self.temperatureLabel.setAlignment(Qt.AlignCenter)
        self.emojiLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel.setAlignment(Qt.AlignCenter)

        self.cityLabel.setObjectName("cityLabel")
        self.cityInput.setObjectName("cityInput")
        self.getWeatherButton.setObjectName("getWeatherButton")
        self.temperatureLabel.setObjectName("temperatureLabel")
        self.emojiLabel.setObjectName("emojiLabel")
        self.descriptionLabel.setObjectName("descriptionLabel")

        self.setStyleSheet(""" 
            QLabel, QPushButton{
                 font-family: calibri;
            }
            QLabel#cityLabel{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#cityInput{ 
                font-size: 40px;
            }
            QPushButton#getWeatherButton{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperatureLabel{
                font-size: 75px;
            }
            QLabel#emojiLabel{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#descriptionLabel{
                font-size: 50px
            }
        """)

        self.getWeatherButton.clicked.connect(self.GetWeather)

    def GetWeather(self):
        apiKey = "5491fccc353c476f11303497aac7b167"
        city = self.cityInput.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.DisplayWeather(data)
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.DisplayError("Bad request\nPlease check your input")
                case 401:
                    self.DisplayError("Unauthorized\nInvalid API key")
                case 403:
                    self.DisplayError("Forbidden\nAccess id denied")
                case 404:
                    self.DisplayError("Not found\nCity not found")
                case 502:
                    self.DisplayError("Bad Gateway\nInvalid response from the server")
                case 500:
                    self.DisplayError("Internal Server Error\nPlease try again later")
                case 503:
                    self.DisplayError("Service Unavailable\nServer is down")
                case 504:
                    self.DisplayError("Gateway Timeout\nNo response form the server")
                case _:
                    self.DisplayError(f"HTTP error occurred\n{http_error}")

        except requests.exceptions.ConnectionError:
            self.DisplayError("Connection Error:\nCheck your internet connection")

        except requests.exceptions.Timeout:
            self.DisplayError("Timeout Error:\nThe request timeout")

        except requests.exceptions.TooManyRedirects:
            self.DisplayError("Too many Redirects:\nCheck the URL")

        except requests.exceptions.RequestException as req_error:
            self.DisplayError(f"Request Error:\n{req_error}")





    def DisplayError(self, message):
        self.temperatureLabel.setStyleSheet("font-size: 30px")
        self.temperatureLabel.setText(message)
        self.emojiLabel.clear()
        self.descriptionLabel.clear()

    def DisplayWeather(self, data):
        self.temperatureLabel.setStyleSheet("font-size: 75px")
        temperatureK =  data["main"]["temp"]
        temperatureC = temperatureK - 273.15
        weatherID = data["weather"][0]["id"]
        weatherDescription = data["weather"][0]["description"]

        self.temperatureLabel.setText(f"{temperatureC:.0f}°C")
        self.emojiLabel.setText(self.GetWeatherEmoji(weatherID))
        self.descriptionLabel.setText(weatherDescription)

    @staticmethod
    def GetWeatherEmoji(weather_id):

        if 200<= weather_id <= 232:
            return "⛈️"
        elif 300<= weather_id <= 321:
            return "🌦️"
        elif 500<= weather_id <= 531:
            return "🌧️"
        elif 600<= weather_id <= 622:
            return "🌨️"
        elif 701<= weather_id <= 741:
            return "🌫️"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪️"
        elif weather_id == 800:
            return "🌞"
        elif 801 <= weather_id <= 804:
            return "☁️"
        else:
            return ""


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weatherApp = WeatherApp()
    weatherApp.show()
    sys.exit(app.exec_())
