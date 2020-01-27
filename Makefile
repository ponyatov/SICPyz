CWD    = $(CURDIR)
MODULE = $(notdir $(CWD))

NOW = $(shell date +%d%m%y)
REL = $(shell git rev-parse --short=4 HEAD)



.PHONY: all
all: run doxy



run: $(MODULE).py $(MODULE).scm
	python3 $^



.PHONY: doc

WGET = wget -c --no-check-certificate

doc: doc/SICP_ru.pdf doc/SICP_en.pdf
doc/SICP_ru.pdf:
	$(WGET) -O $@ http://newstar.rinet.ru/~goga/sicp/sicp.pdf
doc/SICP_en.pdf:
	$(WGET) -O $@ https://web.mit.edu/alexmv/6.037/sicp.pdf



.PHONY: install
install: doc bin/pip3
bin/pip3:
	python3 -m venv .
	$@ install -U pip
	$@ install -U ply flask



.PHONY: doxy
doxy:
	@ echo
	rm -rf docs ; doxygen doxy.gen 1>/dev/null


.PHONY: merge release zip

MERGE  = Makefile README.md doxy.gen doc
MERGE += $(MODULE).py $(MODULE).scm

merge:
	git checkout master
	git checkout shadow -- $(MERGE)
	$(MAKE) doxy

release:
	git tag $(NOW)-$(REL)
	git push -v && git push -v --tags
	git checkout shadow

zip:
	git archive --format zip --output $(MODULE)_$(NOW)_$(REL).zip HEAD
