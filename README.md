# OpenChamber COPR packaging

This repository publishes two x86_64 packages from OpenChamber to the
`OpenChamber` COPR project:

- `openchamber` repackages the official OpenChamber desktop RPM from GitHub
  Releases and verifies its SHA-256 checksum. Its original GUI launcher remains
  `/usr/bin/openchamber`.
- `openchamber-cli` packages the official `openchamber-web` release tarball,
  installs its production dependencies, and bundles Node.js 24.22.1. It provides
  the separate `/usr/bin/openchamber-cli` command, so the server can run
  headlessly and does not depend on the host's Node version.

Both packages are built for Fedora 43, 44, 45, and Rawhide x86_64.

Install the desktop app:

```bash
sudo dnf copr enable ok8219/OpenChamber
sudo dnf install openchamber
```

Install the CLI/web server:

```bash
sudo dnf install openchamber-cli
openchamber-cli serve --api-only --port 3000 --lan --ui-password 'choose-a-password'
```

The CLI package bundles Node.js 24.22.1, so it does not use the host's Node.js
22. OpenCode itself is not bundled with this web CLI; install the OpenCode CLI
separately and ensure it is available on `PATH`.
