package com.example.predictionapp;

import android.content.Context;
import android.util.Log;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;

public class BiDirClient {

    private Socket socket;
    private Context context;
    private String host;
    private int port;

    private byte[] receivedData;

    public BiDirClient(Context context, String host, int port) {
        this.context = context;
        this.host = host;
        this.port = port;
    }

    public void connectAndReceiveFile() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    // Create a socket connection to the server
                    socket = new Socket(host, port);
                    Log.d("SocketMessage", "Socket connection is established.");

                    // Receive the file from the server
                    InputStream inputStream = socket.getInputStream();
                    byte[] buffer = new byte[1024];
                    int bytesRead;
                    ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                    while ((bytesRead = inputStream.read(buffer)) != -1) {
                        byteArrayOutputStream.write(buffer, 0, bytesRead);
                    }

                    // Save the received data in the global variable
                    receivedData = byteArrayOutputStream.toByteArray();

                    // Log the size and content of the received text file
                    Log.d("SocketMessage", "Received text file size: " + receivedData.length + " bytes");
                    Log.d("SocketMessage", "Received text file content: " + new String(receivedData));

                    // Save the received text file to internal storage (optional)
                    File internalStorageDir = context.getFilesDir();
                    File receivedFile = new File(internalStorageDir, "received_file.txt");
                    FileOutputStream fos = new FileOutputStream(receivedFile);
                    fos.write(receivedData);
                    fos.close();
                    Log.d("SocketMessage", "Received text file saved to internal storage: " + receivedFile.getAbsolutePath());
                    // Close the socket connection
                    socket.close();
                    Log.d("SocketMessage", "Socket connection is closed.");
                } catch (IOException e) {
                    e.printStackTrace();
                    Log.d("SocketMessage", "Socket connection failed: " + e.getMessage());
                }
            }
        }).start();
    }
    public void sendJSONFileToServer() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    // Create a socket connection to the server
                    socket = new Socket(host, port);
                    Log.d("SocketMessage", "Socket connection is established.");

                    // Read the JSON data from the JSON file
                    File internalStorageDir = context.getFilesDir();
                    File jsonFile = new File(internalStorageDir, "user_data.json");
                    FileInputStream fis = new FileInputStream(jsonFile);
                    byte[] buffer = new byte[1024];
                    int bytesRead;
                    ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                    while ((bytesRead = fis.read(buffer)) != -1) {
                        byteArrayOutputStream.write(buffer, 0, bytesRead);
                    }
                    byte[] jsonData = byteArrayOutputStream.toByteArray();

                    // Send the JSON data to the server
                    OutputStream outputStream = socket.getOutputStream();
                    outputStream.write(jsonData);

                    // Close the socket connection
                    socket.close();
                    Log.d("SocketMessage", "Socket connection is closed.");
                } catch (IOException e) {
                    e.printStackTrace();
                    Log.d("SocketMessage", "Socket connection failed: " + e.getMessage());
                }
            }
        }).start();
    }
    // Method to get the received data from the global variable
    /*public byte[] getReceivedData() {
        return receivedData;
    }*/
/*
    public void sendFileToServer() {
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    // Create a socket connection to the server
                    socket = new Socket(host, port);
                    Log.d("SocketMessage", "Socket connection is established.");

                    // Read the received data from the global variable
                    byte[] receivedData = getReceivedData();

                    // Send the data to the server
                    OutputStream outputStream = socket.getOutputStream();
                    outputStream.write(receivedData);

                    // Save the received data to a text file on the server
                    FileOutputStream fos = new FileOutputStream("received_data.txt");
                    fos.write(receivedData);
                    fos.close();
                    Log.d("SocketMessage", "Received data saved to file on the server.");


                    // Close the socket connection
                    socket.close();
                    Log.d("SocketMessage", "Socket connection is closed.");
                } catch (IOException e) {
                    e.printStackTrace();
                    Log.d("SocketMessage", "Socket connection failed: " + e.getMessage());
                }
            }
        }).start();
    }*/

    public void closeSocket() {
        try {
            if (socket != null && !socket.isClosed()) {
                socket.close();
                Log.d("SocketMessage", "Socket connection is closed manually.");
            }
        } catch (IOException e) {
            e.printStackTrace();
            Log.d("SocketMessage", "Error while closing socket: " + e.getMessage());
        }
    }
}
