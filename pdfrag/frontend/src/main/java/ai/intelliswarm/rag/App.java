package ai.intelliswarm.rag;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import okhttp3.*;
import com.google.gson.*;
import java.util.concurrent.TimeUnit;

public class App extends Application {
    private static final OkHttpClient client = new OkHttpClient.Builder()
            .connectTimeout(3, TimeUnit.MINUTES)
            .writeTimeout(3, TimeUnit.MINUTES)
            .readTimeout(3, TimeUnit.MINUTES)
            .build();
    private static final String BACKEND_URL = "http://localhost:8000/ask"; // Adjust if your endpoint is different

    @Override
    public void start(Stage stage) {
        TextField input = new TextField();
        Button askBtn = new Button("Ask");
        TextArea output = new TextArea();

        askBtn.setOnAction(e -> {
            String question = input.getText();
            output.setText("Waiting for response...");
            new Thread(() -> {
                try {
                    String response = askBackend(question);
                    javafx.application.Platform.runLater(() -> output.setText(response));
                } catch (Exception ex) {
                    javafx.application.Platform.runLater(() -> output.setText("Error: " + ex.getMessage()));
                }
            }).start();
        });

        VBox root = new VBox(10, input, askBtn, output);
        stage.setScene(new Scene(root, 500, 400));
        stage.setTitle("Local RAG UI");
        stage.show();
    }

    private String askBackend(String question) throws Exception {
        MediaType JSON = MediaType.parse("application/json; charset=utf-8");
        String json = new Gson().toJson(new Question(question));
        RequestBody body = RequestBody.create(json, JSON);
        Request request = new Request.Builder()
                .url(BACKEND_URL)
                .post(body)
                .build();
        try (Response response = client.newCall(request).execute()) {
            if (!response.isSuccessful()) throw new Exception("Unexpected code " + response);
            return response.body().string();
        }
    }

    static class Question {
        String question;
        Question(String question) { this.question = question; }
    }

    public static void main(String[] args) {
        launch();
    }
}
