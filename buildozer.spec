[app]

title = Snake Game
package.name = snakegame
package.domain = org.snakegame

source.dir = .
source.include_exts = py,png,jpg,jpeg,ttf,wav,mp3

version = 1.0

requirements = python3==3.10.12,hostpython3==3.10.12,sdl2,pygame==2.1.0,arabic-reshaper,python-bidi

orientation = portrait
fullscreen = 1

android.permissions = VIBRATE

android.api = 33
android.minapi = 21
android.ndk = 25b

android.accept_sdk_license = True

android.archs = armeabi-v7a,arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
