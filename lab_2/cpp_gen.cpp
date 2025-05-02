#include <iostream>
#include <fstream>
#include <random>

int main() {
    std::ofstream file;
    file.open("cpp_sequence.txt");

    std::mt19937 engine(std::random_device{}());
    std::bernoulli_distribution bit_dist(0.5);  

    int count = 128;
    while (count--) {
        file.put(bit_dist(engine) ? '1' : '0');
    }

    file.put('\n');
    file.close();

    return 0;
}
