spec := ../openchamber-cli.spec
version := 2.3.2
node_version := 24.14.0
source := openchamber-web-$(version).tgz
source_url := https://github.com/openchamber/openchamber/releases/download/v$(version)/$(source)
node_source := node-v$(node_version)-linux-x64.tar.xz
node_source_url := https://nodejs.org/dist/v$(node_version)/$(node_source)
license_source := LICENSE-$(version)
license_source_url := https://raw.githubusercontent.com/openchamber/openchamber/v$(version)/LICENSE

.PHONY: srpm
srpm:
	curl --fail --location --output $(source) $(source_url)
	curl --fail --location --output $(node_source) $(node_source_url)
	curl --fail --location --output $(license_source) $(license_source_url)
	rpmbuild -bs --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)" $(spec)
