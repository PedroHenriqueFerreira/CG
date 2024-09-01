#include <iostream>
#include <fstream>
#include <string>

using namespace std;

class JSON {
private:
    string data;
    
    bool is_space(char c) {
        return c == ' ' || c == '\n' || c == '\t' || c == '\r';
    }

    char prev(int i) {
        int size = (int) this->data.size();

        if (i < 0 || i > size - 1) return '\0';

        if (is_space(this->data[i])) return this->prev(--i);

        return this->data[i];
    }

    char next(int i) {
        int size = (int) this->data.size();

        if (i < 0 || i > size - 1) return '\0';

        if (is_space(this->data[i])) return this->next(++i);
        
        return this->data[i];
    }

    char start() {
        return this->next(0);
    }

    char end() {
        return this->prev(this->data.size() - 1);
    }

    int start_index() {
        for (int i = 0; i < this->data.size(); i++) {
            if (!this->is_space(this->data[i])) return i;
        }

        throw out_of_range("No start index found");
    }
    
    int end_index() {
        for (int i = this->data.size() - 1; i >= 0; i--) {
            if (!this->is_space(this->data[i])) return i;
        }

        throw out_of_range("No end index found");
    }

    string clean() {
        string cleaned_data;

        int start = this->start_index(), end = this->end_index();

        return this->data.substr(start, end - start + 1);
    }

public:
    JSON () { }
    JSON (string data) : data(data) { }

    JSON operator[] (const string& key) {
        unsigned int level = 0;
        bool has_current_string = false, has_found_key = false;
        char curr_char, prev_char;
        string current_string, data;

        if (this->is_object()) {
            for (int i = 0; i < this->data.size(); i++) {
                curr_char = this->data[i];
                
                if (!has_current_string) {
                    if (this->is_space(curr_char)) continue;

                    if (curr_char == '{' || curr_char == '[') level++;
                    else if (curr_char == '}' || curr_char == ']') level--;
                }

                prev_char = this->prev(i - 1);

                if (prev_char != '\\' && curr_char == '"') has_current_string = !has_current_string;
                if (has_found_key && level >= 1) data += curr_char;

                if (level != 1) continue;
                if (prev_char != '\\' && curr_char == '"') continue;

                if (has_current_string) current_string += curr_char;
                else {
                    if (curr_char == ':' && current_string == key) has_found_key = true;
                    else if (curr_char == ',' && has_found_key) {
                        data.erase(data.size() - 1);

                        break;
                    }

                    current_string = "";
                }

            }

            return JSON(data);
        }

        throw runtime_error("This JSON is not an object");
    }

    JSON operator[] (const unsigned int& index) {
        unsigned int level = 0, current_index = 0;
        bool has_current_string = false, has_found_key = false;
        char curr_char, prev_char;
        string data;

        if (this->is_array()) {
            if (index == 0) has_found_key = true;

            for (int i = 0; i < this->data.size(); i++) {
                curr_char = this->data[i];

                if (!has_current_string) {
                    if (this->is_space(curr_char)) continue;

                    if (curr_char == '{' || curr_char == '[') level++;
                    else if (curr_char == '}' || curr_char == ']') level--;
                }

                prev_char = this->prev(i - 1);

                if (prev_char != '\\' && curr_char == '"') has_current_string = !has_current_string;
                if (has_found_key && level >= 1) data += curr_char;

                if (level != 1) continue;
                if (prev_char != '\\' && curr_char == '"') continue;

                if (!has_current_string && curr_char == ',') {
                    if (has_found_key) {
                        data.erase(data.size() - 1);

                        break;
                    }

                    if (++current_index == index) has_found_key = true;
                }

            }

            if (index == 0) data.erase(0, 1);
            
            return JSON(data);
        }

        throw runtime_error("This JSON is not an array");
    }

    friend ostream& operator<< (ostream& os, const JSON& json) {
        return os << "JSON(" << json.data << ")";
    }

    friend ifstream& operator>> (ifstream& file, JSON& json) {
        string data;
        
        char c;
        while (file.get(c)) data += c;

        json.data = data;

        return file;
    }

    unsigned int size() {
        unsigned int level = 0, size = 0;
        bool has_current_string = false;
        char curr_char, prev_char;

        if (!this->is_array() && !this->is_object()) 
            throw runtime_error("This JSON is not an array or object");

        for (int i = 0; i < this->data.size(); i++) {
            curr_char = this->data[i];
            prev_char = this->prev(i - 1);

            if (!has_current_string) {
                if (this->is_space(curr_char)) continue;

                if (curr_char == '{' || curr_char == '[') level++;
                else if (curr_char == '}' || curr_char == ']') level--;

                if (prev_char == '[' && curr_char == ']') return 0;
                else if (prev_char == '{' && curr_char == '}') return 0;
            }

            if (prev_char != '\\' && curr_char == '"') has_current_string = !has_current_string;

            if (level != 1) continue;
            if (prev_char != '\\' && curr_char == '"') continue;

            if (!has_current_string && curr_char == ',') size++;
        }

        return ++size;
    }

    string to_string() {
        if (!this->is_string()) throw runtime_error("This JSON is not a string");

        int start = this->start_index(), end = this->end_index();

        return this->data.substr(start + 1, end - start - 1);
    }

    int to_int() {
        if (!this->is_number()) throw runtime_error("This JSON is not a number");

        return stoi(this->data);
    }

    float to_float() {
        if (!this->is_number()) throw runtime_error("This JSON is not a number");

        return stof(this->data);
    }

    double to_double() {
        if (!this->is_number()) throw runtime_error("This JSON is not a number");
        
        return stod(this->data);
    }

    bool to_bool() {
        if (!this->is_bool()) throw runtime_error("This JSON is not a boolean");

        return this->clean() == "true";
    }

    bool is_object() {
        return this->start() == '{' && this->end() == '}';
    }

    bool is_array() {
        return this->start() == '[' && this->end() == ']';
    }

    bool is_string() {
        return this->start() == '"' && this->end() == '"';
    }

    bool is_number() {
        char curr_char;
        bool has_dot = false;

        int start = this->start_index(), end = this->end_index();

        for (int i = start; i <= end; i++) {
            curr_char = this->data[i];

            if (!isdigit(curr_char) && curr_char != '.' && curr_char != '-') return false;

            if (curr_char == '-' && i != start) return false;

            if (curr_char == '.') {
                if (has_dot) return false;

                has_dot = true;
            }
        }

        return true;
    }

    bool is_bool() {
        string value = this->clean();

        return value == "true" || value == "false";
    }

    bool is_null() {
        string value = this->clean();

        return value == "null";
    }

    bool is_empty() {
        return this->start() == '\0' && this->end() == '\0';
    }

};

int main()
{

    ifstream file("./file.json");

    if (!file.is_open()) {
        cerr << "Error opening file: " << "./file.json" << endl;
        exit(1);
    }

    JSON json;
    file >> json;
    
    // cout << json["features"][0]["geometry"]["coordinates"][1].size() << endl;
    cout << json["test2"]["test2_1"].to_string() << endl;

    return 0;
}