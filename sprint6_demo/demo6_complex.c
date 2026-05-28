// demo6_complex.c - Complex logical expression
fn main() int {
    int a = 1;
    int b = 0;
    int c = 10;
    int result = 0;
    
    if ((a > 0 || b / a > 0) && c > 5) {
        result = 1000;
    } else {
        result = 2000;
    }
    
    return result;
}
