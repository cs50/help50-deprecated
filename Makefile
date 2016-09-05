MAINTAINER = "CS50 <sysadmins@cs50.harvard.edu>"
NAME = help50
VERSION = 1.0.2

.PHONY: bash
bash:
	docker run -i --rm -v "$(PWD)":/root -t cs50/cli

.PHONY: clean
clean:
	rm -f $(NAME)_$(VERSION)_*.deb
	rm -f $(NAME)-$(VERSION)-*.pkg.tar.xz
	rm -f $(NAME)-$(VERSION)-*.rpm

.PHONY: deb
deb:
	rm -f $(NAME)_$(VERSION)_*.deb
	fpm \
	-m $(MAINTAINER) \
	-n $(NAME) \
	-s dir \
	-t deb \
	-v $(VERSION) \
	--after-install after-install.sh \
	--after-remove after-remove.sh \
	--deb-no-default-config-files \
	--depends curl \
	opt

# TODO: add dependencies
.PHONY: pacman
pacman:
	rm -f $(NAME)-$(VERSION)-*.pkg.tar.xz
	fpm \
	-m $(MAINTAINER) \
	-n $(NAME) \
	-s dir \
	-t pacman \
	-v $(VERSION) \
	--after-install after-install.sh \
	--after-remove after-remove.sh \
	opt


# TODO: add dependencies
.PHONY: rpm
rpm:
	rm -f $(NAME)-$(VERSION)-*.rpm
	fpm \
	-m $(MAINTAINER) \
	-n $(NAME) \
	-s dir \
	-t rpm \
	-v $(VERSION) \
	--after-install after-install.sh \
	--after-remove after-remove.sh \
	opt
