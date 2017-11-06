module View exposing (view)

import Html exposing (Html, div, button, h1, input, span, select, label, table, tr, td)
import Html.Attributes exposing (class, classList, style, placeholder, value)
import Html.Events exposing (onInput, onClick)

import Svg exposing (Svg, svg)
import Svg.Attributes exposing (x,y,width,height,fill,fontFamily,textAnchor)

import Model exposing (..)
import Model.Ui exposing (..)
import Subscription exposing (..)
import Util exposing (..)

import VirtualDom
import Json.Encode as Json
import Debug exposing (log)


view : Model -> Html Msg
view ({ui} as model) =
  case ui.screen of
    MainScreen ->
      renderMainScreen model


renderMainScreen : Model -> Html Msg
renderMainScreen model =
  [ renderNotification model
  , renderAlarmPanel model
  , renderHeatingPanel model ]
  |> div [ class "PageContainer" ]


renderAlarmPanel : Model -> Html Msg
renderAlarmPanel model =
  let
      heading = h1 [] [ Html.text "Alarm" ]
      hourInput = renderSelect InputAlarmHour (List.range 0 23 |> List.map toString) model.alarmSettings.hour
      minuteInput = renderSelect InputAlarmMinute (List.range 0 11 |> List.map ((*) 5) |> List.map toString |> List.map padStringTwoDigits0) model.alarmSettings.minute
      toggleButton =
        label
        [ onClick (ToggleAlarm (not model.alarmSettings.enabled))
        , class "CheckboxSwitch" ]
        [ input [ Html.Attributes.type_ "checkbox" ] []
        , span [ class "CheckboxSlider CheckboxSlider__Round", onClick (ToggleAlarm (not model.alarmSettings.enabled)) ] [] ]
      row =
        table []
          [ tr []
            [ td [] [ hourInput ]
            , td [ class "AlarmPanel__LeftPadding" ] [ Html.text ":" ]
            , td [] [ minuteInput ]
            , td [] [ toggleButton ] ]
          ]
  in
     div [ class "AlarmPanel" ] [ heading, row ]


renderHeatingPanel : Model -> Html Msg
renderHeatingPanel model =
  let
      heading = h1 [] [ Html.text "Heating" ]
      heaters = List.range 0 2 |> List.map (renderHeaterRow model) |> table []
  in
      div [ class "HeatingPanel" ] [ heading, heaters ]


renderHeaterRow : Model -> Int -> Html Msg
renderHeaterRow model heaterIndex =
  let
      title = case heaterIndex of
        0 -> "Chest"
        1 -> "Hip"
        _ -> "Feet"
      buttons =
        List.range 0 3 |> List.map (renderHeaterButton model heaterIndex)
      children =
        (td [] [ Html.text title ]) :: buttons
  in
      tr [] children


renderHeaterButton : Model -> Int -> Int -> Html Msg
renderHeaterButton model heaterIndex buttonIndex =
  let
      isActive = (getHeaterSetting model heaterIndex) == buttonIndex
      label =
        case buttonIndex of
          0 -> "Off"
          1 -> "25"
          2 -> "50"
          _ -> "100"
      buttonColor =
        case buttonIndex of
          0 -> "#48b"
          1 -> "#fc8"
          2 -> "#fa6"
          _ -> "#f84"
      theButton =
        div
        [ onClick (ChangeHeater heaterIndex buttonIndex)
        , classList [ ("UserSelectNone", True), ("HeatingPanel__Button", True), ("HeatingPanel__ActiveButton", isActive) ]
        , style [ ("background-color", (if isActive then buttonColor else "#eee")) ] ]
        [ Html.text label]
  in
      td [] [ theButton ]


renderSelect : (String -> Msg) -> List String -> String -> Html Msg
renderSelect action options currentValue =
  select
    []
    (options |> List.map (\str -> Html.option [ Html.Attributes.selected (str==currentValue), Html.Attributes.value str ] [ Html.text str ]))


padStringTwoDigits0 : String -> String
padStringTwoDigits0 str =
  case String.length str of
    1 -> "0" ++ str
    _ -> str


renderNotification : Model -> Html Msg
renderNotification model =
  case model.errorMsg of
    Nothing ->
      div [] []

    Just msg ->
      div [ class "Notification" ] [ Html.text msg ]
