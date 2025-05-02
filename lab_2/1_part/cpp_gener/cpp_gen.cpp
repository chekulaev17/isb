#include <fstream>
#include <string>
#include <cstdlib>
#include <ctime>
#include <iostream>

void writeSequence(const char* filepath, const std::string& data) {
    std::ofstream output(filepath);
    if (output.is_open()) {
        output.write(data.c_str(), data.size());
        output.close();
    }
}

std::string generateBinarySequence(std::size_t length) {
    std::string result;
    result.reserve(length);
    std::srand(static_cast<unsigned int>(std::time(nullptr)));
    for (std::size_t i = 0; i < length; i++) {
        result.push_back((std::rand() % 2) ? '1' : '0');
    }
    return result;
}

int main() {
    constexpr std::size_t sequenceLength = 128;
    const std::string filename = "cpp_seq.txt";
    auto sequence = generateBinarySequence(sequenceLength);
    std::cout << "Generated binary sequence: " << sequence << std::endl;
    writeSequence(filename.c_str(), sequence);
    std::cout << "Random binary sequence generated and saved to " << filename << std::endl;
    return 0;
}
