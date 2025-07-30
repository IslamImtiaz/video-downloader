[app]
title = Video Downloader
package.name = videodownloader
package.domain = org.kivy.videodownloader
source.dir = .
source.include_exts = py,kv,png,jpg,ttf,txt,md
version = 1.0
requirements = python3,kivy==2.1.0,kivymd==1.1.1,yt-dlp,plyer
orientation = portrait
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b

[buildozer]
log_level = 2
warn_on_root = 1