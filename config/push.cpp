#include <iostream>
#include <string>
#include <fstream>
#include <ctime>
#include <vector>

/*

Pushs new configuration to the config file for later use. Also writes location to cache if needed.
Args should be passed as: [filename, configFileLocation, configuration, newValue]
 - filename: name of the file, always passed in when push.cpp is called
 - configFileLocation: a string representing where the configuration file is located
 - configuration: an integer representing which configuration to edit. the list can be found in config.py
 - newValue: what the configuration should be changed to

*/

using namespace std;

int trySTOI(string sInput){
    int iInput = -1;
    try{
        iInput = stoi(sInput);
        return iInput;
    }catch(const invalid_argument& ia){
        cerr << "Error: --Invalid Argument: --" << ia.what() << endl;
        return -1;
    }catch(const out_of_range& oor){
        cerr << "Error: --Out of Range: --" << oor.what() << endl;
        return -1;
    }catch(exception& ex){ 
        cerr << "Error: --Unexpected-Throw: " << ex.what() << endl;
        return -1;
    }catch(...){
        cerr << "Error: --Undefined-Throw catch_all abort()\n";
        cout << "Sorry, something unexpected happened and the program has to close! Please report the issue\n";
        abort();
    }
    return -1;
}

bool ableFSTREAM(string location){
    fstream file;
    file.open(location);
    try{
        if(file.is_open()){
            return true;
        }else if(!file.is_open()){
            throw runtime_error(string("fstream: failed to open \"")+=location+=string("\""));
        }else{
            cerr << "something unexcepected happened" << endl;
        }
        file.close();
    }catch(runtime_error& fto){
        cerr << "Error: --" << fto.what() << endl;
        return false;
    }catch(exception& ex){
        cerr << "Error: --Unexpected-Throw: --" << ex.what() << endl;
        return false;
    }catch(...){
        cerr << "Error: --Undefined-Throw catch_all abort()\n";
        cout << "Sorry, something unexpected happend, and the program had to close! Please report the issue\n";
        abort();
    }
    file.close();
    return false;
};

int main(int argc, char *argv[]){

    string configFileLocation = argv[1];
    int configuration = trySTOI(argv[2]);
    if (configuration < 0) return 1; // Invalid integer
    int newValue = trySTOI(argv[3]);
    if (newValue < 0) return 1; // Invalid integer
    if (!ableFSTREAM(configFileLocation)) return 2; // Invalid file location
    fstream configFile;
    configFile.open(configFileLocation, ios::in);

    cout << argv[0] << " was called" << endl;
    cout << "configurations found at \"" << argv[1] << "\" (relative)" << endl;
    cout << "called to edit configuration #" << argv[2] << " to be " << argv[3] << endl;

    string newLine = "+c";
    newLine.append(to_string(newValue));
    string line;
    vector <string> configFileVec;
    int lineNum = 1;
    while(getline(configFile, line, '\n')){
        if(lineNum == configuration){
            line = newLine;
        }
        else if(lineNum > configuration){
            return 3; // Configuration DNE
        }
        else if(line == "loc"){
            return 4; // the location of the config file changed
        }
        configFileVec.push_back(line);
        lineNum++;
    }
    configFile.close();
    configFile.open(configFileLocation, ios::out);
    for(auto y : configFileVec){
        configFile << y << '\n';
    }
    configFile.close();
    return 0;
}
