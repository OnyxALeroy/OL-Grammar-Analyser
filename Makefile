# Global Files
TARGET = main
ALLSRCS = grammar.cpp grammar_parser.cpp
MAINSRCS = main.cpp
	MAINSRCS += $(ALLSRCS)
# All Sources
SRCS = $(patsubst %.cpp, src/%.cpp, $(MAINSRCS))
OBJS = $(patsubst %.cpp, %.o, $(SRCS))

#compiler
CC = g++
CFLAGS = -Wall -std=c++23 -O3 -pedantic -Wextra

#linker
CFLAGS += -fsanitize=address -fno-omit-frame-pointer -g3
LDFLAGS += -fsanitize=address

#libraries
# CFLAGS +=
# LDFLAGS +=

#compilation
all: $(TARGET)

%.o : %.cpp
	$(CC) $(CFLAGS) -c $< -o $@

$(TARGET): $(OBJS)
	$(CC) $^ $(LDFLAGS) -o $@ 

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(OBJS) $(TARGET)