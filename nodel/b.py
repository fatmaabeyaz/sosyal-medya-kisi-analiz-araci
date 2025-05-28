from simpletransformers.classification import ClassificationModel
import pandas as pd
import numpy as np
import os

def main():
    # Modeli yükle
    loaded_model = ClassificationModel(
        "bert", 
        "nodel/bert_model", 
        use_cuda=False, 
        num_labels=2,
        args={"local_files_only": True}  # Yerel model için
    )

    # Tahmin yap
    te = "Çok sinirliyim" #umarım geçmiş commiti kimse görmez :)
    ta = loaded_model.predict([te])
    print("Sonuç:", "eksi" if ta[0][0] == 0 else "artı")

if __name__ == "__main__":
    main()