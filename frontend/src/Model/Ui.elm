module Model.Ui exposing (..)


type alias Ui =
  { screen : Screen }


type Screen = MainScreen

initialUi : Ui
initialUi =
  { screen = MainScreen }
