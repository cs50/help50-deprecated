NAME := help50
VERSION := 1.2.2
UPSTREAM := $(NAME)-$(VERSION)
BUILD_DIR := build

.PHONY: clean
clean:
	rm -rf build/
	cd $(NAME) && debuild clean

.PHONY: deb
build: clean
	rsync -a $(NAME)/* $(UPSTREAM)/ --exclude debian
	tar -cvzf $(NAME)_$(VERSION).orig.tar.gz $(UPSTREAM)
	cd $(NAME) && debuild -us -uc -I -i --lintian-opts -i -I --show-overrides
	mkdir -p $(BUILD_DIR)
	mv *.build *.changes *.deb *.dsc *.tar.gz $(UPSTREAM) $(BUILD_DIR)
