//! Workspace member whose doctest fails (nextest alone would miss it).

/// Doubles a number.
///
/// ```
/// assert_eq!(member::double(2), 5);
/// ```
#[must_use]
pub fn double(value: u64) -> u64 {
    value * 2
}
