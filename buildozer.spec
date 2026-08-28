[app]

title = داتیس
package.name = datis
package.domain = com.datis

version = 1.0.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.exclude_exts = spec,db

requirements = python3==3.10.11,kivy==2.2.1

orientation = portrait
fullscreen = 0

icon.filename = datis_logo_icon.png

# مجوزهای اندروید
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# ✅ تغییر API به نسخه 30
android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30

# ✅ قبول خودکار مجوزها
android.accept_sdk_license = True

android.gradle_dependencies =

[buildozer]
log_level = 2
warn_on_root = 1
