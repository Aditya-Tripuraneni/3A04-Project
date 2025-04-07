# SongSnap Desktop

This is the desktop version of SongSnap, built using React Native Expo and Tauri.

## Prerequisites

- Node.js 18+ and npm
- Rust (stable channel) - [Install Rust](https://www.rust-lang.org/tools/install)
- Platform-specific dependencies:
  - **Windows**: Microsoft Visual C++ Build Tools
  - **macOS**: Xcode Command Line Tools
  - **Linux**: `libgtk-3-dev`, `libwebkit2gtk-4.0-dev`, `libappindicator3-dev`, `librsvg2-dev`, `patchelf`

## Development Setup

1. Install dependencies:

```bash
# Install npm dependencies
npm install

# Install Tauri CLI
npm install --save-dev @tauri-apps/cli
```

2. Run development server:

```bash
# Start Expo web server
npm run web

# In another terminal, start Tauri development
npm run tauri dev
```

## Building for Production

```bash
# Build for production
npm run build
npm run tauri build
```

## Project Structure

- `/app`: Expo Router-based application
- `/src-tauri`: Tauri desktop application configuration
- `/assets`: Application assets
- `/components`: Shared React components

## CI/CD

This project uses GitHub Actions for CI/CD:

- Pull Request validation: Runs type-checking and tests
- Main branch: Builds the application for all platforms
- Tags: Creates GitHub releases with installable binaries

## License

No License