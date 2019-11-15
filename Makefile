serve:
	bundle exec jekyll serve -w

venv: venv/bin/activate

venv/bin/activate: requirements.txt
	( \
		test -d venv || virtualenv venv; \
		. venv/bin/activate; pip install -r requirements.txt; \
		touch venv/bin/activate; \
	)

#clean:
#    rm -rf venv
#    find -iname "*.pyc" -delete

testimport: venv
	. venv/bin/activate; python import_speakers.py

import: venv
	. venv/bin/activate; python import_speakers.py >> _data/speakers.yml
