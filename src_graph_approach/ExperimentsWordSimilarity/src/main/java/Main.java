import distance.CosineSimilarityStrategy;
import distance.LevenshteinDistanceStrategy;
import distance.RatcliffObershelpSimilarity;
import wordfinders.BigHugeThesaurus;
import wordfinders.DatamuseConnector;
import wordfinders.WordnikConnector;

public class Main {
    public static void main(String[] args) {
        /*
        * I implemented two apporaches:
        *   1.) Calc the similarity on different stategies
        *   2.) Look up the word searched for in a online dictonary and then look if the second word is contained in the answer of the response
         */


        //Determining what is for use the significant  for Leven., Cos. and Ratc.
        LevenshteinDistanceStrategy levenDistance = new LevenshteinDistanceStrategy();
        System.out.println("Similarity based on the Levenshtein Distance Alg.: " + levenDistance.calcWordDistanceAsDouble("webpage", "website"));

        //This only works with full sentences like: "This webpage is great" and "This website is great"
        CosineSimilarityStrategy cosineSimilarity = new CosineSimilarityStrategy();
        System.out.println("Cosine Similarity: " + cosineSimilarity.calcWordDistanceAsDouble("webpage", "website"));

        RatcliffObershelpSimilarity ratcliffObershelpSimilarity = new RatcliffObershelpSimilarity();
        System.out.println("Similarity based on the Ratcliff Obershelp Alg.: " + ratcliffObershelpSimilarity.calcWordDistanceAsDouble("webpage", "website"));

        //Maybe use 2 or 3 to check if a word is similar but look for good ones (as here just the first is good and the other twos not so
        //Datamuse --> It is free accessable and I assume it is the best
        String[] words = new DatamuseConnector().getSimilarWords("webpage");
        String wordToCompare = "website";
        String contained = "no";
        for (String word : words) {
            if (word.equals(wordToCompare)) {
                contained = "yes";
                break;
            }
        }

        System.out.println("Word is contained: " + contained);

        // Wirdnik Connector --> To get the api key needs 7 days... (until now we have no access) --> Maybe an alternative?
        words = new WordnikConnector().getSimilarWords("Earth");
        wordToCompare = "website";
        contained = "no";
        for (String word : words) {
            if (word.equals(wordToCompare)) {
                contained = "yes";
                break;
            }
        }

        System.out.println("Word is contained: " + contained);

        // BigHugeThesaurus Connector --> Looking at the output of similar words this is not a good dictonary --> Maybe an alternative?
        words = new BigHugeThesaurus().getSimilarWords("webpage");
        wordToCompare = "website";
        contained = "no";
        for (String word : words) {
            if (word.equals(wordToCompare)) {
                contained = "yes";
                break;
            }
        }

        System.out.println("Word is contained: " + contained);
    }
}