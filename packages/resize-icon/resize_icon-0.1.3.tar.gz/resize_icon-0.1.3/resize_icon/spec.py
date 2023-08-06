# spec format in dictionary:
# {
#   'size'                  : int,
#   'should_remove_alpha'   : bool,
#   'should_crop_to_rounded': bool,
#   'crop_height'           : Optional[int],
# }

icon_spec = {
    "ios": {
        "AppIcon.appiconset": {
            "Icon-App-20x20@1x.png": {
                "size": 20,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-App-20x20@2x.png": {
                "size": 40,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-App-20x20@3x.png": {
                "size": 60,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-App-29x29@1x.png": {
                "size": 29,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-App-29x29@2x.png": {
                "size": 58,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-App-29x29@3x.png": {
                "size": 87,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-App-40x40@1x.png": {
                "size": 40,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-App-40x40@2x.png": {
                "size": 80,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-App-40x40@3x.png": {
                "size": 120,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-App-60x60@2x.png": {
                "size": 120,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-App-60x60@3x.png": {
                "size": 180,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-App-76x76@1x.png": {
                "size": 76,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-App-76x76@2x.png": {
                "size": 152,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-App-83.5x83.5@2x.png": {
                "size": 167,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "ItunesArtwork@2x.png": {
                "size": 1024,
                "should_remove_alpha": True,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
        },
        # iTunes artwork
        "iTunesArtwork@1x.png": {
            "size": 512,
            "should_remove_alpha": True,
            "should_crop_to_rounded": False,
            "crop_height": None,
        },
        "iTunesArtwork@2x.png": {
            "size": 1024,
            "should_remove_alpha": True,
            "should_crop_to_rounded": False,
            "crop_height": None,
        },
        "iTunesArtwork@3x.png": {
            "size": 1536,
            "should_remove_alpha": True,
            "should_crop_to_rounded": False,
            "crop_height": None,
        },
    },
    "imessenger": {
        "icon-messages-app-27x20@1x.png": {
            "size": 27,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 20,
        },
        "icon-messages-app-27x20@2x.png": {
            "size": 54,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 40,
        },
        "icon-messages-app-27x20@3x.png": {
            "size": 81,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 60,
        },
        "icon-messages-app-iPadAir-67x50@2x.png": {
            "size": 134,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 100,
        },
        "icon-messages-app-iPadAir-74x55@2x.png": {
            "size": 148,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 110,
        },
        "icon-messages-app-iPhone-60x45@1x.png": {
            "size": 60,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 45,
        },
        "icon-messages-app-iPhone-60x45@2x.png": {
            "size": 120,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 90,
        },
        "icon-messages-app-iPhone-60x45@3x.png": {
            "size": 180,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 135,
        },
        "icon-messages-settings-29x29@2x.png": {
            "size": 58,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 58,
        },
        "icon-messages-settings-29x29@3x.png": {
            "size": 87,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 87,
        },
        "icon-messages-transcript-32x24@1x.png": {
            "size": 32,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 24,
        },
        "icon-messages-transcript-32x24@2x.png": {
            "size": 64,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 48,
        },
        "icon-messages-transcript-32x24@3x.png": {
            "size": 96,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 72,
        },
        "icon-messages-app-store-1024x1024.png": {
            "size": 1024,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 1024,
        },
        "icon-messages-app-store-1024x768.png": {
            "size": 1024,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": 768,
        },
    },
    "watchkit": {
        "AppIcon.appiconset": {
            # WatchKit Notification Center icon
            "Icon-24@2x.png": {
                "size": 48,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-27.5@2x.png": {
                "size": 55,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            # WatchKit Long-Look notification icon
            "Icon-40@2x.png": {
                "size": 80,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-44@2x.png": {
                "size": 88,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-50@2x.png": {
                "size": 100,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            # WatchKit App icon
            "Icon-29@2x.png": {
                "size": 58,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-29@3x.png": {
                "size": 87,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            # WatchKit Short-Look icon
            "Icon-86@2x.png": {
                "size": 172,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-98@2x.png": {
                "size": 196,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "Icon-108@2x.png": {
                "size": 216,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "ItunesArtwork@2x.png": {
                "size": 1024,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
        }
    },
    "android": {
        # TODO: Keep this? Android docs says it is resized by the system
        "mipmap-mdpi": {
            "ic_launcher.png": {
                "size": 48,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "ic_launcher_foreground.png": {
                "size": 108,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "ic_launcher_round.png": {
                "size": 48,
                "should_remove_alpha": False,
                "should_crop_to_rounded": True,
                "crop_height": None,
            },
        },
        "mipmap-hdpi": {
            "ic_launcher.png": {
                "size": 72,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "ic_launcher_foreground.png": {
                "size": 162,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "ic_launcher_round.png": {
                "size": 72,
                "should_remove_alpha": False,
                "should_crop_to_rounded": True,
                "crop_height": None,
            },
        },
        "mipmap-xhdpi": {
            "ic_launcher.png": {
                "size": 96,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "ic_launcher_foreground.png": {
                "size": 216,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "ic_launcher_round.png": {
                "size": 96,
                "should_remove_alpha": False,
                "should_crop_to_rounded": True,
                "crop_height": None,
            },
        },
        "mipmap-xxhdpi": {
            "ic_launcher.png": {
                "size": 144,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "ic_launcher_foreground.png": {
                "size": 324,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "ic_launcher_round.png": {
                "size": 144,
                "should_remove_alpha": False,
                "should_crop_to_rounded": True,
                "crop_height": None,
            },
        },
        "mipmap-xxxhdpi": {
            "ic_launcher.png": {
                "size": 192,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "ic_launcher_foreground.png": {
                "size": 432,
                "should_remove_alpha": False,
                "should_crop_to_rounded": False,
                "crop_height": None,
            },
            "ic_launcher_round.png": {
                "size": 192,
                "should_remove_alpha": False,
                "should_crop_to_rounded": True,
                "crop_height": None,
            },
        },
        "playstore-icon.png": {
            "size": 512,
            "should_remove_alpha": False,
            "should_crop_to_rounded": False,
            "crop_height": None,
        },
    },
}
