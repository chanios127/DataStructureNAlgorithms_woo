#include "LinkedListStack.h"

int main( void )
{
    int i= 0;
    int Count = 0;
    Node* Popped;
    Node* Top;
    LinkedListStack* Stack;

    LLS_CreateStack(&Stack);
    
    LLS_Push( Stack, LLS_CreateNode("abc") );
    LLS_Push( Stack, LLS_CreateNode("def") );
    LLS_Push( Stack, LLS_CreateNode("efg") );
    LLS_Push( Stack, LLS_CreateNode("hij") );

    Count = LLS_GetSize(Stack);
    printf( "Size: %d, Top: %s\n\n", 
        Count, LLS_Top(Stack)->Data );

    for ( i=0; i<Count; i++ )
    {
        if ( LLS_IsEmpty(Stack) )
            break;

        Popped = LLS_Pop( Stack );

        printf( "Popped: %s, ", Popped->Data );

 

        if ( ! LLS_IsEmpty(Stack) ) 
        {
            Top = LLS_Top(Stack);
            printf( "Current Top: %s\n", Top->Data );    // 여기서 자꾸 오류가 나는 것으로 보임. 
        }
        else
        {
            printf( "Stack Is Empty.\n");
        }

        LLS_DestroyNode(Popped);
    }

    LLS_DestroyStack(Stack);

    return 0;
}
