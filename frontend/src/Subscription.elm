module Subscription exposing (..)

import Http

import Model exposing (..)
import Model.Ui exposing (..)


type Msg
  = InputAlarmHour String
  | InputAlarmMinute String
  | ToggleAlarm Bool
  | ChangeHeater Int Int
  | GetAlarmFromServer (Result Http.Error AlarmSettings)
  | GetHeatingFromServer (Result Http.Error (List Int))


subscriptions : Model -> Sub Msg
subscriptions {ui} =
  [] |> Sub.batch
