// expect: lint bool_comparison
fn is_on(flag: bool) -> bool {
    flag == true
}

#[test]
fn on() {
    assert!(is_on(true));
}
