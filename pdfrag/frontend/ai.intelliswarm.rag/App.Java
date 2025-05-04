public class App extends Application {
    @Override
    public void start(Stage stage) {
        TextField input = new TextField();
        Button askBtn = new Button("Ask");
        TextArea output = new TextArea();

        askBtn.setOnAction(e -> {
            // Call backend API via OkHttp and display output
        });

        VBox root = new VBox(10, input, askBtn, output);
        stage.setScene(new Scene(root, 500, 400));
        stage.setTitle("Local RAG UI");
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}
