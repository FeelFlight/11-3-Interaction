module Util exposing (..)

import String

pi = 3.1415926536


interpolate : Float -> Float -> Float -> Float
interpolate a b p =
  a + (b-a) * p


parseInt : String -> Int
parseInt str =
  str |> String.toInt |> Result.withDefault 0


parseFloat : String -> Float
parseFloat str =
  str |> String.toFloat |> Result.withDefault 0


validateInputs : List String -> Bool
validateInputs strings =
  strings |> List.all (\str -> parseInt str > 0)
