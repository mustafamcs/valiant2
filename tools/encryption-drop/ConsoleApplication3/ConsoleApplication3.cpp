#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <ctime>

const std::string fileNames[] = { "mob_drop_item.txt", "special_item_group.txt" };
const std::string deleteStrList[] = { "Type", "Group", "{", "}" };

void ClearDropFile()
{
    for (auto& fileName : fileNames)
    {
        //Type Group delete
        std::ifstream fileRead(fileName);
        if (!fileRead.is_open())
            return;

        std::vector<std::string> lines;
        std::string line;

        while (std::getline(fileRead, line))
        {
            bool deleteLine = false;

            for (const std::string& deleteStr : deleteStrList)
            {
                if (line.find(deleteStr) != std::string::npos)
                {
                    deleteLine = true;
                    break;
                }
            }

            if (!deleteLine)
            {
                size_t tabPos = line.find_first_not_of(" \t");
                if (tabPos != std::string::npos)
                    line = line.substr(tabPos);

                lines.push_back(line);
            }
        }

        fileRead.close();

        std::ofstream fileWrite(fileName);

        if (!fileWrite.is_open())
            return;

        for (const std::string& newLine : lines)
        {
            fileWrite << newLine << std::endl;
        }

        fileWrite.close();

        //Prob Delete
        std::ifstream fileRead2(fileName);
        if (!fileRead2.is_open())
            return;

        lines.clear();

        while (std::getline(fileRead2, line))
        {
            lines.push_back(line);
        }

        fileRead2.close();

        std::ofstream fileWrite2(fileName);

        if (!fileWrite2.is_open())
            return;

        for (std::string& line : lines)
        {
            size_t tabPos = 0;
            for (int i = 0; i < 3; ++i)
            {
                tabPos = line.find('\t', tabPos);
                if (tabPos == std::string::npos)
                {
                    break;
                }
                tabPos++;
            }

            if (tabPos != std::string::npos)
            {
                line.erase(tabPos - 1);
            }
        }

        for (const std::string& newLine : lines)
        {
            fileWrite2 << newLine << std::endl;
        }

        fileWrite2.close();
    }
}

void EncryptionLine(std::string& line)
{
    for (auto& str : line)
    {
        int randNumber = rand() % (20 - 1 + 1) + 1;
        switch (str)
        {
            case '0': {randNumber > 10 ? str = 's' : str = 'a'; break; }
            case '1': {randNumber > 10 ? str = 'e' : str = 'b'; break; }
            case '2': {randNumber > 10 ? str = 'x' : str = 'c'; break; }
            case '3': {randNumber > 10 ? str = 'p' : str = 'd'; break; }
            case '4': {randNumber > 10 ? str = 'o' : str = 'f'; break; }
            case '5': {randNumber > 10 ? str = 'r' : str = 'k'; break; }
            case '6': {randNumber > 10 ? str = 'n' : str = 'l'; break; }
            case '7': {randNumber > 10 ? str = 'z' : str = 'm'; break; }
            case '8': {randNumber > 10 ? str = 'y' : str = 'q'; break; }
            case '9': {randNumber > 10 ? str = 'g' : str = 't'; break; }

            default:    break;
        }
    }
}

void EncryptionFile()
{
    for (auto& fileName : fileNames)
    {
        std::ifstream fileRead(fileName);
        if (!fileRead.is_open())
            return;

        std::vector<std::string> lines;
        std::string line;

        while (std::getline(fileRead, line))
        {
            EncryptionLine(line);
            lines.push_back(line);
        }

        fileRead.close();

        std::ofstream fileWrite(fileName);

        if (!fileWrite.is_open())
            return;

        for (const std::string& newLine : lines)
        {
            fileWrite << newLine << std::endl;
        }

        fileWrite.close();
    }
}



int main()
{
    srand(time(0));
    ClearDropFile();
    EncryptionFile();
    return 1;
}

