dla.bin: dla.cpp dla.h
	g++ -g dla.cpp -o dla.bin

run: dla.bin
	./dla.bin -verbose 

viewer.bin: viewer.cpp
	g++ -g viewer.cpp -o viewer.bin -lGL -lGLU -lglut

clean:
	rm -rf dla.bin