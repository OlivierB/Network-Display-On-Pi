#ifndef JSON_HPP
#define JSON_HPP


/**
 * Json class
 * 
 * 
 */

// Library header
#include <iostream>
#include <string>
#include <vector>
 #include <set>


class Json
{
public:
    Json();

    void add(std::string key, std::string val);
    void add(std::string key, int val);
    void add(std::string key, double val);
    void add(std::string key, float val);

    void add(std::string key, std::vector<std::string> val);
    void add(std::string key, std::vector<int> val);
    void add(std::string key, std::vector<double> val);
    void add(std::string key, std::vector<float> val);

    void add(std::string key, std::set<std::string> val);

    void add(std::string key, Json val);

    std::string toString();

private:
	std::vector<std::string> json_str;

};


#endif