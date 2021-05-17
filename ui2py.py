from PyQt5 import uic

# ServerSocketUI.py dosyası oluşturulur,
# mainWindow.ui dosyası oluşturulan .py dosyasına dönüştürülür.
with open("ServerSocketUI.py", "w",encoding = "utf-8",) as fout:
    uic.compileUi("mainWindow.ui",fout)