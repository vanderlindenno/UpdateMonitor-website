# Android app UpdateMonitor – website

Source of **[updatemonitor.app](https://updatemonitor.app/)**, the website of **UpdateMonitor**, a privacy-first Android app that keeps a history of every app update, install and removal on your phone.

## About the app

- History of app updates, installs and removals, with a calendar view
- Overview of which apps can use sensitive permissions such as camera, microphone and location
- Warnings about newly granted permissions and apps installed from outside the Play Store
- Export for IT support
- Free, no ads, no account, no internet permission. All data stays on the device.
- Available in English and Norwegian

The Android app is on its way to Google Play. Made by Nordic Appworks, who also make [RebootMonitor](https://rebootmonitor.com/).

## Pages

| Page | Topic |
|------|-------|
| [Home](https://updatemonitor.app/) | Overview, screenshots, FAQ |
| [Norsk](https://updatemonitor.app/no/) | Norwegian homepage |
| [Guides](https://updatemonitor.app/guides/) | How-to guides |
| [Android app permissions](https://updatemonitor.app/guides/android-app-permissions.html) | See which apps can use what |
| [Android app update history](https://updatemonitor.app/guides/android-app-update-history.html) | Find when an app was last updated |
| [Apps outside the Play Store](https://updatemonitor.app/guides/find-apps-outside-play-store.html) | Spot sideloaded apps |
| [Privacy policy](https://updatemonitor.app/privacy.html) | What the app and the website do with data |

## About this repository

A plain static website hosted on GitHub Pages, without analytics or tracking. After a push that changes pages, two GitHub Actions update `lastmod` in `sitemap.xml` and notify Bing about the changed pages.

Found an error on the site? Please [open an issue](https://github.com/vanderlindenno/UpdateMonitor-website/issues).

© 2026 Nordic Appworks. All rights reserved.
