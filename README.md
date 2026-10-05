# OpenChamber COPR packaging

This repository builds [OpenChamber](https://github.com/openchamber/openchamber)
from the upstream `v2.1.1` source tag for Fedora 44 x86_64. The spec installs
the RPM produced by OpenChamber's Electron build into the final COPR RPM.

After the GitHub Actions workflow completes, install it with:

```bash
sudo dnf copr enable ok8219/OpenChamber
sudo dnf install openchamber
```

## Publishing

The `Copr build` workflow creates the `OpenChamber` COPR project if it is
missing, then submits an SCM build for `fedora-44-x86_64`. Add these repository
secrets before triggering the workflow:

- `COPR_LOGIN`
- `COPR_TOKEN`
- `COPR_USERNAME` (normally `ok8219`)

Create the token at <https://copr.fedorainfracloud.org/api/>. The token user
must be permitted to create and manage the selected COPR project.

## Updating OpenChamber

Update `version` in `.copr/Makefile` and `Version` in `openchamber.spec` to
the same upstream release version, then push to `main`.
