module HttpClient exposing (getAlarm, postAlarm, postHeating)

import Http exposing (expectStringResponse)
import Json.Decode as Decode exposing (Decoder,field,string,bool,list,int)
import Json.Encode as Encode
import Debug exposing (log)

import Model exposing (..)

import Subscription exposing (..)


rootUrl = "/api/v1.0/"
username = "ansi"
password = "test"


commonHeaders : List Http.Header
commonHeaders =
  [ Http.header "authorization" "Basic YW5zaTp0ZXN0"
  , Http.header "cache-control" "no-cache"
  , Http.header "username" username
  , Http.header "password" password ]


getAlarm : Model -> Cmd Msg
getAlarm model =
  Http.request
    { method = "GET"
    , headers = commonHeaders
    , url = rootUrl ++ "alarm"
    , body = Http.emptyBody
    , expect = Http.expectJson alarmDecoder
    , timeout = Nothing
    , withCredentials = True
    }
  |> Http.send GetAlarmFromServer


postAlarm : Model -> Cmd Msg
postAlarm {alarmSettings} =
  let
      hour = alarmSettings.hour |> String.toInt |> Result.withDefault 0 |> Encode.int
      minute = alarmSettings.minute |> String.toInt |> Result.withDefault 0 |> Encode.int
      enabled = alarmSettings.enabled |> Encode.bool
  in
    Http.request
      { method = "POST"
      , headers = commonHeaders
      , url = rootUrl ++ "alarm"
      , body = (Http.jsonBody <| Encode.object [("hour", hour), ("minute", minute), ("enabled", enabled) ])
      , expect = Http.expectJson alarmDecoder
      , timeout = Nothing
      , withCredentials = False
      }
    |> Http.send GetAlarmFromServer


postHeating : List Int -> Cmd Msg
postHeating heaters =
  let
      heatersToEncode =
        case heaters |> List.map Encode.int of
          [ chest, hip, feet ] ->
            [ ("chest", chest), ("hip", hip), ("feet", feet) ]
          _ ->
            []
  in
      Http.request
        { method = "POST"
        , headers = [(Http.header "Content-Type" "application/json")]
        , url = rootUrl ++ "heating"
        , body = (Http.jsonBody <| Encode.object heatersToEncode)
        , expect = Http.expectJson heatingDecoder
        , timeout = Nothing
        , withCredentials = False
        }
    |> Http.send GetHeatingFromServer


alarmDecoder : Decoder AlarmSettings
alarmDecoder =
  Decode.map3 AlarmSettings (field "hour" string) (field "minute" string) (field "enabled" bool)


heatingDecoder : Decoder (List Int)
heatingDecoder =
  list int
