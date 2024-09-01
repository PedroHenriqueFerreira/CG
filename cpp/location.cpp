#include <iostream>
#include <fstream>

using namespace std;

class Location
{
private:
    string filepath;

public:
    Location(const string& file) {
        this->filepath = file;

        this->load();
    }

    void load() {
        cout << "Loading file: " << filepath << endl;

        ifstream file(this->filepath);

        if (!file.is_open()) {
            cerr << "Error opening file: " << this->filepath << endl;

            exit(1);
        }

        json data;
        file >> data;

        float x = data.at("features")[0].at("geometry").at("coordinates")[0][0]; //
        float y = data.at("features")[0].at("geometry").at("coordinates")[0][1]; //

        cout << x << " " << y << endl;

        file.close();
    }
};

int main()
{
    Location location("./maps/russas.geojson");

    return 0;
}