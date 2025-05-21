import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTextEdit, QSpinBox, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from data_moduls.veriÇekme03 import scrape_user_tweets
from data_moduls.nlp import analiz, toku

class WorkerThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, username, tweet_count):
        super().__init__()
        self.username = username
        self.tweet_count = tweet_count
        
    def run(self):
        try:
            # Veri çekme işlemi
            tweets = scrape_user_tweets(self.username, self.tweet_count)
            
            # JSON verisini hazırla
            json_data = []
            for tweet in tweets:
                idu = tweet['url'].split("/")[-1]
                json_data.append({
                    "id": idu,
                    "datetime": tweet['datetime'],
                    "tweet": tweet['text'],
                    "likes": tweet['likes'],
                    "retweets": tweet['retweets'],
                    "replies": tweet['replies'],
                    "url": tweet['url']
                })
            
            # Geçici klasör oluştur
            klasor_adi = "temp"
            if not os.path.exists(klasor_adi):
                os.makedirs(klasor_adi)
            
            # Dosyaya kaydet
            yol = os.path.join(klasor_adi, f"{self.username}.json")
            with open(yol, "w", encoding="utf-8") as dosya:
                import json
                json.dump(json_data, dosya, ensure_ascii=False, indent=4)
            
            # NLP analizi yap
            metinler = toku(yol)
            if metinler:
                analiz_sonucu = analiz(metinler)
                self.finished.emit(analiz_sonucu)
            else:
                self.error.emit("Tweet bulunamadı.")
                
        except Exception as e:
            self.error.emit(f"Bir hata oluştu: {str(e)}")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sosyal Medya Kişi Analiz Aracı")
        self.setMinimumSize(800, 600)
        
        # Ana widget ve layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Kullanıcı adı girişi
        username_layout = QHBoxLayout()
        username_label = QLabel("Twitter Kullanıcı Adı:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adını girin (@ işareti olmadan)")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # Tweet sayısı girişi
        tweet_count_layout = QHBoxLayout()
        tweet_count_label = QLabel("Analiz Edilecek Tweet Sayısı:")
        self.tweet_count_input = QSpinBox()
        self.tweet_count_input.setRange(1, 100)
        self.tweet_count_input.setValue(10)
        tweet_count_layout.addWidget(tweet_count_label)
        tweet_count_layout.addWidget(self.tweet_count_input)
        layout.addLayout(tweet_count_layout)
        
        # Analiz butonu
        self.analyze_button = QPushButton("Analiz Et")
        self.analyze_button.clicked.connect(self.start_analysis)
        layout.addWidget(self.analyze_button)
        
        # Sonuç alanı
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        
        # Durum çubuğu
        self.statusBar().showMessage("Hazır")
        
    def start_analysis(self):
        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir kullanıcı adı girin!")
            return
            
        self.analyze_button.setEnabled(False)
        self.statusBar().showMessage("Analiz yapılıyor...")
        self.result_text.clear()
        
        # Worker thread'i başlat
        self.worker = WorkerThread(username, self.tweet_count_input.value())
        self.worker.finished.connect(self.handle_results)
        self.worker.error.connect(self.handle_error)
        self.worker.start()
        
    def handle_results(self, results):
        self.result_text.setText(results)
        self.analyze_button.setEnabled(True)
        self.statusBar().showMessage("Analiz tamamlandı")
        
    def handle_error(self, error_message):
        QMessageBox.critical(self, "Hata", error_message)
        self.analyze_button.setEnabled(True)
        self.statusBar().showMessage("Hata oluştu")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 