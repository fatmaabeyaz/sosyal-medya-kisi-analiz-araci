import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QLabel, QLineEdit, QPushButton, 
                            QTextBrowser, QSpinBox, QMessageBox, QDialog,
                            QFrame, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QTextCursor
import markdown
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

class StatusIndicator(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        
        # Ana layout
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # İndikatör kutusu
        self.indicator = QFrame()
        self.indicator.setFixedSize(20, 20)
        self.indicator.setFrameShape(QFrame.Shape.Box)
        self.indicator.setFrameShadow(QFrame.Shadow.Sunken)
        self.indicator.setStyleSheet("background-color: gray;")
        
        # Metin etiketi
        self.label = QLabel(text)
        self.label.setStyleSheet("color: #E0E0E0;")
        
        # Layout'a ekle
        layout.addWidget(self.indicator)
        layout.addWidget(self.label)
        layout.addStretch()
        
        self.setLayout(layout)
    
    def set_status(self, success):
        color = "green" if success else "gray"
        self.indicator.setStyleSheet(f"background-color: {color};")
        if success:
            self.label.setStyleSheet("color: #FFFFFF;")
        else:
            self.label.setStyleSheet("color: #E0E0E0;")

class WorkerThread(QThread):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    status_update = pyqtSignal(str, bool)
    progress_update = pyqtSignal(int)
    
    def __init__(self, username, tweet_count):
        super().__init__()
        self.username = username
        self.tweet_count = tweet_count
        
    def run(self):
        try:
            # Tweet'leri çek
            self.status_update.emit("tweet_cekme", False)
            self.progress_update.emit(10)
            tweets = scrape_user_tweets(self.username, self.tweet_count)
            
            if not tweets:
                self.error.emit("Tweet bulunamadı.")
                return
            
            # JSON verisini hazırla
            json_data = []
            total_tweets = len(tweets)
            for i, tweet in enumerate(tweets):
                progress = 20 + int((i / total_tweets) * 30)
                self.progress_update.emit(progress)
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
            
            # Dosyaya kaydet
            self.status_update.emit("tweet_cekme", True)
            self.status_update.emit("kaydetme", False)
            
            klasor_adi = "temp"
            if not os.path.exists(klasor_adi):
                os.makedirs(klasor_adi)
            
            yol = os.path.join(klasor_adi, f"{self.username}.json")
            with open(yol, "w", encoding="utf-8") as dosya:
                import json
                json.dump(json_data, dosya, ensure_ascii=False, indent=4)
            
            self.status_update.emit("kaydetme", True)
            
            # NLP analizi yap
            self.progress_update.emit(60)
            self.status_update.emit("api_baglanti", False)
            metinler = toku(yol)
            if not metinler:
                self.error.emit("Tweet'ler okunamadı.")
                return
            
            self.status_update.emit("api_baglanti", True)
            self.status_update.emit("api_cevap", False)
            
            self.progress_update.emit(80)
            analiz_sonucu = analiz(metinler)
            self.progress_update.emit(100)
            if analiz_sonucu:
                self.status_update.emit("api_cevap", True)
                self.finished.emit(analiz_sonucu)
            else:
                self.error.emit("Analiz sırasında bir hata oluştu.")
                
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
        
        # Üst kısım - yan yana yerleştirme
        top_layout = QHBoxLayout()
        
        # Kullanıcı adı girişi
        username_label = QLabel("Twitter Kullanıcı Adı:")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Kullanıcı adını girin (@ işareti olmadan)")
        top_layout.addWidget(username_label)
        top_layout.addWidget(self.username_input)
        
        # Tweet sayısı girişi
        tweet_count_label = QLabel("Tweet Sayısı:")
        self.tweet_count_input = QSpinBox()
        self.tweet_count_input.setRange(1, 100)
        self.tweet_count_input.setValue(10)
        top_layout.addWidget(tweet_count_label)
        top_layout.addWidget(self.tweet_count_input)
        
        # Analiz butonu
        self.analyze_button = QPushButton("Analiz Et")
        self.analyze_button.clicked.connect(self.start_analysis)
        top_layout.addWidget(self.analyze_button)
        
        # Üst kısmı ana layout'a ekle
        layout.addLayout(top_layout)
        
        # Durum göstergeleri
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.Shape.StyledPanel)
        status_layout = QVBoxLayout(status_frame)
        
        # Durum göstergeleri - yan yana yerleştirme
        status_indicators_layout = QHBoxLayout()
        self.tweet_status = StatusIndicator("Tweet çekme aşamasında")
        self.save_status = StatusIndicator("Tweet kaydetme aşamasında")
        self.api_conn_status = StatusIndicator("API bağlantı aşamasında")
        self.api_resp_status = StatusIndicator("API yanıt aşamasında")
        
        status_indicators_layout.addWidget(self.tweet_status)
        status_indicators_layout.addWidget(self.save_status)
        status_indicators_layout.addWidget(self.api_conn_status)
        status_indicators_layout.addWidget(self.api_resp_status)
        status_indicators_layout.addStretch()
        
        status_layout.addLayout(status_indicators_layout)
        layout.addWidget(status_frame)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Sonuç alanı
        self.result_text = QTextBrowser()
        self.result_text.setOpenExternalLinks(True)
        self.result_text.setStyleSheet("""
            QTextBrowser {
                background-color: #2C3E50;
                color: white;
                font-size: 12px;
                padding: 10px;
                border: 1px solid #BDC3C7;
            }
            QTextBrowser a {
                color: #3498DB;
            }
            QTextBrowser a:hover {
                color: #2980B9;
            }
        """)
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
                else:
                    QMessageBox.warning(self, "Uyarı", "API anahtarı boş olamaz!")
                    self.check_api_key()
            else:
                QMessageBox.warning(self, "Uyarı", "API anahtarı olmadan analiz yapılamaz!")
                sys.exit()
        
    def start_analysis(self):
        username = self.username_input.text().strip()
        if not username:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir kullanıcı adı girin!")
            return
            
        self.analyze_button.setEnabled(False)
        self.statusBar().showMessage("Analiz yapılıyor...")
        self.result_text.clear()
        
        # Durum göstergelerini sıfırla
        self.tweet_status.set_status(False)
        self.save_status.set_status(False)
        self.api_conn_status.set_status(False)
        self.api_resp_status.set_status(False)
        
        # Worker thread'i başlat
        self.worker = WorkerThread(username, self.tweet_count_input.value())
        self.worker.finished.connect(self.handle_results)
        self.worker.error.connect(self.handle_error)
        self.worker.status_update.connect(self.update_status)
        self.worker.progress_update.connect(self.progress_bar.setValue)
        self.worker.start()
    
    def update_status(self, status_type, success):
        if status_type == "tweet_cekme":
            self.tweet_status.label.setText("Tweet'ler çekildi" if success else "Tweet çekme aşamasında")
            self.tweet_status.set_status(success)
        elif status_type == "kaydetme":
            self.save_status.label.setText("Tweet'ler kaydedildi" if success else "Tweet kaydetme aşamasında")
            self.save_status.set_status(success)
        elif status_type == "api_baglanti":
            self.api_conn_status.label.setText("API bağlantısı kuruldu" if success else "API bağlantı aşamasında")
            self.api_conn_status.set_status(success)
        elif status_type == "api_cevap":
            self.api_resp_status.label.setText("API yanıtı alındı" if success else "API yanıt aşamasında")
            self.api_resp_status.set_status(success)
        
    def handle_results(self, results):
        # Markdown'ı HTML'e çevir
        html = markdown.markdown(results, extensions=['extra', 'codehilite'])
        # HTML'i göster
        self.result_text.setHtml(html)
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