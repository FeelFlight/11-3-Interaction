module Main exposing (..)

import Html exposing (Html)

import Model exposing (Model,initialModel)
import Update exposing (update)
import View exposing (view)
import Subscription exposing (subscriptions)
import HttpClient

--------------------------------------------------------------------------- MAIN

main : Program Never Model Subscription.Msg
main =
  Html.program
  { init = (initialModel, HttpClient.getAlarm initialModel)
  , update = update
  , view = view
  , subscriptions = subscriptions }
