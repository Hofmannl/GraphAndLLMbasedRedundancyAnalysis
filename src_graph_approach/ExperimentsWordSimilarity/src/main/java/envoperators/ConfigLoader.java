package envoperators;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class ConfigLoader {

    public static final String CONFIG_PROPERTIES = "config.properties";
    public static final String API_KEY_WORDNIK = "api_key_wordnik";
    public static final String API_KEY_BIGHUGETHESAURUS = "api_key_bighugethesaurus";
    public static final Properties PROPS = ConfigLoader.loadProperties();

    public static Properties loadProperties() {
        try (InputStream input = ConfigLoader.class.getClassLoader().getResourceAsStream(CONFIG_PROPERTIES)) {
            Properties properties = new Properties();
            properties.load(input);
            return properties;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public static String getApiKeyWordnik() throws IOException {
        assert PROPS != null;
        return PROPS.getProperty(API_KEY_WORDNIK);
    }

    public static String getApiKeyBigHugeThesaurus() throws IOException {
        assert PROPS != null;
        return PROPS.getProperty(API_KEY_BIGHUGETHESAURUS);
    }
}
