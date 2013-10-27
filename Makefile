prefix = /usr
bindir = $(prefix)/bin

all:

install:
	install -m 755 crux $(DESTDIR)$(bindir)/crux

