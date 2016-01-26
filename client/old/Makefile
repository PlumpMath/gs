all:
#	g++ i9n.c -fPIC -shared -lsteam_api -m32 -L. -o i9c_32.so
#	g++ i9n.c -fPIC -shared -lsteam_api_64 -L. -o i9c_64.so
	g++ i9n.c -fPIC -shared -lsteam_api -L. -o i9c_64.so
	LD_LIBRARY_PATH=. ./test.py
