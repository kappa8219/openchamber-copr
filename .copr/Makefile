spec ?= ../openchamber.spec
version := 2.4.0
node_version := 24.14.0
node_source := node-v$(node_version)-linux-x64.tar.xz
license_source := LICENSE-$(version)

ifeq ($(notdir $(spec)),openchamber-cli.spec)
source := openchamber-web-$(version).tgz
source_url := https://github.com/openchamber/openchamber/releases/download/v$(version)/$(source)
node_source_url := https://nodejs.org/dist/v$(node_version)/$(node_source)
license_source_url := https://raw.githubusercontent.com/openchamber/openchamber/v$(version)/LICENSE
web_sources := curl --fail --location --output $(node_source) $(node_source_url) && curl --fail --location --output $(license_source) $(license_source_url)
else
source := OpenChamber-$(version)-linux-x86_64.rpm
source_url := https://github.com/openchamber/openchamber/releases/download/v$(version)/$(source)
web_sources := true
endif

.PHONY: srpm
srpm:
	curl --fail --location --output $(source) $(source_url)
	$(web_sources)
	rpmbuild -bs --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)" $(spec)
