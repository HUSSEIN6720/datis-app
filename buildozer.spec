[app]

title = داتیس
package.name = datis
package.domain = com.datis

version = 1.0.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
source.exclude_exts = spec,db

# ✅ درست: kivy
requirements = python3==3.10.11,kivy==2.1.0

orientation = portrait
fullscreen = 0

icon.filename = datis_logo_icon.png

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

android.api = 30
android.minapi = 21
android.ndk = 23b
android.sdk = 30

android.accept_sdk_license = True
android.allow_download = True

android.gradle_dependencies =

[buildozer]
log_level = 2
warn_on_root = 1
