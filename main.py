from PyQt5.QtCore import QUrl, Qt, QEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QGridLayout, QWidget, QHBoxLayout, QVBoxLayout, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Web Browser')
        self.setGeometry(100, 100, 1200, 800)

        # Create the QWebEngineView and QVideoWidget
        self.view = QWebEngineView(self)
        self.videoWidget = QVideoWidget(self)
        self.videoWidget.hide()

        # Create the main layout and add the QWebEngineView and QVideoWidget to it
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.videoWidget)
        mainWidget = QWidget(self)
        mainWidget.setLayout(layout)
        self.setCentralWidget(mainWidget)

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

        # Connect the loadFinished signal of the QWebEngineView to a custom slot
        self.view.loadFinished.connect(self.onLoadFinished)

        # Create an instance of QMediaPlayer and set the QVideoWidget as the video output
        self.mediaPlayer = QMediaPlayer(self)
        self.videoWidget.setMediaObject(self.mediaPlayer)

        # Create a flag to track whether a video is being played or not
        self.isPlaying = False

    def onLoadFinished(self):
        # Check if the page contains any video elements
        self.view.page().runJavaScript("""
            var videos = document.getElementsByTagName('video');
            if (videos.length > 0) {
                window.hasVideos = true;
            } else {
                window.hasVideos
                }
        """, self.onJavaScriptResult)

    def onJavaScriptResult(self, result):
        # If the page has videos, try to play each one until a successful playback is achieved
        if result:
            self.view.page().runJavaScript("""
                var videos = document.getElementsByTagName('video');
                var sources = [];
                for (var i = 0; i < videos.length; i++) {
                    for (var j = 0; j < videos[i].children.length; j++) {
                        var source = videos[i].children[j];
                        if (source.type == 'video/mp4') {
                            sources.push(source.src);
                        }
                    }
                }
                window.videoSources = sources;
            """, self.onVideoSources)

    def onVideoSources(self, sources):

        # Set the sources list as the current playlist of the QMediaPlayer and try to play the first video
        self.mediaPlayer.setPlaylist(sources)
        self.mediaPlayer.play()
        self.isPlaying = True

        # Connect the mediaStatusChanged signal of the QMediaPlayer to a custom slot
        self.mediaPlayer.mediaStatusChanged.connect(self.onMediaStatusChanged)

        # Show the QVideoWidget and hide the QWebEngineView
        self.videoWidget.show()
        self.view.hide()


    def tryPlayVideo(self, result):
        sources = result
        for src in sources:
            self.mediaPlayer.setCurrentSource(Phonon.MediaSource(url))
            if self.mediaPlayer.error() == QMediaPlayer.NoError:
                self.videoWidget.show()
                self.mediaPlayer.play()
                self.isPlaying = True
                break

    def onVideoPlayed(self, result):
        # Connect the mediaStatusChanged signal of the QMediaPlayer to a custom slot
        self.mediaPlayer.mediaStatusChanged.connect(self.onMediaStatusChanged)

    def onMediaStatusChanged(self, status):
        # If the playback of the current video has finished, try to play the next video
        if status == QMediaPlayer.EndOfMedia:
            index = self.mediaPlayer.currentIndex() + 1
            if index < self.mediaPlayer.playlist().mediaCount():
                self.mediaPlayer.setCurrentIndex(index)
                self.mediaPlayer.play()
            else:
                self.isPlaying = False
                self.mediaPlayer.stop()
                self.videoWidget.hide()
                self.view.show()
            
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
        visitedWebsites = ['https://en.wikipedia.org/wiki/Main_Page', 'https://www.google.de/',
                               'https://www.youtube.com/']
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