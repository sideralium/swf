.PHONY: dl/preloader x/preloader c/preloader

domain = https://darkorbit-22.bpsecure.com
rpath = assets/spacemap

dl/preloader:
	[ -f $(rpath)/preloader.swf ] || wget --directory-prefix $(rpath) -L $(domain)/spacemap/preloader.swf

x/preloader: dl/preloader
	test -s $(rpath)/preloader-0/preloader-0.main.asasm || { echo "GNU sort does not exist! Exiting..."; exit 1; }
	cd $(rpath); abcexport preloader.swf; rabcdasm preloader-0.abc
	cd $(rpath)/preloader-0; \
		git init -b preloader-$(shell sha256sum $(rpath)/preloader.swf | cut -c -8); \
		git add .; \
		git commit -m "init"

c/preloader:
	rabcasm $(rpath)/preloader-0/preloader-0.main.asasm
	abcreplace $(rpath)/preloader.swf 0 $(rpath)/preloader-0/preloader-0.main.abc
