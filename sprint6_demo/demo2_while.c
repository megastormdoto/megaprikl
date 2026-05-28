// demo2_while.c - While loop
fn main() int {
    int i = 0;
    int sum = 0;
    
    while (i < 5) {
        sum = sum + i;
        i = i + 1;
    }
    
    return sum;
}
