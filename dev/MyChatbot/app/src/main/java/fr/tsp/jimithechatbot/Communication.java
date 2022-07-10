package fr.tsp.jimithechatbot;

import android.os.StrictMode;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.*;

public class Communication {

    private final String url;

    public Communication(String url, String sentence, String macAddress) {
        // Initialize the object Request
        this.url = url + String.format("?question=%s;mac=%s", fillSpace(sentence), macAddress);
    }

    public static String fillSpace(String str) {
        StringBuilder rep = new StringBuilder();
        for(int i=0; i<str.length(); i++) {
            if (str.charAt(i) == ' ') {
                rep.append("_");
            }
            else {
                rep.append(str.charAt(i));
            }
        }
        return rep.toString();
    }

    public String html(){
        // Return the html code of the page at url
        try {
            return get(this.url);
        } catch (IOException e) {
            //e.printStackTrace();
            return MainActivity.error;
        }
    }

    private static String readIt(InputStream is) throws IOException {
        BufferedReader r = new BufferedReader(new InputStreamReader(is));
        StringBuilder response = new StringBuilder();
        String line;
        while ((line = r.readLine()) != null) {
            response.append(line).append('\n');
        }
        return response.substring(0, response.length()-1);
    }

    public static String get(String url) throws IOException {
        // Get content of the page url
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        InputStream is = null;
        try {
            final HttpURLConnection conn = (HttpURLConnection) new URL(url).openConnection();
            conn.setReadTimeout(300000 /* milliseconds */);
            conn.setConnectTimeout(300000 /* milliseconds */);
            conn.setRequestMethod("GET"); conn.setDoInput(true);
            // Starts the query
            conn.connect();
            is = conn.getInputStream();
            //Read the InputStream and save it in a string
            return readIt(is);
        } finally {
            // Makes sure that the InputStream is closed after the app is // finished using it.
            if (is != null) {
                is.close();
            }
        }
    }

}
