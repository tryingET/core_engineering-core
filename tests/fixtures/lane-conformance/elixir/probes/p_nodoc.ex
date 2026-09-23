# expect: lint Modules should have a @moduledoc tag.
defmodule MyApp.PNoDoc do
  def f(a), do: a
end
