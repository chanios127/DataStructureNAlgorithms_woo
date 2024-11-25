
#include <stdio.h>

void printDataSet(int DataSet[], int Length) {
	int i;
	for (i = 0; i < Length; i++) {
		printf("%d", DataSet[i]);
	}
	printf("\n");

}

void Swap(int* A, int* B)
{
	int Temp = *A;
	*A = *B;
	*B = Temp;
}

int Partition(int DataSet[], int Left, int Right, int Length)
{
	int First = Left;
	int Pivot = DataSet[First];
	printf("Pivot : %d \n", Pivot);
	
	++Left;

	while (Left <= Right)
	{
		while (DataSet[Left] <= Pivot && Left < Right)
			++Left;

		while (DataSet[Right] >= Pivot && Left <= Right)
			--Right;

		if (Left < Right)
		{
			printf(" Swap(DataSet[%d](%d)<=> DataSet[%d](%d)) \n",Left, DataSet[Left], Right, DataSet[Right]);
			Swap(&DataSet[Left], &DataSet[Right]);
			printDataSet(DataSet, Length);
		}
		else
			break;
	}
	if (Right != First)
	{
		printf("Swap(Pivot = DataSet[%d](%d)<=> DataSet[%d](%d)) \n", First, DataSet[First], Right, DataSet[Right]);
		Swap(&DataSet[First], &DataSet[Right]);
	}
	else
		printf("nonSwap");
	printDataSet(DataSet, Length);
	return Right;
}

void QuickSort(int DataSet[], int Left, int Right, int Length)
{
	if (Left < Right)
	{
		printf("Range: %d ~ %d \n", Left, Right);
		int Index = Partition(DataSet, Left, Right, Length);

		QuickSort(DataSet, Left, Index - 1, Length);
		QuickSort(DataSet, Index + 1, Right, Length);
	}
}

void BubbleSort(int DataSet[], int Length)
{
	int i = 0;
	int j = 0;
	int temp = 0;

	for (i = 0; i < Length - 1; i++)
	{
		for (j = 0; j < Length - (i + 1); j++)
		{
			if (DataSet[j] > DataSet[j + 1])
			{
				temp = DataSet[j + 1];
				DataSet[j + 1] = DataSet[j];
				DataSet[j] = temp;
			}
		}
	}
}

void InsertionSort(int DataSet[], int Length)
{
	int i = 0;
	int j = 0;
		int value = 0;

	for (i = 1; i < Length; i++)
	{
		if (DataSet[i - 1] <= DataSet[i])
			continue;

		value = DataSet[i];

		for (j = 0; j < i; j++)
		{
			if (DataSet[j] > value)
			{
				memmove(&DataSet[j + 1], &DataSet[j], sizeof(DataSet[0]) * (i - j));
				//memmove(ToPtr, FromPtr, Length)
				DataSet[j] = value;
				break;
			}
		}
	}
}


int main(void)
{
	int DataSet[] = { 10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
	int Length = sizeof DataSet / sizeof DataSet[0];
	int i = 0;
	printf("Before: ");
	printDataSet(DataSet, Length);

	QuickSort(DataSet, 0, Length - 1, Length);

	printf("After: ");
	printDataSet(DataSet, Length);

	return 0;
