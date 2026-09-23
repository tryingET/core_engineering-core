# expect: fmt mix format failed due to --check-formatted
# expect: ci mix format failed due to --check-formatted
defmodule MyApp.PFmt do
  @moduledoc false
  def f(  a ),   do: a
end
