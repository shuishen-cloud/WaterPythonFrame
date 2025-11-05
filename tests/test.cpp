/*
 * Filename:  test.cpp
 * Project:   tests
 * Author:    lwy
 * ***
 * Created:   2025/11/04 Tuesday 16:15:18
 * Modified:  2025/11/04 Tuesday 16:15:21
 * ***
 * Description: test code for debugger
 */

#include <iostream>

using namespace std;

int main(void){
    int sum = 0;
    int * p = &sum;
    
    for(int i = 0; i < 10; i++){
        sum += i;
        *p += i;
    }

    return 0;
}b