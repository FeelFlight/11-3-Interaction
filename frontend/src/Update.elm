module Update exposing (..)


import Model exposing (..)
import Model.Ui exposing (..)
import Subscription exposing (..)
import HttpClient exposing (..)

import Debug exposing (log)


update : Msg -> Model -> (Model, Cmd Msg)
update action ({alarmSettings} as model) =
  case action of
    InputAlarmHour str ->
      changeAlarm model { alarmSettings | hour = str }

    InputAlarmMinute str ->
      changeAlarm model { alarmSettings | minute = str }

    ToggleAlarm enabled ->
      changeAlarm model { alarmSettings | enabled = enabled }

    ChangeHeater index newSetting ->
      let
          heaters = model.heaters |> replaceInList index newSetting
      in
          ({ model | heaters = heaters }, HttpClient.postHeating heaters)

    GetAlarmFromServer (Ok alarmSettings) ->
      ({ model | alarmSettings = alarmSettings |> log "alarmSettings__", errorMsg = Nothing }, Cmd.none)

    GetAlarmFromServer (Err error) ->
      (model, Cmd.none)
      -- ({ model | errorMsg = Just "Could not read alarm" }, Cmd.none)

    GetHeatingFromServer (Ok heaters) ->
      ({ model | heaters = heaters, errorMsg = Nothing |> log "heating__" }, Cmd.none)

    GetHeatingFromServer (Err error) ->
      (model, Cmd.none)
      -- ({ model | errorMsg = Just "Could not read heating" }, Cmd.none)


changeAlarm : Model -> AlarmSettings -> (Model, Cmd Msg)
changeAlarm oldModel alarmSettings =
  let
      newModel = { oldModel | alarmSettings = alarmSettings }
  in
      (newModel, HttpClient.postAlarm newModel)
