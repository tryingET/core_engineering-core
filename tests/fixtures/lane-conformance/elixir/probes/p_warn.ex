# expect: compile variable "x" is unused
# expect: ci variable "x" is unused
defmodule MyApp.PWarn do
  @moduledoc false
  def f(x), do: 1
end
