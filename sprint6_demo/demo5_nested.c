// demo5_nested.c - Nested if
fn main() int {
    int x = 5;
    int y = 10;
    int result = 0;
    
    if (x > 0) {
        if (y > 5) {
            result = 100;
        } else {
            result = 200;
        }
    } else {
        result = 300;
    }
    
    return result;
}
