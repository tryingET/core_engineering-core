# expect: typecheck does not match the success typing
defmodule MyApp.PSpec do
  @moduledoc false
  @spec f(integer()) :: atom()
  def f(x), do: x + 1
end
