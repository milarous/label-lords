# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Default dark mode interface with updated dark theme styling.
- Modernized responsive UI using a shared base template and card-based layout.
- Updated page flow and buttons for clearer navigation and gameplay actions.
- Redesigned home screen as a comprehensive dashboard with sidebar actions and main content displaying label overview and signed artists list.
- Made status information (current week and funds) persist in header across all game pages.
- Updated manage artist page navigation to return to main menu instead of signed artists page.
- Added persistent save/load support with 3 local save slots and slot metadata display on the dashboard.

## [0.1.0] - 2026-04-12

### Added
- Initial web release of the Label Lords record label management simulation.
- Migrated the app from a tkinter GUI to a Flask web application.
- Added HTML templates for browser-based gameplay.
- Added label setup and unsigned artist signing.
- Added signed artist management: promotion, single/album releases, and weekly revenue.
- Added revenue depreciation over time.
- Renamed the main application script from `cw3-clone.py` to `main.py`.
