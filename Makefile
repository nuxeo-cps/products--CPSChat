.PHONY: check clean

check:
	pychecker2 *.py

clean:
	find . -name "*~" -or -name "*.pyc" -print0 | xargs -0 rm -f
	rm -rf doc/api
	cd tests ; make clean

doc:
	happydoc -d doc/api *.py
