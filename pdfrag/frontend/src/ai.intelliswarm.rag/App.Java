--module-path "C:\javafx-sdk-17.0.1\lib" --add-modules javafx.controls,javafx.fxml 

String responseBody = response.body().string();
String answer = new Gson().fromJson(responseBody, JsonObject.class).get("answer").getAsString();
return answer; 