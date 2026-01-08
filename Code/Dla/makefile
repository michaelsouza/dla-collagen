CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -O2

# Diretório onde estão os códigos fontes
SRC_DIR = Code/Dla

# Nome do executável final
TARGET = fast_dla

# Arquivo fonte principal
SRC = $(SRC_DIR)/fast_dla.cpp

all: $(TARGET)

$(TARGET): $(SRC)
$(CXX) $(CXXFLAGS) $(SRC) -o $(TARGET)

clean:
rm -f $(TARGET) *.o
