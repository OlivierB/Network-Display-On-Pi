// Class header
#include <Json.hpp>

// Library header
#include <sstream>



using namespace std;

Json::Json()
{

};

void Json::add(std::string key, std::string val)
{
    string tmp = "\"" + key + "\" : \"" + val + "\"";
    json_str.push_back(tmp);
};

void Json::add(std::string key, int val)
{
    string tmp = "\"" + key + "\" : ";

    ostringstream convert;
    convert << val;

    json_str.push_back(tmp + convert.str());
};

void Json::add(std::string key, double val)
{
    string tmp = "\"" + key + "\" : ";

    ostringstream convert;
    convert << val;

    json_str.push_back(tmp + convert.str());
};

void Json::add(std::string key, float val)
{
    string tmp = "\"" + key + "\" : ";

    ostringstream convert;
    convert << val;

    json_str.push_back(tmp + convert.str());
};

void Json::add(std::string key, std::vector<std::string> val)
{
    string tmp = "\"" + key + "\" : [";

    for(unsigned int i = 0; i < val.size(); i++)
    {
        tmp += "\"" + val.at(i) + "\"";
        if(i < val.size()-1)
            tmp += ", ";
    }

    tmp += "]";
    json_str.push_back(tmp);
};

void Json::add(std::string key, std::vector<int> val)
{
    string tmp = "\"" + key + "\" : [";

    for(unsigned int i = 0; i < val.size(); i++)
    {
        ostringstream convert;
        convert << val.at(i);
        tmp += convert.str();
        if(i < val.size()-1)
            tmp += ", ";
    }

    tmp += "]";
    json_str.push_back(tmp);
};

void Json::add(std::string key, std::vector<double> val)
{
    string tmp = "\"" + key + "\" : [";

    for(unsigned int i = 0; i < val.size(); i++)
    {
        ostringstream convert;
        convert << val.at(i);
        tmp += convert.str();
        if(i < val.size()-1)
            tmp += ", ";
    }

    tmp += "]";
    json_str.push_back(tmp);
};

void Json::add(std::string key, std::vector<float> val)
{
    string tmp = "\"" + key + "\" : [";

    for(unsigned int i = 0; i < val.size(); i++)
    {
        ostringstream convert;
        convert << val.at(i);
        tmp += convert.str();
        if(i < val.size()-1)
            tmp += ", ";
    }

    tmp += "]";
    json_str.push_back(tmp);
};

void Json::add(std::string key, Json val)
{
    string tmp = "\"" + key + "\" : " + val.toString();
    json_str.push_back(tmp);
};


std::string Json::toString()
{
    string tmp = "{";

    for(unsigned int i = 0; i < json_str.size(); i++)
    {
        tmp += json_str.at(i);
        if(i < json_str.size()-1)
            tmp += ", ";
    }

    tmp += "}";

    return tmp;
}
