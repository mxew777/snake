[app]
title = Snake
package.name = snake
package.domain = org.snakegame

source.dir = .
source.include_exts = py

version = 1.0

requirements = python3,pygame

orientation = portrait
fullscreen = 1

android.permissions = VIBRATE
android.api = 33
android.minapi = 21
android.ndk = 25b

android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
