spec ?= ../openchamber.spec
version := 2.8.1
license_source := LICENSE-$(version)

ifeq ($(notdir $(spec)),openchamber-cli.spec)
source := openchamber-web-$(version).tgz
source_url := https://github.com/openchamber/openchamber/releases/download/v$(version)/$(source)
license_source_url := https://raw.githubusercontent.com/openchamber/openchamber/v$(version)/LICENSE
web_sources := curl --fail --location --output $(license_source) $(license_source_url)
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
