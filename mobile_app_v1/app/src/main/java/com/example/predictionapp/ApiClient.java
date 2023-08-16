package com.example.predictionapp;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import java.io.IOException;
public class ApiClient {
    private static final String BASE_URL = "http://20.193.137.241:3000/api/";

    public static String fetchDataByCategory(int categoryNumber) throws IOException {
        OkHttpClient client = new OkHttpClient();
        String endpoint = "allItems?category=" + categoryNumber;
        Request request = new Request.Builder()
                .url(BASE_URL + endpoint)
                .build();

        try (Response response = client.newCall(request).execute()) {
            if (response.isSuccessful() && response.body() != null) {
                return response.body().string();
            }
        }

        return null;
    }
}

