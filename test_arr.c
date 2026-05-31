extern void* malloc(int size);

fn main() int {
    int* arr = malloc(5 * 4);
    arr[0] = 10;
    return arr[0];
}
