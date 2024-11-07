package distance;

import info.debatty.java.stringsimilarity.RatcliffObershelp;

//Example for a Sequence based algorithm - Implementation from: https://github.com/tdebatty/java-string-similarity?tab=readme-ov-file
public class RatcliffObershelpSimilarity implements Distance{

    /**
     * Ratcliff/Obershelp Pattern Recognition (Gestalt Pattern Matching)
     *
     * This string-matching algorithm determines the similarity between two strings. It was developed by John W. Ratcliff and
     * John A. Obershelp and was first published in Dr. Dobb's Journal in July 1988. The algorithm is commonly known for its
     * application in diff utilities, primarily used in text comparison and pattern recognition tasks.
     *
     * The Ratcliff/Obershelp algorithm computes the similarity score between two strings, which is a measure of the
     * proportion of matching characters between the sequences, including recursively matched characters in the longest
     * common subsequences. The resulting similarity value is a double precision number in the range [0.0, 1.0], where 0.0
     * indicates no similarity (completely different strings) and 1.0 indicates identical strings.
     *
     * The "distance" between two strings, based on this algorithm, can be calculated as (1 - similarity score), where a
     * value of 0 indicates no difference, and a value close to 1 suggests a greater dissimilarity.
     *
     * Based on: <a href="https://github.com/tdebatty/java-string-similarity?tab=readme-ov-file">Project "java-string-similarity"</a>
     *
     *  @param word1 the first string to compare; should be a non-null, plain text string.
     *  @param word2 the second string to compare; should be a non-null, plain text string.
     *  @return the cosine similarity between the two strings, ranging from 0.0 to 1.0, where 1.0 indicates identical
     */
    @Override
    public double calcWordDistanceAsDouble(String word1, String word2) {
        RatcliffObershelp ro = new RatcliffObershelp();
        double score = ro.similarity(word1, word2);
        return score;
    }
}
