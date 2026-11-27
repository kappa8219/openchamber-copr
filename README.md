# OpenChamber COPR packaging

This repository publishes two x86_64 packages from OpenChamber to the
`OpenChamber` COPR project:

- `openchamber` repackages the official OpenChamber desktop RPM from GitHub
  Releases and verifies its SHA-256 checksum. Its original GUI launcher remains
  `/usr/bin/openchamber`.
- `openchamber-cli` packages the official `openchamber-web` release tarball and
  installs its production dependencies. It provides the separate
  `/usr/bin/openchamber-cli` command, so the server can run headlessly. It runs
  on the system Node.js 24 (`nodejs24` package, pulled in automatically); since
  OpenChamber 2.8.1 the web package bundles its own OpenCode server, so no
  separate OpenCode installation is required.

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

The CLI package requires Fedora's `nodejs24` package (Node.js 24.14 or newer),
which is installed automatically as a dependency. The OpenCode server is bundled
in the `openchamber-web` tarball since OpenChamber 2.8.1, so the CLI works
without a separate OpenCode install.
