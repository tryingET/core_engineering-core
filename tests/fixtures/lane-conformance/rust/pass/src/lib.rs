//! Root package of the rust lane conformance fixture.

/// Adds two numbers.
///
/// ```
/// assert_eq!(lane_probe::add(1, 2), 3);
/// ```
#[must_use]
pub fn add(a: u64, b: u64) -> u64 {
    a + b
}

#[cfg(test)]
mod tests {
    use super::add;

    #[test]
    fn adds() {
        assert_eq!(add(2, 3), 5);
    }
}
