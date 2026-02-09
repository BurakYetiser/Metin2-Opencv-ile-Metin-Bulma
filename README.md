# Metin2-Opencv-ile-Metin-Bulma
Bu bot, OpenCV tabanlı görüntü işleme kullanılarak geliştirilmiştir. Oyun içi belleğe veya packet yapısına müdahale etmeden, tamamen görsel tanıma üzerinden çalışır.

Ekrandaki Metin Taşı isimlerini (nameplate) algılar, karakterin konumuna göre en uygun hedefi seçer ve imleci otomatik olarak hedef üzerinde sabitler. Metin yokken belirlenen tarama bölgelerinde bekleyerek yeni hedefleri aramaya devam eder.

# Metin Ekleme
Dosyalarda gördüğünüz .jpg uzantılı fotoğraflara uygun şekilde istediğiniz metinin fotoğrafını çekin ve koyun. Koyduğunuz fotoğrafın adı neyse main'in içindeki TEMPLATES = [ ] kısmının içine koddaki gibi yazın.


# Özellikler
OpenCV matchTemplate kullanımı
Metin taşı isimleri, referans görseller (nameplate) üzerinden algılanır.

Çoklu nameplate desteği
Birden fazla metin türü (nameplate1, nameplate2, vb.) aynı anda taranabilir.

Gerçek hedef kilitleme sistemi
Bir metne kilitlenildiğinde, metin yok olana kadar hedef değiştirilmez.
Mob isimleri veya geçici yazılar kilidi bozmaz.

HUD / üst yazı filtreleme (ROI)
Görev, sistem mesajları ve üst HUD alanı tarama dışında bırakılarak yanlış algılamalar engellenir.

Stabil imleç kontrolü
Deadzone, smoothing ve clamp mekanizmaları ile imleç titremesi ve yukarı kayma sorunları giderilmiştir.

Dinamik tarama davranışı
Metin bulunamadığında imleç:
-üst bölgede belirli süre bekler
-ardından alt bölgeye geçerek taramaya devam eder

Macro / Autohotkey
Bot yalnızca imleç konumlandırır; tıklama işlemi donanımsal makrolarla birleştirilebilir.

Yönetici mod uyumlu
Launcher üzerinden başlatılan oyunlarda dahi stabil çalışacak şekilde tasarlanmıştır.

# Kullanılan Teknolojiler
-Python 3
-OpenCV
-NumPy
-MSS (ekran yakalama)
-Win32 API (imleç kontrolü)

# ⚠️ Not
Bu proje görüntü işleme pratiği amacıyla geliştirilmiştir.
Bu proje python 3.11.9'la uyumlu çalışacak şekilde yazılmıştır.
