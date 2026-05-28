// demo4_shortcircuit.c - Short-circuit AND
fn main() int {
    int a = 0;
    int b = 5;
    int result = 0;
    
    if (a != 0 && b / a > 2) {
        result = 1;
    } else {
        result = 2;
    }
    
    return result;
}
