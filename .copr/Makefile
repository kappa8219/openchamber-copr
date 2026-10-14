spec := ../openchamber.spec
version := 2.3.2
source := OpenChamber-$(version)-linux-x86_64.rpm
source_url := https://github.com/openchamber/openchamber/releases/download/v$(version)/$(source)

.PHONY: srpm
srpm:
	curl --fail --location --output $(source) $(source_url)
	rpmbuild -bs --define "_sourcedir $(CURDIR)" --define "_srcrpmdir $(outdir)" $(spec)
