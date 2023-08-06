from PyQt5.QtWidgets import QApplication
import sys
import WeatherAppGUI  

def main():           
    app = QApplication(sys.argv)
    out = WeatherAppGUI.Window(app)
    out.show()
    app.exec_()  

if __name__ == "__main__":
          main()