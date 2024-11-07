package distance;

import org.apache.commons.text.similarity.CosineSimilarity;

import java.util.HashMap;
import java.util.Map;

//Example for a Token based algorithm
public class CosineSimilarityStrategy implements Distance {

    /**
     * Calculates the cosine similarity between two strings as a double precision value, representing the
     * distance between the words. This method transforms each input string into a vector where each dimension corresponds
     * to a word from the string and the magnitude in that dimension represents the frequency of the word.
     *
     * The method first normalizes both strings to lower case to ensure case insensitivity, then splits each string
     * into words based on spaces. Each word's frequency is counted and stored in a map, which is then used to
     * populate another map that represents the vector for cosine similarity computation.
     *
     * The cosine similarity is computed between these two vectors, with the result indicating how similar the two
     * strings are. A value of 1.0 means the strings are identical in terms of word frequency (though not necessarily
     * in order), while a value of 0 indicates no similarity.
     *
     * @param word1 the first string to compare
     * @param word2 the second string to compare
     * @return the cosine similarity between the two strings, ranging from 0.0 to 1.0
     */
    @Override
    public double calcWordDistanceAsDouble(String word1, String word2) {
        CosineSimilarity cosineSimilarity = new CosineSimilarity();

        word1 = word1.toLowerCase();
        word2 = word2.toLowerCase();
        String[] words1 = word1.split(" ");
        String[] words2 = word2.split(" ");

        Map<String, Integer> wordCount1 = new HashMap<>();
        calcWordsCount(words1, wordCount1);
        Map<String, Integer> wordCount2 = new HashMap<>();
        calcWordsCount(words2, wordCount2);

        Map<CharSequence, Integer> vectorWord1 = new HashMap<>();
        Map<CharSequence, Integer> vectorWord2 = new HashMap<>();
        fillMap(wordCount1, vectorWord1);
        fillMap(wordCount2, vectorWord2);

        return cosineSimilarity.cosineSimilarity(vectorWord1, vectorWord2);
    }

    private void fillMap(Map<String, Integer> wordCount1, Map<CharSequence, Integer> vectorWord1) {
        for (String key : wordCount1.keySet()) {
            Integer count = wordCount1.get(key);
            vectorWord1.put(key, count);
        }
    }

    private void calcWordsCount(String[] words1, Map<String, Integer> wordCount) {
        for (String word : words1) {
            if (!word.isEmpty()) {
                wordCount.put(word, wordCount.getOrDefault(word, 0) + 1);
            }
        }
    }
}
