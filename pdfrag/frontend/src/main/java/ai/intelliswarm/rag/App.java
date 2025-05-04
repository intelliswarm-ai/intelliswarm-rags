package ai.intelliswarm.rag;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.image.Image;
import javafx.scene.image.ImageView;
import javafx.scene.input.*;
import javafx.scene.layout.*;
import javafx.stage.Stage;
import okhttp3.*;
import okio.BufferedSource;
import java.io.*;
import java.nio.file.Files;
import java.util.concurrent.TimeUnit;
import javafx.embed.swing.SwingFXUtils;
import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;

public class App extends Application {
    private static final OkHttpClient client = new OkHttpClient.Builder()
            .connectTimeout(3, TimeUnit.MINUTES)
            .writeTimeout(3, TimeUnit.MINUTES)
            .readTimeout(3, TimeUnit.MINUTES)
            .build();
    private static final String BACKEND_URL = "http://localhost:8000/ask";
    private File selectedImageFile = null;
    private TextArea output;
    private ImageView imageView;

    @Override
    public void start(Stage stage) {
        TextField input = new TextField();
        Button askBtn = new Button("Ask");
        output = new TextArea();
        output.setEditable(false);

        // Image preview
        imageView = new ImageView();
        imageView.setFitWidth(200);
        imageView.setPreserveRatio(true);

        Label dropLabel = new Label("Drag and drop or paste (Ctrl+V) an image here");
        dropLabel.setStyle("-fx-border-color: gray; -fx-padding: 20; -fx-alignment: center;");
        dropLabel.setMaxWidth(Double.MAX_VALUE);
        dropLabel.setAlignment(Pos.CENTER);

        // Submit on Enter
        input.setOnAction(e -> askBtn.fire());

        // Ask button action
        askBtn.setOnAction(e -> {
            String question = input.getText();
            output.setText("Waiting for response...");
            new Thread(() -> {
                String response = askWithImage(question, selectedImageFile);
                Platform.runLater(() -> output.setText(response));
            }).start();
        });

        // Drag and drop image
        dropLabel.setOnDragOver(event -> {
            if (event.getGestureSource() != dropLabel && event.getDragboard().hasFiles()) {
                event.acceptTransferModes(TransferMode.COPY);
            }
            event.consume();
        });

        dropLabel.setOnDragDropped(event -> {
            Dragboard db = event.getDragboard();
            boolean success = false;
            if (db.hasFiles()) {
                File file = db.getFiles().get(0);
                if (isImageFile(file)) {
                    setSelectedImageFile(file);
                    output.setText("Image ready: " + file.getName());
                    success = true;
                } else {
                    output.setText("Please drop an image file.");
                }
            }
            event.setDropCompleted(success);
            event.consume();
        });

        VBox root = new VBox(10, input, askBtn, dropLabel, imageView, output);
        root.setPrefWidth(500);
        root.setPrefHeight(500);
        root.setAlignment(Pos.TOP_CENTER);

        // Clipboard paste support (Ctrl+V)
        output.setOnKeyPressed(event -> {
            if (event.getCode() == KeyCode.V && event.isControlDown()) {
                Clipboard clipboard = Clipboard.getSystemClipboard();
                if (clipboard.hasImage()) {
                    Image img = clipboard.getImage();
                    imageView.setImage(img);
                    output.setText("Image pasted from clipboard.");
                    // Save the image to a temporary file for upload
                    try {
                        File tempFile = File.createTempFile("pasted_image", ".png");
                        tempFile.deleteOnExit();
                        BufferedImage bImage = SwingFXUtils.fromFXImage(img, null);
                        ImageIO.write(bImage, "png", tempFile);
                        selectedImageFile = tempFile;
                    } catch (Exception ex) {
                        output.setText("Failed to save pasted image: " + ex.getMessage());
                    }
                }
            }
        });
        Platform.runLater(output::requestFocus);

        stage.setScene(new Scene(root));
        stage.setTitle("Intelliswarm.ai RAG UI");
        stage.show();
    }

    private boolean isImageFile(File file) {
        String name = file.getName().toLowerCase();
        return name.endsWith(".png") || name.endsWith(".jpg") || name.endsWith(".jpeg") || name.endsWith(".gif");
    }

    private void setSelectedImageFile(File file) {
        selectedImageFile = file;
        Image img = new Image(file.toURI().toString());
        imageView.setImage(img);
    }

    private String askWithImage(String question, File imageFile) {
        try {
            MultipartBody.Builder builder = new MultipartBody.Builder()
                    .setType(MultipartBody.FORM)
                    .addFormDataPart("question", question);

            if (imageFile != null) {
                builder.addFormDataPart(
                    "file",
                    imageFile.getName(),
                    RequestBody.create(imageFile, MediaType.parse(Files.probeContentType(imageFile.toPath()))));
            }

            RequestBody requestBody = builder.build();

            Request request = new Request.Builder()
                    .url(BACKEND_URL)
                    .post(requestBody)
                    .build();

            // Streaming response handling
            try (Response response = client.newCall(request).execute()) {
                if (!response.isSuccessful()) throw new IOException("Unexpected code " + response);

                BufferedSource source = response.body().source();
                StringBuilder answer = new StringBuilder();
                while (!source.exhausted()) {
                    String chunk = source.readUtf8Line();
                    if (chunk != null && !chunk.isEmpty()) {
                        answer.append(chunk).append(" ");
                        String[] words = answer.toString().split("\\s+");
                        StringBuilder formatted = new StringBuilder();
                        for (int i = 0; i < words.length; i++) {
                            formatted.append(words[i]);
                            if ((i + 1) % 40 == 0) {
                                formatted.append('\n');
                            } else {
                                formatted.append(' ');
                            }
                        }
                        Platform.runLater(() -> output.setText(formatted.toString().trim()));
                    }
                }
                return answer.toString();
            }
        } catch (Exception e) {
            return "Error: " + e.getMessage();
        }
    }

    public static void main(String[] args) {
        launch();
    }
}
