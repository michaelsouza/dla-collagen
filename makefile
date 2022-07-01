dla.bin: dla.cpp dla.h
	g++ -Wall -g dla.cpp -o dla.bin

run_bin: dla.bin
	./dla.bin -verbose 

viewer.bin: viewer.cpp
	g++ -g viewer.cpp -o viewer.bin -lGL -lGLU -lglut

dla.prf: dla.cpp dla.h
	g++ -pg dla.cpp -o dla.prf

run_prf: dla.prf
	./dla.prf
	gprof dla.prf gmon.out > profiling.txt

clean:
	rm -rf dla.bin