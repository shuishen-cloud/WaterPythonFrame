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

void test(){
    int a = 1;
    return;
}

int main(void){
    int sum = 1;
    int * p = &sum;
    test();
    for(int i = 0; i < 10; i++){
        sum += i;
        *p += i;
    }

    return 0;
}