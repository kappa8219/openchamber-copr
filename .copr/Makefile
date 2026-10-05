spec := ../openchamber.spec
version := 2.1.1
source := openchamber-$(version).tar.gz
source_url := https://github.com/openchamber/openchamber/archive/refs/tags/v$(version).tar.gz

.PHONY: srpm
srpm:
	curl --fail --location --output $(source) $(source_url)
	rpmbuild -bs --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)" $(spec)
