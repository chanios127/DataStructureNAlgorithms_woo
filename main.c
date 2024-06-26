#include <stdio.h> //헤더 파일 (표준 입출력 함수 헤더파일)

int main(){
    // 각각의 자료형 크기를 바이트 단위로 출력하는 내용
    // sizeof 연산자는 변수나 자료형의 메모리 크기를 바이트 단위로 반환함
    
    // char : 1바이트의 메모리를 사용.
    printf("char 자료형 크기 : %d byte\n", sizeof(char));
    
    // signed char : 부호가 있는 1바이트 정수.
    printf("signed char 자료형 크기 : %d byte\n", sizeof(signed char));
    
    // unsigned char : 부호 없는 1바이트 정수.
    printf("unsigned char 자료형 크기 : %d byte\n", sizeof(unsigned char));
    
    // short : 정수, 적어도 2바이트의 메모리를 사용.
    printf("short 자료형 크기 : %d byte\n", sizeof(short));
    
    // signed short : 부호가 있는 정수, 적어도 2바이트를 사용.
    printf("signed short 자료형 크기 : %d byte\n", sizeof(signed short));
    
    // unsigned short : 부호 없는 정수, 적어도 2바이트를 사용.
    printf("unsigned short 자료형 크기 : %d byte\n", sizeof(unsigned short));
    
    // int : 적어도 2바이트는 되어야 하는 정수.
    printf("int 자료형 크기 : %d byte\n", sizeof(int));
    
    // signed int : 부호가 있는 정수로 적어도 2바이트를 사용.
    printf("signed int 자료형 크기 : %d byte\n", sizeof(signed int));
    
    // unsigned int : 부호 없는 정수로 적어도 2바이트를 사용.
    printf("unsigned int 자료형 크기 : %d byte\n", sizeof(unsigned int));
    
    // long : 적어도 4바이트는 되어야 하는 정수.
    printf("long 자료형 크기 : %d byte\n", sizeof(long));
    
    // signed long : 부호가 있는 정수로 적어도 4바이트를 사용.
    printf("signed long 자료형 크기 : %d byte\n", sizeof(signed long));
    
    // unsigned long : 부호 없는 정수로 적어도 4바이트를 사용.
    printf("unsigned long 자료형 크기 : %d byte\n", sizeof(unsigned long));
    
    // long long : 적어도 8바이트는 되어야 하는 정수.
    printf("long long 자료형 크기 : %d byte\n", sizeof(long long));
    
    // signed long long : 부호가 있는 정수, 적어도 8바이트를 사용.
    printf("signed long long 자료형 크기 : %d byte\n", sizeof(signed long long));
    
    // unsigned long long :부호 없는 정수로 적어도 8바이트를 사용.
    printf("unsigned long long 자료형 크기 : %d byte\n", sizeof(unsigned long long));
    
    // float : 실수를 나타내며, 일반적으로 4바이트를 사용.
    printf("float 자료형 크기 : %d byte\n", sizeof(float));
    
    // double : float 형보다 큰 범위의 실수를 나타내며, 일반적으로 8바이트를 사용.
    printf("double 자료형 크기 : %d byte\n", sizeof(double));
    
    // long double : double 형보다 더 큰 범위의 실수.
    printf("long double 자료형 크기 : %d byte\n", sizeof(long double));
	return 0;
}
