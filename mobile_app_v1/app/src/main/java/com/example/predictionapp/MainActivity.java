package com.example.predictionapp;

import static android.service.controls.ControlsProviderService.TAG;

import android.annotation.SuppressLint;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothSocket;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.ContextWrapper;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.PackageManager;
import android.content.res.AssetManager;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;
import android.Manifest;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import org.java_websocket.drafts.Draft;
import org.java_websocket.drafts.Draft_6455;
import org.java_websocket.handshake.ServerHandshake;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;
import org.tensorflow.lite.Interpreter;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OptionalDataException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.HttpURLConnection;
import java.net.Socket;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.net.UnknownHostException;
import java.nio.MappedByteBuffer;
import java.nio.channels.FileChannel;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.List;
import java.util.Set;
import java.util.UUID;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.net.Socket;
import android.util.Log;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.zxing.integration.android.IntentIntegrator;
import com.google.zxing.integration.android.IntentResult;

import okhttp3.WebSocket;


public class MainActivity extends AppCompatActivity{
    private static final int REQUEST_ENABLE_BT = 1;
    Interpreter localTfliteModel;
    Interpreter receivedTfliteModel;
    float localModelAccuracy = 0;
    float receivedModelAccuracy = 0;
    int[][] dataArray;
    private static final String SERVER_ADDRESS = "141.145.200.6";
    private static final int SERVER_PORT = 8000;
    Button buttonBT;
    private String host ;
    private int port;

    private EditText etName, etGender, etNIC, etCity;
    private Button sendMsgButton;
    private TextView dataTextView;
    private TextView receivedDataTextView;
    private Handler handler;
    private BluetoothReceiver bluetoothReceiver;
    private BluetoothAdapter bluetoothAdapter;
    private BluetoothDevice selectedDevice;
    private static final int REQUEST_CODE_QR_SCAN = 101;
    //private WebSocketAndroidClient webSocketClient;
    private BiDirCom socketClient;
    private BiDirClient client;


    private Socket socket;

    @SuppressLint("MissingInflatedId")


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Log.i("INT", "Loading");
        MyLogger.i("COLORED TAG", "This is an info message with color.");
        socketConnect();

    }
    //socket connection
    public void socketConnect(){
        host = "192.168.8.136";
        port = 9999;
        new Thread(new Runnable(){
            @Override
            public void run() {
                socket = null;
                try {
                    socket = new Socket(host, port);
                    Log.d("SOCKET OPEN", "Socket connection is established.");
                    // Print the loop from 1 to 10
                    // Receive a custom message from the server
                    InputStream inputStream = socket.getInputStream();
                    BufferedReader reader = new BufferedReader(new InputStreamReader(inputStream));
                    String message = reader.readLine();

                   if (message.equals("FAILED")) {
                        Log.d("SERVER RESPONSE", "Server reached the connection limit. Stop connecting.");
                        return; // Exit the thread to stop trying to connect
                    }else{
                       Log.d("SOCKET CONNECT","Connection is successfully done");
                   }
                    //disconnectCart(socket);
                    //sendUserData();
                    //receiveData();

                } catch (IOException e) {
                    e.printStackTrace();
                    Log.d("SOCKET FAIL", "Socket connection failed: " + e.getMessage());
                }
            }
        }).start();

    }
   /* public void disconnectCart(Socket socket) {

        // Disconnect the socket
        try {
            socket.close();
            Log.d("SOCKET CLOSE", "Socket connection is closed.manually");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }


    }

    @Override
    protected void onResume() {
        super.onResume();
        IntentFilter filter = new IntentFilter(BluetoothAdapter.ACTION_STATE_CHANGED);
        registerReceiver(bluetoothReceiver, filter);
        //handleBluetoothActions();
    }

    @Override
    protected void onPause() {
        super.onPause();
        unregisterReceiver(bluetoothReceiver);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        // File csvFile = new File(getFilesDir(), "user_data.csv");
        if (requestCode == REQUEST_ENABLE_BT) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                //handleBluetoothActions();
            } else {
                // Bluetooth permission denied, handle accordingly (e.g., show a message, disable Bluetooth feature, etc.)
                //Toast.makeText(MainActivity.this, "Bluetooth permission denied", Toast.LENGTH_SHORT).show();
            }
        }
    }
    @Override
    protected void onActivityResult(int requestCode, int resultCode, @Nullable Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        IntentResult result = IntentIntegrator.parseActivityResult(requestCode, resultCode, data);
        String scannedData ="";
        String ipAddress = "";
        int port = 0 ;
        if (result != null && result.getContents() != null) {
            scannedData = result.getContents();
            String dataType = result.getFormatName(); // Get the data type
            Log.d("QR RESULT", "Scanned Data: " + scannedData + ", Data Type: " + dataType);
            //url = "ws://" + scannedData + ":9999";
            String[] parts = scannedData.split(":");
            if(parts.length == 2){
                ipAddress = parts[0];
                port = Integer.parseInt(parts[1]);
                Log.i("split data: ","IP: "+ ipAddress+ ", PORT: "+ port);
            }
            // Create an Intent to send the scanned URL back to MainActivity
            Intent intent = new Intent();
            intent.putExtra("scanned_url", scannedData);
            setResult(RESULT_OK, intent);

        } else {
            // If the scanning process was canceled
            // You can handle it here, for example, show a message to the user.
            Log.d(TAG, "Scanning canceled");
            setResult(RESULT_CANCELED);

        }
        if ( resultCode == RESULT_OK && data != null) {

            // Check if the scannedUrl is not null
            Log.d("SOCKET: ", scannedData);
            client = new BiDirClient(this,"192.168.8.136",9999);
            client.socketConnection();
            Toast.makeText(this, scannedData, Toast.LENGTH_SHORT).show();

        }else {
            Log.i("DATA INTENT: ","DATA IS NOT FETCHED");
        }

    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // Check if the BiDirCom object is not null before calling the disconnectWebSocket() method
        if (socketClient != null)
            client.closeSocket();



    }


    public void onConnectToCartButtonClicked(View view) {
        //webSocketClient.disconnect();
        startQRCodeScan();

    }
    public void onDisconnectCartButtonClicked(View view){
        if (socketClient != null)
            client.closeSocket();

    }
    private class FileReceiveTask extends AsyncTask<Void, Void, Boolean> {

        @Override
        protected Boolean doInBackground(Void... params) {
            try {
                String SERVER_IP = "192.168.8.169";
                int PORT = 9999;
                Socket socket = new Socket(SERVER_IP, PORT);
                Log.d(TAG, "Socket connection is established.");

                // Create a file to save the received data
                File outputFile = new File(getExternalFilesDir(null), "checkout_data_file.txt");

                InputStream inputStream = socket.getInputStream();
                FileOutputStream outputStream = new FileOutputStream(outputFile);
                BufferedInputStream bufferedInputStream = new BufferedInputStream(inputStream);

                byte[] buffer = new byte[1024];
                int bytesRead;
                while ((bytesRead = bufferedInputStream.read(buffer)) != -1) {
                    outputStream.write(buffer, 0, bytesRead);
                }

                outputStream.close();
                inputStream.close();
                socket.close();

                Log.d(TAG, "File received and saved to: " + outputFile.getAbsolutePath());
                return true;
            } catch (IOException e) {
                Log.e(TAG, "Error while receiving file: " + e.getMessage());
                return false;
            }
        }

        @Override
        protected void onPostExecute(Boolean result) {
            if (result) {
                Log.d(TAG, "File received successfully");
                // Handle the received file here
                // You can access the file using the File object outputFile
            } else {
                Log.d(TAG, "File receive failed");
            }
        }
    }

    private void initiate(){

        // Get references to UI elements
        etName = findViewById(R.id.editTextName);
        etGender = findViewById(R.id.editTextGender);
        etNIC = findViewById(R.id.editTextNIC);
        etCity = findViewById(R.id.editTextCity);
        Button btnSave = findViewById(R.id.buttonSave);
        File csvFile = new File(getFilesDir(), "user_data.csv");
        btnSave.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                saveFormJson();
            }
        });


        //registerReceiver(receiver, filter);
        try {
            copyModelToInternalStorage(this, "model.tflite");
            // Success: Model copied to internal storage
        } catch (IOException e) {
            e.printStackTrace();
            // Error: Failed to copy model
        }

    }


    private void saveForm() {

        String name = etName.getText().toString();
        String gender = etGender.getText().toString();
        String NIC = etNIC.getText().toString();
        String city = etCity.getText().toString();

        String userData = name + "," + gender + "," + NIC + "," + city + "\n";
        // Create the file name

        String userDataCsv = "user_data.csv";

        String existingFormData = readFormData();

        if (existingFormData != null && existingFormData.contains(userData)) {
            //Check whether an user exists or not
            Toast.makeText(getApplicationContext(), "This user has been already added", Toast.LENGTH_SHORT).show();

        } else {
            try {
                FileOutputStream fileOutputStream = openFileOutput(userDataCsv, Context.MODE_APPEND);
                fileOutputStream.write(userData.getBytes());
                fileOutputStream.close();
                Calendar calendar = Calendar.getInstance();
                loadModel("model");
                int currentMonth = calendar.get(Calendar.MONTH) + 1;
                predict(currentMonth, Integer.parseInt(gender));
                // Clear the text boxes
                etName.setText("");
                etGender.setText("");
                etNIC.setText("");
                etCity.setText("");

                Toast.makeText(getApplicationContext(), "A new user is added ", Toast.LENGTH_SHORT).show();

            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    private void saveFormJson() {
        String name = etName.getText().toString();
        String gender = etGender.getText().toString();
        String NIC = etNIC.getText().toString();
        String city = etCity.getText().toString();

        // Create a JSON object to hold the user data
        JSONObject userDataJson = new JSONObject();
        try {
            userDataJson.put("name", name);
            userDataJson.put("gender", gender);
            userDataJson.put("NIC", NIC);
            userDataJson.put("city", city);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        // Create the file name
        String userDataJsonFile = "user_data.json";

        String existingFormData = readFormData();

        if (existingFormData != null && existingFormData.contains(userDataJson.toString())) {
            // Check whether a user exists or not
            Toast.makeText(getApplicationContext(), "This user has been already added", Toast.LENGTH_SHORT).show();
        } else {
            try {
                FileOutputStream fileOutputStream = openFileOutput(userDataJsonFile, Context.MODE_APPEND);
                // Convert the JSON object to a JSON string
                String userDataJsonString = userDataJson.toString() + "\n";
                fileOutputStream.write(userDataJsonString.getBytes());
                fileOutputStream.close();
                Calendar calendar = Calendar.getInstance();
                loadModel("model");
                int currentMonth = calendar.get(Calendar.MONTH) + 1;
                predict(currentMonth, Integer.parseInt(gender));
                // Clear the text boxes
                etName.setText("");
                etGender.setText("");
                etNIC.setText("");
                etCity.setText("");

                Toast.makeText(getApplicationContext(), "A new user is added ", Toast.LENGTH_SHORT).show();

            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }


    private String readFormData() {
        try {
            FileInputStream fis = openFileInput("user_data.csv");
            InputStreamReader isr = new InputStreamReader(fis);
            BufferedReader br = new BufferedReader(isr);

            StringBuilder stringBuilder = new StringBuilder();
            String line;

            while ((line = br.readLine()) != null) {
                stringBuilder.append(line).append("\n");
            }
            br.close();
            return stringBuilder.toString();
        } catch (IOException e) {
            e.printStackTrace();
        }

        return null;
    }
    //read csv file for asset
    private void readCsv(String v){
        // Load the CSV file from the assets folder
        String fileName = "dataset.csv";
        String[] data = loadDataFromAsset(this, fileName);
        Log.i("MyApp", "data set Loaded");
        // Preview the data in the console


// Split the first row into column names (if needed)
        String[] columnNames = data[0].split(",");

// Initialize the intData array
        int[][] intData = new int[data.length-1][columnNames.length];

// Convert the data into integers and store in the intData array
        for (int i = 1; i < data.length; i++) {
            String[] rowData = data[i].split(",");
            for (int j = 0; j < columnNames.length; j++) {
                intData[i-1][j] = Integer.parseInt(rowData[j]);
            }
        }
        Log.i("MyApp", "Save to Globle array");
        dataArray =intData;
    }

    private String[] loadDataFromAsset(Context context, String fileName) {
        AssetManager assetManager = context.getAssets();
        StringBuilder stringBuilder = new StringBuilder();

        try {
            // Open the CSV file as an InputStream and read its contents
            InputStream inputStream = assetManager.open(fileName);
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));

            String line;
            while ((line = bufferedReader.readLine()) != null) {
                stringBuilder.append(line).append("\n");
            }

            bufferedReader.close();
        } catch (IOException e) {
            e.printStackTrace();
        }

        // Convert the CSV data to an array of Strings
        return stringBuilder.toString().split("\n");
    }

//close read csv
private float modelAccuracy(String accuracyMode){
    int[][] data= dataArray;

    float[][] input_values = new float[data.length][2];
    int[][] realOutput = new int[data.length][1];

    for (int i = 0; i < data.length; i++) {
        input_values[i][0] = (float) data[i][0];
        input_values[i][1] = (float) data[i][1];
        realOutput[i][0] = data[i][2];
    }

// define input and output arrays
    float[][] x_np = new float[input_values.length][2];
    float[][] output = new float[1][7];

    int correctPredictions = 0;

// loop over input values
    for (int i = 0; i < input_values.length; i++) {
        // set input values
        x_np[i] = input_values[i];
        x_np[i][0] /= 12;
        x_np[i][1] /= 12;

        // run prediction
        if(accuracyMode=="localModel"){
            localTfliteModel.run(x_np[i], output);
        }

        else if(accuracyMode=="receivedModel"){
            receivedTfliteModel.run(x_np[i], output);
        }
        // get predicted label for this input value
        int y_pred = argmax(output, 1)[0];
        int value = realOutput[i][0];

        if (y_pred == value) {
            correctPredictions++;
        }
        // print the predicted label
//            Log.i("MyApp", "Prediction for input " + i + ": " + y_pred);
//            Log.i("MyApp", "Real value for input " + i + ": " + value);
    }

    float accuracy = ((float) correctPredictions / input_values.length) * 100;
    Log.i("MyApp", accuracyMode+" Accuracy: " + accuracy + "%");
    return accuracy;

}

    //close model accuracy

    //check data type
    private void dType(String v){
        try {
            InputStream inputStream = getAssets().open("model.tflite");
            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
            byte[] buffer = new byte[4096];
            int len;
            while ((len = inputStream.read(buffer)) != -1) {
                byteArrayOutputStream.write(buffer, 0, len);
            }
            String result = byteArrayOutputStream.toString("UTF-8");
            Log.i("MyApp", "Data type : "+result);
        } catch (IOException e) {
            e.printStackTrace();
        }

    }
    //close data type

    private void loadModel(String fileName) {
        try {
            if (fileName == "model") {
                localTfliteModel = new Interpreter(loadFile(fileName));
                Log.i(" Prediction App", fileName + " is loaded success fully");
            } else if (fileName == "receivedModel") {
                receivedTfliteModel = new Interpreter(loadFile(fileName));
                Log.i(" Prediction App", fileName + " is  loaded success fully");

            } else {
                Log.i(" Prediction App", fileName + " is  not loaded");

            }

        } catch (Exception ex) {
            ex.printStackTrace();
            Log.i("Prediction App", "Error");
            Log.i("Prediction App", ex.toString());
        }
    }

    private MappedByteBuffer loadFile(String fileName) throws IOException {
        // Get the path to the model file in the internal storage directory
        File directory = new File("/data/data/com.example.predictionapp/files");
        File modelFile = new File(directory, fileName + ".tflite");

        // Open the model file as a FileInputStream
        FileInputStream inputStream = new FileInputStream(modelFile);

        // Get a FileChannel from the FileInputStream
        FileChannel fileChannel = inputStream.getChannel();

        // Get the start offset and declared length of the model file
        long startOffset = 0;
        long declareLength = modelFile.length();

        // Map the model file to a MappedByteBuffer
        MappedByteBuffer mappedByteBuffer = fileChannel.map(FileChannel.MapMode.READ_ONLY, startOffset, declareLength);

        // Close the input stream and file channel
        inputStream.close();
        fileChannel.close();

        // Return the MappedByteBuffer
        return mappedByteBuffer;
    }

    private void predict(int month, int gender) {
        float[] x_data = {month, gender};

        float[][] x_np = new float[1][2];
        x_np[0] = x_data;
        x_np[0][0] /= 12;
        x_np[0][1] /= 12;

        float[][] output = new float[1][7];
        localTfliteModel.run(x_np, output);
        int[] y_pred_model_1 = argmax(output, 1);

        TextView txtPredictItem = findViewById(R.id.textItem);

        for (int i = 0; i < y_pred_model_1.length; i++) {
            Log.i(" Prediction App ", "Prediction results: " + String.valueOf(y_pred_model_1[i]));
            txtPredictItem.setText("Predicted Item: " + String.valueOf(y_pred_model_1[i]));
        }
    }

    public static void copyModelToInternalStorage(Context context, String modelName) throws IOException {
        InputStream inputStream = context.getAssets().open(modelName);

        File modelFile = new File("/data/data/com.example.predictionapp/files", modelName);
        OutputStream outputStream = new FileOutputStream(modelFile);

        byte[] buffer = new byte[1024];
        int length;
        while ((length = inputStream.read(buffer)) > 0) {
            outputStream.write(buffer, 0, length);
        }
        Log.i("local model", "is transferred successfully");
        outputStream.flush();
        outputStream.close();
        inputStream.close();
    }

    public static int[] argmax(float[][] array, int axis) {
        int[] result = new int[array.length];
        for (int i = 0; i < array.length; i++) {
            float max = array[i][0];
            int index = 0;
            for (int j = 1; j < array[i].length; j++) {
                if (array[i][j] > max) {
                    max = array[i][j];
                    index = j;
                }
            }
            result[i] = index;
        }
        return result;
    }
      *//*
    The internal storage of an Android app is considered to be relatively secure because it is private to the app and
     inaccessible to other apps by default. Other apps cannot read or modify the files stored in the internal storage
      of your app, and the files stored in the internal storage are deleted when the user uninstalls the app.
     *//*
    *//*
    By default, files stored in the internal storage of an Android app are not visible to the user or accessible through
     file managers or other apps on the device. This is because the internal storage is private to the app and other apps
      do not have permission to access it.
     *//*

    *//*
    If the size of the model is small and the model does not change frequently, you can save it in the app's asset folder
     or in the internal storage of the app. The internal storage is a private storage that is only accessible to the app,
      and it is a good option for storing sensitive data like models.

    If the size of the model is large and you want to reduce the load time of the model, you can consider using the cache memory
     of the app. Cache memory is a fast memory that is used to store frequently accessed data. However, it is important to note
      that the cache memory is not a persistent storage, which means that data in the cache memory can be deleted by the system
      at any time to free up space.
     *//*


    //http network

   *//* private void downloadImage(String imageUrl) {
        new AsyncTask<String, Void, Bitmap>() {
            @Override
            protected Bitmap doInBackground(String... params) {
                String imageUrl = params[0];
                try {
                    URL url = new URL(imageUrl);
                    HttpURLConnection connection = (HttpURLConnection) url.openConnection();
                    connection.setDoInput(true);
                    connection.connect();
                    InputStream input = connection.getInputStream();
                    Bitmap bitmap = BitmapFactory.decodeStream(input);
                    return bitmap;
                } catch (Exception e) {
                    e.printStackTrace();
                    return null;
                }
            }

            @Override
            protected void onPostExecute(Bitmap result) {
                super.onPostExecute(result);
                if (result != null) {
                    saveImageToInternalStorage(result);
                    Log.i("DownloadImage", "Image downloaded successfully");
                } else {
                    Log.i("DownloadImage", "Failed to download image");
                }
            }
        }.execute(imageUrl);
    }
*//*
    *//*private void saveImageToInternalStorage(Bitmap bitmap) {

        ContextWrapper cw = new ContextWrapper(getApplicationContext());

// Get the path to the "models" directory in internal storage
        File directory = new File(cw.getFilesDir(), "models");
        directory.mkdirs();

// Create a new file in the "models" directory and save the image to it
        File mypath = new File(directory, "image.jpg");
        FileOutputStream fos = null;
        try {
            fos = new FileOutputStream(mypath);
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, fos);
            fos.close();
        } catch (Exception e) {
            e.printStackTrace();
        }


    }*//*

    //http test network

    private void startQRCodeScan() {
        IntentIntegrator integrator = new IntentIntegrator(this);
        integrator.setDesiredBarcodeFormats(IntentIntegrator.QR_CODE);
        integrator.setPrompt("Scan a QR Code");
        integrator.setCameraId(0); // Use the rear camera (0) or front camera (1)
        integrator.initiateScan();


    }
    // Method to parse the JSON data into a list of lists of integers
*/
    }
