package com.example.predictionapp;

import android.util.Log;

import java.io.FileOutputStream;
import java.io.IOException;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;
import okio.ByteString;

public class WebSocketClient extends WebSocketListener {

    private static final String SERVER_URL = "ws://192.168.8.169:9999";
    private WebSocket webSocket;

    public void start() {
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder().url(SERVER_URL).build();
        webSocket = client.newWebSocket(request, this);
    }

    @Override
    public void onMessage(WebSocket webSocket, String text) {
        // Handle the message received from the server
        System.out.println("Received from server: " + text);
    }
    @Override
    public void onMessage(WebSocket webSocket, ByteString bytes) {
        // Handle received file chunks here.
        // In this example, we'll write the chunks to a file.
        try (FileOutputStream fos = new FileOutputStream("received_file.txt", true)) {
            fos.write(bytes.toByteArray());
            Log.d("SocketMessage", "Received text file from server");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    @Override
    public void onClosing(WebSocket webSocket, int code, String reason) {
        // WebSocket connection is closing.
        Log.d("webSocket", "web socket connection is colosed: " + code + reason);

    }

    @Override
    public void onFailure(WebSocket webSocket, Throwable t, okhttp3.Response response) {
        // Handle connection failure here.
        Log.d("SocketMessage", "connection is failed: " + response);

    }

    public void sendMessage(String message) {
        if (webSocket != null) {
            webSocket.send(message);
        }
    }

    public void close() {
        if (webSocket != null) {
            webSocket.close(1000, "Goodbye!");
        }
    }
}
