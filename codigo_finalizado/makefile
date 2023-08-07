CXX = g++
CXXFLAGS = -std=c++11 -Wall -Wextra -pedantic -I/usr/local/include

SRCS = stress_f.cpp
OBJS = $(SRCS:.cpp=.o)
EXEC = stress_f

all: $(EXEC)

$(EXEC): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $(EXEC) -lboost_program_options

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(EXEC)