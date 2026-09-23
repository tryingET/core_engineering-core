//! Workspace member with a lint violation.

/// Reports whether the flag is set.
#[must_use]
pub fn is_on(flag: bool) -> bool {
    flag == true
}
