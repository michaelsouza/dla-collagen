dla.bin: dla.cpp
	g++ -g dla.cpp -o dla.bin

clean: 
	rm -rf dla.bin