NY: tests clean doc

tests:
	./runtests.py

clean:
	find . -name '*~' | xargs rm -f
	find . -name '*.pyc' | xargs rm -f
	rm -rf doc/api

doc:
	happydoc -d doc/api *.py
