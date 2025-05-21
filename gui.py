import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTextEdit, QSpinBox, QMessageBox, QDialog, QInputDialog)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from data_moduls.veriÇekme03 import scrape_user_tweets
from data_moduls.nlp import analiz, toku

class ApiKeyDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("API Anahtarı Gerekli")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Açıklama metni
        label = QLabel("DeepSeek API anahtarınızı girin:")
        layout.addWidget(label)
        
        # API key giriş alanı
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.api_key_input)
        
        # Butonlar
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("Tamam")
        self.cancel_button = QPushButton("İptal")
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Buton bağlantıları
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
    
    def get_api_key(self):
        return self.api_key_input.text()

class WorkerThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    log = pyqtSignal(str)  # Yeni log sinyali
    
    def __init__(self, username, tweet_count):
        super().__init__()
        self.username = username
        self.tweet_count = tweet_count
        
    def run(self):
        try:
            # Veri çekme işlemi
            self.log.emit("Tweet'ler çekiliyor...")
            tweets = scrape_user_tweets(self.username, self.tweet_count)
            
            # JSON verisini hazırla
            self.log.emit("Tweet'ler işleniyor...")
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
            self.log.emit("Tweet'ler kaydediliyor...")
            yol = os.path.join(klasor_adi, f"{self.username}.json")
            with open(yol, "w", encoding="utf-8") as dosya:
                import json
                json.dump(json_data, dosya, ensure_ascii=False, indent=4)
            
            # NLP analizi yap
            self.log.emit("Kişilik analizi yapılıyor...")
            metinler = toku(yol)
            if metinler:
                analiz_sonucu = analiz(metinler)
                if analiz_sonucu:
                    self.finished.emit(analiz_sonucu)
                else:
                    self.error.emit("Analiz sırasında bir hata oluştu.")
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
        
        # Log alanı
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(100)
        layout.addWidget(self.log_text)
        
        # Sonuç alanı
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        
        # Durum çubuğu
        self.statusBar().showMessage("Hazır")
        
        # API key kontrolü
        self.check_api_key()
        
    def check_api_key(self):
        api_key_exists = os.path.exists("api_key.txt")
        api_key_valid = False
        
        if api_key_exists:
            with open("api_key.txt", "r") as f:
                api_key = f.read().strip()
                api_key_valid = bool(api_key)
        
        if not api_key_exists or not api_key_valid:
            dialog = ApiKeyDialog(self)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                api_key = dialog.get_api_key()
                if api_key:
                    with open("api_key.txt", "w") as f:
                        f.write(api_key)
                    self.log("API anahtarı kaydedildi.")
                else:
                    QMessageBox.warning(self, "Uyarı", "API anahtarı boş olamaz!")
                    self.check_api_key()
            else:
                QMessageBox.warning(self, "Uyarı", "API anahtarı olmadan analiz yapılamaz!")
                sys.exit()
    
    def log(self, message):
        self.log_text.append(message)
        print(message)  # Terminal'e de yazdır
        
    def start_analysis(self):
        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir kullanıcı adı girin!")
            return
            
        self.analyze_button.setEnabled(False)
        self.statusBar().showMessage("Analiz yapılıyor...")
        self.result_text.clear()
        self.log_text.clear()
        
        # Worker thread'i başlat
        self.worker = WorkerThread(username, self.tweet_count_input.value())
        self.worker.finished.connect(self.handle_results)
        self.worker.error.connect(self.handle_error)
        self.worker.log.connect(self.log)
        self.worker.start()
        
    def handle_results(self, results):
        self.result_text.setText(results)
        self.analyze_button.setEnabled(True)
        self.statusBar().showMessage("Analiz tamamlandı")
        self.log("Analiz tamamlandı!")
        
    def handle_error(self, error_message):
        QMessageBox.critical(self, "Hata", error_message)
        self.analyze_button.setEnabled(True)
        self.statusBar().showMessage("Hata oluştu")
        self.log(f"Hata: {error_message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec()) 