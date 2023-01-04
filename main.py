from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QGridLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Web Browser')
        self.setGeometry(100, 100, 1200, 800)

        self.view = QWebEngineView(self)
        self.setCentralWidget(self.view)

        # Create a QLineEdit widget and add it to a toolbar
        # at the top of the main window
        self.searchBar = QLineEdit(self)
        toolbar = self.addToolBar('')
        toolbar.addWidget(self.searchBar)

        # Connect the returnPressed signal of the search bar to a custom slot
        self.searchBar.returnPressed.connect(self.onSearch)

        # Add a back button and connect its clicked signal to the back method
        self.backButton = QPushButton('Back', self)
        toolbar.addWidget(self.backButton)
        self.backButton.clicked.connect(self.view.back)

        # Add a forward button and connect its clicked signal to the forward method
        self.forwardButton = QPushButton('Forward', self)
        toolbar.addWidget(self.forwardButton)
        self.forwardButton.clicked.connect(self.view.forward)

        # Add a refresh button and connect its clicked signal to the reload method
        self.refreshButton = QPushButton('Refresh', self)
        toolbar.addWidget(self.refreshButton)
        self.refreshButton.clicked.connect(self.view.reload)

        # Add a home button and connect its clicked signal to the showHomePage method
        self.homeButton = QPushButton('Home', self)
        toolbar.addWidget(self.homeButton)
        self.homeButton.clicked.connect(self.showHomePage)

        # Create an instance of the HomePage class
        self.homePage = HomePage(self)

    def load(self, url):
        self.view.load(QUrl(url))

    def onSearch(self):
        # Get the text from the search bar and use it as the URL
        url = self.searchBar.text()
        self.load(url)

    def showHomePage(self):
        # Show the home page widget and hide the browser view
        self.view.hide()
        self.homePage.show()


class HomePage(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.browser = parent
        self.initUI()

    def initUI(self):
        # Create a grid layout and set it as the layout for the home page widget
        grid = QGridLayout()
        self.setLayout(grid)

        # Add a button for each visited website
        visitedWebsites = ['https://en.wikipedia.org/wiki/Main_Page', 'https://www.google.de/', 'https://www.youtube.com/']
        row = 0
        col = 0
        for website in visitedWebsites:
            button = QPushButton(website, self)
            button.clicked.connect(lambda checked, url=website: self.onButtonClick(url))
            grid.addWidget(button, row, col)
            col += 1
            if col >= 3:
                col = 0
                row += 1

    def onButtonClick(self, url):
        # Load the clicked website in the main browser window
        self.browser.load(url)
        self.browser.view.show()
        self.hide()

def main():
    app = QApplication([])
    browser = Browser()
    browser.showHomePage()
    browser.show()
    app.exec_()

if __name__ == '__main__':
    main()

