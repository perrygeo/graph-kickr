
SOURCE = /Users/mperry/Library/Mobile Documents/iCloud~com~hurtsdevelopment~hurtsergo/Documents/Saved Workouts

default: sync generate openlatest

archive/README.md:
	mkdir -p archive
	touch archive/README.md

charts/README.md:
	mkdir -p charts
	touch charts/README.md

sync: archive/README.md
	cp -r "$(SOURCE)/" archive/

clean:
	rm charts/*.png
	
generate: archive/README.md charts/README.md
	./archive-fits.sh
	./generate-charts.sh

openlatest:
	open charts/$(shell ls -1t charts/ | head -n 1)

