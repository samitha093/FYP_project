package com.example.predictionapp;

import static android.service.controls.ControlsProviderService.TAG;


import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.ActivityInfo;
import android.content.res.ColorStateList;
import android.graphics.Color;
import android.os.AsyncTask;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.FrameLayout;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AlertDialog;
import androidx.core.content.ContextCompat;

import com.google.android.material.bottomnavigation.BottomNavigationView;
import com.google.android.material.snackbar.Snackbar;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.SocketException;
import com.journeyapps.barcodescanner.CaptureManager;
import com.journeyapps.barcodescanner.DecoratedBarcodeView;


public class ScanQRCodeActivity extends Activity {
    private Button btnConnectToCart;
    private Button btnDisconnectCart;
    private FrameLayout frameLayoutScanner;
    private boolean isConnected = false;
    private BottomNavigationView bottomNavigationView;
    private TextView tvGreeting;
    private boolean isQRRead;
    private String host;
    private int port;
    private Socket socket;
    private DecoratedBarcodeView barcodeView;
    private CaptureManager captureManager;
    private boolean isScannerVisible = false;
    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.qr_scan_layout);
        // Initialize views
        tvGreeting = findViewById(R.id.tvGreeting);
        tvGreeting.setText("Hi User, Welcome to smart cart app");


        // Initialize views
        tvGreeting = findViewById(R.id.tvGreeting);
        tvGreeting = findViewById(R.id.tvGreeting);
        try {
            FileInputStream fis = openFileInput("user_data.json");
            InputStreamReader isr = new InputStreamReader(fis);
            BufferedReader br = new BufferedReader(isr);
            StringBuilder sb = new StringBuilder();
            String line;

            while ((line = br.readLine()) != null) {
                sb.append(line);
            }

            br.close();
            isr.close();
            fis.close();

            // Parse JSON data
            JSONObject userData = new JSONObject(sb.toString());
            String name = userData.getString("name");

            if (name != null && !name.isEmpty()) {
                String greeting = "Hi " + name + ", Welcome to smart cart app";
                tvGreeting.setText(greeting);
            } else {
                tvGreeting.setText("Hi User, Welcome to smart cart app");
            }
        } catch (JSONException e) {
            e.printStackTrace();
        } catch (FileNotFoundException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        btnConnectToCart = findViewById(R.id.btnConnectToCart);
        btnDisconnectCart = findViewById(R.id.btnDisconnectCart);
        frameLayoutScanner = findViewById(R.id.frameLayoutScanner);

        btnConnectToCart.setOnClickListener(view -> {
            isConnected = true;
            toggleViews();
            startScanQR();
        });
        // Initialize the barcode scanner view
//        barcodeView = findViewById(R.id.barcodeScannerView);
//        captureManager = new CaptureManager(this, barcodeView);
//        captureManager.initializeFromIntent(getIntent(), savedInstanceState);
//        captureManager.decode();

        btnDisconnectCart.setOnClickListener(view -> {
            isConnected = false;
            toggleViews();
            Toast.makeText(ScanQRCodeActivity.this, "Cart will be disconnected by this", Toast.LENGTH_SHORT).show();
            try {
                socketDisconnect();
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        });
        ImageView ivLogout = findViewById(R.id.ivLogout);
        ivLogout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                showLogoutConfirmationDialog(v);
            }
        });
//        ImageView ivLogout = findViewById(R.id.ivLogout);
//        ivLogout.setOnClickListener(new View.OnClickListener() {
//            @Override
//            public void onClick(View v) {
//                // Handle ImageView click here, or you can call your deleteFileIfExists method directly.
//                deleteFileIfExists();
//            }
//        });

        // Set up the initial state of the views
        toggleViews();
        bottomNavigationView = findViewById(R.id.bottom_navigation);

        bottomNavigationView.setOnNavigationItemSelectedListener(
                new BottomNavigationView.OnNavigationItemSelectedListener()

                {
                    @RequiresApi(api = Build.VERSION_CODES.O)
                    @Override
                    public boolean onNavigationItemSelected (@NonNull MenuItem item){
                        BottomNavigationView navigationView = findViewById(R.id.bottom_navigation);
                        Menu menu = navigationView.getMenu();

                        // Reset icon tint of all items to the default color
                        for (int i = 0; i < menu.size(); i++) {
                            MenuItem menuItem = menu.getItem(i);
                            menuItem.setIconTintList(null); // Reset to default color
                        }

                        // Set the icon tint of the selected item to the desired color
                        item.setIconTintList(ColorStateList.valueOf(Color.parseColor("#87978F")));
                        switch (item.getItemId()) {
                            case R.id.menu_scan:
                                // Already in ScanQRActivity
                                return true;
                            case R.id.menu_me:
                                startActivity(new Intent(ScanQRCodeActivity.this, UserProfileActivity.class));
                                return true;
                            case R.id.menu_just_for_you:
                                startActivity(new Intent(ScanQRCodeActivity.this, ProductPreviewActivity.class));
                                return true;
                        }
                        return false;
                    }
                });
    }

    private class SocketTask extends AsyncTask<Void, Void, Void> {

        @Override
        protected Void doInBackground(Void... voids) {
            //asynchrounousProcess(host,port);
            /*try {
                Thread.sleep(25000);
                socketDisconnect();
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }*/
            return null;
        }

    }
    //UI and Background proceess
    public void asynchrounousProcess(String host, int port){
        new Thread(new Runnable(){
            @Override
            public void run() {
                //socket = null;
                //host = "192.168.8.169";
                //port = 9999;

                // Start separate threads for reading and sending messages
                //Thread for socket

                Thread socketThread = new Thread(new Runnable() {
                    @Override
                    public void run() {

                        try {
                            socket = new Socket(host, port);
                        } catch (IOException e) {
                            throw new RuntimeException(e);
                        }

                        Log.d("SOCKET REQUEST", "Socket connection requesting....");
                        readMessages(getApplicationContext());

                    }
                });
                //Thread for UI Process
                Thread UIThread = new Thread(new Runnable() {
                    @Override
                    public void run() {

                    }
                });

                socketThread.start();
                UIThread.start();

                // Wait for the threads to finish
                try {
                    socketThread.join();
                    UIThread.join();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }


            }
        }).start();


    }

    // common template for send all data
    private void sendMessages(String messageToSend) {
        try {
            OutputStream outputStream = socket.getOutputStream();
            PrintWriter writer = new PrintWriter(outputStream, true);
            writer.println(messageToSend);

        } catch (IOException e) {
            e.printStackTrace();
            Log.d("Socket Error", "Error while sending messages: " + e.getMessage());
        }
    }

    //read data from cart not work
    public void readMessages(Context context) {
        try {
            InputStream inputStream = socket.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
            String message;
            boolean isAlreadyPrint = false;

            FileOutputStream fileOutputStream = context.openFileOutput("dummy_data.txt", Context.MODE_APPEND | Context.MODE_PRIVATE);

            while (true) {
                message = reader.readLine();
                if (message == null) {
                    // Socket connection is closed, break the loop
                    Log.d("SOCKET NULL RECEIVING", "Server reached the connection limit. Stop connecting.");
                    break;
                }

                else if (message.equals("FAILED")) {
                    handleMultiUser();
                    Log.d("SOCKET REFUSE", "Server reached the connection limit. Stop connecting.");
                    fileOutputStream.close(); // Close the file output stream
                    return; // Exit the thread to stop trying to connect
                }
                else if (message.equals("SOCKET CONNECTED")) {
                    Log.d("SOCKET ESTABLISH", "Connected successfully.");
                    sendUserData(); //sending user data
                    Thread.sleep(1000);
                    sendDataSet(); //sending data set
                    //converting 250 data from txt file to csv
                    GetStartedActivity.convertTxtToCsv(getApplicationContext());
                    //clear 250 data set from data
                    GetStartedActivity.clearCheckoutData(getApplicationContext());

                }

                if (!isAlreadyPrint) {
                    Log.d("SOCKET ESTABLISH", "Connected successfully.");

                    isAlreadyPrint = true;
                }
                if (message.equals("FILE")) {
                    Log.d("SOCKET FILE RECEIVING", "RECEIVING START.");
                    Log.d("Received File", message);
                    while(true){
                        message = reader.readLine();
                        Log.d("Received Message", message);
                        // Write the received message to the file
                        // Add a newline after each message
                        if (message.equals("ENDING")){
                            // Print the received message to the console using Log
                            Log.d("BREAK","break");
                            break;
                        }
                        fileOutputStream.write(message.getBytes());
                        fileOutputStream.write("\n".getBytes());
                    }

                    // Get the file path of the saved file
                    String filePath = context.getFilesDir() + "/" + "dummy_data.txt";
                    // Print a success message indicating that the file has been saved
                    Log.d("FILE SAVED", "Received messages have been successfully saved to the file: " + filePath);
                    //fileOutputStream.close(); // Close the file output stream
                    //return; // Exit the thread to stop trying to connect
                }else{
                    //print normal message
                    Log.d("Received Message new", message);
                }
            }
            fileOutputStream.close();
        } catch (SocketException e) {
            // Handle the socket exception, which occurs when the connection is reset
            handleDisconnect();
        } catch (IOException e) {
            // Handle the exception (e.g., log or rethrow it)
            e.printStackTrace();
        } catch (InterruptedException e) {
            throw new RuntimeException(e);
        }
        /*catch (InterruptedException e) {

            throw new RuntimeException(e);
        }*/
    }

    //send checkout data set
    private void sendDataSet() {
        Context context = this; // Get the context if not available in the method already
        File receivedFile = new File(context.getFilesDir(), "dummy_data.txt");
        int dataSetSize = 100;
        if(receivedFile.exists()){
            try (BufferedReader reader = new BufferedReader(new FileReader(receivedFile))) {
                int dataCount = dataSetCount();
                if(dataCount >= dataSetSize){
                    String line;
                    line = "FILE";
                    sendMessages(line);

                    int lineCount = 0;
                    while ((line = reader.readLine()) != null && lineCount < dataSetSize) {
                        // Display each line in the console log
                        Log.d("READ LINE", line);
                        sendMessages(line);
                        if( lineCount%50 == 0){
                            Thread.sleep(5000);
                            line = "FILE";
                            sendMessages(line);
                        }
                        lineCount++;
                    }
                }else
                    Log.i("MSG","DATA SET IS NOT SUFFICIENT TO SEND");

                Thread.sleep(5000);

            } catch (IOException e) {
                e.printStackTrace();
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }else{
            Log.i("CHECKOUT DATA", "Still you do not receive data");
        }

    }
    private int dataSetCount() {
        int dataRowCount = 0;
        Context context = this; // Get the context if not available in the method already
        File receivedFile = new File(context.getFilesDir(), "dummy_data.txt");
        if (receivedFile.exists()) {
            try (BufferedReader reader = new BufferedReader(new FileReader(receivedFile))) {
                 // Counter for data rows

                // Skip the first line if it's a header or not a data row
                String line = reader.readLine();
                if (line != null) {
                    dataRowCount++; // Count the first line
                }

                while ((line = reader.readLine()) != null) {
                    // Process each line here, e.g., count data rows
                    dataRowCount++;
                }

                // Now dataRowCount contains the total number of data rows in the file
                Log.i("Total data rows: " , String.valueOf(dataRowCount));
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return dataRowCount;
    }
    private void sendUserData() {
       /* // Get the Intent that started this activity
        Intent intent = getIntent();

    // Retrieve the user data from the Intent extras
        String userDataJsonString = intent.getStringExtra("userData");

        if (userDataJsonString != null) {
            try {
                // Parse the user data JSON string
                JSONObject userData = new JSONObject(userDataJsonString);

                // Retrieve individual data fields
                String name = userData.getString("name");
                String gender = userData.getString("gender");
                String email = userData.getString("email");
                String age = userData.getString("age");
                String city = userData.getString("city");

                // Now you can use the retrieved data to populate your UI or perform other tasks
                // For example, set text views or update UI elements with the user data
                sendMessages("USER DATA");
                sendMessages("[" + name + "," + gender + "," + email+ "," + age + "," + city + "]");
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }*/

        try {
            FileInputStream fis = openFileInput("user_data.json");
            InputStreamReader isr = new InputStreamReader(fis);
            BufferedReader br = new BufferedReader(isr);
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line);
            }
            br.close();
            isr.close();
            fis.close();

            // Parse JSON data
            JSONObject userData = new JSONObject(sb.toString());
            String name = userData.getString("name");
            String gender = userData.getString("gender");
            String email = userData.getString("email");
            String age = userData.getString("age");
            String city = userData.getString("city");


            //  Send the data
            sendMessages("USER DATA");
            sendMessages("[" + name + "," + gender + "," + email+ "," + age + "," + city + "]");


        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    //socket disconnect Manually
    public void socketDisconnect() throws InterruptedException {
        try {
            if (socket != null && socket.isConnected()) {
                socket.close();
                Log.d("SOCKET DISCONNECT", "Socket connection manually closed.");
            }
        } catch (IOException e) {
            e.printStackTrace();
            Log.d("SOCKET DISCONNECT", "Error while closing socket: " + e.getMessage());
        }
    }


    private void toggleViews() {
        if (isConnected) {
            btnConnectToCart.setVisibility(View.GONE);
            btnDisconnectCart.setVisibility(View.VISIBLE);
            frameLayoutScanner.setVisibility(View.VISIBLE);
        } else {
            btnConnectToCart.setVisibility(View.VISIBLE);
            btnDisconnectCart.setVisibility(View.GONE);
            frameLayoutScanner.setVisibility(View.GONE);
        }
    }



    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        IntentResult result = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);
        String scannedData ="";
        String ipAddress = "";
        //int port = 0 ;
        /*if (result != null && result.getContents() != null) {
            scannedData = result.getContents();
            String dataType = result.getFormatName(); // Get the data type
            Log.d("QR RESULT", "Scanned Data: " + scannedData + ", Data Type: " + dataType);
            //url = "ws://" + scannedData + ":9999";
            String[] parts = scannedData.split(":");
            if(parts.length == 2){
                host = parts[0];
                port = Integer.parseInt(parts[1]);
                Log.i("split data: ","IP: "+ host+ ", PORT: "+ port);
                isQRRead = true;
                Log.d("QR READ STATE", String.valueOf(isQRRead));
                asynchrounousProcess(host,port);
            }else {
                // Handle invalid QR code format
                Log.e("split data: ", "Invalid QR code format: " + scannedData);
                showSnackbar("Invalid QR code format. Please scan a valid QR code.");
                btnDisconnectCart.setVisibility(View.GONE);
                btnConnectToCart.setVisibility(View.VISIBLE);
            }*/


        if (result != null && result.getContents() != null) {
            scannedData = result.getContents();
            String dataType = result.getFormatName(); // Get the data type
            Log.d("QR RESULT", "Scanned Data: " + scannedData + ", Data Type: " + dataType);

            // Check if scanned data follows the desired pattern (IP:Port)
            if (scannedData.matches("\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}\\.\\d{1,3}:\\d+")) {
                String[] parts = scannedData.split(":");
                if (parts.length == 2) {
                    host = parts[0];
                    port = Integer.parseInt(parts[1]);
                    Log.i("split data: ", "IP: " + host + ", PORT: " + port);
                    isQRRead = true;
                    Log.d("QR READ STATE", String.valueOf(isQRRead));
                    asynchrounousProcess(host, port);
                } else {
                    // Handle invalid QR code format
                    Log.e("split data: ", "Invalid QR code format: " + scannedData);
                    showSnackbar("Invalid QR code format. Please scan a valid QR code.");
                    btnDisconnectCart.setVisibility(View.GONE);
                    btnConnectToCart.setVisibility(View.VISIBLE);
                }// Create an Intent to send the scanned URL back to MainActivity
                Intent intent = new Intent();
                intent.putExtra("scanned_url", scannedData);
                setResult(RESULT_OK, intent);
            } else {
                // Handle non-matching format (e.g., URLs)
                Log.e("QR Format", "Invalid QR code format: " + scannedData);
                showSnackbar("Invalid QR code format. Please scan a valid QR code.");
                btnDisconnectCart.setVisibility(View.GONE);
                btnConnectToCart.setVisibility(View.VISIBLE);
            }
        } else {
            // If the scanning process was canceled
            // You can handle it here, for example, show a message to the user.
            Log.d(TAG, "Scanning canceled");
            setResult(RESULT_CANCELED);

        }
        if ( resultCode == RESULT_OK && data != null) {

            // Check if the scannedUrl is not null
            Log.d("SOCKET: ", scannedData);
            //client = new BiDirClient(this,"192.168.8.136",9999);
            //client.socketConnection();
            Toast.makeText(this, scannedData, Toast.LENGTH_SHORT).show();

        }else {
            Log.i("DATA INTENT: ","DATA IS NOT FETCHED");
        }
    }
    public void startScanQR() {
        // Start the QR code scanner
        IntentIntegrator integrator = new IntentIntegrator(this);
        integrator.setDesiredBarcodeFormats(IntentIntegrator.QR_CODE);
        integrator.setPrompt("Scan a QR Code");
        integrator.setCameraId(0); // Use the rear camera (0) or front camera (1)
        integrator.initiateScan();
    }
    public void logout() {
        // Clear any user session or data here, if needed

        SharedPreferences sharedPreferences = getSharedPreferences("user_prefs", MODE_PRIVATE);
        SharedPreferences.Editor editor = sharedPreferences.edit();

        // Clear user data and set login state to false
        editor.clear();
        editor.putBoolean("isLoggedIn", false);

        editor.apply();
        // Navigate back to the GetStartedActivity or LoginActivity
        Intent intent = new Intent(this, GetStartedActivity.class); // Change to your desired destination activity
        intent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK);
        startActivity(intent);
        finish(); // Optional, depending on your navigation flow
    }

    private void handleDisconnect() {
        // Show a message to the user (using a Toast)
        runOnUiThread(() -> {
            showSnackbar("Mobile is disconnected by Smart Cart");
        });

        // Update UI elements as needed
        // For example, toggle the state of the disconnect/connect button
        runOnUiThread(() -> {
            btnDisconnectCart.setVisibility(View.GONE);
            btnConnectToCart.setVisibility(View.VISIBLE);
        });
    }
    private void showSnackbar(String message) {
        Snackbar snackbar = Snackbar.make(findViewById(android.R.id.content), message, Snackbar.LENGTH_LONG);

        // Customize the appearance of the Snackbar
        View snackbarView = snackbar.getView();
        snackbarView.setBackgroundColor(ContextCompat.getColor(this, com.google.android.material.R.color.cardview_light_background)); // Set light red background color
        Snackbar.SnackbarLayout snackbarLayout = (Snackbar.SnackbarLayout) snackbarView;
        TextView textView = snackbarLayout.findViewById(com.google.android.material.R.id.snackbar_text);
        textView.setTextColor(Color.DKGRAY);

        // Center the Snackbar
        FrameLayout.LayoutParams params = (FrameLayout.LayoutParams) snackbarView.getLayoutParams();
        params.gravity = Gravity.CENTER;
        snackbarView.setLayoutParams(params);

        snackbar.show();    }
    private void showLogoutConfirmationDialog(View view) {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Logout");
        builder.setMessage("Are you sure you want to logout?");
        builder.setPositiveButton("Logout", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                // Perform logout action here
                logout();
            }
        });
        builder.setNegativeButton("Cancel", null);
        AlertDialog dialog = builder.create();
        dialog.show();
    }
    private void handleMultiUser() {
        // Show a message to the user (using a Toast)
        runOnUiThread(() -> {
            showSnackbar("Smart Cart is busy with another customer");
        });

        runOnUiThread(() -> {
            btnDisconnectCart.setVisibility(View.GONE);
            btnConnectToCart.setVisibility(View.VISIBLE);
        });
    }
    //----------------testing----------------------//
    public void deleteFileIfExists() {
        String filename = "dummy_data.txt";
        Context context = getApplicationContext();

        try {
            boolean deleted = context.deleteFile(filename);
            if (deleted) {
                // File was deleted successfully
                Log.i("File deleted: " , filename);
            } else {
                // File did not exist or couldn't be deleted
                Log.i("File not found or couldn't be deleted: " , filename);
            }
        } catch (Exception e) {
            // Handle any exceptions that might occur during file deletion
            e.printStackTrace();
        }
    }
    public void onConnectToCartClick(View view) {

        barcodeView.setVisibility(View.VISIBLE);
        captureManager.onResume();
        captureManager.decode();
    }

}
