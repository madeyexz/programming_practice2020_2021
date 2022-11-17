#include <iostream>
#include <string>
// #define pi 3.1415926
using namespace std;


int main(void){
//    float pi = 3.1415926;
const float pi = 3.1415926;
    int r = 10;
    float area;
    area = 2*pi*r;
    cout << "The area of the circle is: " << area << endl;
    cout << "size of area is: " << sizeof(area) << "\n";
    return 0;
}