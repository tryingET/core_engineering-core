//! Workspace member: gates without `--workspace` never reach this crate.

/// Doubles a number.
#[must_use]
pub fn double(value: u64) -> u64 {
    value * 2
}

#[cfg(test)]
mod tests {
    #[test]
    fn doubles() {
        assert_eq!(super::double(2), 4);
    }
}
