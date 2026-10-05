spec := ../openchamber.spec
version := 2.1.1
source := openchamber-$(version).tar.gz
source_url := https://github.com/openchamber/openchamber/archive/refs/tags/v$(version).tar.gz
bun_version := 1.4.2
bun_source := bun-linux-x64.zip
bun_source_url := https://github.com/oven-sh/bun/releases/download/bun-v$(bun_version)/$(bun_source)

.PHONY: srpm
srpm:
	curl --fail --location --output $(source) $(source_url)
	curl --fail --location --output $(bun_source) $(bun_source_url)
	rpmbuild -bs --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)" $(spec)
