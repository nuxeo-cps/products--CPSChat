check:
	pychecker2 *.py

clean:
	find . -name '*~' | xargs rm -f
	find . -name '*.pyc' | xargs rm -f
	rm -rf doc/api
	cd tests ; make clean

doc:
	happydoc -d doc/api *.py
