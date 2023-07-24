
package com.example.predictionapp;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;

public class WebSocketAndroidClient extends WebSocketListener {
    private WebSocket webSocket;
    public  void connect(){
        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder().url("ws://192.168.8.169:9999").build();
        WebSocketAndroidClient socketListener = new WebSocketAndroidClient();
        WebSocket ws = client.newWebSocket(request, socketListener);

        // Send messages asynchronously without waiting for the server's response
        String message1 = "Hello from Android 1!";
        String message2 = "Hello from Android 2!";
        ws.send(message1);
        ws.send(message2);

        webSocket = client.newWebSocket(request,socketListener);

    }
    @Override
    public void onOpen(WebSocket webSocket, Response response) {
        // WebSocket connection is established
        System.out.println("WebSocket connection opened!");
    }

    @Override
    public void onMessage(WebSocket webSocket, String text) {
        // Received a message from the Python server
        System.out.println("Received from Python: " + text);

    }

    @Override
    public void onClosed(WebSocket webSocket, int code, String reason) {
        // WebSocket connection is closed
        System.out.println("WebSocket connection closed!");
    }

    public void disconnect(){
        if (webSocket != null) {
            webSocket.cancel();
        }
    }
}
