package distance;

import java.util.Arrays;
import org.apache.commons.text.similarity.LevenshteinDistance;

// Example of a edit based algorithm
public class LevenshteinDistanceStrategy implements Distance {

    /**
     * Calculates a normalized distance score between two strings using a dynamic programming approach.
     * This method implements a variation of the Levenshtein distance algorithm, which measures the minimum number
     * of single-character edits (insertions, deletions, or substitutions) required to change one word into the other.
     * The distance is then normalized by the maximum length of the two input strings to provide a relative measure of similarity.
     *
     * The normalization ensures that the score is scaled between 0 and 1, where 0 indicates no difference (the strings are identical),
     * and 1 indicates the maximum possible distance relative to the length of the longer string.
     *
     * The cost of substitution is determined by the `costOfSubstitution` method, which needs to be defined to use
     * this method correctly. This allows for customization based on specific character changes.
     *
     * Based on: <a href="https://www.baeldung.com/java-levenshtein-distance">How to Calculate Levenshtein Distance in Java?</a>
     * and <a href="https://stackoverflow.com/questions/6087281/similarity-score-levenshtein">stack overflow: Similarity Score - Levenshtein</a>
     *
     * @param word1 the first string to compare; should not be null and should represent text data.
     * @param word2 the second string to compare; should not be null and should represent text data.
     * @return a double value representing the normalized edit distance, scaled such that 1 represents identical strings
     * and 0 represents the maximum difference.
     */
    @Override
    public double calcWordDistanceAsDouble(String word1, String word2) {
        //Baase on https://www.baeldung.com/java-levenshtein-distance
        int[][] dp = new int[word1.length() + 1][word2.length() + 1];

        for (int i = 0; i <= word1.length(); i++) {
            for (int j = 0; j <= word2.length(); j++) {
                if (i == 0) {
                    dp[i][j] = j;
                }
                else if (j == 0) {
                    dp[i][j] = i;
                }
                else {
                    dp[i][j] = min(dp[i - 1][j - 1]
                                    + costOfSubstitution(word1.charAt(i - 1), word2.charAt(j - 1)),
                            dp[i - 1][j] + 1,
                            dp[i][j - 1] + 1);
                }
            }
        }

        double score = ((double) dp[word1.length()][word2.length()]) / (Math.max(word1.length(), word2.length()));
        score = Math.abs(score - 1);
        return score;
    }

    private int min(int... numbers) {
        return Arrays.stream(numbers)
                .min().orElse(Integer.MAX_VALUE);
    }

    private int costOfSubstitution(char a, char b) {
        return a == b ? 0 : 1;
    }
}
