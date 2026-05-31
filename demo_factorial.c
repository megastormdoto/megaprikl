fn factorial(n int) int {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

fn main() int {
    int arr[6];
    int i = 0;
    int sum = 0;
    
    i = 0;
    while (i < 6) {
        arr[i] = factorial(i);
        i = i + 1;
    }
    
    i = 0;
    while (i < 6) {
        sum = sum + arr[i];
        i = i + 1;
    }
    
    return sum;
}
