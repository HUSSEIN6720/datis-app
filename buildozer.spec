[app]

title = داتیس
package.name = datis
package.domain = com.datis

version = 1.0.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.exclude_exts = spec,db

requirements = python3==3.9,kivy==2.0.0

orientation = portrait
fullscreen = 0

icon.filename = datis_logo_icon.png

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# ✅ تغییر API و NDK به نسخه‌های پشتیبانی‌شده
android.api = 30
android.minapi = 21
android.ndk = 28c
android.sdk = 30

android.accept_sdk_license = True
android.allow_download = True

# ✅ اضافه کردن این خط برای جلوگیری از خطای bootstrap
android.bootstrap = sdl2

android.gradle_dependencies =

[buildozer]
log_level = 2
warn_on_root = 1
