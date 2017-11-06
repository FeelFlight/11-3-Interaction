module Model exposing (..)

import Set

import Model.Ui exposing (..)


type alias Model =
  { ui : Ui
  , alarmSettings : AlarmSettings
  , heaters : List Int
  , errorMsg : Maybe String }


type alias AlarmSettings =
  { hour : String
  , minute : String
  , enabled : Bool }


initialModel : Model
initialModel =
  { ui = initialUi
  , alarmSettings = AlarmSettings "3" "45" False
  , heaters = [ 0, 0, 0 ]
  , errorMsg = Nothing }


getHeaterSetting : Model -> Int -> Int
getHeaterSetting model heaterIndex =
  model.heaters |> getInList heaterIndex


replaceInList : Int -> x -> List x -> List x
replaceInList index newElement list =
  let
      left = list |> List.take index
      right = list |> List.drop (index + 1)
  in
      left ++ [ newElement ] ++ right


getInList : Int -> List Int -> Int
getInList index list =
  list |> List.drop index |> List.head |> Maybe.withDefault 0
