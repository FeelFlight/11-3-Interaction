module HttpClient exposing (getAlarm, postAlarm)

import Http exposing (expectStringResponse)
import Json.Decode as Decode exposing (Decoder,field,string,bool,list,int)
import Json.Encode as Encode
import Debug exposing (log)

import Model exposing (..)

import Subscription exposing (..)


-- rootUrl = "http://172.26.2.68:8036/api/v1.0/"
rootUrl = "http://172.26.2.195:8036/api/v1.0/"
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


getHeating : Model -> Cmd Msg
getHeating model =
  Http.request
    { method = "GET"
    , headers = commonHeaders
    , url = rootUrl ++ "heating"
    , body = Http.emptyBody
    , expect = Http.expectJson heatingDecoder
    , timeout = Nothing
    , withCredentials = False
    }
  |> Http.send GetHeatingFromServer


alarmDecoder : Decoder AlarmSettings
alarmDecoder =
  Decode.map3 AlarmSettings (field "hour" string) (field "minute" string) (field "enabled" bool)


-- postHeating : List Int -> Http.Request (List Int)
-- postHeating heaters =
--   Http.request
--     { method = "POST"
--     , headers = [(Http.header "Content-Type" "application/json")]
--     , url = rootUrl ++ "heating"
--     , body = (Http.jsonBody <| Encode.object [("heating", (heaters |> List.map toString |> String.concat |> Encode.string)) ])
--     , expect = Http.expectJson heatingDecoder
--     , timeout = Nothing
--     , withCredentials = False
--     }


heatingDecoder : Decoder (List Int)
heatingDecoder =
  list int