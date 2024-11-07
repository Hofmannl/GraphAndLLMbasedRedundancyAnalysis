package wordfinders;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.http.HttpResponse.BodyHandlers;
import java.util.LinkedList;
import java.util.List;

import envoperators.ConfigLoader;
import org.json.JSONArray;
import org.json.JSONObject;

public class WordnikConnector implements WordRelationshipFinder {
    public static final String URL;
    public static final String RELATED_WORDS_USE_CANONICAL_FALSE_LIMIT_PER_RELATIONSHIP;
    private static final String API_KEY;

    static {
        try {
            URL = "https://api.wordnik.com/v4/word.json/";
            RELATED_WORDS_USE_CANONICAL_FALSE_LIMIT_PER_RELATIONSHIP = "/relatedWords?useCanonical=false&relationshipTypes=synonym&limitPerRelationshipType=100&api_key=";
            API_KEY = ConfigLoader.getApiKeyWordnik();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    @Override
    public String[] getSimilarWords(String word) {
        List<String> similarWords = new LinkedList<String>();
        if (API_KEY != null) {
            HttpClient client = HttpClient.newHttpClient();


            try {
                URI uri = URI.create(URL + word + RELATED_WORDS_USE_CANONICAL_FALSE_LIMIT_PER_RELATIONSHIP + API_KEY);
                HttpRequest request = HttpRequest.newBuilder()
                        .uri(uri)
                        .GET()
                        .build();

                HttpResponse<String> response = client.send(request, BodyHandlers.ofString());

                if (response.statusCode() == 200) {
                    // Parse the JSON response
                    JSONArray jsonArray = new JSONArray(response.body());
                    for (int i = 0; i < jsonArray.length(); i++) {
                        JSONObject relationType = jsonArray.getJSONObject(i);
                        JSONArray words = relationType.getJSONArray("words");
                        System.out.println("Relationship type: " + relationType.getString("relationshipType"));
                        for (int j = 0; j < words.length(); j++) {
                            JSONObject wordObj = jsonArray.getJSONObject(i);
                            similarWords.add(wordObj.getString("word"));
                        }
                    }
                } else {
                    System.out.println("Failed to retrieve data: HTTP error code " + response.statusCode());
                }
            } catch (IOException | InterruptedException e) {
                e.printStackTrace();
            }
        }

        return similarWords.toArray(new String[0]);
    }
}
