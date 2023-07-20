package com.example.predictionapp;

import static android.service.controls.ControlsProviderService.TAG;

import android.os.Build;
import android.util.Log;
import android.widget.Toast;

import androidx.annotation.RequiresApi;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;
import okio.ByteString;

import android.content.Context;

public class FileTransferWebSocketClient {
    private WebSocket webSocket;
    private Context context;

    public FileTransferWebSocketClient(Context context) {
        this.context = context;
    }

    public void connectWebSocket() {

        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder()
                .url("ws://192.168.8.169:9999")
                .build();

        WebSocketListener webSocketListener = new WebSocketListener() {
            @RequiresApi(api = Build.VERSION_CODES.R)
            @Override
            public void onOpen(WebSocket webSocket, okhttp3.Response response) {
                Log.d("webSocket", "WebSocket connection is open.");
            }

            @Override
            public void onMessage(WebSocket webSocket, String text) {
                // Handle received messages here (in case you need to exchange control messages).
                Log.d("SocketMessage", "Received text message from server: " + text);
            }

            public void onMessage(WebSocket webSocket, ByteString bytes) {
                // Handle received file chunks here.
                // In this example, we'll write the chunks to a file in internal storage.

                // Get the app's internal storage directory from the provided Context
                File internalStorageDir = context.getFilesDir();

                // Create a File object with the desired file name "received_file.txt"
                File receivedFile = new File(internalStorageDir, "received_file.txt");

                try (FileOutputStream fos = new FileOutputStream(receivedFile, true)) {
                    fos.write(bytes.toByteArray());
                    Log.d("SocketMessage", "Received file from server and saved to internal storage");
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }

            @Override
            public void onClosing(WebSocket webSocket, int code, String reason) {
                // WebSocket connection is closing.
                Log.d("webSocket", "web socket connection is closed: " + code + reason);

            }

            @Override
            public void onFailure(WebSocket webSocket, Throwable t, okhttp3.Response response) {
                // Handle connection failure here.
                Log.d("SocketMessage", "connection is failed: " + t);

            }
        };

        webSocket = client.newWebSocket(request, webSocketListener);
    }

    public void disconnectWebSocket() {
        if (webSocket != null) {
            webSocket.cancel();
        }
    }
}
