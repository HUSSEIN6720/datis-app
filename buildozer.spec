[app]

# نام برنامه (همون اسمی که روی گوشی میبینی)
title = داتیس

# نام پکیج (یکتا باشه)
package.name = datis

# دامنه (میتونی هر چی دوست داری بذاری)
package.domain = com.datis

# ورژن برنامه
version = 1.0.0

# فرمت ورژن
version.regex = (\d+\.\d+\.\d+)

# فایل اصلی
source.dir = .

# پسوند فایل‌هایی که باید شامل بشن
source.include_exts = py,png,jpg,kv,atlas,json

# فایل‌هایی که نباید شامل بشن
source.exclude_exts = spec,db

# وابستگی‌ها
requirements = python3==3.10.11,kivy==2.2.1

# جهت صفحه
orientation = portrait

# تمام صفحه
fullscreen = 0

# آیکون برنامه (یه فایل PNG بذار توی پوشه)
# icon.filename = icon.png

# مجوزهای اندروید
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# API اندروید
android.api = 33
android.minapi = 21

# SDK و NDK
android.ndk = 23b
android.sdk = 33

# Gradle
android.gradle_dependencies =

# بیلدوزر
[buildozer]
log_level = 2
warn_on_root = 1
