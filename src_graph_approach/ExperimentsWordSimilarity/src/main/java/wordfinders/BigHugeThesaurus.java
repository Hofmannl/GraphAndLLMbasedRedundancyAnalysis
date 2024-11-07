package wordfinders;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;

import envoperators.ConfigLoader;
import org.json.JSONArray;
import org.json.JSONObject;
import wordfinders.WordRelationshipFinder;

public class BigHugeThesaurus implements WordRelationshipFinder {

    // Big Huge Thesaurus API endpoint
    private static final String API_URL;

    static {
        try {
            API_URL = "https://words.bighugelabs.com/api/2/" + ConfigLoader.getApiKeyBigHugeThesaurus();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public String[] getSimilarWords(String word) {
        List<String> similarWords = new ArrayList<>();

        try {
            HttpClient client = HttpClient.newHttpClient();
            URI uri = URI.create(API_URL + "/" + word + "/json");

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(uri)
                    .GET()
                    .build();

            // Send request and handle response
            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

            // Check response code
            if (response.statusCode() == 200) {
                // Parse JSON response
                JSONObject jsonObject = new JSONObject(response.body());
                JSONObject nounObject = jsonObject.getJSONObject("noun");
                JSONArray synonymsArray = nounObject.getJSONArray("syn");
                for (int i = 0; i < synonymsArray.length(); i++) {
                    similarWords.add(synonymsArray.getString(i));
                }
            } else {
                System.out.println("Failed to retrieve data: HTTP error code " + response.statusCode());
            }
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }

        return similarWords.toArray(new String[0]);
    }
}
