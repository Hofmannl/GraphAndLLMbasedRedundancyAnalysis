package wordfinders;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.util.ArrayList;
import java.util.List;
import org.json.JSONArray;
import org.json.JSONObject;

public class DatamuseConnector implements WordRelationshipFinder {

    @Override
    public String[] getSimilarWords(String word) {
        HttpClient client = HttpClient.newHttpClient();
        List<String> similarWords = new ArrayList<>();

        try {
            URI uri = URI.create("https://api.datamuse.com/words?ml=" + word);
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(uri)
                    .GET()
                    .build();

            HttpResponse<String> response = client.send(request, BodyHandlers.ofString());

            // Check if the response code is HTTP OK (200)
            if (response.statusCode() == 200) {
                // Parse the JSON response
                JSONArray jsonArray = new JSONArray(response.body());
                for (int i = 0; i < jsonArray.length(); i++) {
                    JSONObject wordObj = jsonArray.getJSONObject(i);
                    similarWords.add(wordObj.getString("word"));
                }
            } else {
                System.out.println("Failed to retrieve data: HTTP error code " + response.statusCode());
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        // Convert List to array
        return similarWords.toArray(new String[0]);
    }

}
