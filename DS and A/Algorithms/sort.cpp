#include <iostream>
#include <string>
#include <vector>
#include <fstream>

using namespace std;

int main(int argc, char const* argv[]) {
    vector<string> lines;

    if (argc > 1) {
        ifstream input_file(argv[1]);
            string line;
            while (getline(input_file, line)) {
                lines.push_back(line);
            }
        input_file.close();
    }
    else {
        string line;
        while (getline(cin, line)) {
            lines.push_back(line);
        }
    }

    for (int i = 1; i < lines.size(); i++) {
        string key = lines[i];
        int j = i - 1;
        while (j >= 0 && lines[j] > key) {
            lines[j + 1] = lines[j];
            j--;
        }
        lines[j + 1] = key;
    }

    for (int i = 0; i < lines.size(); i++) {
        cout << lines[i] << endl;
    }

    return 0;
}
